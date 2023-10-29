#pragma once

#include <stdint.h>
#include <stdbool.h>

#define MAX_INST 16

extern uint8_t inst_ids[MAX_INST];
extern uint8_t inst_rpt[MAX_INST];
extern uint8_t inst_count;
extern uint8_t inst_cursor_pos;

extern bool list_empty;

void remove_inst(uint8_t inst_index);
void move_inst(uint8_t inst1_index, uint8_t inst2_index);
void add_inst(uint8_t inst_id);

void update_inst_list();