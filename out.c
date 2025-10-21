# include "stdio.h" 
 
 int sum ( int a , int b ) { 
 return a + b ; 
 } 
  int main ( ) { int arr[] = { 0 , 1 , 2 , 3 , 4 , 5 } ; for ( int i = 0 ; i < sizeof ( arr ) / sizeof ( arr [ 0 ] ) ; i ++ ) { printf ( "%d\n" , sum ( arr [ i ] , i ) ) ; } }