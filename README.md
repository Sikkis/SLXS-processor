# summer_project
The file contains how the project that it was submitted is structured. The SLXS tool is stored 
into the tool folder with the algorithms and operators containing samples of SLXS code. The extras
folder contains small applications that was used in the early stages of the project but may be useful.

-algorithms
    -AES
        aes_slxs.txt                | The AES algorithm implementation on SLXS
        aes_reference.txt           | The reference Aes algorithm.
    -PRESENT
        present.c                   | The Present algorithm implementation on C     
        present.txt                 | The Present algorithm implementation on SLXS
        present_precomputedval.txt  | The Present algorithm implementation on SLXS
    -extras
        -intelhex_converter                      
            intelhex_converter.c    | Intel hex converter implementation on C
        -mem_template
            template_creator.c      | Memory template implementation on C
        -simulator
            main.c                  | SLXS Simulator on C
            Makefile
    -operators
        and.txt                     | The and operation on SLXS
        div_mod.txt                 | The division, modulo operation on SLXS
        lshift.txt                  | The left shift operation on SLXS
        macros.txt                  | Macros examples on SLXS
        mul.txt                     | The mulitply operation on SLXS
        or.txt                      | The or operation on SLXS
        rshift.txt                  | The right shift operation on SLXS
    -tool
        -output_files               | Output files created SLXS tool 
            mem0.hex                | First intel hex format file
            mem1.hex                | Second intel hex format file
            mem2.hex                | Third intel hex format file 
            mem3.hex                | Forth intel hex format file
        slxs.py                     | The SLXS tool 
        slxs_macros.py              | The SLXS tool with macros
    README.MD                       | Readme file with how to use tutorial
    results.txt                     | Results of operators and algorithms
------------------------------------------------------------------------------------------
How to run SLXS tool:
------------------------------------------------------------------------------------------  
Inside the tool folder to run the code:
python slxs.py -i inputfile         | will create the compiled file
python slxs.py -f                   | will create the four hex files
python slxs.py -s                   | will use the simulator and output the file

Recommended use:
python slxs.py -i inputfile -f -s   | The three options together so the [-p] option will be enabled
python slxs.py -i inputfile -f -s -p variables | Shows the requested variables

option [-u] Enables the undefined variables.

Better explanation of the options are inside the manual.
------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------
How to run extra material programs:
------------------------------------------------------------------------------------------     
  Simulator
  Compile code:
    make
  Run code:
    ./slxs.exe mem0.hex  mem1.hex mem2.hex mem3.hex 0
------------------------------------------------------------------------------------------
  Intelhex_converter:
  Compile code:
    gcc intelhex_converter.c
  Run code:
    ./a.out inputfile
------------------------------------------------------------------------------------------
  template_creator:
  Compile code:
    gcc template_creator.c
  Run code:
    ./a.out
------------------------------------------------------------------------------------------   