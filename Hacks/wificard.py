import tkinter as tk
import subprocess
import re
import os
from PIL import Image, ImageTk

# Başlangıç durumu
choosed = False
interfaces = []
cardd = ""


# ifconfig komutunu çalıştır ve çıktısını al
def get_interfaces():
    result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout
    return re.findall(r'^\S+', output, re.MULTILINE)


# Arayüz isimlerini almak
def update_interfaces():
    global interfaces
    if not choosed:
        interfaces = get_interfaces()  # Gerçek ağ arayüzlerini al
    else:
        interfaces = ["deauth flood", "beacon spam", "evil portal", "targeted attacks"]


# Arayüz güncellenmesi
update_interfaces()

# Label güncelleme fonksiyonları
def change_family_members_back(event):
    global interfaces
    current_text = label.cget("text")
    if current_text in interfaces:
        prev_index = (interfaces.index(current_text) - 1) % len(interfaces)
        new_text = interfaces[prev_index]
    else:
        new_text = interfaces[0]
    label.config(text=new_text)

def change_family_members(event):
    global interfaces
    current_text = label.cget("text")
    if current_text in interfaces:
        next_index = (interfaces.index(current_text) + 1) % len(interfaces)
        new_text = interfaces[next_index]
    else:
        new_text = interfaces[0]
    label.config(text=new_text)

# Başlangıçta görülecek yazıyı ayarla
def stgame(event=None):
    update_interfaces()
    if not choosed:
        label.config(text=interfaces[0])  # Başlangıçta görülecek yazı
    if choosed:
        print("doğruda")
        print(interfaces)

# Seçilen işlemi başlat
def stagame(event):
    global choosed
    if not choosed:
        global cardd
        cardd = label.cget("text")[:-1]
        monitor(cardd)
        choosed = True  # Doğru atama
    else:
        stgame()
        Attacks = label.cget("text")
        run(Attacks)

# Koşan işlemi başlat
def run(code):
    script = {
        "targeted attacks": os.path.join(os.getcwd(),"scan_net.py"),
    }
    if code in script:
        script_path = script[code]
        subprocess.run(["python", script_path], cwd=os.path.dirname(script_path))
    else:
        print("Geçersiz program adı!")

# Wi-Fi kartını monitör moduna alma
def monitor(card):
    print("Wi-Fi süreçleri sonlandırılıyor...")
    try:
        subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Hata: Süreçleri sonlandırırken bir sorun oluştu: {e}")

    if not card:
        print("Hata: Geçerli bir kart adı sağlanmadı.")
        return

    print(f"{card} monitör moduna alınıyor...")
    try:
        subprocess.run(["sudo", "airmon-ng", "start", card], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Hata: 'airmon-ng' komutunu çalıştırırken bir sorun oluştu: {e}")
        return

    new_interface_name = ""
    try:
        result = subprocess.run(["iwconfig", card], capture_output=True, text=True)
        if "Mode:Monitor" in result.stdout:
            print(f"{card} şu anda monitör modunda.")
            new_interface_name = card
        else:
            print(f"Hata: {card} monitör modunda değil.")
    except Exception as e:
        print(f"Hata: iwconfig komutu sırasında bir sorun oluştu: {e}")
        return

    if new_interface_name:
        try:
            with open("adapters.txt", "w") as file:
                file.write(f"adapters=({card},{new_interface_name})")
            print(f"adapter=({card},)")
            global choosed
            choosed = True
            stgame()
        except Exception as e:
            print(f"Hata: Yeni adı kaydederken bir sorun oluştu: {e}")
    else:
        print("Hata: Yeni ağ adaptörü adı alınamadı.")


def rere(event=None):
    global choosed  # Global 'choosed' değişkenini kullan
    global interfaces  # Global 'interfaces' değişkenini kullan

    choosed = False  # Seçimi sıfırla

    # Arayüz listesine tekrar sorgu atılıyor
    result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout
    interfaces = re.findall(r'^\S+', output, re.MULTILINE)  # Arayüzleri regex ile al

    # İlk arayüzü göster
    label.config(text=interfaces[0])
    print("Seçim sıfırlandı ve ilk arayüz gösterildi.")


# Kullanıcı ekranına uygun font boyutunu hesaplama
def calculate_font_size(screen_width, screen_height):
    base_width = 480
    base_height = 320
    font_size = int((screen_width / base_width + screen_height / base_height) / 2 * 16)
    return font_size

# GUI oluşturma
root = tk.Tk()
root.title("main")  # Başlık çubuğunu kaldır

# Ekran boyutlarını al
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Font boyutunu hesapla
font_size = calculate_font_size(screen_width, screen_height)

root.geometry(f'{screen_width}x{screen_height}+0+0')

# Arka plan resmi yükleme
try:
    image = Image.open("../images/BADBMMOO.png")
    image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    resim = ImageTk.PhotoImage(image)

    # Arka plan resmini eklemek için Label widget'ı oluştur
    background_label = tk.Label(root, image=resim)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Referansı koru
    background_label.image = resim

except Exception as e:
    print(f"Resim yüklenemedi: {e}")

# Label widget'ını oluştur ve yazıyı ekle
label = tk.Label(root, text="", font=("Arial", font_size), fg="white", bg="black")
label.pack(side="bottom", pady=20)

# Kontrol tuşları
root.bind("<Return>", stgame)  # Enter tuşu ile yazıyı ekle
root.bind("<a>", change_family_members_back)  # 'A' tuşu ile bir önceki oyunu seç
root.bind("<A>", change_family_members_back)
root.bind("<d>", change_family_members)  # 'D' tuşu ile bir sonraki oyunu seç
root.bind("<D>", change_family_members)
root.bind("<w>", stagame)  # 'W' tuşu ile seçilen oyunu başlat
root.bind("<W>", stagame)
root.bind("<s>", lambda event: rere(event))  # 'S' tuşu ile tekrar başlat
root.bind("<S>", lambda event: rere(event))

# GUI'yi çalıştır
root.mainloop()
