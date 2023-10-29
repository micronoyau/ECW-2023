#include <gb/gb.h>

#include "inst_list_renderer.h"
#include "inst_list.h"

#include "utils/math.h"
#include "utils/io.h"

#include "res/sprites/selector.h"

#define INST_LIST_WIN_X 2
#define INST_LIST_WIN_Y 2
#define INST_LIST_WIN_WIDTH 11

#define INST_TILES_SIZE 8
#define INST_TILES_OFFSET 12

#define INST_REPEAT_WIN_X 14
#define INST_REPEAT_WIN_Y 2

#define GB_X_OFFSET 8
#define GB_Y_OFFSET 16

/// @brief Initilize the instruction list renderer
void init_inst_list_renderer() 
{
    SPRITES_8x8;

    // Fill VRAM with sprite data
    set_sprite_data(0, 1, selector_data);
    set_sprite_tile(0, 0);

    // Move the cursor to the 
    uint8_t cursor_x = GB_X_OFFSET + INST_LIST_WIN_X * INST_TILES_SIZE;
    uint8_t cursor_y = GB_Y_OFFSET + INST_LIST_WIN_Y * INST_TILES_SIZE;
    move_sprite(0, cursor_x, cursor_y);

    SHOW_SPRITES;
}

/// @brief Draw the instruction list on the screen
void draw_inst_list() 
{
    // Draw all instruction tiles or "No inst" if the instruction list is empty
    if(list_empty) 
    {
        bnprintf(INST_LIST_WIN_X, INST_LIST_WIN_Y, 7, "No inst");
    } 
    else 
    {
        // Calculate the scrolling list starting element index
        uint8_t start_x = max(inst_cursor_pos - INST_LIST_WIN_WIDTH + 1, 0);

        for(uint8_t x = start_x, i = 0; i < INST_LIST_WIN_WIDTH; x++, i++) 
        {
            if(i < inst_count) 
            {
                set_bkg_tile_xy(INST_LIST_WIN_X + i, INST_LIST_WIN_Y, INST_TILES_OFFSET + inst_ids[x]);
            } 
            else 
            {
                set_bkg_tile_xy(INST_LIST_WIN_X + i, INST_LIST_WIN_Y, 0);
            }
        }
    }

    draw_inst_cursor();
    draw_inst_repeat();
}

/// @brief Draw the selection cursor
void draw_inst_cursor() 
{
    // Calculate cursor position and move cursor sprite
    uint8_t cursor_y = GB_Y_OFFSET + INST_LIST_WIN_Y * INST_TILES_SIZE;
    uint8_t cursor_x = min(
        GB_X_OFFSET + (INST_LIST_WIN_X + inst_cursor_pos) * INST_TILES_SIZE, 
        GB_X_OFFSET + (INST_LIST_WIN_X + INST_LIST_WIN_WIDTH - 1) * INST_TILES_SIZE
    );

    move_sprite(0, cursor_x, cursor_y);
}

/// @brief Draw the repeat counter for the selected instruction
void draw_inst_repeat() 
{
    if(list_empty) 
    {
        bnprintf(INST_REPEAT_WIN_X, INST_REPEAT_WIN_Y, 4, "    ");
    } 
    else 
    {
        bnprintf(INST_REPEAT_WIN_X, INST_REPEAT_WIN_Y, 4, "x%u  ", inst_rpt[inst_cursor_pos]);
    }
}