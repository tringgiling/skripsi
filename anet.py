import time
import subprocess
import pandas as pd
import shutil
import os
from datetime import datetime
import PySimpleGUI as sg

interface = "wlan1mon"  #buat raspii
### Scan WIFI di sekitar
pantau_awal = subprocess.call("sudo ./pantau.sh awal", shell=True) 			# Scanning di awal2 buat milih AP yang mau di lindungi	
file_csv_akhir = [["                  ","                  "]]

MAC_ET = ['                  ']
AP = "                  "
channel_ET = " "
power_ET = "   "
waktu_jam = "        "
jumlah_paket_deauth = 0


waktu_tanggal = datetime.now().strftime("%d_%m_%y")
bulan = datetime.now().strftime("%B")
#GUI Scan Akses Poin

def buat_window1():
	layout = [
		[sg.Button("Scan AP",
                  key= '-tombol_layout_1-'),
        sg.Button("Evil Twin",
                  key='-tombol_layout_2-'),
        sg.Button("Rekaman",
                  key='-tombol_layout_3-')
                  ],
        [sg.Text('Menu Scan Access Point',font=(20),justification=('center'))],
        [sg.Table(values=file_csv_akhir,
                  headings=["Akses Poin" , "BSSID"],
                  display_row_numbers=True,
                  auto_size_columns=True,
                  justification = "center",
                  enable_events = True,
                  bind_return_key = True,
                  key='-tabel_AP-',
                  num_rows=5)],
         #[sg.InputText(key='-pilih_AP-')],
         [sg.Button('Scan Access Point',
				  #image_filename= 'silang.png',
                  image_size= (50,20), 
				  #button_color=(sg.theme_background_color(),sg.theme_background_color()),
				  key='-tombol_scan-'),
         sg.Button('Pilih Access Point',
				  #image_filename= 'silang.png',
                  image_size= (50,20), 
				  #button_color=(sg.theme_background_color(),sg.theme_background_color()),
				  key='-tombol_pilih_AP-')]
    ]
	return sg.Window('Anet', layout, finalize=True)
#===========================================================
def buat_window2():
	layout= [
		[sg.Button("Scan AP",
                  key= '-tombol_layout_1-'),
        sg.Button("Evil Twin",
                  key='-tombol_layout_2-'),
        sg.Button("Rekaman",
                  key='-tombol_layout_3-')
                  ],
		[sg.Text('                               Evil Twin Terdeteksi                ', font=(20))],
		[sg.Table(values= [[AP,MAC_ET[0],power_ET,channel_ET,waktu_jam]],
				headings=["SSID","BSSID","Power (dBm)","Kanal", "Terdeteksi"],
				auto_size_columns=True,
				justification = "center",
				key='-tabel_ET-')],
		[sg.Text('SSID Akses Poin yang dilindungi  '),
		 sg.Text(' : -                  ',auto_size_text = True, key = '-nama_AP-')],
		[sg.Text('Status Serangan Kepada Evil Twin '),
		 sg.Text(': -         ',auto_size_text = True, key = '-status_ET-')],
		[sg.Text('Jumlah Paket Serangan Terkirim '), 
		 sg.Text("   : " + str(jumlah_paket_deauth) + " buah",
					auto_size_text = True,)],
		[sg.Button('Mulai Pencarian ET',key='-tombol_cari-'),
		 sg.Button('Hentikan Serangan', key='-tombol_serangan-'),
		 sg.Button('Lihat Serangan', key='-tombol_lihat_serangan-')]
				]
	return sg.Window('Anet', layout, finalize=True)
#===========================================================
def buat_window3():
	layout = [
		[sg.Button("Scan AP",
                  key= '-tombol_layout_1-'),
        sg.Button("Evil Twin",
                  key='-tombol_layout_2-'),
        sg.Button("Rekaman",
                  key='-tombol_layout_3-')
                  ],
        [sg.Text('Eksport Rekaman (Log)',font=(20),justification=('center'))],
        [sg.Button('Packet Capture'),
         sg.InputText(" ",key='-pcap-',readonly=True)],
        [sg.Button('    Tabel AP     '),
         sg.InputText("  ",key='-csv-',readonly=True)],
        [sg.Button('   Ringkasan    '),
         sg.InputText(" ",key='-txt-',readonly=True)],
         [sg.Button('Eksport', key='-eksport-')]
    ]
	return sg.Window('ANET', layout, finalize=True)
#===========================================================
def main():
	window1 = buat_window1()
	window2 = buat_window2()
	window3 = buat_window3()
	window2.hide()
	window3.hide()
	
	while True:
		window, event, values = sg.read_all_windows()
		if event == sg.WIN_CLOSED:
			stop_pantau = subprocess.call("sudo ./stop_pantau.sh", shell=True)
			break
		
		if window == window1: 					
			if event == '-tombol_layout_2-':
				window1.hide()
				window2.un_hide()
				window3.hide()
			if event == '-tombol_layout_3-':
				window1.hide()
				window2.hide()
				window3.un_hide()
				
			if event  == '-tombol_scan-':
				file_csv = pd.read_csv("hasil_pantauan-01.csv")
				kolom_tampil = [" ESSID","BSSID"]
				file_csv=file_csv.reindex(columns=kolom_tampil)
				file_csv.dropna(inplace = True)	
				file_csv_akhir = file_csv.values.tolist()
				window['-tabel_AP-'].update(file_csv_akhir)
		        
			if event == '-tombol_pilih_AP-' :
				list_AP_BSSID = file_csv["BSSID"].values.tolist()
				list_AP_ESSID = file_csv[" ESSID"].values.tolist()
				AP_Dilindungi = list_AP_ESSID[(values['-tabel_AP-'])[0]]
				index_ESSID = [i for i, e in enumerate(list_AP_ESSID) if e == AP_Dilindungi]
				MAC_AP_Dilindungi = [list_AP_BSSID[i] for i in index_ESSID]
				print(list_AP_BSSID)
				print(MAC_AP_Dilindungi)
				print("nilainya adalah " + str(values['-tabel_AP-']))
				sg.popup("Akses Poin Terpilih :"+AP_Dilindungi)
			
		if window == window2: 					
			if event == '-tombol_layout_1-':
				window1.un_hide()
				window2.hide()
				window3.hide()
			if event == '-tombol_layout_3-':
				window1.hide()
				window2.hide()
				window3.un_hide()
			
			if event == '-tombol_cari-':
				window['-nama_AP-'].update(AP_Dilindungi)
				pantau_fokus = subprocess.call(["sudo","./pantau.sh",AP_Dilindungi.lstrip()])
				
				while True :
					file_csv_fokus = pd.read_csv("hasil_pantauan-01.csv", usecols=["BSSID"," ESSID"," channel"," Power"])
					file_csv_fokus.dropna(inplace = True)
					AP_scan = file_csv_fokus[" ESSID"].values.tolist()
					MAC_scan = file_csv_fokus["BSSID"].values.tolist()
					channel_scan = file_csv_fokus[" channel"].values.tolist()
					power_scan = file_csv_fokus[" Power"].values.tolist()
					MAC_ET = [x for x in MAC_scan if x not in MAC_AP_Dilindungi]
					
					if AP_Dilindungi in AP_scan and MAC_ET  :
						waktu_jam = datetime.now().strftime("%X")
						index_MAC_ET = MAC_scan.index(MAC_ET[0])																	
						channel_ET = channel_scan[index_MAC_ET]
						power_ET =  power_scan[index_MAC_ET]
						window['-tabel_ET-'].update([[AP_Dilindungi,MAC_ET[0],power_ET,channel_ET,waktu_jam]])
						window['-status_ET-'].update("Berjalan")
						subprocess.run(["sudo", "tmux", "kill-server"])
						time.sleep(3)
						subprocess.run(["sudo", "airmon-ng", "start", interface, str(channel_ET).lstrip()])
						subprocess.call(["sudo", "./pantau.sh", "serang",MAC_ET[0].lstrip()])
						break
					
					time.sleep(0.7)

			if event == '-tombol_serangan-':
				subprocess.run(["sudo", "tmux", "kill-server"])
				window['-status_ET-'].update("Berhenti")
				
			if event == '-tombol_lihat_serangan-':
				file_serang= open("serang.txt","r")
				buka_serang = file_serang.read()
				sg.popup_scrolled(buka_serang,title = "Status Serangan")
			
		if window == window3:
			if event == '-tombol_layout_1-':
				window1.un_hide()
				window2.hide()
				window3.hide()
			if event == '-tombol_layout_2-':
				window1.hide()
				window2.un_hide()
				window3.hide()
			
			if event == '-eksport-' :
				try:
					os.makedirs("rekaman/" + bulan + "/" + waktu_tanggal)
				except:
					sg.popup ("Folder " + bulan + "/" + waktu_tanggal + " sudah dibuat")
				
				window['-pcap-'].update("rekaman/" + bulan + "/" + waktu_tanggal + "/" + waktu_jam +".cap")
				window['-csv-'].update("rekaman/" + bulan + "/" + waktu_tanggal + "/" + waktu_jam +".csv")
				window['-txt-'].update("rekaman/" + bulan + "/" + waktu_tanggal + "/Rangkuman_rekaman.txt")
				log_mac= open("rekaman/" + bulan + "/" + waktu_tanggal +"/Rangkuman_rekaman.txt","a")
				log_mac.write("\n==================\n")
				log_mac.write("Tanggal : " + waktu_tanggal +"\n")
				log_mac.write("Waktu : " + waktu_jam +"\n")
				log_mac.write("Akses Poin (AP) Yang Dilindungi : "+ AP_Dilindungi +"\n")
				log_mac.write("MAC Address  AP Yang Dilindungi: ")
				log_mac.write(" dan ".join(MAC_AP_Dilindungi) + "\n" + "\n")
				log_mac.write("Evil Twin yang terdeteksi, Peniru Akses Poin : "+ AP_Dilindungi + "\n")
				log_mac.write("MAC Address  Evil Twin Yang Terdeteksi: ")
				log_mac.write(" dan ".join(MAC_ET))
				log_mac.write("\nChannel yang dipakai Evil twin : " + channel_ET)
				log_mac.close
				shutil.move("hasil_pantauan-01.csv","rekaman/" + bulan + "/" + waktu_tanggal + "/" + waktu_jam +".csv")
				shutil.move("hasil_pantauan-01.cap","rekaman/" + bulan + "/" + waktu_tanggal + "/" + waktu_jam +".cap")
				shutil.move("serang-01.cap","rekaman/" + bulan + "/" + waktu_tanggal + "/" + waktu_jam +"-serang.cap")
			
	window1.close()
	window2.close()
	window3.close()

if __name__ == '__main__':
	main()
