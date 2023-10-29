#include <gb/gb.h>

#include "simu_renderer.h"
#include "simu.h"

#include "res/sprites/bot.h"

#define SIMU_TILES_SIZE 8

#define GB_X_OFFSET 8
#define GB_Y_OFFSET 16

/// @brief Initialize simulation renderer
void init_simu_renderer() {
    SPRITES_8x8;

    // Create bot sprite data
    set_sprite_data(1, 1, bot_data);
    set_sprite_tile(1, 1);
    move_sprite(1, GB_X_OFFSET + SIMU_X * SIMU_TILES_SIZE, GB_Y_OFFSET + SIMU_Y * SIMU_TILES_SIZE);

    SHOW_SPRITES;
}

/// @brief Draw the bot of sprite layer
void draw_simu() {
    move_sprite(1, GB_X_OFFSET + (SIMU_X + bot_x) * SIMU_TILES_SIZE, GB_Y_OFFSET + (SIMU_Y + bot_y) * SIMU_TILES_SIZE);
}