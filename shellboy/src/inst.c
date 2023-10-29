#include "inst.h"
#include "simu.h"

bool (*inst_funcs[4])() = {
    inst_go_up,
    inst_go_right,
    inst_go_down,
    inst_go_left
};

bool inst_go_left() {
    return move_bot(-1, 0);
}

bool inst_go_right() {
    return move_bot(1, 0);
}

bool inst_go_up() {
    return move_bot(0, -1);
}

bool inst_go_down() {
    return move_bot(0, 1);
}