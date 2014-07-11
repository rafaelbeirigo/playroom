#!/bin/bash

roda () {
    for epsopt in 0.0 0.0003
    do
	FOLDER="logs/epsopt/$epsopt"
	if ! [ -e $FOLDER ]
	then
	    mkdir -p $FOLDER
	fi

	for i in {1..100}
	do
	    python Playroom.py --nox --no_cardinal --epsopt=$epsopt
	done


	LOGS="logs/*.log"
	if [ -e  $LOGS ]
	then
	    mv $LOGS $FOLDER
	fi
    done
}

roda
