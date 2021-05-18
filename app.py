import json, os
from flask import Flask, render_template, redirect, url_for
from google.oauth2 import service_account
import gspread


app = Flask(__name__)
app.config.from_pyfile('config.py')


# Download Google service account credentials, rename to 'key.json' for this to work
#   TODO - move to .env, build dict in code


with open('key.json', 'r') as json_creds:
    acct_info = json.load(json_creds)


credential = service_account.Credentials.from_service_account_info(acct_info)
scopes = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"]

scoped_credential = credential.with_scopes(scopes)

client = gspread.authorize(scoped_credential)
sheet = client.open("weather").sheet1


@app.route('/', methods=["GET"])
def main_page():
    #print(sheet.get_all_records())

    return render_template("index.html")


@app.errorhandler(404)
def handle_404_error(e):
  return redirect(url_for("main_page"))


if __name__ == '__main__':
    app.run()
