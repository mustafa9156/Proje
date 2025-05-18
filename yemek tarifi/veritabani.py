
class Veritabani:
    def __init__(self):
        self.tarifler = []

    def tarif_ekle(self, tarif):
        self.tarifler.append(tarif)

    def tarif_ara(self, kelime):
        return [t for t in self.tarifler if kelime.lower() in t.ad.lower()]
