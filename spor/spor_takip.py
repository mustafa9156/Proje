class Sporcu:
    def __init__(self, ad, spor_dali):
        self.ad = ad
        self.spor_dali = spor_dali
        self.antrenman_programi = []
        self.ilerleme = []

    def program_olustur(self, antrenman):
        self.antrenman_programi.append(antrenman)

    def ilerleme_kaydet(self, ilerleme_bilgisi):
        self.ilerleme.append(ilerleme_bilgisi)

    def rapor_al(self):
        rapor = f"Sporcu: {self.ad}\nSpor Dalı: {self.spor_dali}\nAntrenman Programı:\n"
        for i, ant in enumerate(self.antrenman_programi, 1):
            rapor += f"{i}. {ant.ad} - {ant.detay}\n"
        rapor += "İlerleme Kaydı:\n"
        for i, ilerleme in enumerate(self.ilerleme, 1):
            rapor += f"{i}. {ilerleme}\n"
        return rapor


class Antrenman:
    def __init__(self, ad, detay):
        self.ad = ad
        self.detay = detay


class Takip:
    def __init__(self):
        self.sporcular = []

    def sporcu_ekle(self, sporcu):
        self.sporcular.append(sporcu)

    def sporcu_bul(self, ad):
        for s in self.sporcular:
            if s.ad == ad:
                return s
        return None
