#ifndef X11_FAST_H
#define X11_FAST_H

#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <stdint.h>

typedef struct {
    Display* display;
    Window window;
    GC gc;
    Pixmap buffer;
    int width, height;
    XImage* ximage;
    char* pixels;
    int char_size;
    uint32_t bg_color;
} X11Context;

// Инициализация окна
X11Context* x11_init(int width, int height, const char* title);

// Закрытие окна
void x11_close(X11Context* ctx);

// Заливка цветом (RGB)
void x11_fill(X11Context* ctx, uint8_t r, uint8_t g, uint8_t b);

// Обновление окна (вывод буфера на экран)
void x11_flush(X11Context* ctx);

// Рисование символа из bitmap-шрифта
void x11_draw_char(X11Context* ctx, int x, int y, char c, uint8_t r, uint8_t g, uint8_t b);

// Рисование пикселя
void x11_draw_pixel(X11Context* ctx, int x, int y, uint8_t r, uint8_t g, uint8_t b);

// Проверка нажатия клавиши (неблокирующая)
int x11_key_pressed(X11Context* ctx, char* key);

int x11_get_mouse_coords(X11Context* ctx, int* x, int* y);


#endif
