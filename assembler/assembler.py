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

        #delete whole line comments
        if line.find("//") >= 0:
            t = line.split("//")
            line= t[0]

        #delete block comments
        if line.find("/*") >= 0:
            t = line.split("/*")
            t1 = t[1].split("*/")
            line = t[0]+t1[1]

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
    # print instructions
    # print variables
    f.close()

def write_file():
    #create memory blocks format address + [ins,ins,ins,] later
    memory = []
    global i
    x=0
    while x<=0xFFFF:
        memory.append([x])
        x+=4
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
    for x in xrange(0,var_counter/4):
        temp.append(0)
    memory[i].append(temp)
    i+=1

    functions = [] # Contains function_name, address

    #Write instructions
    for inst in instructions:
        #check if instruction is a function and save the address
        if inst[0].find(":") > 0:
            fun = inst[0].split(":")
            # print fun
            inst[0] = fun[1]
            # print inst
            functions.append([fun[0],memory[i][0]]) #push to function name,address
            # print "memory"+ str(memory[i][0])

        #handle the first three variable of the instuction and add them to temp
        # print "memory"+ str(memory[i])
        # print "normal"
        temp = []
        for x in xrange(0,3):
            # print inst[x]
            for var in variables:
                if inst[x] == var[0]:
                    # print str(x) + str(var[0])
                    # print "address "+ ('{:05x}'.format(var[2])+" ")
                    temp.append(var[2])
                    break

        #Checks if instuction is simple and adds next address
        if len(inst) == 3:
            temp.append(memory[i+1][0])
        #Checks if instuction is a jump and adds name of the jump
        elif len(inst) == 4:
            temp.append(inst[3])

        #adds temp array to memory
        memory[i].append(temp)
        temp = []
        i+=1

    #find all jumps and replace them with the addresses
    for x in xrange(0,i):
        try:
            val = int(memory[x][1][3])
        except ValueError:
            for fun in functions:
                if memory[x][1][3] == fun[0]:
                    memory[x][1][3] = fun[1]

    # add loop at the end of the program.
    memory[i].append([4,4,4,memory[i][0]])

    #Write the file
    f = open ("output.txt",'w')
    #Write the file
    for x in xrange(0,i+1):
        f.write('{:04x}'.format(memory[x][0])+" ")
        f.write('{:05x}'.format(memory[x][1][0])+" ")
        f.write('{:05x}'.format(memory[x][1][1])+" ")
        f.write('{:05x}'.format(memory[x][1][2])+" ")
        f.write('{:05x}'.format(memory[x][1][3])+"\n")
    f.close()

    # print " "
    # for x in xrange(0,i+1):
    #     print memory[x]
if __name__ == "__main__":
    main(sys.argv[1:])
