#include <ESP32-HUB75-MatrixPanel-I2S-DMA.h>

// LED panel configuration
#define PANEL_WIDTH 64
#define PANEL_HEIGHT 64
#define CLKPHASE false
#define BRIGHTNESS 32  // 0-255

// LED panel pins
const HUB75_I2S_CFG::i2s_pins HUB75_PINMAP { 
  R1_PIN_DEFAULT,   //  R1 -> 25
  G1_PIN_DEFAULT,   //  G1 -> 26
  B1_PIN_DEFAULT,   //  B1 -> 27
  R2_PIN_DEFAULT,   //  R2 -> 14
  G2_PIN_DEFAULT,   //  G2 -> 12
  B2_PIN_DEFAULT,   //  B2 -> 13
  A_PIN_DEFAULT,    //   A -> 23
  B_PIN_DEFAULT,    //   B -> 19
  C_PIN_DEFAULT,    //   C -> 5
  D_PIN_DEFAULT,    //   D -> 17
  32,               //   E -> 32
  LAT_PIN_DEFAULT,  // LAT -> 4
  OE_PIN_DEFAULT,   //  OE -> 15
  CLK_PIN_DEFAULT   // CLK -> 16
};

// other pins
#define ON_OFF_SWITCH_PIN 22
#define BUILTIN_LED_PIN 2
#define RELAY_PIN 21

#define BAUD_RATE 115200


MatrixPanel_I2S_DMA *dma_display = nullptr;


void drawTest() {
  int x, w;
  int h = PANEL_HEIGHT * 5 / 6;
  uint16_t color;
  uint8_t a;
  for (int i = 0; i < 6; i++){
    int x = PANEL_HEIGHT * i / 6;
    int w = (PANEL_HEIGHT * (i+1) / 6) - x;
    if (i == 0) color = dma_display->color565(0xff,0xff,0x00);
    else if (i == 1) color = dma_display->color565(0x00,0xff,0xff);
    else if (i == 2) color = dma_display->color565(0x00,0xff,0x00);
    else if (i == 3) color = dma_display->color565(0xff,0x00,0xff);
    else if (i == 4) color = dma_display->color565(0xff,0x00,0x00);
    else color = dma_display->color565(0x00,0x00,0xff);
    dma_display->fillRect(x, 0, w, h, color);
    a = 0x31 * i;
    color = dma_display->color565(a, a, a);
    dma_display->fillRect(x, h, w, PANEL_HEIGHT - h, color);
  }
}

void setup() {
  Serial.begin(BAUD_RATE);

  pinMode(ON_OFF_SWITCH_PIN, INPUT_PULLUP);

  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW); // start off

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

  delay(500);
}

int last_state = -1;
int count = 0;
void loop() {

  // read the on/off switch
  int read = digitalRead(ON_OFF_SWITCH_PIN);
  if (read == HIGH) {
    digitalWrite(RELAY_PIN, HIGH);
    if (last_state != HIGH) {
      drawTest();
      delay(50);
    }
  } else {
    digitalWrite(RELAY_PIN, LOW);
    if (last_state != LOW) {
      dma_display->clearScreen();
      delay(50);
    }
  }
  last_state = read;

  // serial read
  char *buffer;
  size_t buffer_len = Serial.readBytesUntil('\n', buffer, 1024))
  if (buffer_len > 0) {
    
  }

  // serial write
  if (count % 300 == 0) {
    Serial.println("hello from the ESP32");
  }

  count++;
  delay(10);
}
