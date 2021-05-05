#!/bin/bash

if [[ $1 == "awal" ]]						# buat milih AP yang mau dilindungi di awal2
then
	sudo airmon-ng start wlxa0f3c11b46fa # Mulai Mode Monitor #wlp10s0f0
	tmux new -d 								# ngebuat session khusus buat nanti ngejalanin airodump-ng
	sudo tmux send -Rt 0 airodump-ng SPACE -w SPACE hasil_pantauan SPACE --write-interval SPACE 1 SPACE  wlan0mon ENTER #ngejalanin airodump di tmux session 0 #wlp10s0f0mon
	echo "Tunggu bentar ok?" 
	sleep 7s


else 												# Mode fokus, Airodump cuma mantau AP dilindungi aja
	sudo rm hasil_pantauan-01.*
	tmux kill-session -t 0
	tmux new -d
	sudo tmux send -Rt 0 airodump-ng SPACE -N SPACE "'$1'" SPACE -w SPACE hasil_pantauan SPACE --write-interval SPACE 1 SPACE wlan0mon  ENTER #ngejalanin airodump di tmux session 0 #wlp10s0f0mon
	echo Melakukan Scaning Ke "$1" 
	sleep 7s
fi
