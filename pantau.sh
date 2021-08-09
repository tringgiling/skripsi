#!/bin/bash

if [[ $1 == "awal" ]]						# buat milih AP yang mau dilindungi di awal2
then
	sudo airmon-ng start wlan1 #Mulai Mode Monitor #wlp10s0f0
	tmux new -d 								# ngebuat session khusus buat nanti ngejalanin airodump-ng
	sudo tmux send -Rt 0 airodump-ng SPACE -w SPACE hasil_pantauan SPACE --output-format SPACE csv,pcap SPACE --write-interval SPACE 1 SPACE  wlan1mon ENTER  

elif [[ $1 == "serang" ]]
then
	tmux new -d
	sudo tmux send -Rt 0 airodump-ng SPACE -w SPACE serang SPACE --output-format SPACE pcap SPACE  wlan1mon ENTER
	tmux new -d
	sudo tmux send -Rt 1 aireplay-ng SPACE --deauth SPACE 0 SPACE -a SPACE $2 SPACE wlan1mon SPACE ">" SPACE serang.txt ENTER

else 												# Mode fokus, Airodump cuma mantau AP dilindungi aja
	sudo rm hasil_pantauan-*
	tmux kill-session -t 0
	tmux new -d
	sudo tmux send -Rt 0 airodump-ng SPACE -N SPACE "'$1'" SPACE -w SPACE hasil_pantauan SPACE --output-format SPACE csv,pcap SPACE --write-interval SPACE 1 SPACE wlan1mon  ENTER #ngejalanin airodump di tmux session 0 #wlp10s0f0mon 
	sleep 5s
fi
