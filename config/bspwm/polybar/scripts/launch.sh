#!/usr/bin/env bash

killall -q polybar
while pgrep -x polybar >/dev/null; do sleep 1; done

if type "xrandr"; then
  for m in $(xrandr --query | grep " connected" | cut -d" " -f1); do
    MONITOR=$m polybar --reload -c ~/.config/bspwm/polybar/config.ini top &
  done
else
  polybar --reload -c ~/.config/bspwm/polybar/config.ini top &
fi

echo "Polybar запущен..."
