#!/bin/bash

roda () {
    for epsopt in 0.9 1.0
    do
	FOLDER="logs/epsopt-sempilha/$epsopt"
	if ! [ -e $FOLDER ]
	then
	    mkdir -p $FOLDER
	fi

	for i in {1..100}
	do
	    python Playroom.py --nox --no_cardinal --epsopt=$epsopt
	done
    done
}

roda
