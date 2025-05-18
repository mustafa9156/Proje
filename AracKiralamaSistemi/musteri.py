class Musteri:
    def __init__(self, musteri_id, isim, telefon):
        self.musteri_id = musteri_id
        self.isim = isim
        self.telefon = telefon

    def __str__(self):
        return f"Müşteri ID: {self.musteri_id}, İsim: {self.isim}, Telefon: {self.telefon}"
