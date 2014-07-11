#!/bin/bash

roda () {
    for epsopt in 0.0 0.0003 0.003 0.03 0.6
    do
	for i in {1..100}
	do
	    python Playroom.py --nox --no_cardinal --epsopt=$epsopt
	done

	FOLDER="logs/epsopt/$epsopt"
	if ! [ -e $FOLDER ]
	then
	    mkdir -p $FOLDER
	fi

	LOGS="logs/*.log"
	if [ -e  $LOGS ]
	then
	    mv $LOGS $FOLDER
	fi
    done
}

roda
