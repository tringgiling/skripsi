#/bin/bash

#AP_dilindungi=4E:A7:65:10:ED:02

#ini mau ngescan semua AP dulu ceritanya, biar memudahkan user memilih AP
# yang mau di jaga
#kendala nya, airodump nya harus di stop setelah x detik, biar ngga ganggu input user 

sudo ./pemantau.sh
cat hasil_pantauan.csv
echo "masukan nama AP yang ingin dilindungi : "
read AP_dilindungi

cat nyoba_2.csv | grep $AP_dilindungi | egrep -o '[[:alnum:]]{2}:[[:alnum:]]{2}:[[:alnum:]]{2}:[[:alnum:]]{2}:[[:alnum:]]{2}:[[:alnum:]]{2}' #| grep -v $AP_dilindungi
