CC = g++
CPPFLAGS = -g -Wall -O2 
LDFLAGS =

CPX_INCDIR  = /opt/CPLEX_Studio/cplex/include
CPX_LIBDIR  = /opt/CPLEX_Studio/cplex/lib/x86-64_linux/static_pic
CPX_LDFLAGS = -lcplex -lm -pthread

OBJ = cplex.o 

%.o: %.cpp
		$(CC) $(CPPFLAGS) -I$(CPX_INCDIR) -c $^ -o $@

main: $(OBJ)
		$(CC) $(CPPFLAGS) $(OBJ) -o cplex -L$(CPX_LIBDIR) $(CPX_LDFLAGS)

clean:
		rm -rf $(OBJ) cplex

.PHONY: clean


