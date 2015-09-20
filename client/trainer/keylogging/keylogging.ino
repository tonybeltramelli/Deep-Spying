/*
  @author Tony Beltramelli www.tonybeltramelli.com - created 19/09/15
*/

#include <Ethernet.h>
#include <SPI.h>

#include "KeyLoggingTrainer.h"

byte mac[] = {  0x90, 0xA2, 0xDA, 0x0D, 0xA3, 0xED };
byte ip[] = { 192, 168, 0, 177 };

byte serverAddress[] = { 192, 168, 0, 20 };
int serverPort = 8000;

KeyLoggingTrainer trainer = KeyLoggingTrainer();

void setup()
{
  Serial.begin(9600);
  while (!Serial);
  
  trainer.setup(mac, ip);
  
  delay(2000);
  
  String timestamp = trainer.sendData(serverAddress, serverPort, "d", false);
  Serial.println("reference timestamp: "+timestamp);
  trainer.setReferenceTime(timestamp);
}

void loop()
{ 
  trainer.sendData(serverAddress, serverPort, trainer.getJSON("a"), true);
  delay(5000);
}
