#pragma once

#include <stdint.h>

void load_font();

uint8_t bprint_char(uint8_t x, uint8_t y, char chr);
uint8_t bprint_int(uint8_t x, uint8_t y, uint8_t i);

void bnprintf(uint8_t x, uint8_t y, uint8_t n, const char* format, ...);