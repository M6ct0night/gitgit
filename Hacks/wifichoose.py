import tkinter as tk

scanlist = [('TP-Link_CEFA', 'e8:48:b8:be:ce:fa', 2)]

networks = []

# Sayacı tutacak değişken
counter = 1
# Seçilen tuple'ları tutacak liste
secilen = []
# Seçim tamamlandı flag'ı
selection_complete = False

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
def decrease_number(event):
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
    global selection_complete, result_label, note_label
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


def startt(list):
    global networks, root, counter, secilen, selection_complete, result_label, note_label
    networks = list
    root = tk.Tk()
    root.title("Tuple Elemanları Yazdır")
    root.geometry("480x400")  # Pencere boyutu
    root.configure(bg="black")  # Arka plan siyah

    # Sayacı tutacak değişken
    counter = 1
    # Seçilen tuple'ları tutacak liste
    secilen = []
    # Seçim tamamlandı flag'ı
    selection_complete = False

    # Seçilen sayıları göstermek için etiket
    number_label = tk.Label(root, text="Seçilen Sayılar:", fg="green", bg="black", font=("Arial", 12))
    number_label.pack(pady=10, fill="both", padx=20)

    # Sonuç etiketi
    result_label = tk.Label(root, text="Seçimlerinizi tamamladıktan sonra 'Enter' tuşuna basın.", fg="green", bg="black",
                            font=("Arial", 12), justify="left", anchor="w")
    result_label.pack(pady=10, fill="both", padx=20)

    # Not etiketi (gizlenecek)
    note_label = tk.Label(root, text="Seçimlerinizi tamamladıktan sonra 'Enter' tuşuna basın.", fg="green", bg="black",
                          font=("Arial", 12))
    note_label.pack(pady=10, fill="both", padx=20)

    # Klavye tuşlarına basıldığında işlem yapma
    root.bind("<a>", decrease_number)  # 'a' tuşuna basıldığında sayıyı azalt
    root.bind("<d>", increase_number)  # 'd' tuşuna basıldığında sayıyı artır
    root.bind("<w>", save_selected_tuple)  # 'w' tuşuna basıldığında seçilen tuple'ı kaydet
    root.bind("<Return>", print_selected_list)  # 'Enter' tuşuna basıldığında seçilen tuple'ları yazdır

    # İlk yazdırma
    print_first_elements()

    root.mainloop()


startt(scanlist)
