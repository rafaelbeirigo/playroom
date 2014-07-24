#!/bin/bash

roda () {
    for epsopt in 0.8
    do
	FOLDER="logs/epsopt/$epsopt"
	if ! [ -e $FOLDER ]
	then
	    mkdir -p $FOLDER
	fi

	for i in {1..50}
	do
	    python Playroom.py --nox --no_cardinal --epsopt=$epsopt
	done
    done
}

roda
