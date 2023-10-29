#include <gb/gb.h>

#include "utils/io.h"
#include "simu.h"
#include "simu_renderer.h"
#include "inst_list.h"
#include "inst.h"

#define EMPTY_TILE_ID 0
#define FLAG_TILE_ID 17

uint8_t bot_x = 1;
uint8_t bot_y = 1;

/// @brief Move the bot
/// @param dx The delta x
/// @param dy The delta y
bool move_bot(int8_t dx, int8_t dy) 
{
    uint8_t tile_id = get_bkg_tile_xy(SIMU_X + bot_x + dx, SIMU_Y + bot_y + dy);

    // Check if we can move to the next tile
    if(tile_id == EMPTY_TILE_ID || tile_id == FLAG_TILE_ID) 
    {
        bot_x += dx;
        bot_y += dy;
        return true;
    } else {
        return false;
    }
}

/// @brief Start the simulation
void simulate() 
{
    // Execute each instruction of the instruction list
    for(uint8_t i = 0; i < inst_count; i++) 
    {
        uint8_t inst_id = inst_ids[i];
        uint8_t inst_rp = inst_rpt[i];

        // Repeat the instruction n times
        for(uint8_t j = 0; j < inst_rp; j++) {
            if(inst_funcs[inst_id]()) {
                // Draw only if the instruction succeeded
                draw_simu();
                delay(100);
            }
        }
    }

    uint8_t final_tile_id = get_bkg_tile_xy(SIMU_X + bot_x, SIMU_Y + bot_y);

    // Check the final tile ID to check if the bot is on the flag
    if(final_tile_id == FLAG_TILE_ID) {
        bnprintf(1, 4, 18, "Flag is at 0x06FA ");

        while(true)
            delay(100);
    } else {
        bnprintf(1, 4, 18, "Failed. Try again.");

        delay(2000);

        bot_x = 1;
        bot_y = 1;

        bnprintf(1, 4, 18, "                  ");
    }
}