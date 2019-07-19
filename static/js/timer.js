// Set Timer
var time = 10

// Update the count down every 1 second
var x = setInterval(function() {

	// If the count down is finished, write some text
	if (time == 0) {
		clearInterval(x);
		document.getElementById("timer").textContent = "TIME'S UP!!!";
	} else 
	{
		// Update time
		document.getElementById("timer").textContent = time;
		time = time - 1;
	}

}, 1000);
