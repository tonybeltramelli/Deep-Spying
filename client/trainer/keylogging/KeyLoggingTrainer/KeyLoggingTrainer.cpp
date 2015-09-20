/*
  @author Tony Beltramelli www.tonybeltramelli.com - created 19/09/15
*/
  
#include "KeyLoggingTrainer.h"

KeyLoggingTrainer::KeyLoggingTrainer(byte mac[], byte ip[])
{
	Ethernet.begin(mac, ip);

	delay(1000);

	_startingTime = millis();
	_referenceTime = 0;
}

String KeyLoggingTrainer::sendData(byte serverAddress[], int port, String data, boolean ignoreResponse)
{ 
  String response = "";
  
  if (!_client.connect(serverAddress, port)) return response;
  
  _client.println("POST / HTTP/1.1"); 
  _client.print("Content-Length: "); 
  _client.println(data.length()); 
  _client.println("Content-Type: text/plain");
  _client.println(); 
  _client.print(data);
  
  if(ignoreResponse)
  {
    if(_client.connected()) _client.stop();
    return response;
  }
  
  boolean startRecording = false;
  
  while(_client.connected())
  {
    if(_client.available())
    {
      char c = _client.read();
      
      if (startRecording) response += c;
      
      if (c == '#')
      {
        startRecording = !startRecording;
        if(!startRecording) _client.stop();
      }
    }
  }
  
  response = response.substring(0, response.length() - 1);
  return response;
}

void KeyLoggingTrainer::setReferenceTime(String timestamp)
{
  int HEAD_LENGTH = 6;
  
  char length = timestamp.length();

  _head = "";
  String tail = "";
  
  for(int i = 0; i < length; i++)
  {
    if(i < HEAD_LENGTH)
    {
      _head += timestamp[i];
    }else{
      tail += timestamp[i];
    }
  }
  
  _referenceTime = tail.toInt();
}

String KeyLoggingTrainer::getJSON(String label)
{
  String data = "{\"sensor_name\":\"labels\",\"data_points\":[{\"timestamp\":" + _getTimestamp();
  data = data + ",\"label\":\"" + label + "\"}]}";
  
  return data;
}

String KeyLoggingTrainer::_getTimestamp()
{
  return _head + String(_referenceTime);
}