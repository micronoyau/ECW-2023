#include <gb/gb.h>

#include "res/tilesets/tiles.h"
#include "res/maps/map.h"

#include "utils/io.h"
#include "utils/inputs.h"

#include "inst_list.h"
#include "inst_list_renderer.h"
#include "simu.h"
#include "simu_renderer.h"

const char* flag = "  ***REDACTED***  ";

/// @brief Draw the game background just once
void init_background() {
    set_bkg_data(0, 18, tiles_data);
    set_bkg_tiles(0, 0, 20, 18, map_data);

    SHOW_BKG;
}

int main() {
    load_font();
    
    // Initialize game components
    init_background();
    init_inst_list_renderer();
    init_simu_renderer();

    // Game loop
    while(true) {
        update_inst_list();
        update_keys();

        draw_inst_list();
        draw_simu();
    }
}