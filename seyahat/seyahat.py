import tkinter as tk
from tkinter import messagebox
from seyahat import Seyahat, Rota, Konaklama  # seyahat.py'den sınıfları alıyoruz

class SeyahatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Seyahat Planlama Uygulaması")
        self.root.geometry("500x400")

        # Seyahat nesnesi
        self.seyahat = Seyahat()

        # Rota girişi
        tk.Label(root, text="Başlangıç:").pack()
        self.baslangic_entry = tk.Entry(root)
        self.baslangic_entry.pack()

        tk.Label(root, text="Varış:").pack()
        self.varis_entry = tk.Entry(root)
        self.varis_entry.pack()

        tk.Label(root, text="Duraklar (virgülle ayır):").pack()
        self.duraklar_entry = tk.Entry(root)
        self.duraklar_entry.pack()

        tk.Label(root, text="Mesafe (km):").pack()
        self.mesafe_entry = tk.Entry(root)
        self.mesafe_entry.pack()

        # Konaklama girişi
        tk.Label(root, text="Konaklama İsmi:").pack()
        self.konaklama_isim_entry = tk.Entry(root)
        self.konaklama_isim_entry.pack()

        tk.Label(root, text="Konaklama Fiyatı (TL):").pack()
        self.konaklama_fiyat_entry = tk.Entry(root)
        self.konaklama_fiyat_entry.pack()

        tk.Label(root, text="Konaklama Adresi:").pack()
        self.konaklama_adres_entry = tk.Entry(root)
        self.konaklama_adres_entry.pack()

        tk.Label(root, text="Yıldız Sayısı:").pack()
        self.konaklama_yildiz_entry = tk.Entry(root)
        self.konaklama_yildiz_entry.pack()

        # Plan metni
        tk.Label(root, text="Plan Detayları:").pack()
        self.plan_text = tk.Text(root, height=4)
        self.plan_text.pack()

        # Buton
        tk.Button(root, text="Seyahati Kaydet", command=self.seyahati_kaydet).pack(pady=10)

        # Sonuç gösterme alanı
        self.sonuc_label = tk.Label(root, text="", justify="left")
        self.sonuc_label.pack()

    def seyahati_kaydet(self):
        try:
            baslangic = self.baslangic_entry.get()
            varis = self.varis_entry.get()
            duraklar = [d.strip() for d in self.duraklar_entry.get().split(",")] if self.duraklar_entry.get() else []
            mesafe = float(self.mesafe_entry.get())

            konaklama_isim = self.konaklama_isim_entry.get()
            konaklama_fiyat = float(self.konaklama_fiyat_entry.get())
            konaklama_adres = self.konaklama_adres_entry.get()
            konaklama_yildiz = int(self.konaklama_yildiz_entry.get())

            plan = self.plan_text.get("1.0", tk.END).strip()

            rota = Rota(baslangic, varis, duraklar, mesafe)
            konaklama = Konaklama(konaklama_isim, konaklama_fiyat, konaklama_adres, konaklama_yildiz)
            self.seyahat = Seyahat(rota, konaklama, plan)

            self.sonuc_label.config(text=str(self.seyahat))

        except ValueError:
            messagebox.showerror("Hata", "Lütfen tüm alanları doğru şekilde doldurun.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SeyahatApp(root)
    root.mainloop()
