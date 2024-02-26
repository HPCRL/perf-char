
objects = factor.o 

all: factor 

factor: $(objects)
	g++ -O3  -std=c++11 $(objects) -o factor

%.o: %.cc
	g++ -O3 -std=c++11 -c $< -o $@ -g

clean:
	rm -f factor  $(objects)


.PHONY: clean all 



