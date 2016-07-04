#!/usr/bin/python

import sys, getopt

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
# -s or -intel_hex:
#   This options converts the the address code of the SLXS processor to the Intel
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
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:s",["help","input=","intel_hex"])
    except getopt.GetoptError:
        print 'test.py -i <filename>'
        sys.exit(2)
    for opt, arg in opts:
        #Prints in the standar output the help bar.
        if opt in ('-h',"--help"):
            print "SLSX  micro assembler:"
            print "usage: assembler.py -i <filename> [-s]"
            print "------------------------------------------------------------"
            print "Options:"
            print " 1. [-h|--help] prints the help menu."
            print " 2. [-i|--input] takes a file with SLSX code as an argument\n    and creates an output file with the memory addresses."
            print " 3. [-s|--intel_hex] creates four files in hex_intel format\n    that can be used in the simulator. "
            print "------------------------------------------------------------"
            sys.exit()
        # Calls the read_file function.
        elif opt in ("-i","--input"):
            print "Creating output.txt memory file.."
            read_file(arg)
            memory_creation()
            write_file()
            print "output.txt is succesfuly created"
        #Splits memory on 4 hex_intel files.
        elif opt in ("-s","--intel_hex"):
            print "Creating hex_intel files.."
            intel_hex_converter()
            print "Files were succesfuly created"

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

    f = open(filename, 'r')
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
                line = line.strip(";").split(",")

                #Checks if variables in instruction have correct format. [Error Handling]
                if len(line) > 4:
                    print "the "+str(line)+" contains to many variables."
                    print "Exiting .."
                    raise SystemExit
                elif len(line)< 3:
                    print "the "+str(line)+" contains to few variables."
                    print "Exiting .."
                    raise SystemExit
                #End of checks

                instructions.append(line)

            #Else if line is a variable add it to array variables
            else:
                line = line.split(":")

                # [Error Handling]
                #Check if variable is not a system var.
                if line[0].startswith("_"):
                    print "Only system can declare strings starting with '_'"
                    print "Exiting .."
                    raise SystemExit
                for v in variables:
                    #Check if variable name already exists
                    if  v[0]==line[0]:
                        print "Variable already exists."
                        print "Exiting .."
                        raise SystemExit
                #End of [Error Handling]

                #Adds variable to array and check if its a hex or decimal
                if line[1].find("x") > 0 or line[1].find("X") > 0:
                    #Checks if variable is a number [Error Handling]
                    try:
                        variables.append([line[0],int(line[1],16),var_counter])
                    except ValueError:
                        print "The variable on line '"+str(line)+"'is not a number."
                        print "Exiting .."
                        raise SystemExit
                else:
                    #Checks if variable is a number [Error Handling]
                    try:
                        variables.append([line[0],int(line[1],10),var_counter])
                    except ValueError:
                        print "The variable "+str(line)+"is not a number."
                        print "Exiting .."
                        raise SystemExit

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

    #First line writen :Jump to the codefirst line.
    memory[0].append([4,4,4,code_starts])

    #Store variables to memory.
    i = 1
    temp = []
    for x in variables:
        temp.append(x[1])
        if x[2]%4 == 3:
            memory[i].append(temp)
            i+=1
            temp = []

    #Fill the empty variable slots.
    for x in xrange(0,var_counter/4):
        temp.append(0)
    memory[i].append(temp)
    i+=1

    functions = [] # Contains function_name, address.

    #Write instructions.
    for inst in instructions:
        #Check if instruction is a function and save the address.
        if inst[0].find(":") > 0:
            fun = inst[0].split(":")
            inst[0] = fun[1]

            #[Error Handling]
            #Checks if label does not start with "_".
            if  fun[0].startswith("_") and ( not fun[0].startswith("_main")):
                print "Only system can declare labels starting with '_'"
                print "Exiting .."
                raise SystemExit

            #Checks for duplicate labels.
            for t in functions:
                if fun[0] == t[0]:
                    print "Duplicate label detected: "+str(fun[0])
                    print "Exiting .."
                    raise SystemExit
            #End of [Error Handling]
            functions.append([fun[0],memory[i][0]]) #Push to function name,address.

        shift_val=0
        #Checks if the commands have a shift.
        if inst[2].find("_shift") > 0:
            inst[2]=inst[2].replace("_shift", "")
            shift_val=0x10000

        temp = []
        #Handle the first three variables of the instuction and add them to temp.
        for x in xrange(0,3):
            for var in variables:
                if inst[x] == var[0]:
                    temp.append(var[2])
                    break

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

    #Find all jumps and replace them with the addresses.
    for x in xrange(0,i):
        #Check if the address is a string.
        try:
            val = int(memory[x][1][3])
        except ValueError:
            shift_val=0
            if memory[x][1][3].find("_shift") > 0:
                memory[x][1][3]=memory[x][1][3].replace("_shift", "")
                shift_val=0x10000

            for fun in functions:
                if memory[x][1][3] == fun[0]:
                    memory[x][1][3] = fun[1]|shift_val

    #Adds loop at the end of the program.
    memory[i].append([4,4,4,memory[i][0]])

# The write_file() function creates the output.txt file
def write_file():
    #Write the file.
    f = open ("output.txt",'w')
    #Write the file.
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

    f = [0,1,2,3]
    f[0] = open("mem0.hex","w")
    f[1] = open("mem1.hex","w")
    f[2] = open("mem2.hex","w")
    f[3] = open("mem3.hex","w")

    size = 0x03
    typ  = 0
    address = 0

    #Take memory array and create intel_hex files.
    for x in xrange(0,i+1):

        #For each memory address write to correct file.
        for t in xrange(0,4):
            #sum is the two's compliment that is insert on the end of each block.
            sum = -(size+(address&0xff)+(address>>8&0xff)+typ+(memory[x][1][t]&0xff)+(memory[x][1][t]>>8&0xff)+(memory[x][1][t]>>16&0xff))&0xff;
            f[t].write(":"+'{:02x}'.format(size))
            f[t].write('{:04x}'.format(address))
            f[t].write('{:02x}'.format(typ))
            f[t].write('{:06x}'.format(memory[x][1][t]))
            f[t].write('{:02x}'.format(sum)+"\n")
        address+=1

    #The :00000001FF indicates the EOF.
    for t in xrange(0,4):
        f[t].write(":00000001FF")

    for x in f:
        x.close()

if __name__ == "__main__":
    main(sys.argv[1:])
