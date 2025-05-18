class Antrenman:
    def __init__(self, ad, detaylar):
        self.ad = ad
        self.detaylar = detaylar

    def __str__(self):
        return f"{self.ad}: {self.detaylar}"
