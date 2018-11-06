CXX = g++
C11 = ${CXX} -std=c++11
current_dir = $(notdir $(shell pwd))
parent_dir = $(notdir ${current_dir}/..)
.PHONY : clean data custom
# setting up suffix rules
.SUFFIXES : .cc .h .o
# for creating object files
.cc.o :
	${C11} $*.cc -c -o $*.o

##<<Different commands for makefile>>

## all : runs main code
all : data

## data : runs the diffusion according to the loaded data from ChanLab
data :
	python2 main.py -D $(ARGS)

## homogen : scores our different models according to some homogenous score
homogen :
	python2 homogeneity.py

## clean : remove auto-generated files
clean :
	rm -f *.pyc

help : makefile
	@sed -n 's/^##//p' $<
