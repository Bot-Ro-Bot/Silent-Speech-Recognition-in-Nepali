// this is just a template and is not currently used in the app script... 
function recordStart() {
	var audio = new Audio("static/resource/beep.mp3");
	audio.play();
		
	// document.write("hero of sparta")

	var startTime = new Date().getTime();
	var x = setInterval(function(){
		var currentTime = new Date().getTime();
		var timeDifference = currentTime - startTime
		document.getElementById('timer').innerHTML = timeDifference
		if(timeDifference >= 6){
			clearInterval(x);
			document.getElementById('timer').innerHTML = "Recorded...";
		}
	}, 1000);
}

$(document).ready(function(){
	$('#loadBtn').click(function(){
		$.get('/start_stream', {status:'run'}, function(data, textStatus, jqXHR) {
			recordStart();
		});
	});
});



// function recordStart() {
// 	var audio = new Audio("static/resource/beep.mp3");
// 	audio.play();
		
// 	document.write("hero of sparta")
// }
