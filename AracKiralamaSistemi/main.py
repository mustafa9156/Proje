from arac import Arac
from musteri import Musteri
from kiralama import Kiralama

# Araçlar
arac1 = Arac(1, "Toyota Corolla")
arac2 = Arac(2, "Honda Civic")

# Müşteriler
musteri1 = Musteri(101, "")
musteri2 = Musteri(102, "")

# Kiralama sistemi
kiralama_sistemi = Kiralama()

# Kiralama yap
kiralama_sistemi.kiralama_yap(arac1, musteri1)

# Kiralama bilgisi
kiralama_sistemi.kiralama_bilgisi()

# Kiralama iptal et
kiralama_sistemi.kiralama_iptal_et(1)
