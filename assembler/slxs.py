#!/usr/bin/python
import sys, getopt, os
#The main function take the folowing options and arguments as parameter.
#-h or --help:
#   Prints the manual of the program.
# -i <filename> or --input <filename> :
#   Takes an slsx progam and create the memory file. It has the following format:
#       ADDRESS VALUE VALUE VALUE VALUE
#       example:
#          0000 00004 00004 00004 0000C
#   1. ADDRESS: its an 16 bit hex number that reference a physical memory.
#   2. VALUE:   a 17 bit hex number that contains address or variable stored into
#               the memory.
# -f or -intel_hex:
#   This option converts the the address code of the SLXS processor to the Intel
#   Hex file format. It takes the memory array and produces 4 output files.
#   Each Intel Hex block in the SLXS simulator contains the following data:
#       1. Start code, one character, an ASCII colon ':'.
#       2. Byte count, two hex digits, indicating the number of bytes (hex digit
#          pairs) in the data field.
#       3. Address, four hex digits, representing the 16-bit beginning memory address
#          offset of the data.
#       4. Record type, two hex digits, 00 to 05,in the implimentation the 01 and 03 is
#          used only.
#       5. Data, six hex digits.
#       6. Checksum, two hex digits, a computed value that can be used to verify the
#          record has no errors.
# -s or --simulator:
#   This option simulates an slxs processor.The four file created by the -f option
#   are used to create the simulator_output.txt file that contains the result.
#   The slsx processor has the following defintion:
#        slxs a,b,c,d
#        D=*b-*a
#        C = D ^ c
#        T = C >>1
#
#        If MSB(d) =  0 : *b = C
#        else if MSB(d) 1 : *b = T
#
#       if D <= 0 goto d
#       else got to PC+1
# -p
# Reads from the command line and prints the requested variables before and after the simulator
# runs. Every variable must be seperated by a comma "," and all the previous options must be
# enable.If the variable does not exist nothing is displayed.
# Example:
# python slxs.py -i input.txt -f -s -p temp,List,var
#
def main(argv):

    try:
        opts, args = getopt.getopt(argv,"hi:fsp:",["help","input=","intel_hex","simulator"])
    except getopt.GetoptError:
        print 'python test.py --help'
        sys.exit(2)

    #Option Flags
    input_flag = False
    intel_hex_flag = False
    simulator_flag = False
    print_flag = False

    global registers
    registers = []
    global memfiles
    memfiles = []
    # Create directory for output files
    directory ="output_files"
    if not os.path.exists(directory):
        os.makedirs(directory)

    for x in xrange(0,4):
        memfiles.append(directory+"/mem"+str(x)+".hex")

    for opt, arg in opts:
        #Prints in the standar output the help bar.
        if opt in ('-h',"--help"):
            print help_text
            sys.exit()
        #Enable option to create memory
        elif opt in ("-i","--input"):
            input_flag = True
            input_file = arg
        #Enable option for intel_hex format
        elif opt in ("-f","--intel_hex"):
            intel_hex_flag = True
        #Enable option for simulator
        elif opt in ("-s","--simulator"):
            simulator_flag = True
        #Enable option to print variables requested by user
        elif opt in ("-p"):
            print_flag = True
            reg = arg.split(",")
    #Run options in correct order
    if input_flag:
        print "Creating output.txt memory file.."
        read_file(input_file)
        memory_creation()
        write_file()
        print "The output.txt is succesfuly created.\n"
    if intel_hex_flag:
        print "Creating hex_intel files.."
        intel_hex_converter()
        print "Files were succesfuly created.\n"
    if simulator_flag:
        print "Creating result of slsx proccessor."
        simulator()
        print "File simulator_output.txt has been created.\n"
    if print_flag and input_flag and intel_hex_flag and simulator_flag:
        print "Variables"
        print "Before:"
        for r in reg:
            for v in variables:
                k= v[0].split("(")
                if r==k[0]:
                    pos = v[2]/4
                    mem_block = v[2]%4
                    print  v[0]+":"
                    #print "Before: " +str(v[1])
                    print "Before: "+'{:04x}'.format(v[1])
                    #print "After: "+str(mem[mem_block][pos])+"\n"
                    print "After: "+'{:04x}'.format(mem[mem_block][pos])
# The read_file() function takes the input file and splits the code into variables
# and instructions. It also strips the comments and handles some common errors
# that may occur.
def read_file(filename):
    #Read the file.
    global variables
    global instructions
    global var_counter
    instructions = []
    variables = [["Zero",0,4]] # [name,value,address]
    var_counter = 5 #The variable location inside the memory.

    try:
        f = open(filename, 'r')
    except IOError:
        print "Error opening the file \nExiting .."
        raise SystemExit

    for line in f:

        #Remove white spaces from line.
        line = line.strip("\n").replace(" ", "")

        #Delete whole line comments.
        if line.find("//") >= 0:
            t = line.split("//")
            line= t[0]

        #Delete block comments.
        if line.find("/*") >= 0:
            t = line.split("/*")
            t1 = t[1].split("*/")
            line = t[0]+t1[1]

        #Checks if line contains code or it is empty.
        if line:
            #If line is an instruction add it to array instructions.
            if line.find(";") > 0:
                if not line.endswith(";"):
                    print "An instruction does not end correctly with a semicolumn"
                    raise SystemExit

                line = line.strip(";").split(",")

                #Checks if variables in instruction have correct format. [Error Handling]
                if len(line) >=5:
                    print line[4]
                    if line[4]!="_SH":
                        print "the "+str(line)+" contains to many variables.\nExiting .."
                        raise SystemExit
                elif len(line)< 3:
                    print "the "+str(line)+" contains to few variables.\nExiting .."
                    raise SystemExit
                #End of checks

                instructions.append(line)

            #Else if line is a variable add it to array variables
            else:
                line = line.split(":")

                # [Error Handling]
                #Check if variable is not a system var.
                if line[0].startswith("_"):
                    print "Only system can declare strings starting with '_'\nExiting .."
                    raise SystemExit

                for v in variables:
                    list_flag =  False
                    #Check if variable name already exists
                    if  v[0]==line[0]:
                        print v[0]
                        print "Variable already exists. \nExiting .."
                        raise SystemExit

                try:
                    line[1]
                except:
                    print "The line "+str(line)+" does not contains a semicolumn ';' "
                    print "Exciting.."
                    raise SystemExit
                #End of [Error Handling]

                #Variable is a list
                if line[1].startswith("["):
                    list_flag = True
                    var_list = line[1].replace("[", "").replace("]","").split(",")

                    #add pointer to start of the list.
                    variables.append([line[0],var_counter+1,var_counter])
                    var_counter += 1

                    for v in xrange(0,len(var_list)):
                        if var_list[v].startswith("0x") or line[1].startswith("0X"):
                            variables.append([line[0]+"("+str(v)+")",int(var_list[v],16),var_counter])
                        else:
                            variables.append([line[0]+"("+str(v)+")",int(var_list[v],10),var_counter])
                        var_counter+=1
                #Adds variable to array and check if its a hex or decimal
                elif line[1].startswith("0x") or line[1].startswith("0X"):
                    #Checks if variable is a number [Error Handling]
                    try:
                        variables.append([line[0],int(line[1],16),var_counter])
                    except ValueError:
                        print "The variable on line '"+str(line)+"'is not a number.\n\nExiting .."
                        raise SystemExit
                else:
                    #Checks if variable is a number [Error Handling]
                    try:
                        #if it is a negative number change it to the compliment.
                        if int(line[1],10) < 0:
                            variables.append([line[0],int('{:04x}'.format(int(line[1],10)+2**17),16),var_counter])
                        # The number is possitive
                        else:
                            variables.append([line[0],int(line[1],10),var_counter])
                    except ValueError:
                        flag_var= False
                        flag_address= False
                        #if variable is a pointer
                        if line[0].startswith('*'):
                            flag_address= True
                            line[0]=line[0].replace("*","")
                        #Find the variable we want to have the value or the address.
                        for v in variables:
                            if v[0]== line[1]:
                                if flag_address==True:
                                    variables.append([line[0],v[2],var_counter])
                                else:
                                    variables.append([line[0],v[1],var_counter])
                                flag_var= True
                        if not flag_var:
                            print "The variable "+str(line)+"is not a number or a known variable.\nExiting .."
                            raise SystemExit
                if not list_flag:
                    var_counter+=1
    f.close()

# The memory_creation() function creates the memory array that contains the addresses.
# The memory first contains the variables and the the instuctions.
def memory_creation():
    #Create memory blocks format address + [v,v,v,v]
    global memory
    memory = []
    global i

    #initialise memory
    x=0
    while x<=0xFFFF:
        memory.append([x])
        x+=4
    code_starts = var_counter+ var_counter/4

    #Store variables to memory.
    i = 1
    temp = []

    for x in xrange(0,len(variables)):
        temp.append(variables[x][1])
        if x%4==3:
            memory[i].append(temp)
            i+=1
            temp = []

    #Fill the empty variable slots.
    if len(variables)%4!=0:
        for x in xrange(0,4-len(variables)%4):
            temp.append(0)
        memory[i].append(temp)
        i+=1

    #Memory address of undefined variables

    und_var= i

    #Leave space for variables from program.
    for x in xrange (i,i+10):
        memory[x].append([0,0,0,0])
    i+=10

    functions = [] # Contains function_name, address.
    possision=0
    #Write instructions.
    flag_main = False
    for inst in instructions:
        #Check if instruction is a function and save the address.
        if inst[0].find(":") > 0:
            fun = inst[0].split(":")
            inst[0] = fun[1]

            #First line written: Jump to the code
            if(fun[0].startswith("_main")):
                memory[0].append([4,4,4,i*4])
                flag_main  = True
            #[Error Handling]
            #Checks if label does not start with "_"
            if  fun[0].startswith("_") and ( not fun[0].startswith("_main")):
                print "Only system can declare labels starting with '_'\nExiting .."
                raise SystemExit

            #Checks for duplicate labels.
            for t in functions:
                if fun[0] == t[0]:
                    print "Duplicate label detected: "+str(fun[0])+"\nExiting .."
                    raise SystemExit
            for v in variables:
                if fun[0] == v[0]:
                    print "Function can not have the same name as a variable: Duplicate["+str(fun[0])+"]\nExiting .."
                    raise SystemExit
            #End of [Error Handling]
            functions.append([fun[0],memory[i][0]]) #Push to function name,address.

        shift_val=0
        #Checks if the commands have a shift.
        if "_SH" in inst:
            shift_val=0x10000
            inst.pop()

        temp = []
        #Handle the first three variables of the instuction and add them to temp.
        for x in xrange(0,3):
            #store undefined variables to memory.
            try:
                #Checks if the number is hex or decimal
                if inst[x].startswith("0x") or inst[x].startswith("0X"):
                    memory[und_var][1][possision%4] = int(inst[x],16)
                else:
                    memory[und_var][1][possision%4] = int(inst[x],10)

                #if b==undefined variable exit.[Error Handling]
                if x==1:
                    print "Second variable cant be undefined.\nExiting .."
                    raise SystemExit

                temp.append(und_var*4+possision)
                possision=possision+1

                if(possision%4==0):
                    und_var+=1
                    possision=0

            #if it is not a number then check the declared variables
            except ValueError:
                #variable is a label pointer
                label_flag = True
                #add the variable to the temp
                for var in variables:
                    if inst[x] == var[0]:
                        label_flag =False # it is not a label flag
                        temp.append(var[2])
                        break
                #add the label pointer to the temp
                if label_flag:
                    temp.append(inst[x])
                    # print inst[x]


        #Checks if instuction is simple and adds next address.
        if len(inst) == 3:
            temp.append(memory[i+1][0]|shift_val)
        #Checks if instuction is a jump and adds name of the jump.
        elif len(inst) == 4:
            temp.append(inst[3])

        #Adds temp array to memory.
        memory[i].append(temp)
        temp = []
        i+=1

    if not flag_main:
        print "Error the program does not contain a '_main' function\nExiting .."
        raise SystemExit
    #Find all jumps + label pointers and replace them with the addresses.
    for x in xrange(0,i):
        for counter in xrange (0,3):
            try:
                int(memory[x][1][counter])
            except ValueError:
                if memory[x][1][counter].find('(') > 0:
                    lbl= memory[x][1][counter].split('(')
                    lbl[1]= lbl[1].replace(')',"")

                    for fun in functions:
                        if lbl[0] == fun[0]:
                            memory[x][1][counter] = fun[1]+int(lbl[1])
                #The string is neither a variable or a label
                else:
                    print "The variable "+memory[x][1][counter]+" is undifined"
                    raise SystemExit

        #Jump Check if the address is a string(label).
        try:
            int(memory[x][1][3])
        except ValueError:
            for fun in functions:
                if memory[x][1][3] == fun[0]:
                    memory[x][1][3] = fun[1]|shift_val

    #Removes one line
    i-=1
    #Error Handling
    #Checks memory if there is an undeclared label
    for x in xrange(0,i):
        for t in xrange(0,4):
            if not str(memory[x][1][t]).isdigit():
                print "The "+ str(memory[x][1][t])+ " is not declared"
                raise SystemExit

    flag_loop = False
    for fun in functions:
        if fun[0]=="loop":
            if fun[1] == i*4:
                flag_loop = True
    if flag_loop==False:
        print "The loop label has to be declared at the end of the program"
        raise SystemExit
    #End of Error Handling

# The write_file() function creates the output.txt file
def write_file():
    #Write the file.
    try:
        f = open ("output_files/output.txt",'w')
    except IOError:
        print "Error creating the file\nExiting .."
        raise SystemExit

    #Write the file.
    # for x in xrange(0,i+1):
    #     print memory[x]
    for x in xrange(0,i+1):
        f.write('{:04x}'.format(memory[x][0])+" ")
        f.write('{:05x}'.format(memory[x][1][0])+" ")
        f.write('{:05x}'.format(memory[x][1][1])+" ")
        f.write('{:05x}'.format(memory[x][1][2])+" ")
        f.write('{:05x}'.format(memory[x][1][3])+"\n")

    f.close()

# The intel_hex_converter() function takes the memory array and creates four files
# that have the intel hex format.
def intel_hex_converter():

    mem =[[],[],[],[]]
    size = 0x03
    typ  = 0
    address = 0

    try:
        f = open("output_files/output.txt", 'r')
    except IOError:
        print "Error opening the file\nExiting .."
        raise SystemExit

    for line in f:
        line = line.strip("\n")
        temp=line.split(" ")
        mem[0].append(int(temp[1],16))
        mem[1].append(int(temp[2],16))
        mem[2].append(int(temp[3],16))
        mem[3].append(int(temp[4],16))

    f.close()

    f = [0,1,2,3]
    try:
        for x in xrange(0,4):
            f[x] = open(memfiles[x],"w")
    except IOError:
        print "Error creating one of the file\nExiting .."
        raise SystemExit

    #Take memory array and create intel_hex files.
    for x in xrange(0,len(mem[0])):

        #For each memory address write to correct file.
        for t in xrange(0,4):
            #sum is the two's compliment that is insert on the end of each block.
            sum = -(size+(address&0xff)+(address>>8&0xff)+typ+(mem[t][x]&0xff)+(mem[t][x]>>8&0xff)+(mem[t][x]>>16&0xff))&0xff;
            f[t].write(":"+'{:02x}'.format(size))
            f[t].write('{:04x}'.format(address))
            f[t].write('{:02x}'.format(typ))
            f[t].write('{:06x}'.format(mem[t][x]))
            f[t].write('{:02x}'.format(sum)+"\n")
        address+=1

    #The :00000001FF indicates the EOF.
    for t in xrange(0,4):
        f[t].write(":00000001FF")

    for x in f:
        x.close()

# The simulator() function simulates the SLXS simulator.
def simulator():

    f = [0,1,2,3]

    try:
        for x in xrange(0,4):
            f[x] = open(memfiles[x],"r")
    except IOError:
        print "Error opening one of the file\nExiting .."
        raise SystemExit
    #memory stracture
    global mem
    mem =[[],[],[],[]]
    PC=0 #current address

    #For each file while there are data put it in memory
    for count_file in xrange(0,4):
        for line in f[count_file]:
            if line.startswith(":03"):
                address = int(line[3:7],16)
                data = int(line[9:15],16)
                mem[count_file].append(data)

    #Close Files
    for x in f:
        x.close()
    #Core
    rounds = 0
    try:
        while True:
            rounds+=1
            #Read memory addresses
            A = mem[PC & 3][(PC>>2) & 65535]
            addr_B = mem[(PC+1) & 3][((PC+1)>>2) & 16383] & 65535
            C = mem[(PC+2) & 3][((PC+2)>>2) & 65535]
            D = mem[(PC+3) & 3][((PC+3)>>2) & 65535]
            #print "A: "+str(A)+" addr_B: "+str(addr_B)+" C: "+str(C)+" D: "+str(D)
            #print "A: "+str('{:04x}'.format(A))+" addr_B: "+str('{:04x}'.format(addr_B))+" C: "+str('{:04x}'.format(C))+" D: "+str('{:04x}'.format(D))

            #Read Data
            A = mem[A & 3][(A>>2) & 16383]
            B = mem[addr_B & 3][(addr_B>>2) & 16383]
            C = mem[C & 3][(C>>2) & 16383]
            #print "A: "+str(A)+" B: "+str(B)+ " C: "+str(C)
            #print "A: "+str('{:04x}'.format(A))+" B: "+str('{:04x}'.format(B))+ " C: "+str('{:04x}'.format(C))

            #ALU
            Delta = (B - A) & 131071
            Gamma = (Delta ^ C) & 131071
            Theta = (Gamma>>1) & 65535
            #print "Delta: "+str(Delta)+" Gamma: "+str(Gamma)+" Theta: "+str(Theta)
            #print "Delta: "+str('{:04x}'.format(Delta))+" Gamma: "+str('{:04x}'.format(Gamma))+" Theta: "+str('{:04x}'.format(Theta))

            #Write to memory
            if D>>16&1:
                mem[addr_B & 3][addr_B>>2] = Theta
            else:
                mem[addr_B & 3][addr_B>>2] = Gamma
            #PC
            if ((Delta>>16) and 1) or Delta == 0 :
                PC = (D & 65535)
            else:
                PC+=4
            if (PC==(len(mem[0])-1)*4):
                break
        #print "\n"
    except:
        print"\nError while runing the code.."
        raise SystemExit

    print "Number of rounds :"+str(rounds)
    try:
        f = open ("output_files/simulator_output.txt",'w')
    except IOError:
        print "Error creating the file\nExiting .."
        raise SystemExit

    #Write the file.
    for x in xrange(0,len(mem[0])):
        f.write('{:04x}'.format(x<<2)+" ")
        f.write('{:05x}'.format(mem[0][x])+" ")
        f.write('{:05x}'.format(mem[1][x])+" ")
        f.write('{:05x}'.format(mem[2][x])+" ")
        f.write('{:05x}'.format(mem[3][x])+"\n")

    f.close()


################################################################################
help_text="""SLSX  micro assembler:
usage: assembler.py -i <filename> [-s]
------------------------------------------------------------
Options:
1. [-h|--help] prints the help menu.
2. [-i|--input] takes a file with SLSX code as an argument
   and creates an output file with the memory addresses.
3. [-f|--intel_hex] creates four files in hex_intel format
   that can be used in the simulator.
4. [-s|--simulator] It simulates an slxs proccessor. The
   four hex files created by the -f option are used.
5. [-p] Prints the variables before and after the emulator
   runs. All the preivous options must be enable. If the
   variable does not exist nothing is displayed.
------------------------------------------------------------"""
################################################################################
if __name__ == "__main__":
    main(sys.argv[1:])
