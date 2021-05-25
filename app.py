import json, os, ast
from flask import Flask, render_template, redirect, url_for
from google.oauth2 import service_account
from dotenv import load_dotenv
import gspread, pandas


def get_credential():
    '''Reads environment vars, builds and returns scoped Google credential object'''

    # Build credential dict
    account = {
        "type": "service_account",
        "project_id": os.environ['GOOGLE_PROJECT_ID'],
        "private_key_id": os.environ['GOOGLE_PRIVATE_KEY_ID'],
        "private_key": os.environ['GOOGLE_PRIVATE_KEY'],
        "client_email": os.environ['GOOGLE_CLIENT_EMAIL'],
        "client_id": os.environ['GOOGLE_CLIENT_ID'],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ['GOOGLE_CLIENT_CERT_URL']}

    # Build scopes list
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"]

    # Construct credentials
    credential = service_account.Credentials.from_service_account_info(account)
    scoped_credential = credential.with_scopes(scopes)

    return scoped_credential


# Setup
app = Flask(__name__)
app.config.from_pyfile('config.py')
load_dotenv('.env')

# Open Google sheet
client = gspread.authorize(get_credential())
sheet = client.open("weather").sheet1

# Setup pandas dataframe
data = sheet.get_all_values()
headers = data.pop(0)
df = pandas.DataFrame(data, columns=headers)


@app.route('/', methods=["GET"])
def main_page():
    #Do stuff here

    return render_template("index.html")


@app.errorhandler(404)
def handle_404_error(e):
  return redirect(url_for("main_page"))


if __name__ == '__main__':
    app.run()
