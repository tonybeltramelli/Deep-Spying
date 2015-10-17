#!/usr/bin/env bash

# @author Tony Beltramelli
# www.tonybeltramelli.com

./main.py process

ITERATION=10
MIN=6
MAX=12

function run
{
	for i in $(seq $MIN $MAX);
	do
		./main.py $1 "singlelayer_"$i $ITERATION $i
	done

	for i in $(seq $MIN $MAX);
	do
		for j in $(seq $MIN $MAX);
		do
			./main.py $1 "multilayer_"$i"_"$j $ITERATION $i $j
		done
	done
}

run validate

