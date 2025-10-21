# include "stdio.h" 
 typedef struct { int x ; int y ; } Vec2 ; int Vec2_sum ( Vec2* this ) { return this -> x + this -> y ; } int main ( ) { Vec2 some_vec = { 10 , 15 } ; }