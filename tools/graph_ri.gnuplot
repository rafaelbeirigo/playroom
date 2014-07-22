set terminal postscript eps color solid "Helvetica" 24
set term postscript eps font ",12"

set output "./graph.eps"

set multiplot layout 7,1

# plot x u 1:1
# plot exp(x) u 2:1
# plot 1/x u 3:1

# plot x
# plot exp(x)
# plot 1/x

set xrange [0-2.5e3:5e5+2.5e3]
set yrange [-0.04:0.55]
set format x "%2.1e"
set format y "%2.1f"
set xtics 2.5e5
set ytics (0.0,0.5,1.0)

set ylabel 'lightON'
plot "< grep light_ON ./a.log" with impulses notitle
set ylabel 'lightOFF'
plot "< grep light_OFF ./a.log" with impulses notitle

set ylabel 'bellON'
plot "< grep bell_sound_ON ./a.log" with impulses notitle

set ylabel 'musicON'
plot "< grep music_ON ./a.log" with impulses notitle
set ylabel 'musicOFF'
plot "< grep music_OFF ./a.log" with impulses notitle

set ylabel 'monkeyON'
plot "< grep monkey_sound_ON ./a.log" with impulses notitle
set ylabel 'monkeyOFF'
plot "< grep monkey_sound_OFF ./a.log" with impulses notitle

unset multiplot
