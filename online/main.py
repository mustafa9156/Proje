import tkinter as tk
from tkinter import ttk, messagebox

class Kullanici:
    def __init__(self, kullanici_adi, sifre, rol):
        self.kullanici_adi = kullanici_adi
        self.sifre = sifre
        self.rol = rol

class DersIcerik:
    def __init__(self, baslik, icerik):
        self.baslik = baslik
        self.icerik = icerik

class Kurs:
    def __init__(self, isim, egitmen=None):
        self.isim = isim
        self.egitmen = egitmen
        self.icerikler = []

class Sistem:
    def __init__(self):
        self.kullanicilar = [Kullanici("admin", "1234", "admin")]
        self.kurslar = []

    def kullanici_ekle(self, kullanici_adi, sifre, rol):
        if any(k.kullanici_adi == kullanici_adi for k in self.kullanicilar):
            return False
        self.kullanicilar.append(Kullanici(kullanici_adi, sifre, rol))
        return True

    def kullanici_giris(self, kullanici_adi, sifre):
        for k in self.kullanicilar:
            if k.kullanici_adi == kullanici_adi and k.sifre == sifre:
                return k
        return None

    def kurs_ekle(self, isim, egitmen):
        if any(k.isim == isim for k in self.kurslar):
            return False
        self.kurslar.append(Kurs(isim, egitmen))
        return True

    def kurs_sil(self, kurs_ismi):
        self.kurslar = [k for k in self.kurslar if k.isim != kurs_ismi]

    def kullanici_sil(self, kullanici_adi):
        self.kullanicilar = [k for k in self.kullanicilar if k.kullanici_adi != kullanici_adi]

class OnlineEgitimApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Eğitim Platformu")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f8ff")

        self.sistem = Sistem()
        self.current_user = None

        self.login_ekran()

    def temizle(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_ekran(self):
        self.temizle()
        tk.Label(self.root, text="Online Eğitim Platformu - Giriş", font=("Arial", 24, "bold"), bg="#f0f8ff").pack(pady=30)

        frame = tk.Frame(self.root, bg="#f0f8ff")
        frame.pack()

        tk.Label(frame, text="Kullanıcı Adı:", bg="#f0f8ff").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.login_kullanici_entry = tk.Entry(frame)
        self.login_kullanici_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Şifre:", bg="#f0f8ff").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.login_sifre_entry = tk.Entry(frame, show="*")
        self.login_sifre_entry.grid(row=1, column=1, pady=5)

        tk.Button(self.root, text="Giriş Yap", command=self.giris_yap, width=20, bg="#1e90ff", fg="white").pack(pady=15)

    def giris_yap(self):
        kadi = self.login_kullanici_entry.get().strip()
        sifre = self.login_sifre_entry.get().strip()
        kullanici = self.sistem.kullanici_giris(kadi, sifre)

        if kullanici:
            self.current_user = kullanici
            if kullanici.rol == "admin":
                self.admin_panel()
            elif kullanici.rol == "egitmen":
                self.egitmen_panel()
            elif kullanici.rol == "ogrenci":
                self.ogrenci_panel()
        else:
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre.")

    def admin_panel(self):
        self.temizle()
        tk.Label(self.root, text=f"Admin Paneli - Hoşgeldin {self.current_user.kullanici_adi}",
                 font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=15)

        ust_frame = tk.Frame(self.root, bg="#f0f8ff")
        ust_frame.pack(pady=5)

        # Kullanıcı ekleme
        kf = tk.LabelFrame(ust_frame, text="Kullanıcı Ekle", padx=10, pady=10)
        kf.grid(row=0, column=0, padx=10)

        self.admin_kullanici_adi = tk.Entry(kf)
        self.admin_sifre = tk.Entry(kf, show="*")
        self.admin_rol = ttk.Combobox(kf, values=["egitmen", "ogrenci"], state="readonly")
        self.admin_rol.current(0)

        for i, (label, widget) in enumerate(zip(["Kullanıcı Adı:", "Şifre:", "Rol:"],
                                                [self.admin_kullanici_adi, self.admin_sifre, self.admin_rol])):
            tk.Label(kf, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            widget.grid(row=i, column=1, pady=5)

        tk.Button(kf, text="Kullanıcı Ekle", bg="#1e90ff", fg="white", command=self.admin_kullanici_ekle).grid(columnspan=2, pady=5)

        # Kurs ekleme
        kursf = tk.LabelFrame(ust_frame, text="Kurs Ekle", padx=10, pady=10)
        kursf.grid(row=0, column=1, padx=10)

        self.admin_kurs_adi = tk.Entry(kursf)
        self.admin_egitmen_secim = ttk.Combobox(kursf, state="readonly")
        self.guncelle_egitmen_listesi()

        for i, (label, widget) in enumerate(zip(["Kurs İsmi:", "Eğitmen:"],
                                                [self.admin_kurs_adi, self.admin_egitmen_secim])):
            tk.Label(kursf, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            widget.grid(row=i, column=1, pady=5)

        tk.Button(kursf, text="Kurs Ekle", bg="#1e90ff", fg="white", command=self.admin_kurs_ekle).grid(columnspan=2, pady=5)

        # Kullanıcı ve kurs listeleri
        alt_frame = tk.Frame(self.root, bg="#f0f8ff")
        alt_frame.pack(pady=10, fill="both", expand=True)

        sol = tk.Frame(alt_frame, bg="#f0f8ff")
        sol.pack(side="left", padx=10, expand=True)

        tk.Label(sol, text="Kullanıcılar", bg="#f0f8ff", font=("Arial", 12, "bold")).pack()
        self.admin_kullanici_listbox = tk.Listbox(sol, height=10)
        self.admin_kullanici_listbox.pack(padx=5, pady=5, fill="both", expand=True)
        tk.Button(sol, text="Kullanıcı Sil", bg="red", fg="white", command=self.kullanici_sil).pack(pady=5)

        sag = tk.Frame(alt_frame, bg="#f0f8ff")
        sag.pack(side="left", padx=10, expand=True)

        tk.Label(sag, text="Kurslar", bg="#f0f8ff", font=("Arial", 12, "bold")).pack()
        self.admin_kurs_listbox = tk.Listbox(sag, height=10)
        self.admin_kurs_listbox.pack(padx=5, pady=5, fill="both", expand=True)
        tk.Button(sag, text="Kurs Sil", bg="red", fg="white", command=self.kurs_sil).pack(pady=5)

        self.guncelle_admin_listeler()

        tk.Button(self.root, text="Çıkış Yap", command=self.cikis_yap, bg="#555", fg="white").pack(pady=10)

    def egitmen_panel(self):
        self.temizle()
        tk.Label(self.root, text=f"Eğitmen Paneli - Hoşgeldin {self.current_user.kullanici_adi}",
                 font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=15)

        egitmen_kurslari = [k for k in self.sistem.kurslar if k.egitmen == self.current_user]

        self.kurs_listbox = tk.Listbox(self.root)
        self.kurs_listbox.pack(pady=10, fill="x", padx=20)

        for kurs in egitmen_kurslari:
            self.kurs_listbox.insert(tk.END, kurs.isim)

        tk.Label(self.root, text="Yeni İçerik Başlığı").pack()
        self.icerik_baslik_entry = tk.Entry(self.root)
        self.icerik_baslik_entry.pack()

        tk.Label(self.root, text="Yeni İçerik Metni").pack()
        self.icerik_metni_entry = tk.Text(self.root, height=5)
        self.icerik_metni_entry.pack()

        tk.Button(self.root, text="İçerik Ekle", bg="#1e90ff", fg="white", command=self.icerik_ekle).pack(pady=10)
        tk.Button(self.root, text="Çıkış Yap", command=self.cikis_yap, bg="#555", fg="white").pack(pady=5)

    

    def icerik_ekle(self):
        secim = self.kurs_listbox.curselection()
        if not secim:
            messagebox.showwarning("Uyarı", "Bir kurs seçmelisiniz.")
            return

        baslik = self.icerik_baslik_entry.get().strip()
        icerik = self.icerik_metni_entry.get("1.0", tk.END).strip()

        if not baslik or not icerik:
            messagebox.showwarning("Uyarı", "Başlık ve içerik boş bırakılamaz.")
            return

        secilen_kurs_adi = self.kurs_listbox.get(secim[0])
        kurs = next((k for k in self.sistem.kurslar if k.isim == secilen_kurs_adi), None)

        if kurs:
            kurs.icerikler.append(DersIcerik(baslik, icerik))
            messagebox.showinfo("Başarılı", "İçerik eklendi.")
            self.icerik_baslik_entry.delete(0, tk.END)
            self.icerik_metni_entry.delete("1.0", tk.END)

    def ogrenci_panel(self):
        self.temizle()
        tk.Label(self.root, text=f"Öğrenci Paneli - Hoşgeldin {self.current_user.kullanici_adi}",
                 font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=15)
        tk.Button(self.root, text="Çıkış Yap", command=self.cikis_yap, bg="#555", fg="white").pack(pady=10)

    def guncelle_egitmen_listesi(self):
        egitmenler = [k.kullanici_adi for k in self.sistem.kullanicilar if k.rol == "egitmen"]
        self.admin_egitmen_secim['values'] = egitmenler
        if egitmenler:
            self.admin_egitmen_secim.current(0)

    def admin_kullanici_ekle(self):
        kadi = self.admin_kullanici_adi.get().strip()
        sifre = self.admin_sifre.get().strip()
        rol = self.admin_rol.get()
        if not kadi or not sifre:
            messagebox.showwarning("Hata", "Alanlar boş bırakılamaz.")
            return
        if self.sistem.kullanici_ekle(kadi, sifre, rol):
            self.admin_kullanici_adi.delete(0, tk.END)
            self.admin_sifre.delete(0, tk.END)
            self.guncelle_admin_listeler()
            self.guncelle_egitmen_listesi()
        else:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten var.")
        
    def ogrenci_panel(self):
        self.temizle()
        tk.Label(self.root, text=f"Öğrenci Paneli - Hoşgeldin {self.current_user.kullanici_adi}",
            font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=15)

        frame = tk.Frame(self.root, bg="#f0f8ff")
        frame.pack(pady=10)

        tk.Label(frame, text="Kurslar", font=("Arial", 14, "bold"), bg="#f0f8ff").pack()

        self.ogrenci_kurs_listbox = tk.Listbox(frame, width=40)
        self.ogrenci_kurs_listbox.pack(padx=10, pady=5)

        for kurs in self.sistem.kurslar:
            self.ogrenci_kurs_listbox.insert(tk.END, kurs.isim)

        tk.Button(frame, text="İçerikleri Göster", bg="#1e90ff", fg="white", command=self.icerikleri_goster).pack(pady=5)

        self.icerik_alani = tk.Text(self.root, height=15, width=80)
        self.icerik_alani.pack(pady=10)

        tk.Button(self.root, text="Çıkış Yap", command=self.cikis_yap, bg="#555", fg="white").pack(pady=10)

    def icerikleri_goster(self):
        secim = self.ogrenci_kurs_listbox.curselection()
        if not secim:
            messagebox.showwarning("Uyarı", "Bir kurs seçmelisiniz.")
            return

        secilen_kurs_adi = self.ogrenci_kurs_listbox.get(secim[0])
        kurs = next((k for k in self.sistem.kurslar if k.isim == secilen_kurs_adi), None)

        self.icerik_alani.delete("1.0", tk.END)
        if kurs and kurs.icerikler:
            for ic in kurs.icerikler:
                self.icerik_alani.insert(tk.END, f"Başlık: {ic.baslik}\nİçerik: {ic.icerik}\n\n")
        else:
            self.icerik_alani.insert(tk.END, "Bu kurs için içerik bulunmamaktadır.\n")


    def admin_kurs_ekle(self):
        kurs = self.admin_kurs_adi.get().strip()
        egitmen_adi = self.admin_egitmen_secim.get()
        egitmen = next((k for k in self.sistem.kullanicilar if k.kullanici_adi == egitmen_adi), None)

        if self.sistem.kurs_ekle(kurs, egitmen):
            self.admin_kurs_adi.delete(0, tk.END)
            self.guncelle_admin_listeler()
        else:
            messagebox.showerror("Hata", "Bu kurs zaten var.")

    def kullanici_sil(self):
        secim = self.admin_kullanici_listbox.curselection()
        if secim:
            veri = self.admin_kullanici_listbox.get(secim[0])
            kadi = veri.split(" ")[0]
            self.sistem.kullanici_sil(kadi)
            self.guncelle_admin_listeler()
            self.guncelle_egitmen_listesi()

    def kurs_sil(self):
        secim = self.admin_kurs_listbox.curselection()
        if secim:
            veri = self.admin_kurs_listbox.get(secim[0])
            kurs_ismi = veri.split(" - ")[0]
            self.sistem.kurs_sil(kurs_ismi)
            self.guncelle_admin_listeler()

    def guncelle_admin_listeler(self):
        self.admin_kullanici_listbox.delete(0, tk.END)
        for k in self.sistem.kullanicilar:
            self.admin_kullanici_listbox.insert(tk.END, f"{k.kullanici_adi} ({k.rol})")

        self.admin_kurs_listbox.delete(0, tk.END)
        for kurs in self.sistem.kurslar:
            egitmen_adi = kurs.egitmen.kullanici_adi if kurs.egitmen else "Yok"
            self.admin_kurs_listbox.insert(tk.END, f"{kurs.isim} - Eğitmen: {egitmen_adi}")

    def cikis_yap(self):
        self.current_user = None
        self.login_ekran()

if __name__ == "__main__":
    root = tk.Tk()
    app = OnlineEgitimApp(root)
    root.mainloop()
