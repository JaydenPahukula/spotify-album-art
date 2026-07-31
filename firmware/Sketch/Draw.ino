
// draw a test image to the panel
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