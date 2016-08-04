/* Variables */
Z   : 0
clear: 10
move1: 0
move2: 10
mul1 : 5
mul2 : 2
div1 : 9
div2 : 2
shift: 1
ls: 2
rs:2
xor1: 5
xor2: 1
add1: 5
add2: 1
sub1: 6
sub2: 2
and1: 5
and2: 1
or1: 6
or2: 1

/*main function*/
_main: Z,Z,Z;
      _CLR,clear;
      _MOV,move1,move2;
      _MUL,mul1,mul2;
      _DIV,div1,div2;
      _LSHIFT,shift,ls;
      _RSHIFT,shift,rs;
      _XOR,xor1,xor2;
      _ADD,add1,add2;
      _SUB,sub1,sub2;
      _AND,and1,and2;
      _OR,or1,or2;
loop: Z,Z,Z,loop;

/*command:*/
//python slxs_macros.py -i tests/macros.asm -s -f -p clear,move1,mul1,div1,div2,shift,xor1,add1,sub1,and1,or1
