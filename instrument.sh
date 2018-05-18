#!/bin/bash

min_size=5
max_size=10
loops=10

# COLOPOWAAAA
GREEN="\033[1;32m"
NC="\033[0;0m"

# Generate random number of 32-bit words
_rand_input(){
	size=$((RANDOM % (max_size - min_size + 1) + min_size))
	dd if=/dev/urandom count=$size bs=4 2>/dev/null | tr "\0" "\1"
}

# Main
file="$1"
for ((i=0;i<loops;i++)); do
	input=`_rand_input`
	#echo -n $input | xxd
	
	# Call callgrind (execution trace)
	echo -e "${GREEN}Calling callgrind... ($((i+1))/$loops)${NC}"
	echo -n $input | valgrind --tool=callgrind --callgrind-out-file=${file}.$i.out $file &>/dev/null
	echo -e "${GREEN}Converting trace to dot...${NC}"
	python3 ./gprof2dot.py -f callgrind ${file}.$i.out > ${file}.$i.dot
	#dot -Tpng ${file}.$i.dot > ${file}.$i.png
	
	# Call cologrind (memory access)
	echo -e "${GREEN}Calling cologrind... ($((i+1))/$loops)${NC}"
	echo -n $input | valgrind --tool=cologrind --cologrind-out-file=${file}.$i.dot $file &>/dev/null
	echo -e "${GREEN}Calling Converting dot to am...${NC}"
	python3 ./dot2am.py colo ${file}.$i.dot ${file}.$i.am
done