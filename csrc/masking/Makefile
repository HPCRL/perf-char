
objects = mask.o 

all: mask 

mask: $(objects)
	g++ -O3  -std=c++11 $(objects) -o mask

%.o: %.cc
	g++ -O3 -std=c++11 -c $< -o $@ -g

clean:
	rm -f mask  $(objects)


.PHONY: clean all 



