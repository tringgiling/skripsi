import re
import time
import subprocess
import pandas as pd 		

### Sambutan																
print ("Selamat Datang Di Anti Evil Twin !!!")
print("Tunggu Sebentar, sedang melakukan scan AP\n")

### Scan WIFI di sekitar
pantau_awal = subprocess.call("sudo ./pantau.sh awal", shell=True) 			# Scanning di awal2 buat milih AP yang mau di lindungi	
file_csv = pd.read_csv("hasil_pantauan-01.csv", usecols=["BSSID"," ESSID"]) # Nampilin kolom yang diinginkan aja
file_csv.dropna(inplace = True)																#nge drop Kolom kosong (Dalam hal ini, nyaring kolom ESSID, jadi dari station Mac kebawah datanya bakal di drop, jadi cuma AP doang yang tampil)
print(file_csv)

### Memilih AP Yang ingin dilindungi
AP_Dilindungi = input("\nSilahkan Pilih Akses Poin yang ingin dilindungi : ")
AP_Dilindungi = " " + AP_Dilindungi														#Nge trik "satu spasi sebelum" dari isi kolom ESSID hasil Airodumb
file_csv_BSSID = file_csv["BSSID"]														#Ngambil Kolom tertentu
file_csv_ESSID = file_csv[" ESSID"]
list_AP_BSSID = file_csv_BSSID.values.tolist()										#Ngubah dataframe ke list supaya gampang if else nya
list_AP_ESSID = file_csv_ESSID.values.tolist()
index_ESSID = [i for i, e in enumerate(list_AP_ESSID) if e == AP_Dilindungi] #Ngambil No Index dari AP_Dilindungi buat dicocokin sama Index list_AP_BSSID
MAC_AP_Dilindungi = [list_AP_BSSID[i] for i in index_ESSID]							#Ngambil Alamat MAC yang baris nya sama kaya AP_Dilindungi
print (MAC_AP_Dilindungi)

### Mulai Fokus memantau AP, dan mencari evil twin
print("\nSedang mencoba memantau Wifi : " + AP_Dilindungi)
pantau_fokus = subprocess.call(["sudo","./pantau.sh",AP_Dilindungi])		#Masuk sihh, cuman ngga bisa pake format, harus cari cara lain
				

######## WHILE - IF ELSE buat scanning evil twinn ############ 
while True :
	file_csv_fokus = pd.read_csv("hasil_pantauan-01.csv", usecols=["BSSID"," ESSID"," channel"," Power"])
	file_csv_fokus.dropna(inplace = True)
	AP_scan = file_csv_fokus[" ESSID"].values.tolist()
	MAC_scan = file_csv_fokus["BSSID"].values.tolist()
	MAC_ET = [x for x in MAC_scan if x not in MAC_AP_Dilindungi]
	print(file_csv_fokus)
	
	if AP_Dilindungi in AP_scan and MAC_ET  :
		print ("ada Evil Twin")
		print (MAC_ET)
		break
		
	else:
		print ("Belum terdeteksi")
		time.sleep(0.7)
		bersih_layar = subprocess.call('clear')
		
pause1 = input(" Lanjutkan Proses? (enter)")	
stop_pantau = subprocess.call("sudo ./stop_pantau.sh", shell=True)					# ngestop airodump, kalau semuanya udah beres

