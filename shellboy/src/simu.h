#pragma once

#include <stdint.h>
#include <stdbool.h>

extern uint8_t bot_x;
extern uint8_t bot_y;

bool move_bot(int8_t dx, int8_t dy);
void simulate();