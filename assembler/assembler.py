#!/usr/bin/python

import sys, getopt

#The main function take the arguments as parameter.
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hr:")
    except getopt.GetoptError:
        print 'test.py -r <filename>'
        sys.exit(2)
    for opt, arg in opts:
        #Prints in the standar output the help bar
        if opt == '-h':
            print "SLSX assembler"
            sys.exit()
        # Calls the read_file function
        elif opt in ("-r"):
            read_file(arg)
            write_file()

def read_file(filename):
    #Read the file
    global variables
    global instructions
    global var_counter
    instructions = []
    variables = [["Zero",0,4]] # [name,value,address]
    var_counter = 5 # the variable location inside the memory

    f = open(filename, 'r')
    for line in f:
        #remove white spaces from line
        line = line.replace(" ", "")
        #if line is an instruction
        if line.find(";") > 0:
            line = line.strip(";\n").split(",")
            instructions.append(line)

        #else if line is a variable
        else:
            line = line.strip("\n").split(":")
            # add variable to array and check if its a hex or decimal
            if line[1].find("x") > 0 or line[1].find("X") > 0:
                variables.append([line[0],int(line[1],16),var_counter])
            else:
                variables.append([line[0],int(line[1],10),var_counter])
            var_counter+=1
    print instructions
    print variables
    f.close()

def write_file():
    #create memory blocks format address + [ins,ins,ins,] later
    memory = []
    i=0
    while i<=0xFFFF:
        memory.append([i])
        i+=4
    code_starts = var_counter+ var_counter/4

    #First line writen :Jump to the codefirst line.
    memory[0].append([4,4,4,code_starts])

    #store variables to memory
    i = 1
    temp = []
    for x in variables:
        temp.append(x[1])
        if x[2]%4 == 3:
            memory[i].append(temp)
            i+=1
            temp = []
    #fill the empty variable slots
    for x in range(0,var_counter/4):
        temp.append(0)
    memory[i].append(temp)
    i+=1

    #Write instructions
    for inst in instructions:
        if inst[0].find(":") > 0:
            print ("jump"+str(i))
            jump = inst[0].split(":")
            if (jump[0]=="code"):
                print "aa"
        else:
            print "normal"

    #Write the file
    f = open ("output.txt",'w')
    #Write the file
    for x in xrange(0,4):
        f.write('{:04x}'.format(memory[x][0])+" ")
        f.write('{:05x}'.format(memory[x][1][0])+" ")
        f.write('{:05x}'.format(memory[x][1][1])+" ")
        f.write('{:05x}'.format(memory[x][1][2])+" ")
        f.write('{:05x}'.format(memory[x][1][3])+"\n")
    f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
