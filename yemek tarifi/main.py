
from tarif import Tarif
from malzeme import Malzeme
from kullanici import Kullanici
from veritabani import Veritabani

def main():
    vt = Veritabani()

    while True:
        print("\n1. Tarif Ekle\n2. Tarif Ara\n3. Tarifleri Listele\n4. Çıkış")
        secim = input("Seçiminiz: ")

        if secim == "1":
            ad = input("Tarif adı: ")
            icerik = input("Tarif içeriği: ")
            malzemeler = []
            while True:
                malzeme_adi = input("Malzeme adı (bitirmek için 'q'): ")
                if malzeme_adi.lower() == 'q':
                    break
                miktar = input("Miktarı: ")
                malzemeler.append(Malzeme(malzeme_adi, miktar))
            tarif = Tarif(ad, malzemeler, icerik)
            vt.tarif_ekle(tarif)
            print("Tarif eklendi.")

        elif secim == "2":
            anahtar = input("Aranacak kelime: ")
            sonuc = vt.tarif_ara(anahtar)
            for t in sonuc:
                print(t)

        elif secim == "3":
            for t in vt.tarifler:
                print(t)

        elif secim == "4":
            break

        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    main()
