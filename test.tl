#include "stdio.h"

struct Vec2 {
    x : int;
    y : int;
}

fn Vec2_sum(this : *Vec2) : int {
    return this->x + this->y;
}

fn main() : int {
    var some_vec : Vec2 = {10, 15};
    
}
