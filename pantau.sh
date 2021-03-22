#/bin/bash

sudo airmon-ng start wlp10s0f0 # Mulai Mode Monitor
tmux new -d # ngebuat session khusus buat nanti ngejalanin airodump-ng
sudo tmux send -Rt 0 airodump-ng SPACE -w SPACE hasil_pantauan SPACE --write-interval SPACE 1 SPACE wlp10s0f0mon ENTER #ngejalanin airodump di tmux session 0

echo "Tunggu bentar ok?" 
sleep 7s
