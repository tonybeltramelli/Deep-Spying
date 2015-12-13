#!/usr/bin/env bash

# @author Tony Beltramelli
# www.tonybeltramelli.com

# Handle arguments
if [ $# -eq 0 ]
	then
	echo "Error: no arguments supplied"
	echo "Usage:"
	echo "	-name <session name>"
	exit 1
elif [ $# -ne 0 ]
	then
	for i in "$@"
	do
	    PARAM=`echo $1 | awk -F= '{print $1}'`
	    VALUE=`echo $2 | sed 's/^[^=]*=//g'`
	    case $PARAM in
	        -name)
				NAME=$VALUE
				;;
	    esac
	    shift
	done
fi

cd ../analytics
./main.py extract n y y
./main.py evaluate $NAME

