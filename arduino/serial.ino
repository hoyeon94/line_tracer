#include < SoftwareSerial.h > 
#include < AFMotor.h > AF_DCMotor motor_L(4);
AF_DCMotor motor_R(3);
int SPEED,DELAY
int ROTATE_SPEED,ROTATE_DELAY
String Speed;
char LorR;
int I,s;
byte DataToRead[8];
void setup() {
	SPEED = 200;
	ROTATE_SPEED = 250;
	DELAY = 100;
	ROTATE_DELAY = 150;
	Serial.begin(9600);
	motor_L.run(FORWARD);
	motor_R.run(FORWARD);
}
void loop() {
	DataToRead[5] = '\n';
	Serial.readBytesUntil(char(13), DataToRead, 8);
	/* For Debugging, send string to RPi */
	for (i = 0; i < 6; i ++) {
		Serial.write(DataToRead[i]);
		if (DataToRead[i] == '\n') 
		            break;
	}
	/* End of Debugging */
	LorR = DataToRead[0];
	Speed = "";
	for (i = 1; (DataToRead[i] != '\n') && (i < 6); i ++) {
		Speed += DataToRead[i];
	}
	s = Speed.toInt();
	if (LorR == 'L') {
		motor_L.setSpeed(ROTATE_SPEED);
		motor_R.setSpeed(0);
		delay(ROTATE_DELAY);
		motor_L.setSpeed(0);
		motor_R.setSpeed(0);
		Serial.write("complete");
		// Turn left wheel with speed s
	} else if (LorR == 'R') {
		motor_R.setSpeed(ROTATE_SPEED);
		motor_L.setSpeed(0);
		delay(ROTATE_DELAY);
		motor_L.setSpeed(0);
		motor_R.setSpeed(0);
		Serial.write("complete");
		// Turn right wheel with speed s
	} else if (LorR == 'S') {
		motor_L.setSpeed(0);
		motor_R.setSpeed(0);
	} else if (LorR == 'F') {
		motor_L.setSpeed(SPEED);
		motor_R.setSpeed(SPEED);
		delay(DELAY);
		motor_L.setSpeed(0);
		motor_R.setSpeed(0);
		Serial.write("complete");
	}
}
