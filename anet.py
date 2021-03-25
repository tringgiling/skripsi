import re
import subprocess
import pandas as pd # buat baca csv
print ("Selamat Datang Di Anti Evil Twin !!!")
print("Tunggu Sebentar, sedang melakukan scan AP\n")

tes = subprocess.call("sudo ./pantau.sh", shell=True) ##bisa

########## Alternatif lain kalau pandas nya ngambek ######################
#csv = open("hasil_pantauan-02.csv", "r")
#cari_SSID = re.findall("PNJ_Hotspot",csv.read()) # tipe data nya list
#cari_MAC = re.findall("\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}",csv.read()) # tipe data nya list
#print(cari_SSID)
#print(cari_MAC)
############################################################

# milih kolom ESSID nya pake satu spasi ya iqbaaaallllll :)
file_csv = pd.read_csv("hasil_pantauan-01.csv", usecols=["BSSID"," ESSID"]) # Nampilin kolom yang diinginkan aja
file_csv.dropna(inplace = True)										#nge drop Kolom kosong (Dalam hal ini, nyaring kolom ESSID, jadi dari station Mac kebawah datanya bakal di drop, jadi cuma AP doang yang tampil)
print(file_csv)

AP_Dilindungi = input("\nSilahkan Pilih Akses Poin yang ingin dilindungi : ")
list_AP = file_csv.values.tolist()										#Ngubah dataframe ke list supaya gampang if else nya

if AP_Dilindungi in list_AP:											# Nge cek inputan user, tpi masih gagal
	print("Adaaaa")
else:
	print("Tidaakk")




stop_pantau = subprocess.call("sudo ./stop_pantau.sh", shell=True)		# ngestop airodump, kalau semuanya udah beres

