// Set Timer
var time = 10


var xhr = new XMLHttpRequest();
xhr.open('GET', '{{ url_for('stream_prediction') }}');

var position = 0

function handleNewData() {
	var messages = xhr.responseText.split('\n');
	messages.slice(position, -1).forEach(function(value) {
		document.getElementById("scorer").textContent = value;  // update the latest value in place
	});
	position = messages.length - 1;
}


// Update the count down every 1 second
var x = setInterval(function() {
	xhr.send();
	handleNewData();

	// If the count down is finished, write some text
	if (time == 0) {
		clearInterval(x);
	} 

}, 1000);
