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

set xrange [0.0:*]
set yrange [0.0:1.0]
set format y "%2.1f"
set ytics (0.0, 0.5,1.0)

set ylabel 'light_ON'
plot "< grep light_ON ./a.log" with impulses notitle
set ylabel 'light_OFF'
plot "< grep light_OFF ./a.log" with impulses notitle

set ylabel 'music_ON'
plot "< grep music_ON ./a.log" with impulses notitle
set ylabel 'music_OFF'
plot "< grep music_OFF ./a.log" with impulses notitle

set ylabel 'bell_ON'
plot "< grep bell_sound_ON ./a.log" with impulses notitle

set ylabel 'toy_monkey_ON'
plot "< grep toy_monkey_sound_ON ./a.log" with impulses notitle
set ylabel 'toy_monkey_OFF'
plot "< grep toy_monkey_sound_OFF ./a.log" with impulses notitle

unset multiplot
