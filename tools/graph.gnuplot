# Gnuplot graph generation script
# Gregory Kuhlmann, 2002

# Color output
set terminal postscript eps color solid "Helvetica" 24
set term postscript eps font ",12"

# Black & White output
#set terminal postscript eps monochrome dashed "Helvetica" 24

# Output file
set output "./graph.eps"

# Title
set title ""

# Appearance
set style data lines
set key bottom right
set border 3
set xtics nomirror
set grid ytics
set ytics 1 nomirror
set multiplot

# Axes
set xrange [-0.5:50]
set xlabel "Training Time (hours)"

set yrange [3:13]
set ylabel "Episode Duration (seconds)"

# Plot Data
plot \
     "/home/rafaelbeirigo/ciencia/rcss/keepaway/logs/201303121238-LTI-PROJETO-TM.kwy.out"    title '4v3 From Scratch - PRQL', \
