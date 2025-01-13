import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import re

# Ağ arayüzlerini getir
def get_interfaces():
    try:
        result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, text=True)
        return re.findall(r'^\S+', result.stdout, re.MULTILINE)
    except Exception as e:
        print(f"Error fetching interfaces: {e}")
        return []

# Monitör modunu başlat
def start_monitor_mode(card):
    print(f"{card} monitör moduna alınıyor...")
    try:
        subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], check=True)
        subprocess.run(['sudo', 'airmon-ng', 'start', card], check=True)
        print(f"{card} monitör modunda.")
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e}")

# Aile üyesi seçim fonksiyonları
def change_interface(step):
    current_text = label.cget("text")
    if current_text in interfaces:
        index = (interfaces.index(current_text) + step) % len(interfaces)
        label.config(text=interfaces[index])
    else:
        label.config(text=interfaces[0])

# Pencere yeniden boyutlandırıldığında arka plan ve yazıyı güncelle
def resize(event):
    # Arka planı yeniden boyutlandır
    resized_image = original_image.resize((event.width, event.height), Image.ANTIALIAS)
    bg_image = ImageTk.PhotoImage(resized_image)
    background_label.config(image=bg_image)
    background_label.image = bg_image  # Referansı koru

    # Yazı boyutunu ekran boyutuna göre ölçekle
    font_size = max(12, int(event.height * 0.05))
    label.config(font=("Arial", font_size))

# Oyun başlatma
def start_game(event):
    selected_interface = label.cget("text")
    if selected_interface:
        start_monitor_mode(selected_interface)

# Tkinter GUI
root = tk.Tk()
root.overrideredirect(True)  # Başlık çubuğunu kaldır
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")  # Tam ekran yap

# Arka plan resmi
try:
    original_image = Image.open("BADBMMOO.png")  # Resmi yükle
    bg_image = ImageTk.PhotoImage(original_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS))
    background_label = tk.Label(root, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"Resim yüklenemedi: {e}")

# Label
label = tk.Label(root, text="Seçim Bekleniyor", font=("Arial", 24), fg="white", bg="black")
label.place(relx=0.5, rely=0.9, anchor="center")  # Ekranın alt merkezine yerleştir

# Ağ arayüzlerini yükle
interfaces = get_interfaces()
if interfaces:
    label.config(text=interfaces[0])

# Klavye kısayolları
root.bind("<a>", lambda event: change_interface(-1))
root.bind("<d>", lambda event: change_interface(1))
root.bind("<w>", start_game)

# Pencere yeniden boyutlandırıldığında işlev çağır
root.bind("<Configure>", resize)

# Tkinter döngüsü
root.mainloop()
