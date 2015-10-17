#!/usr/bin/env bash

# @author Tony Beltramelli
# www.tonybeltramelli.com

./main.py process

iteration=1
MIN=5
MAX=12

function run
{
	for i in $(seq $MIN $MAX);
	do
		./main.py $1 $i"_layer" $iteration $i
	done

	for i in $(seq $MIN $MAX);
	do
		for j in $(seq $MIN $MAX);
		do
			./main.py $1 $i"_"$j"_multilayer" $iteration $i $j
		done
	done
}

run validate
