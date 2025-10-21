#include "libterm.h"   
#include <unistd.h>    
#include <stdio.h>     

int main() {
    
    x11_draw_char(ctx, 10, 10, 'P', 255, 255, 255);
    x11_draw_pixel(ctx, 30, 30, 255, 0, 0);

    const char* text = "test test";
    for (int i = 0; text[i]; i++) {
        x11_draw_char(ctx, 10 + i * 8, 30, text[i], 0, 255, 0); 
    }
    
    x11_flush(ctx);

    char key = 0;
    while (1) {
        if (x11_key_pressed(ctx, &key)) {
            printf("Key pressed: %d\n", key); 
            if (key == 100) {
                printf("DODIK\n");
            }
            if (key == 27) break;
        }
        usleep(1000); 
    }
    
    x11_close(ctx);
    return 0;
}
