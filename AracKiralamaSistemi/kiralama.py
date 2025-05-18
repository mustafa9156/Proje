class Kiralama:
    def __init__(self):
        self.kiralama_listesi = [] 

    def kiralama_yap(self, arac, musteri):
        if arac.kiralama_durumu:
            print(f"{arac.model} zaten kirada.")
            return False
        arac.arac_durumu_guncelle(True)
        self.kiralama_listesi.append({'arac': arac, 'musteri': musteri})
        print(f"{musteri.isim} için {arac.model} kiralandı.")
        return True

    def kiralama_iptal_et(self, arac_id):
        for kiralama in self.kiralama_listesi:
            if kiralama['arac'].arac_id == arac_id:
                kiralama['arac'].arac_durumu_guncelle(False)
                self.kiralama_listesi.remove(kiralama)
                print(f"Arac ID {arac_id} kiralama iptal edildi.")
                return True
        print("Kiralama bulunamadı.")
        return False

    def kiralama_bilgisi(self):
        for kiralama in self.kiralama_listesi:
            print(f"{kiralama['musteri'].isim} -> {kiralama['arac'].model}")
