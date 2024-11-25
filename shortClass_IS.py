class ShortSoiskatel(Soiskatel):
    def __init__(self, fam, imya, otchestvo):
        super().__init__(fam, imya, otchestvo, "", "", date(1900, 1, 1), "", "")
    
    def __str__(self):
        return f"{self.fam} {self.imya[0]}. {self.otchestvo[0]}."
