
class Malzeme:
    def __init__(self, ad, miktar):
        self.ad = ad
        self.miktar = miktar

    def __str__(self):
        return f"{self.ad} ({self.miktar})"
