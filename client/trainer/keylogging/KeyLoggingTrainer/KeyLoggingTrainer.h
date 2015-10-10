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
        void setup(byte mac[]);
        String sendData(byte serverAddress[], int serverPort, String data, boolean ignoreResponse);
        String getJSON(String label);
        void setReferenceTime(String timestamp);
    private:
        EthernetClient _client;
        unsigned long _startTime;
        unsigned long _delay;
        unsigned long _referenceTime;
        String _head;
        //
        String _getTimestamp();
};

#endif
