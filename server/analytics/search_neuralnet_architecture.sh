#!/usr/bin/env bash

# @author Tony Beltramelli
# www.tonybeltramelli.com

# Handle arguments
if [ $# -eq 0 ]
	then
	echo "Error: no arguments supplied"
	echo "Usage:"
	echo "	-min <minimum number of neurons per layer>"
	echo "	-max <maximum number of neurons per layer>"
	exit 1
elif [ $# -ne 0 ]
	then
	for i in "$@"
	do
	    PARAM=`echo $1 | awk -F= '{print $1}'`
	    VALUE=`echo $2 | sed 's/^[^=]*=//g'`
	    case $PARAM in
	        -min)
				MIN=$VALUE
				;;
	        -max)
				MAX=$VALUE
				;;
	    esac
	    shift
	done
fi

echo "Train with MIN: $MIN and MAX: $MAX"

# Extract features
./main.py process

# Evaluate neural net architectures using k-fold cross-validation
ITERATION=10

function run
{
	for i in $(seq $MIN $MAX);
	do
		neurons=$(echo "50*$i" | bc)
		./main.py $1 "singlelayer_"$neurons $ITERATION $neurons
	done
}

run validate
