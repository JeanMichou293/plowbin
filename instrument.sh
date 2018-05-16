#!/bin/bash

min_size=5
max_size=10
loops=10

# Generate random number of 32-bit words
_rand_input(){
	size=$((RANDOM % (max_size - min_size + 1) + min_size))
	dd if=/dev/urandom count=$size bs=4 2>/dev/null
}

# Main
file="$1"
for ((i=0;i<loops;i++)); do
	input=`_rand_input`
	
	# Call callgrind (execution trace)
	echo -n $input | valgrind --tool=callgrind --callgrind-out-file=${file}.$i.out $file &>/dev/null
	python ./gprof2dot.py -f callgrind ${file}.$i.out > ${file}.$i.dot
	#dot -Tpng ${file}.$i.dot > ${file}.$i.png
	
	# Call cologrind (memory access)
	echo -n $input | valgrind --tool=cologrind file=${file}.$i.dot &>/dev/null
done