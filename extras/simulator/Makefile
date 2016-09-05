################################################################################
## Guilherme Ozari de Almeida                                                 ##
## email: goaex-developer@yahoo.com.br                                        ##
################################################################################
##                                                                            ##
## File:        Makefile                                                      ##
## Date:        18.06.2012                                                    ##
## Version:     1.0                                                           ##
## Author:      Guilherme Almeida                                             ##
##                                                                            ##
## Description: Makefile for software compilation                             ##
## Notes:                                                                     ##
## Issues:                                                                    ##
## Revision history                                                           ##
##         Rev        Date        Who    Description                          ##
##         1.0        18/06/12    GOA    Inicial release                      ##
##                                                                            ##
##                                                                            ##
##          -Reproduction in whole or in part is prohibited without-          ##
##                -the written consent of the copyright owner-                ##
################################################################################

CC=g++
CFLAGS=-c -Wall
LDFLAGS=
SOURCES=main.c
OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=slxs.exe

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS) 
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

%.o: %.c
	$(CC) $(CFLAGS) $< -o $@

