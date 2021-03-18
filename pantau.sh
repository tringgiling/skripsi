#/bin/bash

sudo airmon-ng start wlp10s0f0 # Mulai Mode Monitor
tmux new -d # ngebuat session khusus buat nanti ngejalanin airodump-ng
sudo tmux send -Rt 0 airodump-ng SPACE -w SPACE hasil_pantauan SPACE --write-interval SPACE 1 SPACE wlp10s0f0mon ENTER #ngejalanin airodump di tmux session 0

echo "Tunggu bentar ok?" 
sleep 7s
#sleep 3s #dipake buat ngasih jeda antara proses airodump dan cat
cat hasil_pantauan-01.csv # btw ni rada deg degan karna penamaan file dari airodump suka sotoy nambahin -01,-02 nya sesuka dia wkwkkw 
echo -n "Masukan nama AP yang ingin dilindungi : "
read AP_dilindungi

cat hasil_pantauan-01.csv | grep $AP_dilindungi | egrep -o '[[:alnum:]]{2}:[[:alnum:]]{2}:[[:alnum:]]{2}:[[:alnum:]]{2}:[[:alnum:]]{2}:[[:alnum:]]{2}' > list_MAC_dilindungi.txt
echo -n "Sedang Memantau....."
read evil_twin_mulai
#Kalau mau maksain ngambil MAC Evil Twin Pake metode grep, bisa coba kode dibawah
cat hasil_pantauan-01.csv | grep $AP_dilindungi | egrep -o '[[:alnum:]]{2}:[[:alnum:]]{2}:[[:alnum:]]{2}:[[:alnum:]]{2}:[[:alnum:]]{2}:[[:alnum:]]{2}' | grep -v -f list_MAC_dilindungi.txt > list_Evil_Twin.txt
echo -n "[$(date +"%T")] Evil Twin Terdeteksi !!, Nama nya meniru $AP_dilindungi dan Alamat MAC Evil Twin nya adalah " && cat list_Evil_Twin.txt
sleep 1s #jeda buat nge stop monitor sama ngehapus hasil pantauan

########## Ini nge end semuanya biar resource nya ngga berat ################
sudo rm hasil_pantauan-01.*
sudo airmon-ng stop wlp10s0f0mon
tmux kill-session -t 0
