
class Tarif:
    def __init__(self, ad, malzemeler, icerik):
        self.ad = ad
        self.malzemeler = malzemeler
        self.icerik = icerik
        self.puanlar = []

    def puan_ver(self, puan):
        self.puanlar.append(puan)

    def ortalama_puan(self):
        if not self.puanlar:
            return "Henüz puan verilmedi"
        return sum(self.puanlar) / len(self.puanlar)

    def __str__(self):
        malzeme_listesi = ", ".join([str(m) for m in self.malzemeler])
        return f"Tarif: {self.ad}\nMalzemeler: {malzeme_listesi}\nİçerik: {self.icerik}\nOrtalama Puan: {self.ortalama_puan()}"
