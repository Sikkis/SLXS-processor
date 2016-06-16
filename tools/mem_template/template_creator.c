#include <stdio.h>
#include <stdlib.h>
/*
 * Creates a file containing the all the addresses 
 * that can be used. from 0000-ffff.
 */
int main(int argc, char **argv){

  FILE *file;
  int i=0;

    file=fopen("template.txt", "w");

    while(i<=0xFFFF){
      fprintf(file,"%04x\n",i);
      i=i+4;
    }
    fclose(file);
}
