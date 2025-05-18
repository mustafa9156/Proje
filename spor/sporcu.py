from takip import Takip
from datetime import datetime

class Sporcu:
    def __init__(self, isim, spor_dali):
        self.isim = isim
        self.spor_dali = spor_dali
        self.programlar = []  
        self.takipler = []   

    def program_olustur(self, antrenman):
        self.programlar.append(antrenman)
        print(f"{self.isim} için {antrenman.ad} programı eklendi.")

    def ilerleme_kaydet(self, antrenman, ilerleme_notu):
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M")
        takip = Takip(antrenman, tarih, ilerleme_notu)
        self.takipler.append(takip)
        print(f"{self.isim} için {antrenman.ad} ilerlemesi kaydedildi.")

    def rapor_al(self):
        print(f"\n{self.isim} - {self.spor_dali} Sporcu İlerleme Raporu:")
        if not self.takipler:
            print("Henüz ilerleme kaydı yok.")
            return
        for takip in self.takipler:
            print(takip)
