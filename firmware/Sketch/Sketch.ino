#include <ESP32-HUB75-MatrixPanel-I2S-DMA.h>

// LED panel configuration
#define PANEL_WIDTH 64
#define PANEL_HEIGHT 64
#define CLKPHASE false
#define BRIGHTNESS 32  // 0-255

// LED panel pins
const HUB75_I2S_CFG::i2s_pins HUB75_PINMAP { 
  13, // R1
  12, // G1
  14, // B1
  27, // R2
  26, // G2
  25, // B2
  22, // A
  18, // B
  5,  // C
  17, // D
  23, // E
  4,  // LAT
  15, // OE
  16  // CLK
};

// other pins
#define RELAY_CTRL_PIN 32
#define RELAY_READ_PIN 35
#define BUILTIN_LED_PIN 2

#define BAUD_RATE 115200


MatrixPanel_I2S_DMA *dma_display = nullptr;

void setup() {
  Serial.begin(BAUD_RATE);

  pinMode(RELAY_READ_PIN, INPUT);
  
  pinMode(BUILTIN_LED_PIN, OUTPUT);

  pinMode(RELAY_CTRL_PIN, OUTPUT);
  digitalWrite(RELAY_CTRL_PIN, LOW); // start off

  // panel config
  HUB75_I2S_CFG mxconfig(
    PANEL_WIDTH, PANEL_HEIGHT, 1, HUB75_PINMAP
  );
  mxconfig.clkphase = CLKPHASE;

  // start panel
  dma_display = new MatrixPanel_I2S_DMA(mxconfig);
  dma_display->begin();
  dma_display->setBrightness8(BRIGHTNESS);
  dma_display->clearScreen();

  delay(1000);
  digitalWrite(RELAY_CTRL_PIN, HIGH);
}

int last_relay_state = -1;

void loop() {

  // read the on/off switch
  int relay_state = digitalRead(RELAY_READ_PIN);
  if (relay_state == HIGH) {
    digitalWrite(BUILTIN_LED_PIN, HIGH);
    if (last_relay_state != HIGH) {
      Serial.println("HIGH");
      drawTest();
      delay(50);
    }
  } else {
    digitalWrite(BUILTIN_LED_PIN, LOW);
    if (last_relay_state != LOW) {
      Serial.println("LOW");
      dma_display->clearScreen();
      delay(50);
    }
  }
  last_relay_state = relay_state;

  // serial read
  read_serial();

  // serial write
  // TODO

}
