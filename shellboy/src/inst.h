#pragma once

#include <stdbool.h>

#define INST_UP 0
#define INST_RIGHT 1
#define INST_DOWN 2
#define INST_LEFT 3

#define MAX_INST_TYPES 4

extern bool (*inst_funcs[MAX_INST_TYPES])();

bool inst_go_left();
bool inst_go_right();
bool inst_go_up();
bool inst_go_down();