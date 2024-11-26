from datetime import date

class Soiskatel:
    def __init__(self, fam, imya, otchestvo, kvalifikaciya, professiya, data_rozhdeniya, telefon, adres):
        # Приватные поля
        self.__fam = fam
        self.__imya = imya
        self.__otchestvo = otchestvo
        self.__kvalifikaciya = kvalifikaciya
        self.__professiya = professiya
        self.__data_rozhdeniya = data_rozhdeniya
        self.__telefon = telefon
        self.__adres = adres

    # Геттеры для доступа к данным
    def get_fam(self):
        return self.__fam

    def get_imya(self):
        return self.__imya

    def get_otchestvo(self):
        return self.__otchestvo

    def get_kvalifikaciya(self):
        return self.__kvalifikaciya

    def get_professiya(self):
        return self.__professiya

    def get_data_rozhdeniya(self):
        return self.__data_rozhdeniya

    def get_telefon(self):
        return self.__telefon

    def get_adres(self):
        return self.__adres

    # Сеттеры для изменения данных
    def set_fam(self, fam):
        self.__fam = fam

    def set_imya(self, imya):
        self.__imya = imya

    def set_otchestvo(self, otchestvo):
        self.__otchestvo = otchestvo

    def set_kvalifikaciya(self, kvalifikaciya):
        self.__kvalifikaciya = kvalifikaciya

    def set_professiya(self, professiya):
        self.__professiya = professiya

    def set_data_rozhdeniya(self, data_rozhdeniya):
        self.__data_rozhdeniya = data_rozhdeniya

    def set_telefon(self, telefon):
        self.__telefon = telefon

    def set_adres(self, adres):
        self.__adres = adres
