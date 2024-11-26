class ShortSoiskatel(Soiskatel):
    def __init__(self, fam, imya, otchestvo):
        super().__init__(fam, imya, otchestvo, kvalifikaciya="N/A", professiya="N/A",
                         data_rozhdeniya=date(1900, 1, 1), telefon="0000000000", adres="N/A")

    def __str__(self):
        return f"ShortSoiskatel: {self.get_fam()} {self.get_imya()[0]}. {self.get_otchestvo()[0] if self.get_otchestvo() else ''}."
