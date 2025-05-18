import tkinter as tk
from tkinter import ttk, messagebox

# Tarif sınıfı
class Tarif:
    def __init__(self, ad, malzemeler, icerik, kategori):
        self.ad = ad
        self.malzemeler = malzemeler
        self.icerik = icerik
        self.kategori = kategori

# Giriş ekranı sınıfı
class GirisEkrani(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Giriş Yap")
        self.geometry("300x150")
        self.resizable(False, False)
        self.parent = parent

        ttk.Label(self, text="Kullanıcı Adı:").pack(pady=5)
        self.kullanici_entry = ttk.Entry(self)
        self.kullanici_entry.pack(pady=5)

        ttk.Label(self, text="Şifre:").pack(pady=5)
        self.sifre_entry = ttk.Entry(self, show="*")
        self.sifre_entry.pack(pady=5)

        giris_btn = ttk.Button(self, text="Giriş Yap", command=self.giris_kontrol)
        giris_btn.pack(pady=1)

        self.bind('<Return>', lambda event: self.giris_kontrol())  # Enter tuşu da çalışsın

    def giris_kontrol(self):
        kullanici = self.kullanici_entry.get()
        sifre = self.sifre_entry.get()

        if kullanici == "admin" and sifre == "1234":
            messagebox.showinfo("Başarılı", f"Hoşgeldin {kullanici}!")
            self.destroy()
            self.parent.deiconify()  # Ana pencereyi göster
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")

# Ana uygulama sınıfı
class TarifUygulamasi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Yemek Tarifleri")
        self.geometry("600x450")

        # Ana pencereyi başta gizle
        self.withdraw()

        # Giriş ekranını aç
        self.giris_ekrani = GirisEkrani(self)
        self.giris_ekrani.grab_set()

        # Kategoriler
        self.kategoriler = ["Tümü", "Kahvaltı", "Ana Yemek", "Tatlı", "Çorba", "Salata"]

        # Tarif listesi
        self.tarifler = []

        # Arayüz elemanları
        self._create_widgets()

    def _create_widgets(self):
        # Kategori seçim dropdown
        kategori_label = ttk.Label(self, text="Kategori:")
        kategori_label.pack(pady=5)

        self.kategori_secimi = ttk.Combobox(self, values=self.kategoriler, state="readonly")
        self.kategori_secimi.current(0)  # "Tümü" seçili
        self.kategori_secimi.pack(pady=5)

        # Arama girişi
        arama_label = ttk.Label(self, text="Tarif Adına Göre Ara:")
        arama_label.pack(pady=5)

        self.arama_entry = ttk.Entry(self)
        self.arama_entry.pack(pady=5)

        # Ara butonu
        ara_button = ttk.Button(self, text="Ara", command=self.tarif_ara)
        ara_button.pack(pady=5)

        # Tarif listesi kutusu
        self.listbox = tk.Listbox(self, height=10, width=50)
        self.listbox.pack(pady=10)
        self.listbox.bind("<Double-Button-1>", self.tarif_detay_goster)

        # Tarif ekle butonu
        ekle_button = ttk.Button(self, text="Yeni Tarif Ekle", command=self.tarif_ekle)
        ekle_button.pack(pady=10)

    def tarif_ekle(self):
        # Yeni pencerede tarif ekleme formu
        yeni_pencere = tk.Toplevel(self)
        yeni_pencere.title("Yeni Tarif Ekle")
        yeni_pencere.geometry("400x350")

        ttk.Label(yeni_pencere, text="Tarif Adı:").pack(pady=5)
        ad_entry = ttk.Entry(yeni_pencere)
        ad_entry.pack(pady=5)

        ttk.Label(yeni_pencere, text="Malzemeler (virgülle ayır):").pack(pady=5)
        malzeme_entry = ttk.Entry(yeni_pencere)
        malzeme_entry.pack(pady=5)

        ttk.Label(yeni_pencere, text="Tarif İçeriği:").pack(pady=5)
        icerik_text = tk.Text(yeni_pencere, height=5)
        icerik_text.pack(pady=5)

        ttk.Label(yeni_pencere, text="Kategori:").pack(pady=5)
        kategori_combo = ttk.Combobox(yeni_pencere, values=self.kategoriler[1:], state="readonly")
        kategori_combo.current(0)
        kategori_combo.pack(pady=5)

        def kaydet():
            ad = ad_entry.get().strip()
            malzemeler = [m.strip() for m in malzeme_entry.get().split(",") if m.strip()]
            icerik = icerik_text.get("1.0", "end").strip()
            kategori = kategori_combo.get()

            if not ad or not malzemeler or not icerik:
                messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
                return

            yeni_tarif = Tarif(ad, malzemeler, icerik, kategori)
            self.tarifler.append(yeni_tarif)
            messagebox.showinfo("Başarılı", "Tarif eklendi!")
            yeni_pencere.destroy()
            self.liste_guncelle()

        ttk.Button(yeni_pencere, text="Kaydet", command=kaydet).pack(pady=10)

    def liste_guncelle(self, filtreli_tarifler=None):
        self.listbox.delete(0, tk.END)
        gosterilecek = filtreli_tarifler if filtreli_tarifler is not None else self.tarifler
        for tarif in gosterilecek:
            self.listbox.insert(tk.END, f"{tarif.ad} ({tarif.kategori})")

    def tarif_ara(self):
        arama_metni = self.arama_entry.get().lower()
        secilen_kategori = self.kategori_secimi.get()

        sonuc = []
        for tarif in self.tarifler:
            if (secilen_kategori == "Tümü" or tarif.kategori == secilen_kategori) and arama_metni in tarif.ad.lower():
                sonuc.append(tarif)

        self.liste_guncelle(sonuc)
        if not sonuc:
            messagebox.showinfo("Bilgi", "Aramanıza uygun tarif bulunamadı.")

    def tarif_detay_goster(self, event):
        secilen_index = self.listbox.curselection()
        if not secilen_index:
            return
        tarif = None
        secilen_ad = self.listbox.get(secilen_index).split(" (")[0]
        for t in self.tarifler:
            if t.ad == secilen_ad:
                tarif = t
                break
        if tarif is None:
            return

        detay_pencere = tk.Toplevel(self)
        detay_pencere.title(f"{tarif.ad} Tarifi")
        detay_pencere.geometry("400x300")

        ttk.Label(detay_pencere, text=f"Kategori: {tarif.kategori}").pack(pady=5)
        ttk.Label(detay_pencere, text="Malzemeler:").pack()
        malzeme_text = tk.Text(detay_pencere, height=5, width=40)
        malzeme_text.pack(pady=5)
        malzeme_text.insert(tk.END, "\n".join(tarif.malzemeler))
        malzeme_text.config(state=tk.DISABLED)

        ttk.Label(detay_pencere, text="Tarif:").pack()
        icerik_text = tk.Text(detay_pencere, height=8, width=40)
        icerik_text.pack(pady=5)
        icerik_text.insert(tk.END, tarif.icerik)
        icerik_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = TarifUygulamasi()
    app.mainloop()
