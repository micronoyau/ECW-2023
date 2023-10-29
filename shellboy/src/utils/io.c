#include <gb/gb.h>
#include <stdarg.h>

#include "io.h"
#include "../res/tilesets/font.h"

#define _TEXT_OFF 0xB0
#define _TEXT_CHAR_UPP_A _TEXT_OFF + 0x01
#define _TEXT_CHAR_LOW_A _TEXT_OFF + 0x2a
#define _TEXT_CHAR_DIGIT _TEXT_OFF + 0x1b

#define _TEXT_E_MARK     _TEXT_OFF + 0x25
#define _TEXT_POINT      _TEXT_OFF + 0x26
#define _TEXT_L_BRACKET  _TEXT_OFF + 0x27
#define _TEXT_R_BRACKET  _TEXT_OFF + 0x28
#define _TEXT_UNDERSCORE _TEXT_OFF + 0x29

/// @brief Load the font
void load_font() {
    set_bkg_data(_TEXT_OFF, 68, font_data);
}

/// @brief Print a character at a given position on background layer
/// @param x The X position of the character
/// @param y The Y position of the character 
/// @param chr The character to print
/// @return The size written
uint8_t bprint_char(uint8_t x, uint8_t y, char chr) {
    uint8_t tile = _TEXT_OFF + chr;

    if(chr >= 'a' && chr <= 'z') {
        tile = _TEXT_CHAR_LOW_A + chr - 'a';
    } else if(chr >= 'A' && chr <= 'Z') {
        tile = _TEXT_CHAR_UPP_A + chr - 'A';
    } else if(chr >= '0' && chr <= '9') {
        tile = _TEXT_CHAR_DIGIT + chr - '0';
    } else if(chr == ' ') {
        tile = _TEXT_OFF;
    } else if(chr == '.') {
        tile = _TEXT_POINT;
    } else if(chr == '_') {
        tile = _TEXT_UNDERSCORE;    
    } else if(chr == '{') {
        tile = _TEXT_L_BRACKET;    
    } else if(chr == '}') {
        tile = _TEXT_R_BRACKET;    
    } else if(chr == '!') {
        tile = _TEXT_E_MARK;
    }

    set_bkg_tiles(x, y, 1, 1, &tile);
    return 1;
}

/// @brief Print an integer at a given position on the background layer
/// @param x The X position of the integer
/// @param y The Y position of the integer
/// @param i The integer to print
/// @return The size written
uint8_t bprint_int(uint8_t x, uint8_t y, uint8_t i) {
    if(i < 10) {
        return bprint_char(x, y, '0' + i);
    } else {
        uint8_t size = bprint_int(x, y, i / 10);
        return size + bprint_char(x + size, y, '0' + i % 10);;
    }
}

/// @brief Print a formatted string at a given position on the background layer
/// @param x The X position of the string
/// @param y The Y position of the string
/// @param n The maximum size of the string
/// @param format The string format
/// @param args Format arguments
void bnprintf(uint8_t x, uint8_t y, uint8_t n, const char* format, ...) {
    va_list paramInfo;
    va_start(paramInfo, format);

    uint8_t x_off = 0;

    while(*format != NULL && x_off < n) {

        if(*format == '%' && *(++format) == 'u') {
            x_off += bprint_int(x + x_off, y, (uint8_t)va_arg(paramInfo, uint8_t));
        } else {
            x_off += bprint_char(x + x_off, y, *format);
        }

        format++;
    }

    va_end(paramInfo);
}