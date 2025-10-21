# include "stdio.h" 
 
 int sum ( int a , int b ) { 
 return a + b ; 
 } 
  typedef struct { int a ; int b ; } Some ; int main ( ) { Some test = { 5 , 8 } ; printf ( "%d\n" , sum ( test . a , test . b ) ) ; }