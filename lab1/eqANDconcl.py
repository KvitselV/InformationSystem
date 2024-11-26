def __str__(self):
    return (f"Soiskatel: {self.__fam} {self.__imya} {self.__otchestvo}, "
            f"Квалификация: {self.__kvalifikaciya}, Профессия: {self.__professiya}, "
            f"Дата рождения: {self.__data_rozhdeniya}, Телефон: {self.__telefon}, Адрес: {self.__adres}")

def short_info(self):
    return f"{self.__fam} {self.__imya[0]}. {self.__otchestvo[0] if self.__otchestvo else ''}."

def __eq__(self, other):
    return (self.__fam == other.get_fam() and
            self.__imya == other.get_imya() and
            self.__otchestvo == other.get_otchestvo())
