/*
  @author Tony Beltramelli www.tonybeltramelli.com - created 19/09/15
*/

#include <Ethernet.h>
#include <SPI.h>
#include <Keypad.h>

#include "KeyLoggingTrainer.h"

byte mac[] = {  0x90, 0xA2, 0xDA, 0x0D, 0xA3, 0xED };

byte serverAddress[] = { 192, 168, 52, 231 };
int serverPort = 8000;

const byte ROWS = 4;
const byte COLS = 3;

char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};

byte rowPins[ROWS] = {8, 7, 6, 5};
byte colPins[COLS] = {9, 3, 2};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);
KeyLoggingTrainer trainer = KeyLoggingTrainer();

void setup()
{ 
  Serial.begin(9600);
  while (!Serial);
  
  trainer.setup(mac);
  
  delay(2000);
  
  String timestamp = trainer.sendData(serverAddress, serverPort, "t", false);
  Serial.println("reference timestamp: "+timestamp);
  trainer.setReferenceTime(timestamp);
}

void loop()
{
  char key = keypad.getKey();
  
  if (key)
  {
    String label = String(int(key));
    Serial.println(key);
    trainer.sendData(serverAddress, serverPort, trainer.getJSON(label), true);
  }
}
