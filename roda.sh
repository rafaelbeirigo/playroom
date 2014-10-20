#!/bin/bash

roda () {
    for i in {1..100}
    do
	python Playroom.py --nox --no_cardinal
    done
}

roda
