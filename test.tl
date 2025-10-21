#include "stdio.h"

[!c] {
    int sum(int a, int b) {
        return a + b;
    }
}

fn main() : int {
    var number : int = 6;
    match (number) {
        case 6 || 8 {
            printf("number is 6 or 8\n");
        }
        default {
            printf("idk\n");
        }
    }
}
