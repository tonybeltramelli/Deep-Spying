#!/usr/bin/env bash

# @author Tony Beltramelli
# www.tonybeltramelli.com

./main.py process

iteration=30
MIN=1
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

run train

mkdir -p ../data/result_train
mv ../data/result/* ../data/result_train/

exit 0
run validate
