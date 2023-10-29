#include <gb/gb.h>

#include "inputs.h"

uint8_t curr_keys = 0;
uint8_t prev_keys = 0;

void update_keys() {
    prev_keys = curr_keys;
    curr_keys = joypad();
}