/*
 * The program simulates a slxs processor.It takes 4 files.
 * Each file has the form of intel hex file format.
 * slxs a,b,c,d
 * D = *b-*a
 * C = D ^ c
 * T = C >>1
 *
 * If MSB(d) =  0 : *b = C
 * else if MSB(d) 1 : *b = T
 *
 * if D <= 0 goto d
 * else got to PC+1
 *
 */
#include <stdio.h>


int main(int argc, char **argv){

  FILE *file[4];
  char c;
  unsigned int size, address, type, data, sum;
  int mem[4][16384];
  int A, B, C, D, addr_B, PC=0,Delta, Gamma, Theta;;
  int i, round=0;
  int count_file=0;

  if(argc < 5){
    printf("ERROR: to run the program you need to provide 4 input files for memeory data.\n");
    return -1;
  }

  file[0]=fopen(argv[1], "r");
  file[1]=fopen(argv[2], "r");
  file[2]=fopen(argv[3], "r");
  file[3]=fopen(argv[4], "r");

  // Read input files ///////////////////////////////////////////
  while(count_file < 4){
    size = 3;
    address = 0;
    while(size != 0){
      fscanf(file[count_file], "%c %2x %4x %2x ", &c, &size, &address, &type);
      if(size == 3){
        fscanf(file[count_file], "%6x ", &data);
        mem[count_file][address] = data & 131071;
      }
      fscanf(file[count_file], "%2x ", &sum);
    }
    count_file++;
  }

  fclose(file[0]);
  fclose(file[1]);
  fclose(file[2]);
  fclose(file[3]);
  ///////////////////////////////////////////////////////////////

  for(i=0;i<6;i++){
    printf("%05x %05x %05x %05x %05x\n", i<<2, mem[0][i], mem[1][i], mem[2][i], mem[3][i]);
  }
  // core ///////////////////////////////////////////////////////
  while(!
        (mem[0][(PC>>2) & 16383]==mem[1][(PC>>2) & 16383]
         && mem[1][(PC>>2) & 16383]==mem[2][(PC>>2) & 16383]
         && mem[3][(PC>>2) & 16383]==PC)){
    printf("##%d##\n", round++);
    printf("PC = %05x\n", PC);
    printf("PC>>2& = %05x\n", (PC>>2) & 16383);
    //    for(i=0;i<11;i++){
    //    for(i=64;i<87;i++){
    //    for(i=15870;i<15877;i++){
    //for(i=158;i<170;i++){
    //   printf("%05x %05x %05x %05x %05x\n", i<<2, mem[0][i], mem[1][i], mem[2][i], mem[3][i]);
    // }
    // Read address /////////////////////////////////////////////
    A = mem[PC & 3][(PC>>2) & 65535];
    addr_B = mem[(PC+1) & 3][((PC+1)>>2) & 16383] & 65535;
    C = mem[(PC+2) & 3][((PC+2)>>2) & 65535];
    D = mem[(PC+3) & 3][((PC+3)>>2) & 65535];

    // Read data ////////////////////////////////////////////////
    A = mem[A & 3][(A>>2) & 16383];
    B = mem[addr_B & 3][(addr_B>>2) & 16383];
    C = mem[C & 3][(C>>2) & 16383];

    // ALU //////////////////////////////////////////////////////
    Delta = (B - A) & 131071;
    Gamma = (Delta ^ C) & 131071;
    Theta = (Gamma>>1) & 65535;

    // Write to  memory /////////////////////////////////////////////
    if((D>>16) & 1) {
      mem[addr_B & 3][addr_B>>2] = Theta;
    }
    else {
      mem[addr_B & 3][addr_B>>2] = Gamma;
    }
    // PC ///////////////////////////////////////////////////////
    if(((Delta>>16) & 1) || Delta == 0){
      PC=(D & 65535);
    }
    else {
      PC+=4;
    }
  }
  ///////////////////////////////////////////////////////////////

  printf("##%d##\n", round);
  printf("PC = %05x\n", PC);
  for(i=0;i<6;i++){
    printf("%05x %05x %05x %05x %05x\n", i<<2, mem[0][i], mem[1][i], mem[2][i], mem[3][i]);
  }
  return 0;
}
