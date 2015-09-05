$(document).ready(function(){main();});

var LOCAL_SERVER_ADDRESS = "swat:serverAddress";
var LOCAL_SERVER_PORT = "swat:serverPort";

var serverAddress;
var serverPort;

function main ()
{
	$("main").hide();

	serverAddress = localStorage.getItem(LOCAL_SERVER_ADDRESS);
	serverPort = localStorage.getItem(LOCAL_SERVER_PORT);

	if(serverAddress) $("#serverAddress").val(serverAddress);
	if(serverPort) $("#serverPort").val(serverPort);

	$("#saveButton").click(function(e){
		serverAddress = $("#serverAddress").val();
		serverPort = $("#serverPort").val();

		localStorage.setItem(LOCAL_SERVER_ADDRESS, serverAddress);
		localStorage.setItem(LOCAL_SERVER_PORT, serverPort);

		$(this).parent().hide();
		$("main").show();
	});

	$(".keypad li").on("touchstart", function(e){
		timestamp = Date.now();

		e.stopPropagation();
		e.preventDefault();

		$(this).css({
			background: "#1caaff",
			color: "#fcfcfc"
		});

		var label = $(this).find("span").text();
		send(timestamp, label);
	});

	$(".keypad li").on("touchend", function(e){
		$(this).css({
			background: "#fcfcfc",
			color: "#1caaff"
		});
	});
}

function send(timestamp, label)
{
	$.ajax({
		url: serverAddress+":"+serverPort,
		type: "POST",
		data: "{timestamp: "+timestamp+", label: "+label+"}"
	});
}
