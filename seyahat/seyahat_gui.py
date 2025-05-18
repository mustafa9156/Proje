import tkinter as tk
from tkinter import ttk, messagebox

# Kullanıcı verileri
USERS = {"admin": "1234", "user": "pass"}

# Konaklama sınıfı
class Konaklama:
    def __init__(self, isim, fiyat, adres, yildiz=3):
        self.isim = isim
        self.fiyat = fiyat
        self.adres = adres
        self.yildiz = yildiz

    def __str__(self):
        return f"{self.isim} - {self.yildiz}⭐, {self.adres}, Fiyat: {self.fiyat} TL"

# Rota sınıfı
class Rota:
    def __init__(self, baslangic, varis, mesafe=0):
        self.baslangic = baslangic
        self.varis = varis
        self.mesafe = mesafe

    def __str__(self):
        return f"{self.baslangic} -> {self.varis} ({self.mesafe} km)"

# Seyahat sınıfı
class Seyahat:
    def __init__(self, rota, konaklama, plan):
        self.rota = rota
        self.konaklama = konaklama
        self.plan = plan

    def __str__(self):
        return f"{self.rota}\nKonaklama: {self.konaklama}\nPlan: {self.plan}"

# Giriş ekranı
class GirisEkrani(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Seyahat Planı - Giriş")
        self.geometry("400x350")
        self.configure(bg="#2C3E50")
        self.resizable(False, False)
        self._build_login_ui()

    def _build_login_ui(self):
        label_baslik = tk.Label(self, text="Seyahat Planı", fg="white", bg="#2C3E50",
                               font=("Helvetica", 24, "bold"))
        label_baslik.pack(pady=30)

        label_kullanici = tk.Label(self, text="Kullanıcı Adı", fg="white", bg="#2C3E50", font=("Arial", 14))
        label_kullanici.pack(pady=(10, 5))
        self.entry_kullanici = tk.Entry(self, font=("Arial", 14))
        self.entry_kullanici.pack(pady=5, ipadx=10, ipady=5)

        label_sifre = tk.Label(self, text="Şifre", fg="white", bg="#2C3E50", font=("Arial", 14))
        label_sifre.pack(pady=(15, 5))
        self.entry_sifre = tk.Entry(self, show="*", font=("Arial", 14))
        self.entry_sifre.pack(pady=5, ipadx=10, ipady=5)
        self.entry_sifre.bind("<Return>", lambda e: self._giris_yap())

        btn_giris = tk.Button(self, text="Giriş Yap", font=("Arial", 14, "bold"), bg="#27AE60", fg="white",
                              relief="flat", command=self._giris_yap)
        btn_giris.pack(pady=10, ipadx=20, ipady=8)

    def _giris_yap(self):
        kullanici_adi = self.entry_kullanici.get()
        sifre = self.entry_sifre.get()

        if USERS.get(kullanici_adi) == sifre:
            messagebox.showinfo("Başarılı", f"Hoşgeldiniz, {kullanici_adi}!")
            self.destroy()
            app = SeyahatApp()
            app.mainloop()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış.")
            self.entry_sifre.delete(0, tk.END)

# Ana uygulama
class SeyahatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Seyahat Planlama Uygulaması")
        self.geometry("800x500")
        self.resizable(True, True)

        self.konaklama_listesi = [
            Konaklama("Dağ Otel", 250, "Uludağ", 3),
            Konaklama("Şehir Oteli", 350, "İstanbul Taksim", 4)
        ]

        self.seyahatler = []

        self._build_ui()

    def _build_ui(self):
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Başlangıç Noktası:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.baslangic_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.baslangic_var).grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(main_frame, text="Varış Noktası:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.varis_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.varis_var).grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(main_frame, text="Toplam Mesafe (km):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.mesafe_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.mesafe_var).grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Label(main_frame, text="Konaklama Seçimi:").grid(row=3, column=0, sticky=tk.W, pady=(15,5))
        self.konaklama_listbox = tk.Listbox(main_frame, height=6)
        self.konaklama_listbox.grid(row=4, column=0, columnspan=2, sticky="ew")
        self.konaklama_guncelle()

        # Konaklama Ekle butonu
        ttk.Button(main_frame, text="Konaklama Ekle", command=self.konaklama_ekle_pencere).grid(row=5, column=0, columnspan=2, pady=(5, 15), sticky="ew")

        ttk.Label(main_frame, text="Seyahat Plan Detayları:").grid(row=6, column=0, sticky=tk.W, pady=(15,5))
        self.plan_text = tk.Text(main_frame, height=8)
        self.plan_text.grid(row=7, column=0, columnspan=2, sticky="nsew")

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")

        ttk.Button(btn_frame, text="Planı Kaydet / Güncelle", command=self.plan_kaydet).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(btn_frame, text="Seçili Seyahati Sil", command=self.seyahat_sil).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        ttk.Label(main_frame, text="Oluşturulan Seyahat Planları:").grid(row=0, column=2, sticky=tk.W, padx=(20,0))
        self.seyahat_listbox = tk.Listbox(main_frame, height=20)
        self.seyahat_listbox.grid(row=1, column=2, rowspan=7, sticky="nsew", padx=(20,0))
        self.seyahat_listbox.bind("<<ListboxSelect>>", self.seyahat_secildi)

        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(7, weight=1)

    def konaklama_ekle_pencere(self):
        pencere = tk.Toplevel(self)
        pencere.title("Yeni Konaklama Ekle")
        pencere.geometry("300x300")

        ttk.Label(pencere, text="Otel İsmi:").pack(pady=5)
        isim_entry = ttk.Entry(pencere)
        isim_entry.pack(pady=5, fill=tk.X, padx=10)

        ttk.Label(pencere, text="Fiyat (TL):").pack(pady=5)
        fiyat_entry = ttk.Entry(pencere)
        fiyat_entry.pack(pady=5, fill=tk.X, padx=10)

        ttk.Label(pencere, text="Adres:").pack(pady=5)
        adres_entry = ttk.Entry(pencere)
        adres_entry.pack(pady=5, fill=tk.X, padx=10)

        ttk.Label(pencere, text="Yıldız Sayısı:").pack(pady=5)
        yildiz_entry = ttk.Entry(pencere)
        yildiz_entry.pack(pady=5, fill=tk.X, padx=10)

        def kaydet():
            isim = isim_entry.get().strip()
            fiyat = fiyat_entry.get().strip()
            adres = adres_entry.get().strip()
            yildiz = yildiz_entry.get().strip()

            if not isim or not fiyat or not adres or not yildiz:
                messagebox.showerror("Hata", "Tüm alanları doldurun!")
                return

            try:
                fiyat = int(fiyat)
                yildiz = int(yildiz)
            except ValueError:
                messagebox.showerror("Hata", "Fiyat ve yıldız sayısı sayı olmalıdır.")
                return

            yeni_konaklama = Konaklama(isim, fiyat, adres, yildiz)
            self.konaklama_listesi.append(yeni_konaklama)
            self.konaklama_guncelle()
            pencere.destroy()

        ttk.Button(pencere, text="Kaydet", command=kaydet).pack(pady=10)

    def konaklama_guncelle(self):
        self.konaklama_listbox.delete(0, tk.END)
        for k in self.konaklama_listesi:
            self.konaklama_listbox.insert(tk.END, str(k))

    def plan_kaydet(self):
        baslangic = self.baslangic_var.get().strip()
        varis = self.varis_var.get().strip()
        if not baslangic or not varis:
            messagebox.showerror("Hata", "Başlangıç ve varış noktası boş olamaz!")
            return

        try:
            mesafe = int(self.mesafe_var.get())
        except ValueError:
            messagebox.showerror("Hata", "Mesafe sayısal olmalı!")
            return

        rota = Rota(baslangic, varis, mesafe)

        secim = self.konaklama_listbox.curselection()
        if not secim:
            messagebox.showerror("Hata", "Lütfen bir konaklama seçin!")
            return
        konaklama = self.konaklama_listesi[secim[0]]

        plan = self.plan_text.get("1.0", tk.END).strip()

        secili_index = self.seyahat_listbox.curselection()
        if secili_index:
            idx = secili_index[0]
            self.seyahatler[idx].rota = rota
            self.seyahatler[idx].konaklama = konaklama
            self.seyahatler[idx].plan = plan
            messagebox.showinfo("Başarılı", "Seyahat planı güncellendi.")
        else:
            yeni_seyahat = Seyahat(rota, konaklama, plan)
            self.seyahatler.append(yeni_seyahat)
            messagebox.showinfo("Başarılı", "Yeni seyahat planı kaydedildi.")

        self.seyahat_listesi_guncelle()
        self.temizle()

    def seyahat_listesi_guncelle(self):
        self.seyahat_listbox.delete(0, tk.END)
        for s in self.seyahatler:
            özet = f"{s.rota.baslangic} → {s.rota.varis} | {s.konaklama.isim} | {s.rota.mesafe} km"
            self.seyahat_listbox.insert(tk.END, özet)

    def seyahat_secildi(self, event):
        secimler = self.seyahat_listbox.curselection()
        if not secimler:
            return
        idx = secimler[0]
        secili = self.seyahatler[idx]

        self.baslangic_var.set(secili.rota.baslangic)
        self.varis_var.set(secili.rota.varis)
        self.mesafe_var.set(str(secili.rota.mesafe))

        for i, k in enumerate(self.konaklama_listesi):
            if k.isim == secili.konaklama.isim:
                self.konaklama_listbox.selection_clear(0, tk.END)
                self.konaklama_listbox.selection_set(i)
                self.konaklama_listbox.see(i)
                break

        self.plan_text.delete("1.0", tk.END)
        self.plan_text.insert(tk.END, secili.plan)

    def seyahat_sil(self):
        secimler = self.seyahat_listbox.curselection()
        if not secimler:
            messagebox.showwarning("Uyarı", "Lütfen silmek için bir seyahat planı seçin.")
            return
        idx = secimler[0]
        cevap = messagebox.askyesno("Onay", "Seçili seyahat planını silmek istediğinize emin misiniz?")
        if cevap:
            del self.seyahatler[idx]
            self.seyahat_listesi_guncelle()
            self.temizle()

    def temizle(self):
        self.baslangic_var.set("")
        self.varis_var.set("")
        self.mesafe_var.set("")
        self.konaklama_listbox.selection_clear(0, tk.END)
        self.plan_text.delete("1.0", tk.END)
        self.seyahat_listbox.selection_clear(0, tk.END)

if __name__ == "__main__":
    giris = GirisEkrani()
    giris.mainloop()
