/*
 * Author: Vasilis Sikkis
 *
 * The program converts the the address code of the SLXS processor to the Intel
 * Hex file format. It takes the input file with the SLXS code and produces 4
 * output files.
 * Each Intel Hex block in the SLXS simulator contains the following data:
 *  1. Start code, one character, an ASCII colon ':'.
 *  2. Byte count, two hex digits, indicating the number of bytes (hex digit
 *     pairs) in the data field.
 *  3. Address, four hex digits, representing the 16-bit beginning memory address
 *    offset of the data.
 *  4. Record type, two hex digits, 00 to 05,in the implimentation the 01 and 03 is
 *     used only
 *  5. Data, six hex digits.
 *  6. Checksum, two hex digits, a computed value that can be used to verify the
 *     record has no errors.
 *
 */
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv){

  FILE *file[5];
  unsigned int address=0, sum=0, size=0x03, type=0, add,mem[4];
  int i;

  if(argc < 2){
    printf("ERROR: An input file is required.\n");
    return -1;
  }

  if((file[4]=fopen(argv[1],"r"))==NULL){
    printf("ERROR: The file cannot be opened.\n");
    return -2;
  }
  else{

    file[0]=fopen("mem0.hex", "w");
    file[1]=fopen("mem1.hex", "w");
    file[2]=fopen("mem2.hex", "w");
    file[3]=fopen("mem3.hex", "w");

    /* Reads the file provided and creates the output files. */
    while(fscanf(file[4], "%x %x %x %x %x",&add,&mem[0],&mem[1],&mem[2],&mem[3])!=EOF){

          /*Find out if there are empty spaces on the addresses and continue filling with blank blocks*/
          while(add != address*4){
            for( i = 0; i < 4; i++ ){
              int val=0;
              /*sum is the two's compliment that is insert on the end of each block*/
              sum = -(size+(address&0xff)+(address>>8&0xff)+type+(val&0xff)+(val>>8&0xff)+(val>>16&0xff))&0xff;
              fprintf(file[i], "%02x%04x%02x%06x%02x\n",size,address,type,val,sum);
            }
            address++;
          }

          for( i = 0; i < 4; i++ ){
            /*sum is the two's compliment that is insert on the end of each block*/
            sum = -(size+(address&0xff)+(address>>8&0xff)+type+(mem[i]&0xff)+(mem[i]>>8&0xff)+(mem[i]>>16&0xff))&0xff;
            fprintf(file[i], "%02x%04x%02x%06x%02x\n",size,address,type,mem[i],sum);
          }

          address++;

    }
    /*The :00000001FF indicates the EOF.*/
    for( i = 0; i < 4; i++ ){
      fprintf(file[i], ":00000001FF");
    }
  }

  for( i = 0; i< 5; i++){
    fclose(file[i]);
  }
}
