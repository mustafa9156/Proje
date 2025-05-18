import tkinter as tk
from tkinter import messagebox, simpledialog

USERS = {"admin": "1234", "user": "pass"}

class Arac:
    def __init__(self, arac_id, model, kiralama_durumu=False):
        self.arac_id = arac_id
        self.model = model
        self.kiralama_durumu = kiralama_durumu

class AracKiralamaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Araç Kiralama Sistemi")
        self.geometry("900x600")
        self.minsize(900, 600)
        self.current_user = None
        self.araclar = []
        self._login_screen()

    def _login_screen(self):
        self.login_frame = tk.Frame(self, bg="#2C3E50")
        self.login_frame.place(relwidth=1, relheight=1)

        label = tk.Label(self.login_frame, text="Araç Kiralama Sistemi", fg="white", bg="#2C3E50", font=("Helvetica", 24, "bold"))
        label.pack(pady=40)

        tk.Label(self.login_frame, text="Kullanıcı Adı", fg="white", bg="#2C3E50", font=("Arial", 14)).pack(pady=10)
        self.user_entry = tk.Entry(self.login_frame, font=("Arial", 14))
        self.user_entry.pack(pady=5)

        tk.Label(self.login_frame, text="Şifre", fg="white", bg="#2C3E50", font=("Arial", 14)).pack(pady=10)
        self.pass_entry = tk.Entry(self.login_frame, show="*", font=("Arial", 14))
        self.pass_entry.pack(pady=5)

        login_btn = tk.Button(self.login_frame, text="Giriş Yap", font=("Arial", 14, "bold"), bg="#27AE60", fg="white", relief="flat", command=self._login)
        login_btn.pack(pady=30, ipadx=20, ipady=8)

        self.pass_entry.bind("<Return>", lambda e: self._login())

    def _login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        if USERS.get(username) == password:
            self.current_user = username
            self.login_frame.destroy()
            self._load_data()
            self._build_main_ui()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış.")

    def _load_data(self):
        self.araclar = [
            Arac("1", "Toyota Corolla", False),
            Arac("2", "Ford Focus", False),
            Arac("3", "Honda Civic", False),
            Arac("4", "BMW 320i", True),
            Arac("5", "Mercedes C200", False),
        ]

    def _build_main_ui(self):
        self.sidebar = tk.Frame(self, bg="#34495E", width=220)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text=f"Hoşgeldin, {self.current_user}", fg="white", bg="#34495E", font=("Arial", 14, "bold")).pack(pady=20)

        btn_exit = tk.Button(self.sidebar, text="Çıkış Yap", bg="#E74C3C", fg="white", font=("Arial", 12, "bold"), relief="flat", command=self.quit)
        btn_exit.pack(side="bottom", fill="x", padx=10, pady=20)

        btn_add = tk.Button(self.sidebar, text="Araç Ekle", bg="#2980B9", fg="white", font=("Arial", 12, "bold"), relief="flat", command=self._arac_ekle)
        btn_add.pack(pady=10, padx=10, fill="x")

        # Arama 
        search_frame = tk.Frame(self.sidebar, bg="#34495E")
        search_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(search_frame, text="Araç Ara:", fg="white", bg="#34495E", font=("Arial", 12)).pack(anchor="w")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._filter_araclar)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12))
        search_entry.pack(fill="x", pady=5)

        # Ana içerik 
        self.content = tk.Frame(self, bg="#ECF0F1")
        self.content.pack(side="right", fill="both", expand=True)

        self.canvas = tk.Canvas(self.content, bg="#ECF0F1")
        self.scrollbar = tk.Scrollbar(self.content, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#ECF0F1")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self._show_araclar()

    def _show_araclar(self, filter_text=""):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        filtered = [a for a in self.araclar if filter_text.lower() in a.model.lower() or filter_text.lower() in a.arac_id.lower()]

        for i, arac in enumerate(filtered):
            frame = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid")
            frame.grid(row=i//2, column=i%2, padx=15, pady=15, sticky="nsew")

            durum_renk = "#27AE60" if not arac.kiralama_durumu else "#E74C3C"

            tk.Label(frame, text=arac.arac_id, font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=10, pady=5)
            tk.Label(frame, text=arac.model, font=("Arial", 12), bg="white").pack(anchor="w", padx=10)
            status_label = tk.Label(frame, text="Müsait" if not arac.kiralama_durumu else "Kiralandı", fg="white", bg=durum_renk, font=("Arial", 12, "bold"), width=12)
            status_label.pack(pady=10, padx=10)

            btn_frame = tk.Frame(frame, bg="white")
            btn_frame.pack(pady=5, padx=10, fill="x")

            if not arac.kiralama_durumu:
                tk.Button(btn_frame, text="Kirala", bg="#2980B9", fg="white", relief="flat", command=lambda a=arac: self._arac_kirala(a)).pack(side="left", fill="x", expand=True, padx=5)
            else:
                tk.Button(btn_frame, text="Kiralama İptal", bg="#C0392B", fg="white", relief="flat", command=lambda a=arac: self._kiralama_iptal(a)).pack(side="left", fill="x", expand=True, padx=5)

            tk.Button(btn_frame, text="Sil", bg="#7F8C8D", fg="white", relief="flat", command=lambda a=arac: self._arac_sil(a)).pack(side="left", fill="x", expand=True, padx=5)

    def _filter_araclar(self, *args):
        search = self.search_var.get()
        self._show_araclar(search)

    def _arac_ekle(self):
        arac_id = simpledialog.askstring("Araç Ekle", "Araç ID:")
        if not arac_id:
            return
        model = simpledialog.askstring("Araç Ekle", "Model:")
        if not model:
            return
        if any(a.arac_id == arac_id for a in self.araclar):
            messagebox.showwarning("Uyarı", "Bu Araç ID zaten var.")
            return
        yeni_arac = Arac(arac_id, model)
        self.araclar.append(yeni_arac)
        self._show_araclar(self.search_var.get())

    def _arac_kirala(self, arac):
        if arac.kiralama_durumu:
            messagebox.showinfo("Bilgi", "Bu araç zaten kiralanmış.")
            return
        arac.kiralama_durumu = True
        messagebox.showinfo("Başarılı", f"{arac.model} kiralandı.")
        self._show_araclar(self.search_var.get())

    def _kiralama_iptal(self, arac):
        if not arac.kiralama_durumu:
            messagebox.showinfo("Bilgi", "Bu araç kiralanmamış.")
            return
        arac.kiralama_durumu = False
        messagebox.showinfo("Başarılı", f"{arac.model} kiralama iptal edildi.")
        self._show_araclar(self.search_var.get())

    def _arac_sil(self, arac):
        if messagebox.askyesno("Silme Onayı", f"{arac.model} aracını silmek istediğinize emin misiniz?"):
            self.araclar.remove(arac)
            self._show_araclar(self.search_var.get())

if __name__ == "__main__":
    app = AracKiralamaApp()
    app.mainloop()
