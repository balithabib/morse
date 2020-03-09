#include "pitches.h"
//digital pin 12 has a button attached to it. Give it an name
int buttonPin= 12;
//digital pin 2 has a led attached to it. Give it an name
int ledPin= 2;
// change this to make the song slower or faster
int tempo=112; 

// change this to whichever pin you want to use
int buzzer = 8;

int melody[] = {
  NOTE_E5, 4,  NOTE_B4,8,  NOTE_C5,8,  NOTE_D5,4,  NOTE_C5,8,  NOTE_B4,8,
};

// sizeof gives the number of bytes, each int value is composed of two bytes (16 bits)
// there are two values per note (pitch and duration), so for each note there are four bytes
int notes=sizeof(melody)/sizeof(melody[0])/2; 

// this calculates the duration of a whole note in ms (60s/tempo)*4 beats
int wholenote = (60000 * 4) / tempo;

int divider = 0, noteDuration = 0;

char msg = '  ';   // variable to hold data from serial
 
void setup() {
  //make the button's pin input
  pinMode(buttonPin, INPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
  Serial.print("Program Initiated\n");  
}

void loop_melody() {
  // iterate over the notes of the melody. 
  // Remember, the array is twice th  e number of notes (notes + durations)
  for (int thisNote = 0; thisNote < notes * 2; thisNote = thisNote + 2) {

    // calculates the duration of each note
    divider = melody[thisNote + 1];
    if (divider > 0) {
      // regular note, just proceed
      noteDuration = (wholenote) / divider;
    } else if (divider < 0) {
      // dotted notes are represented with negative durations!!
      noteDuration = (wholenote) / abs(divider);
      noteDuration *= 1.5; // increases the duration in half for dotted notes
    }

    // we only play the note for 90% of the duration, leaving 10% as a pause
    tone(buzzer, melody[thisNote], noteDuration*0.9);

    // Wait for the specified duration before play  ing the next note.
    delay(noteDuration);
    
    // stop the waveform generation before the next note.
    noTone(buzzer);
  }
}

void pc_to_arduino() {
  // While data is sent over serial assign it to the msg
  while (Serial.available()>0){ 
    msg=Serial.read();
  }

  // Turn LED on/off if we recieve 'Y'/'N' over serial 
  if (msg=='H') {            
    digitalWrite(ledPin, HIGH);  // turn LED ON
    tone(buzzer, melody[0], 600);
    delayMicroseconds(1000);
    //loop_melody();
  } else if (msg=='L') {
    digitalWrite(ledPin, LOW); // turn LED OFF
    noTone(buzzer);
    delayMicroseconds(500);
  }
}

void arduino_to_pc() {
    //read the input pin
  int buttonState = digitalRead(buttonPin);

  //if the button is pressed
  if (buttonState == 1){
    Serial.write("1");
  }else{
    Serial.write("0");    
  }
}
void loop(){
  //pc_to_arduino();
  arduino_to_pc();
}
