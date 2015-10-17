#!/usr/bin/env bash

# @author Tony Beltramelli
# www.tonybeltramelli.com

function run
{
	./main.py process $2 $3
	./main.py validate $1 10 9
}

run "accelerometer_only" a an
run "accelerometer_mean_only" a ay
run "gyroscope_only" g gn
run "gyroscope_mean_only" g gy
run "accelerometer_mean_gyroscope_mean" ga gyay
run "accelerometer_mean_gyroscope" ga gnay
run "accelerometer_gyroscope_mean" ga gyan
run "accelerometer_gyroscope" ga gnan

