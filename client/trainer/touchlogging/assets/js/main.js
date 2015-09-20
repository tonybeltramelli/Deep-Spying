/*
	@author Tony Beltramelli www.tonybeltramelli.com - created 05/09/15
*/

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

		var label = $(this).find("span").text().charCodeAt(0);
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
	var data = {
		sensor_name: "labels",
		data_points:[{
			timestamp: timestamp,
			label: label
		}]
	};

	$.ajax({
		url: serverAddress+":"+serverPort,
		type: "POST",
		data: JSON.stringify(data),
		contentType: "text/plain"
	});
}
