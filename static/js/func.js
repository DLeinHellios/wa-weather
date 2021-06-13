// Useful functions for chart generation


	/**
	* Return a simple random hex color for a chart element
	*/

function getColor() {
	var chars = 'ABCDEF0123456789'.split('')
	var color = '#'

	for (var i=0; i<6; i++){
		color += chars[Math.floor(Math.random() * 16)];
	}

	return color;
}
