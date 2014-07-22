#!/bin/bash

LOG_FILE=$1
SUFIX=$2
EPS_FILE=$LOG_FILE.eps
JPG_FILE=$EPS_FILE.jpg;
PNG_FILE=$EPS_FILE.png

get_log () {
    cp $LOG_FILE ./a.log
}

get_eps () {
    echo 'Getting log'
    get_log
    echo 'Gnuploting'
    gnuplot graph_ri.gnuplot
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
    scp $PNG_FILE 143.107.165.124:public_html/b-$SUFIX.png
}

plot () {
    echo 'Getting eps file...'
    get_eps
    echo 'Getting image file...'
    get_png
    rm $EPS_FILE
}

plot
rm a.log
