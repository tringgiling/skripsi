#!/bin/bash

if [[ $1 == "awal" ]]						# buat milih AP yang mau dilindungi di awal2
then
	sudo airmon-ng start wlp10s0f0 # Mulai Mode Monitor
	tmux new -d 								# ngebuat session khusus buat nanti ngejalanin airodump-ng
	sudo tmux send -Rt 0 airodump-ng SPACE -w SPACE hasil_pantauan SPACE --write-interval SPACE 1 SPACE wlp10s0f0mon ENTER #ngejalanin airodump di tmux session 0
	echo "Tunggu bentar ok?" 
	sleep 7s


else 												# Mode fokus, Airodump cuma mantau AP dilindungi aja
	sudo rm hasil_pantauan-01.*
	tmux kill-session -t 0
	tmux new -d
	sudo tmux send -Rt 0 airodump-ng SPACE -N SPACE "$1" SPACE -w SPACE hasil_pantauan SPACE --write-interval SPACE 1 SPACE wlp10s0f0mon ENTER #ngejalanin airodump di tmux session 0
	echo "Yey Masukkk"
	sleep 3s
fi
