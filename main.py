import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os

# Global değişken
evil = False


# 'Evil' modunu değiştiren fonksiyon
def toggle_evil(event):
    global evil
    evil = not evil
    update_ui()



# Arka plan ve metin stilini güncelleyen fonksiyon
def update_ui():
    global evil
    try:
        if evil:
            # Evil mod: Resmi BADBMMOO, Metin arka planı siyah, yazı beyaz
            image = Image.open("images/BADBMMOO.png")
        else:
            # Normal mod: Resmi BMMOO, Metin arka planı beyaz, yazı siyah
            image = Image.open("images/BMMOO.png")

        image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # Resmi yeniden boyutlandır
        resim = ImageTk.PhotoImage(image)
        background_label.config(image=resim)
        background_label.image = resim  # Referansı koru

    except Exception as e:
        print(f"Resim yüklenemedi: {e}")
        background_label.config(image=None)  # Resim yüklenemezse resim alanını temizle
    label.config(fg="white" if evil else "black", bg="black" if evil else "#C6E4C0",
                 text="Evil Mode" if evil else "Normal Mode")


# Aile üyelerini güncelleyen fonksiyonf
def change_family_members(event, direction):
    global evil
    if evil:
        new_members = ["wifi attacks", "BLE attacks", "vpn", "mac changer", "attack5",
                       "attack6", "attack7", "attack8"]
    else:
        new_members = ["space warriors", "Flappy Huseyin", "dino", "mushroom", "tetris",
                       "snake", "2048"]

    current_text = label.cget("text")
    if current_text in new_members:
        current_index = new_members.index(current_text)
        new_index = (current_index + direction) % len(new_members)
    else:
        new_index = 0

    label.config(text=new_members[new_index])



# Oyunu başlatmak için bir placeholder fonksiyon
def start_game(event):
    print(f"Starting game: {label.cget('text')}")
    selected = label.cget("text")
    run(selected)

def run(code):
    script = {
        "Flappy Huseyin": os.path.join(os.getcwd(), "games", "flappybird", "flappy.py"),
        "dino": os.path.join(os.getcwd(), "games", "dino", "dino.py"),
        "mushroom": os.path.join(os.getcwd(), "games", "mushroom", "mantar.py"),
        "snake": os.path.join(os.getcwd(), "games", "snake", "snake.py"),
        "tetris": os.path.join(os.getcwd(), "games", "tetris", "game.py"),
        "2048": os.path.join(os.getcwd(), "games", "20488", "2048.py"),
        "space warriors": os.path.join(os.getcwd(), "games", "spacewarriorss", "spacewar.py"),
        "wifi attacks": os.path.join(os.getcwd(), "Hacks","wificard.py"),
    }
    if code in script:
        script_path = script[code]
        subprocess.run(["python", script_path], cwd=os.path.dirname(script_path))
    else:
        print("Geçersiz oyun adı!")



# Ana pencere
root = tk.Tk()
root.overrideredirect(True)  # Başlık çubuğunu kaldır

# Ekranın boyutlarını al
screen_width = root.winfo_screenwidth()  # Ekran genişliği
screen_height = root.winfo_screenheight()  # Ekran yüksekliği

# Pencereyi ekrana tam sığacak şekilde ayarlamak
root.geometry(f'{screen_width}x{screen_height}+0+0')  # Pencereyi ekrana sığdır

# İlk başta resim
try:
    image = Image.open("images/BMMOO.png")
    image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # Resmi yeniden boyutlandır
    resim = ImageTk.PhotoImage(image)
except Exception as e:
    print(f"Resim yüklenemedi: {e}")
    resim = None

background_label = tk.Label(root, image=resim)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


# Yazı boyutunu resmin boyutuna göre orantılamak için bir oran hesapla
def calculate_font_size():
    base_width = 480  # Normalde pencere genişliği
    base_height = 320  # Normalde pencere yüksekliği
    font_size = int((screen_width / base_width + screen_height / base_height) / 2 * 16)  # Orantılı yazı boyutu
    return font_size


# Metni göstermek için bir etiket (her zaman altta olacak)
font_size = calculate_font_size()

label = tk.Label(
    root,
    text="space warriors",
    font=("Arial", font_size),  # Orantılı font büyüklüğü
    fg="black",
    bg="#C6E4C0"
)
label.place(relx=0.5, rely=0.9, anchor="center")  # Ekranın alt merkezine yerleştir

# Tuş bağlamaları
root.bind("<z>", toggle_evil)  # 'Z' ile 'Evil' modunu değiştir
root.bind("<a>", lambda event: change_family_members(event, -1))  # 'A' ile önceki üyeye geç
root.bind("<d>", lambda event: change_family_members(event, 1))  # 'D' ile sonraki üyeye geç
root.bind("<w>", start_game)  # 'W' ile seçilen oyunu başlat
root.bind("<s>", lambda event: root.quit())  # 'S' ile çıkış yap


root.mainloop()
