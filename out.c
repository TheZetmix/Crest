# include "stdio.h" 
 
 int sum ( int a , int b ) { 
 return a + b ; 
 } 
  int main ( ) { for ( int i = 0 ; i < 30 ; ++ i ) { switch ( i ) { case 10 : case 15 : case 20 : { printf ( "daaa\n" ) ; break ; } default : { printf ( "%d\n" , sum ( i , i + 5 ) ) ; break ; } } } }