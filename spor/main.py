import tkinter as tk
from tkinter import ttk, messagebox
from spor_takip import Sporcu, Antrenman, Takip

class GirisEkrani(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Giriş Yap")
        self.geometry("300x180")  
        self.resizable(False, False)
        self.parent = parent

        ttk.Label(self, text="Kullanıcı Adı:").pack(pady=5)
        self.kullanici_entry = ttk.Entry(self)
        self.kullanici_entry.pack(pady=5)

        ttk.Label(self, text="Şifre:").pack(pady=5)
        self.sifre_entry = ttk.Entry(self, show="*")
        self.sifre_entry.pack(pady=5)

        giris_btn = ttk.Button(self, text="Giriş Yap", command=self.giris_kontrol)
        giris_btn.pack(pady=(15, 10), ipadx=20, ipady=8)

        self.bind('<Return>', lambda event: self.giris_kontrol())


    def giris_kontrol(self):
        kullanici = self.kullanici_entry.get()
        sifre = self.sifre_entry.get()

        if kullanici == "admin" and sifre == "1234":
            messagebox.showinfo("Başarılı", "Giriş başarılı!")
            self.destroy()
            self.parent.deiconify()  
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")

class SporTakipApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spor Takip Uygulaması")
        self.geometry("600x400")

        self.takip = Takip()

        # Ana pencereyi gizle (giriş yapılana kadar)
        self.withdraw()

        self.giris_ekrani = GirisEkrani(self)
        self.giris_ekrani.grab_set()

        self._create_widgets()

    def _create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10, fill="x")

        # Sporcu ekleme
        ttk.Label(frame, text="Sporcu Adı:").grid(row=0, column=0, sticky="w")
        self.sporcu_ad_entry = ttk.Entry(frame)
        self.sporcu_ad_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame, text="Spor Dalı:").grid(row=1, column=0, sticky="w")
        self.spor_dali_entry = ttk.Entry(frame)
        self.spor_dali_entry.grid(row=1, column=1, sticky="ew")

        ttk.Button(frame, text="Sporcu Ekle", command=self.sporcu_ekle).grid(row=2, column=0, columnspan=2, pady=5)

        # Antrenman ekleme
        ttk.Label(frame, text="Antrenman Adı:").grid(row=3, column=0, sticky="w")
        self.antrenman_ad_entry = ttk.Entry(frame)
        self.antrenman_ad_entry.grid(row=3, column=1, sticky="ew")

        ttk.Label(frame, text="Antrenman Detayı:").grid(row=4, column=0, sticky="w")
        self.antrenman_detay_entry = ttk.Entry(frame)
        self.antrenman_detay_entry.grid(row=4, column=1, sticky="ew")

        ttk.Button(frame, text="Antrenman Ekle", command=self.antrenman_ekle).grid(row=5, column=0, columnspan=2, pady=5)

        # İlerleme kaydetme
        ttk.Label(frame, text="İlerleme Bilgisi:").grid(row=6, column=0, sticky="w")
        self.ilerleme_entry = ttk.Entry(frame)
        self.ilerleme_entry.grid(row=6, column=1, sticky="ew")

        ttk.Button(frame, text="İlerleme Kaydet", command=self.ilerleme_kaydet).grid(row=7, column=0, columnspan=2, pady=5)

        # Sporcu seçimi için combobox
        ttk.Label(frame, text="Sporcu Seç:").grid(row=8, column=0, sticky="w")
        self.sporcu_secimi = ttk.Combobox(frame, values=[], state="readonly")
        self.sporcu_secimi.grid(row=8, column=1, sticky="ew")

        # Rapor butonu
        ttk.Button(frame, text="Rapor Al", command=self.rapor_al).grid(row=9, column=0, columnspan=2, pady=10)

        frame.columnconfigure(1, weight=1)

        # Rapor gösterme 
        self.rapor_text = tk.Text(self, height=10)
        self.rapor_text.pack(padx=10, pady=10, fill="both", expand=True)

    def sporcu_ekle(self):
        ad = self.sporcu_ad_entry.get().strip()
        spor_dali = self.spor_dali_entry.get().strip()
        if not ad or not spor_dali:
            messagebox.showerror("Hata", "Lütfen sporcu adı ve spor dalını girin.")
            return
        if self.takip.sporcu_bul(ad):
            messagebox.showerror("Hata", "Bu isimde bir sporcu zaten var.")
            return
        yeni_sporcu = Sporcu(ad, spor_dali)
        self.takip.sporcu_ekle(yeni_sporcu)
        self.sporcu_secimi['values'] = [s.ad for s in self.takip.sporcular]
        messagebox.showinfo("Başarılı", "Sporcu eklendi!")
        self.sporcu_ad_entry.delete(0, tk.END)
        self.spor_dali_entry.delete(0, tk.END)

    def antrenman_ekle(self):
        sporcu_adi = self.sporcu_secimi.get()
        if not sporcu_adi:
            messagebox.showerror("Hata", "Lütfen bir sporcu seçin.")
            return
        antrenman_ad = self.antrenman_ad_entry.get().strip()
        antrenman_detay = self.antrenman_detay_entry.get().strip()
        if not antrenman_ad or not antrenman_detay:
            messagebox.showerror("Hata", "Lütfen antrenman adı ve detayını girin.")
            return
        sporcu = self.takip.sporcu_bul(sporcu_adi)
        if sporcu is None:
            messagebox.showerror("Hata", "Seçilen sporcu bulunamadı.")
            return
        antrenman = Antrenman(antrenman_ad, antrenman_detay)
        sporcu.program_olustur(antrenman)
        messagebox.showinfo("Başarılı", "Antrenman programa eklendi!")
        self.antrenman_ad_entry.delete(0, tk.END)
        self.antrenman_detay_entry.delete(0, tk.END)

    def ilerleme_kaydet(self):
        sporcu_adi = self.sporcu_secimi.get()
        if not sporcu_adi:
            messagebox.showerror("Hata", "Lütfen bir sporcu seçin.")
            return
        ilerleme_bilgisi = self.ilerleme_entry.get().strip()
        if not ilerleme_bilgisi:
            messagebox.showerror("Hata", "Lütfen ilerleme bilgisini girin.")
            return
        sporcu = self.takip.sporcu_bul(sporcu_adi)
        if sporcu is None:
            messagebox.showerror("Hata", "Seçilen sporcu bulunamadı.")
            return
        sporcu.ilerleme_kaydet(ilerleme_bilgisi)
        messagebox.showinfo("Başarılı", "İlerleme kaydedildi!")
        self.ilerleme_entry.delete(0, tk.END)

    def rapor_al(self):
        sporcu_adi = self.sporcu_secimi.get()
        if not sporcu_adi:
            messagebox.showerror("Hata", "Lütfen bir sporcu seçin.")
            return
        sporcu = self.takip.sporcu_bul(sporcu_adi)
        if sporcu is None:
            messagebox.showerror("Hata", "Seçilen sporcu bulunamadı.")
            return
        rapor = sporcu.rapor_al()
        self.rapor_text.delete("1.0", tk.END)
        self.rapor_text.insert(tk.END, rapor)


if __name__ == "__main__":
    app = SporTakipApp()
    app.mainloop()
