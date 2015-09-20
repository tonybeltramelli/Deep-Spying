/*
  @author Tony Beltramelli www.tonybeltramelli.com - created 19/09/15
*/

#ifndef KeyLoggingTrainer_h
#define KeyLoggingTrainer_h

#include <Arduino.h>
#include <Ethernet.h>
#include <SPI.h>

class KeyLoggingTrainer
{
	public:
		void setup(byte mac[], byte ip[]);
		String sendData(byte serverAddress[], int port, String data, boolean ignoreResponse);
		String getJSON(String label);
		void setReferenceTime(String timestamp);
  	private:
  		EthernetClient _client;
		unsigned long _startingTime;
		unsigned long _referenceTime;
		String _head;
		//
  		String _getTimestamp();
};

#endif