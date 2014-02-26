#!/bin/bash

KWY_FILE=$1
OUT_FILE=$KWY_FILE.out
EPS_FILE=$KWY_FILE.eps
JPG_FILE=$EPS_FILE.jpg;
PNG_FILE=$EPS_FILE.png

get_eps () {
    echo 'Cating...'
    cat $KWY_FILE | winsum 900 0.01 30 > 1.out
    echo 'Copying...'
    cp 1.out $OUT_FILE
    echo 'Gnuploting'
    gnuplot graph.gnuplot
    echo 'Moving...'
    mv graph.eps $EPS_FILE
}

get_jpg () {
    gs -sDEVICE=jpeg -dJPEGQ=100 -dNOPAUSE -dBATCH -dSAFER -r300 -sOutputFile=$JPG_FILE $EPS_FILE
}

get_png () {
    convert -density 300 $EPS_FILE -flatten $PNG_FILE
}
publish () {
    scp $PNG_FILE 143.107.165.124:public_html/a.png
}

plot () {
    i=0
    while [ true ]
    do
	i=`expr $i + 1`
	echo $i
	echo 'Getting eps file...'
	get_eps
	echo 'Getting image file...'
	get_png
	echo 'Publishing image file...'
	publish
	echo 'Done.'
	sleep 1
    done
}

plot
gv --watch $EPS_FILE
pkill plota.sh
