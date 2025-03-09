from scapy.all import *
from threading import Thread, Event
import os
import tkinter as tk


# Bulunan ağları tutmak için bir liste
found_networks = []
stop_sniffing_event = Event()
cardi=""

def packet_handler(packet):
    """Wi-Fi paketlerini işler."""
    if stop_sniffing_event.is_set():
        return  # Eğer durdurma isteği varsa, paketi işlemeden çık

    if packet.haslayer(Dot11Beacon):
        # SSID'yi al ve boşsa 'Gizli Ağ' olarak ayarla
        ssid = packet[Dot11Elt].info.decode(errors="ignore") if packet[Dot11Elt].info else "Gizli Ağ"

        # BSSID'yi kontrol et ve 'Gizli Ağ' olarak ayarla
        bssid = packet[Dot11].addr2 if packet[Dot11].addr2 else "Gizli Ağ"

        # Kanal bilgisini al
        channel_info = packet[Dot11Elt:3].info if packet.haslayer(Dot11Elt) else None
        channel = ord(channel_info) if channel_info else "Bilinmiyor"

        if (ssid, bssid, channel) not in found_networks:
            found_networks.append((ssid, bssid, channel))

            # Bulunan ağları sıralayıp yazdır
            sorted_networks = sorted(found_networks, key=lambda x: (x[0], x[1], x[2]))
            display_networks(sorted_networks)
            print_networks(sorted_networks)

            # Bulunan ağları sıralayıp scanlist.txt'ye yaz
            with open("scanlist.txt", "w") as file:
                # `scanlist` adlı liste içinde ağları yaz
                file.write(f"scanlist = {repr(sorted_networks)}\n")


def display_networks(sorted_networks):
    """Tkinter penceresinde ağları sadece SSID ve sırası ile gösterir."""
    # Pencereyi temizle
    for widget in network_list_frame.winfo_children():
        widget.destroy()

    # Her ağ için bir etiket oluştur ve sola hizalı yaz
    for idx, (ssid, _, _) in enumerate(sorted_networks, 1):
        label = tk.Label(network_list_frame, text=f"[{idx}] SSID: {ssid}", font=("Helvetica", 12), fg="green",
                         bg="black", anchor="w")
        label.pack(fill="x")  # Etiketlerin tam genişlikte hizalanmasını sağlar

    # "Ağlar taranıyor. Taramayı sonlandırmak için 'W' tuşuna basabilirsiniz." mesajını göster
    info_label = tk.Label(network_list_frame,
                          text="Ağlar taranıyor. Taramayı sonlandırabilmek için 'W' tuşuna basabilirsiniz.",
                          font=("Helvetica", 10), fg="yellow", bg="black", anchor="w")
    info_label.pack(fill="x")


def print_networks(sorted_networks):
    """Terminalde ağları sadece SSID ve sırası ile gösterir."""
    print("\n[+] Bulunan ağlar (sıralanmış):")
    for idx, (ssid, _, _) in enumerate(sorted_networks, 1):
        print(f"[{idx}] SSID: {ssid}")


def start_sniffing(interface):
    """Belirtilen arayüzde paketleri dinler."""
    print(f"[+] Wi-Fi taraması başlatılıyor ({interface})...")
    sniff(iface=interface, prn=packet_handler, store=False, stop_filter=lambda x: stop_sniffing_event.is_set())


def on_close():
    """Pencereyi kapatırken yapılacak işlemler."""
    print("[!] Program sonlandırılıyor...")
    stop_sniffing_event.set()  # Tarama durdurulacak
    root.quit()


def on_key_press(event):
    """W tuşuna basıldığında taramayı durdur."""
    if event.char == 'w' or event.keysym == 'w':
        print("[!] Tarama durduruluyor...")
        stop_sniffing_event.set()  # Tarama durdurulacak
        stop_message_label.config(text="Tarama sonlandırıldı.")  # 'Tarama sonlandırıldı' mesajını göster

def keypressenter():
    root.destroy()
    startt(found_networks)




def start(card):
    global cardi

    interface = card
    cardi=card
    # Tkinter penceresini başlat
    global root, network_list_frame, stop_message_label
    root = tk.Tk()
    root.title("Wi-Fi Ağ Tarayıcı")

    screen_width = root.winfo_screenwidth()  # Ekran genişliği
    screen_height = root.winfo_screenheight()  # Ekran yüksekliği

    # Pencereyi ekrana tam sığacak şekilde ayarlamak
    root.geometry(f'{screen_width}x{screen_height}+0+0')  # Pencereyi ekrana sığdır

    # Arka plan rengini siyah ve yazı rengini yeşil yap
    root.config(bg="black")

    # Tkinter'de ağları gösterecek bir frame
    network_list_frame = tk.Frame(root, bg="black")
    network_list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Tarama durdurulduğunda görülecek mesaj için bir etiket
    stop_message_label = tk.Label(root, text="", font=("Helvetica", 12), fg="red", bg="black")
    stop_message_label.pack()

    # Başlangıçta bilgi mesajı ekleyelim
    info_message_label = tk.Label(root, text="Lütfen bekleyin, ağlar taranıyor. Bu işlem biraz zaman alabilir...",
                                  font=("Helvetica", 14), fg="yellow", bg="black")
    info_message_label.pack(pady=10)

    # Pencereyi kapatma olayını bağla
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Tuş basıldığında 'w' tuşuna basıldığında taramayı durdurmak için
    root.bind("<w>", on_key_press)
    root.bind('<Return>', keypressenter)

    #### Başlangıç kısmı
    try:
        # Taramayı başlat
        sniff_thread = Thread(target=start_sniffing, args=(interface,))
        sniff_thread.daemon = True  # Ana programla birlikte durması için
        sniff_thread.start()

        # Tkinter penceresini sürekli açık tut
        root.mainloop()

    except KeyboardInterrupt:
        print("\n[!] Çıkış yapılıyor...")



networks = found_networks

# Sayacı tutacak değişken
counter = 1
# Seçilen tuple'ları tutacak liste
secilen = []
# Seçim tamamlandı flag'ı
selection_complete = False

gerisayisi=1

# Global etiket değişkenleri
result_label = None
note_label = None

# Yazdırma fonksiyonu
def print_first_elements():
    global result_label
    result_text = "Tüm Ağlar:\n"
    if networks:
        # Tüm network'leri yazdır
        for idx, tup in enumerate(networks, start=1):
            result_text += f"{idx}. {tup}\n"
    else:
        result_text += "Ağlar bulunamadı.\n"

    result_text += f"\nSeçilen Sayı: {counter}"  # Seçilen sayıyı göster
    result_label.config(text=result_text)


# Sayıyı azaltma fonksiyonu
def decrease_number(event=None):
    global counter
    if counter > 1:
        counter -= 1
    print_first_elements()


# Sayıyı artırma fonksiyonu
def increase_number(event):
    global counter
    if counter < len(networks):
        counter += 1
    print_first_elements()


# 'w' tuşu ile seçilen tuple'ı kaydetme
def save_selected_tuple(event):
    global counter, secilen, selection_complete
    if not selection_complete:  # Seçim tamamlanmadıysa, seçim yapabilirsin
        if 1 <= counter <= len(networks):
            selected_tuple = networks[counter - 1]  # counter 1'den başladığı için -1
            if selected_tuple not in secilen:  # Eğer bu tuple daha önce seçilmemişse
                secilen.append(selected_tuple)  # Tuple'ı seçilenler listesine ekle
                print(f"Seçilen tuple kaydedildi: {selected_tuple}")
            else:
                print("Bu tuple zaten seçildi.")
            print_first_elements()
    else:
        print("Seçimler tamamlandı, artık 'Enter' tuşuna basabilirsiniz.")


# 'Enter' tuşu ile seçilen tuple'ları yazdırma
def print_selected_list(event):
    global selection_complete, result_label, note_label,gerisayisi
    gerisayisi=0
    if not selection_complete:
        selection_complete = True  # Seçim tamamlandı
        result_text = "Seçilen Tuple'lar:\n"
        if secilen:
            for idx, tup in enumerate(secilen, start=1):
                result_text += f"{idx}. {tup}\n"
        else:
            result_text += "Hiçbir tuple seçilmedi.\n"
        result_label.config(text=result_text)
        print("Seçim tamamlandı, seçilen tuple'lar gösterildi.")
        note_label.config(text="Seçim tamamlandı.")  # Notu güncelle
    else:
        result_label.config(text="Seçimler zaten tamamlandı!")

def geri(event=None):  # event parametresini ekledik
    global selection_complete, result_label, note_label, secilen, counter, gerisayisi
    if gerisayisi == 0:
        counter = 1
        secilen = []
        selection_complete = False
        gerisayisi = 0
        result_label.config(text="Seçimlerinizi tamamladıktan sonra 'Enter' tuşuna basın.")
        note_label.config(text="Seçimlerinizi tamamladıktan sonra 'Enter' tuşuna basın.")
        decrease_number(None)  # decrease_number çağırırken None gönderdik
        gerisayisi = 1
        print_first_elements()
    else:
        azaz.destroy()
        start(cardi)

def startt(list):
    global networks, azaz, counter, secilen, selection_complete, result_label, note_label
    networks = list
    azaz = tk.Tk()
    azaz.title("Tuple Elemanları Yazdır")
    azaz.geometry("480x400")  # Pencere boyutu
    azaz.configure(bg="black")  # Arka plan siyah

    # Sayacı tutacak değişken
    counter = 1
    # Seçilen tuple'ları tutacak liste
    secilen = []
    # Seçim tamamlandı flag'ı
    selection_complete = False

    # Seçilen sayıları göstermek için etiket
    number_label = tk.Label(azaz, text="Seçilen Sayılar:", fg="green", bg="black", font=("Arial", 12))
    number_label.pack(pady=10, fill="both", padx=20)

    # Sonuç etiketi
    result_label = tk.Label(azaz, text="Seçimlerinizi tamamladıktan sonra 'Enter' tuşuna basın.", fg="green", bg="black",
                            font=("Arial", 12), justify="left", anchor="w")
    result_label.pack(pady=10, fill="both", padx=20)

    # Not etiketi (gizlenecek)
    note_label = tk.Label(azaz, text="Seçimlerinizi tamamladıktan sonra 'Enter' tuşuna basın.", fg="green", bg="black",
                          font=("Arial", 12))
    note_label.pack(pady=10, fill="both", padx=20)

    # Klavye tuşlarına basıldığında işlem yapma
    azaz.bind("<a>", decrease_number)  # 'a' tuşuna basıldığında sayıyı azalt
    azaz.bind("<d>", increase_number)  # 'd' tuşuna basıldığında sayıyı artır
    azaz.bind("<w>", save_selected_tuple)  # 'w' tuşuna basıldığında seçilen tuple'ı kaydet
    azaz.bind("<s>", geri)  # 'w' tuşuna basıldığında seçilen tuple'ı kaydet
    azaz.bind("<Return>", print_selected_list)  # 'Enter' tuşuna basıldığında seçilen tuple'ları yazdır

    # İlk yazdırma
    print_first_elements()

    root.mainloop()
