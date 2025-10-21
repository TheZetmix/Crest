#include "stdio.h"

[!c] {
    int sum(int a, int b) {
        return a + b;
    }
}

struct Some {
    a : int;
    b : int;
}

fn main() : int {
    var test : Some = {5, 8};
    printf("%d\n", sum(test.a, test.b));
}
