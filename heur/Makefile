CC = g++
CPPFLAGS = -g -Wall -O2 -std=c++0x -Wno-sign-compare
LDFLAGS =

OBJ = pso.o 

%.o: %.cpp
		$(CC) $(CPPFLAGS) -c $^ -o $@

main: $(OBJ)
		$(CC) $(CPPFLAGS) $(OBJ) -o pso 

clean:
		rm -rf $(OBJ) pso

.PHONY: clean


