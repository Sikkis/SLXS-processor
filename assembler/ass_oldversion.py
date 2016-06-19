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
    variables = [["Zero",0,4]] # name,value,address
    var_counter = 5

    f = open(filename, 'r')
    for line in f:
        #if line is an instruction
        if line.find(";") > 0:
            line = line.strip(";\n").split(",")
            instructions.append(line)

        #else if line is a variable
        else:
            line = line.strip("\n").split(":")
            #add variable to array and check if its a hex or decimal
            if line[1].find("x") > 0 or line[1].find("X") > 0:
                variables.append([line[0],int(line[1],16),var_counter])
            else:
                variables.append([line[0],int(line[1],10),var_counter])

            var_counter+=1
    f.close()

def write_file():
    #create memory blocks format address + [ins,ins,ins,] later
    memory = []
    i=0
    while i<=0xFFFF:
        memory.append([i])
        i+=4
    #Write the file
    f = open ("output.txt",'w')
    code_starts = var_counter+ var_counter/4

    #Jump to the  code first line.
    f.write('0000 00004 00004 00004 '+'{:05x}'.format(code_starts)+"\n")
    memory[0].append([4,4,4,code_starts])

    i = 1
    temp = []
    for x in variables:
        temp.append(x[1])
        print temp
        if x[2]%4 == 3:
            memory[i].append(temp)
            i+=1
            temp = []
    for x in range(0,var_counter/4):
        temp.append(0)
    memory[i].append(temp)
    i+=1
    print memory[0]
    print memory[1]
    print memory[2]
    print memory[3]
    #Write the variables
    i = 4
    f.write('{:04x}'.format(i)+" ")
    for x in variables:
        f.write('{:05x}'.format(x[1])+" ")
        if x[2]%4 == 3:
            i+=4
            f.write("\n"+'{:04x}'.format(i)+" ")

    #fill the empty variable slots
    for x in range(0,var_counter/4):
        f.write("00000 ")
    f.write("\n")
    i+=4

    #end of writing variables

    #Write instructions
    for inst in instructions:
        if inst[0].find(":") > 0:
            print ("jump"+str(i))
            jump = inst[0].split(":")
            if (jump[0]=="code"):
                print "aa"
        else:
            print "normal"
    while i<=0xFFFF:
        f.write('{:04x}'.format(i))
        f.write("\n")
        i+=4

    f.close()


if __name__ == "__main__":
    main(sys.argv[1:])
