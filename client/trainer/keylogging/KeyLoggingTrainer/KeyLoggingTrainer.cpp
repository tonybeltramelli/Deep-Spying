/*
  @author Tony Beltramelli www.tonybeltramelli.com - created 19/09/15
*/
  
#include "KeyLoggingTrainer.h"

void KeyLoggingTrainer::setup(byte mac[])
{
    Ethernet.begin(mac);
}

String KeyLoggingTrainer::sendData(byte serverAddress[], int serverPort, String data, boolean ignoreResponse)
{ 
    String response = "";

    if (!_client.connect(serverAddress, serverPort)) return response;
    
    if(!ignoreResponse) _delay = millis();

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
                if(!startRecording)
                {
                    _client.stop();
                }
            }
        }
    }
    
    _delay = millis() - _delay;
    response = response.substring(0, response.length() - 1);
    return response;
}

void KeyLoggingTrainer::setReferenceTime(String timestamp)
{
    _startTime = millis();

    int headLength = 5;
    char length = timestamp.length();

    while(timestamp[headLength] == '0')
    {
        headLength += 1;
    }

    _head = "";
    String tail = "";
  
    for(int i = 0; i < length; i++)
    {
        if(i < headLength)
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
    String timestamp = _getTimestamp();

    String data = "{\"sensor_name\":\"labels\",\"data_points\":[{\"timestamp\":" + timestamp;
    data = data + ",\"label\":" + label + "}]}";
  
    return data;
}

String KeyLoggingTrainer::_getTimestamp()
{
    unsigned long currentTime = millis() + _delay;
    unsigned long diff = _referenceTime + currentTime - _startTime;

    return _head + String(diff);
}
