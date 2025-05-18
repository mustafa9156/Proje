class Takip:
    def __init__(self, antrenman, tarih, ilerleme_notu):
        self.antrenman = antrenman
        self.tarih = tarih
        self.ilerleme_notu = ilerleme_notu

    def __str__(self):
        return f"{self.tarih} - {self.antrenman.ad}: {self.ilerleme_notu}"
