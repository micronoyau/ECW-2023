#include <gb/gb.h>

#include "inst.h"
#include "inst_list.h"
#include "simu.h"

#include "utils/inputs.h"

uint8_t inst_rpt[MAX_INST] = { 0 };
uint8_t inst_ids[MAX_INST] = { 0 };
uint8_t inst_count = 0;
uint8_t inst_cursor_pos = 0;

uint8_t selected_index = 0;

bool listen_new_inst = false;
bool is_moving_inst = false;
bool list_empty = true;

/// @brief Remove an instruction from the instruction list
/// @param inst_index The instruction index to remove in the instruction list
void remove_inst(uint8_t inst_index) 
{
    if(inst_index + 1 != inst_count) 
    {
        // Shift all following instructions in the instruction list
        for(uint8_t i = 0, j = 0; i < MAX_INST && j < MAX_INST; i++, j++) 
        {
            if(i == inst_index) 
            {
                j++;
            }

            inst_ids[i] = inst_ids[j];
            inst_rpt[i] = inst_rpt[j];
        }
    }

    inst_count--;
}

/// @brief Move or merge 2 instructions in the instruction list
/// @param inst1_index The first instruction index to move/merge
/// @param inst2_index The second instruction inex to move/merge
void move_inst(uint8_t inst1_index, uint8_t inst2_index) 
{
    uint8_t inst1_id = inst_ids[inst1_index];
    uint8_t inst2_id = inst_ids[inst2_index];
    uint8_t inst1_rpt = inst_rpt[inst1_index];
    uint8_t inst2_rpt = inst_rpt[inst2_index];

    // First case. IDs are the same, so we merge instructions
    if(inst1_id == inst2_id) 
    {
        uint16_t rpt_sum = inst1_rpt + inst2_rpt;

        if(rpt_sum > 255) 
        {
            // If the sum of repetitions is more than a stack (255),
            // we fill the first stack to the maximum and put the rest in the second
            inst_rpt[inst1_index] = 255;
            inst_rpt[inst2_index] = rpt_sum - 255;
        } 
        else 
        {
            // If the sum of repetitions is less than a stack (255),
            // we merge all in the first stack and delete the second
            inst_rpt[inst1_index] = rpt_sum;
            remove_inst(inst2_index);
        }
    } 
    // Second case. IDs are differents, so we swap instructions
    else 
    {
        inst_ids[inst1_index] = inst2_id;
        inst_ids[inst2_index] = inst1_id;
        inst_rpt[inst1_index] = inst2_rpt;
        inst_rpt[inst2_index] = inst1_rpt;
    }
}

/// @brief Add a new instruction to the instruction list
/// @param inst_id The instruction ID to add
void add_inst(uint8_t inst_id) 
{
    // Check instruction list maximum size
    if(inst_count >= MAX_INST) {
        return;
    }

    inst_ids[inst_count] = inst_id;
    inst_rpt[inst_count] = 1;

    inst_count++;
    list_empty = false;
}

/// @brief Update the list of instruction
void update_inst_list() 
{
    // If we are adding a new instruction, listen for a directional input
    if(listen_new_inst) 
    {
        if(KEY_TRIGGERED(J_LEFT)) 
        {
            add_inst(INST_LEFT);
            listen_new_inst = false;
        } 
        else if(KEY_TRIGGERED(J_RIGHT)) 
        {
            add_inst(INST_RIGHT);
            listen_new_inst = false;
        } 
        else if(KEY_TRIGGERED(J_UP)) 
        {
            add_inst(INST_UP);
            listen_new_inst = false;
        } 
        else if(KEY_TRIGGERED(J_DOWN)) 
        {
            add_inst(INST_DOWN);
            listen_new_inst = false;
        }
    } 
    else 
    {
        // Select previous instruction
        if(KEY_TRIGGERED(J_LEFT)) 
        {
            inst_cursor_pos -= (inst_cursor_pos > 0) ? 1 : 0;
        } 
        // Select next instruction
        else if(KEY_TRIGGERED(J_RIGHT)) 
        {
            inst_cursor_pos += (inst_cursor_pos < inst_count - 1) ? 1 : 0;
        } 
        // Increase instruction repetition
        else if(KEY_TRIGGERED(J_UP) && !list_empty) 
        {
            inst_rpt[inst_cursor_pos] += (inst_rpt[inst_cursor_pos] < 255) ? 1 : 2;
        } 
        // Decrease instruction repetition
        else if(KEY_TRIGGERED(J_DOWN) && !list_empty) 
        {
            inst_rpt[inst_cursor_pos] -= (inst_rpt[inst_cursor_pos] > 1) ? 1 : 2;
        } 
        // Add a new instruction
        else if(KEY_TRIGGERED(J_A)) 
        {
            listen_new_inst = true;
        } 
        // Remove the selected instruction
        else if(KEY_TRIGGERED(J_B) && !list_empty) 
        {
            remove_inst(inst_cursor_pos);
            list_empty = inst_count == 0;
            inst_cursor_pos = 0;
        } 
        // Swap/Merge the selected instruction
        else if(KEY_TRIGGERED(J_SELECT) && !list_empty) 
        {
            if(is_moving_inst) 
            {
                move_inst(inst_cursor_pos, selected_index);
                is_moving_inst = false;
            } 
            else 
            {
                selected_index = inst_cursor_pos;
                is_moving_inst = true;
            }
        } 
        // Start the simulation
        else if(KEY_TRIGGERED(J_START)) 
        {
            simulate();
        }
    }
}