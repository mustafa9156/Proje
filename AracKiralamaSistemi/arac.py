class Arac:
    def __init__(self, arac_id, model, kiralama_durumu=False):
        self.arac_id = arac_id
        self.model = model
        self.kiralama_durumu = kiralama_durumu 

    def arac_durumu_guncelle(self, yeni_durum):
        self.kiralama_durumu = yeni_durum

    def __str__(self):
        durum = "Kirada" if self.kiralama_durumu else "Boşta"
        return f"Arac ID: {self.arac_id}, Model: {self.model}, Durum: {durum}"
