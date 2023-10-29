#pragma once

#include <stdint.h>

#define KEY_TRIGGERED(KEY) ((KEY & curr_keys) && !(KEY & prev_keys))

extern uint8_t curr_keys;
extern uint8_t prev_keys;

void update_keys();