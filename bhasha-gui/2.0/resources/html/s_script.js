<script>
	function submitAndValidate(answers) {
    var txt;
	var score=0
	var text="t_"
  if (confirm("validate your answers")) {
		txt = answers;
		answerKeyMap = ' Answer Key: <br><ul>'
		answers.forEach(function (item, index) {
			id = text + item
			answerKeyMap += "<li> " + (index+1) + " : " + item + " </li>"
			console.log(id)
			textField=document.getElementById(id)
			value=textField.value
			console.log(value)

			if (value== index +1 ){
			score = score + 1
				console.log(item, index+1);
			document.getElementById(id).className = 'correct' 
			}else{
			document.getElementById(id).className = 'error' 
		}
		
		});
	answerKeyMap += "</ul>"
	document.getElementById("score").innerHTML = '<h3 style="color:red"> Your Score is : <b>' + score + '</b> </h3>';
	document.getElementById("answer_key").innerHTML = answerKeyMap

  } else {
		txt = "You pressed Cancel!";
  }

}

function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
		minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
		timer = duration;
        }
    }, 1000);
}

window.onload = function () {
    var fiveMinutes = 60 * 13,
        display = document.querySelector('#time');
    startTimer(fiveMinutes, display);
};

</script>