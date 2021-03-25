import re
import subprocess
import pandas as pd 																			# buat baca csv
print ("Selamat Datang Di Anti Evil Twin !!!")
print("Tunggu Sebentar, sedang melakukan scan AP\n")

#pantau = subprocess.call("sudo ./pantau.sh", shell=True) 


# milih kolom ESSID nya pake satu spasi ya iqbaaaallllll :)
# dan isi dari kolom ESSID nya juga pada pake satu spasi wkwkwkwk bikin susah aja nih airodump

file_csv = pd.read_csv("hasil_pantauan-02.csv", usecols=["BSSID"," ESSID"]) # Nampilin kolom yang diinginkan aja
file_csv.dropna(inplace = True)																#nge drop Kolom kosong (Dalam hal ini, nyaring kolom ESSID, jadi dari station Mac kebawah datanya bakal di drop, jadi cuma AP doang yang tampil)
print(file_csv)

AP_Dilindungi = input("\nSilahkan Pilih Akses Poin yang ingin dilindungi : ")
AP_Dilindungi = " " + AP_Dilindungi														#Nge trik "satu spasi sebelum" dari isi kolom ESSID hasil Airodumb
file_csv_BSSID = file_csv["BSSID"]														#Ngambil Kolom tertentu
file_csv_ESSID = file_csv[" ESSID"]

list_AP_BSSID = file_csv_BSSID.values.tolist()										#Ngubah dataframe ke list supaya gampang if else nya
list_AP_ESSID = file_csv_ESSID.values.tolist()

							
index_ESSID = [i for i, e in enumerate(list_AP_ESSID) if e == AP_Dilindungi] #Ngambil No Index dari AP_Dilindungi buat dicocokin sama Index list_AP_BSSID
MAC_AP_Dilindungi = [list_AP_BSSID[i] for i in index_ESSID]							#Ngambil Alamat MAC yang baris nya sama kaya AP_Dilindungi
print (MAC_AP_Dilindungi)

######## WHILE - IF ELSE buat scanning evil twinn ############ 
# if AP_Dilindungi in list_AP_ESSID and MAC_AP_Dilindungi !=:														# Nge cek inputan user, alhamdulillah udah bisa
	# print("Adaaaa evil twin")
# else:
	# print("Tidaakk")



#stop_pantau = subprocess.call("sudo ./stop_pantau.sh", shell=True)		# ngestop airodump, kalau semuanya udah beres

