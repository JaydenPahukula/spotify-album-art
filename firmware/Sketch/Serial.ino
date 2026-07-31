// functions for sending and receiving messages over serial

// constants
const size_t max_msg_len = 64;
const char msg_start_marker = '<';
const char msg_end_marker = '>';

// state
char curr_msg[max_msg_len];
size_t curr_msg_len = 0;
bool is_receiving = false;

void read_serial() {
  while(Serial.available() > 0) {
    char c = Serial.read();

    if(is_receiving) {
      if (c == msg_end_marker) {
        is_receiving = false;
        curr_msg[curr_msg_len] = 0; // terminate with null
        Serial.print("GOT MESSAGE: ");
        Serial.println(curr_msg);
        curr_msg_len = 0;
      } else {
        curr_msg[curr_msg_len] = c;
        curr_msg_len++;
        if (curr_msg_len == max_msg_len) {
          // message is too long, it can't be valid. Throw it away
          curr_msg_len = 0;
          is_receiving = false;
        }
      }
    } else if (c == msg_start_marker) {
      // start new message
      curr_msg_len = 0; 
      is_receiving = true;
    }
  }
}
