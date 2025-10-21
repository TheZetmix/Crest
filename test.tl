#include "stdio.h"

[!c] {
    int sum(int a, int b) {
        return a + b;
    }
}

fn main() : int {
    for (i : int = 0; i < 30; ++i) {
        match (i) {
            case 10 || 15 || 20 {
                printf("daaa\n");
            }
            default {
                printf("%d\n", sum(i, i+5));
            }
        }
    }
}
