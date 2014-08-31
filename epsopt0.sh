#!/bin/bash

roda () {
    for epsopt in 0.2
    do
	FOLDER="logs/epsopt-sempilha/$epsopt"
	if ! [ -e $FOLDER ]
	then
	    mkdir -p $FOLDER
	fi

	for i in {1..89}
	do
	    python Playroom.py --nox --no_cardinal --epsopt=$epsopt
	done
    done
}

roda
