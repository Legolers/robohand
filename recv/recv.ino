#include <HardwareSerial.h>
#include <Servo.h>

#define DBG
#define FNG_CLOSED 0
#define FNG_OPEN   180



class Hand
{
public:
  Servo servos[6];
  void init(int pins[6]);
  void moveFinger(int fid, int pos);
  void setHand(int pos[6]);
  void reset();
};

void Hand::init(int *pins)
{
  for(int i=0; i < 6; i++)
  {
    this->servos[i].attach(pins[i]);
  }
}
void Hand::moveFinger(int fid, int pos)
{
  this->servos[fid].write(pos);
}
void Hand::setHand(int *pos)
{
  for(int i=0; i<6;i++)
  {
    moveFinger(i,  pos[i]);
  }
}
void Hand::reset()
{
  int tmp[6] = {0,0,0,0,0,0};
  setHand(tmp);
}


short request[6] = {0,0,0,0,0,0};
bool hasData = false;
Hand hand;

void setup()
{
  int tmp[6] = {3,4,5,6,7,2};
  hand.init(tmp);
  hand.reset();
  delay(500);

  Serial.begin(9600);
  Serial.println("RDY");
}

void loop()
{
  byte recv[12];
  if (Serial.available() > 0)
  {
    hasData = true;
    Serial.readBytes(recv,12);
  }
  if (hasData)
  {
    for(int i=0; i < 12; i)
    {
      byte l = recv[i];
      byte r = recv[i+1];
      unsigned short bob = r;
      bob <<= 8;
      bob |= l;
      request[(int)i/2] = bob;

      i+=2;
    }
#ifdef DBG
    for (int i = 0; i < 6; i++)
    {
      Serial.println(request[i]);
    }
#endif
    hand.setHand(request);
    Serial.println("ACK");

    hasData = false;
  }
}