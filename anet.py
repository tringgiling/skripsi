import time
import subprocess
import pandas as pd 	
import shutil	
import os
from datetime import datetime

### Sambutan																
print ("Selamat Datang Di Anti Evil Twin !!!")
print("Tunggu Sebentar, sedang melakukan scan AP\n")

### Scan WIFI di sekitar
pantau_awal = subprocess.call("sudo ./pantau.sh awal", shell=True) 			# Scanning di awal2 buat milih AP yang mau di lindungi	
pd.set_option("display.max_rows", 101)
file_csv = pd.read_csv("hasil_pantauan-01.csv", usecols=["BSSID"," ESSID"]) # Nampilin kolom yang diinginkan aja
file_csv.dropna(inplace = True)																#nge drop Kolom kosong (Dalam hal ini, nyaring kolom ESSID, jadi dari station Mac kebawah datanya bakal di drop, jadi cuma AP doang yang tampil)
print(file_csv)

### Memilih AP Yang ingin dilindungi
AP_Dilindungi_awal = input("\nSilahkan Pilih Akses Poin yang ingin dilindungi : ")
AP_Dilindungi = " " + AP_Dilindungi_awal														#Nge trik "satu spasi sebelum" dari isi kolom ESSID hasil Airodumb
list_AP_BSSID = file_csv["BSSID"].values.tolist()										#Ngubah dataframe ke list supaya gampang if else nya
list_AP_ESSID = file_csv[" ESSID"].values.tolist()
time.sleep(3)
index_ESSID = [i for i, e in enumerate(list_AP_ESSID) if e == AP_Dilindungi] #Ngambil No Index dari AP_Dilindungi buat dicocokin sama Index list_AP_BSSID
MAC_AP_Dilindungi = [list_AP_BSSID[i] for i in index_ESSID]							#Ngambil Alamat MAC yang baris nya sama kaya AP_Dilindungi
print (MAC_AP_Dilindungi)

### Mulai Fokus memantau AP, dan mencari evil twin
print("\nSedang mencoba memantau Wifi : " + AP_Dilindungi)
pantau_fokus = subprocess.call(["sudo","./pantau.sh",AP_Dilindungi_awal])		#Masuk sihh, cuman ngga bisa pake format, harus cari cara lain
				
######## WHILE - IF ELSE buat scanning evil twin 
while True :
	file_csv_fokus = pd.read_csv("hasil_pantauan-01.csv", usecols=["BSSID"," ESSID"," channel"," Power"])
	file_csv_fokus.dropna(inplace = True)
	AP_scan = file_csv_fokus[" ESSID"].values.tolist()
	MAC_scan = file_csv_fokus["BSSID"].values.tolist()
	MAC_ET = [x for x in MAC_scan if x not in MAC_AP_Dilindungi]
	print(file_csv_fokus)
	
	if AP_Dilindungi in AP_scan and MAC_ET  :
		print ("\nAda Evil Twin, MAC nya sebagai berikut : ")
		print(" dan ".join(MAC_ET))
		break
		
	else:
		print ("Belum terdeteksi")
		time.sleep(0.7)
		bersih_layar = subprocess.call('clear')

### Target Lock, siap serang balik


### Menyimpan Rekaman (File Log)
waktu_tanggal = datetime.now().strftime("%d_%m_%y")
waktu_jam = datetime.now().strftime("%X")
try:
	os.mkdir("rekaman/" + waktu_tanggal)
except:
	print ("Folder " + waktu_tanggal + " sudah dibuat")
log_mac= open("rekaman/" + waktu_tanggal +"/list_MAC_dilindungi.txt","a")
log_et = open("rekaman/" + waktu_tanggal +"/list_Evil_Twin.txt","a")

log_mac.write("\n==================\n")
log_mac.write("Daftar MAC untuk Akses Poin"+ AP_Dilindungi +" yang dilindungi pada " + waktu_jam +"\n")
log_mac.write(" dan ".join(MAC_AP_Dilindungi))
log_mac.close

log_et.write("\n==================\n")
log_et.write("Daftar MAC Evil Twin, Peniru Akses Poin"+ AP_Dilindungi +" Terdeteksi pada " + waktu_jam + "\n")
log_et.write(" dan ".join(MAC_ET))
log_et.close

shutil.move("hasil_pantauan-01.csv","rekaman/" + waktu_tanggal + "/" + waktu_jam +".csv")
shutil.move("hasil_pantauan-01.cap","rekaman/" + waktu_tanggal + "/" + waktu_jam +".cap")


### Kalau ingin menutup Aplikasi 		
pause1 = input("\nHentikan Proses? (enter)")	
stop_pantau = subprocess.call("sudo ./stop_pantau.sh", shell=True)					# ngestop airodump, kalau semuanya udah beres

