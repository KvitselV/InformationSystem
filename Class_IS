from datetime import date

class Soiskatel:
    def __init__(self, fam, imya, otchestvo, kvalifikaciya, professiya, data_rozhdeniya, telefon, adres):
        self.fam = self.validate_name(fam, "Фамилия")
        self.imya = self.validate_name(imya, "Имя")
        self.otchestvo = otchestvo
        self.kvalifikaciya = self.validate_non_empty(kvalifikaciya, "Квалификация")
        self.professiya = self.validate_non_empty(professiya, "Профессия")
        self.data_rozhdeniya = self.validate_date(data_rozhdeniya)
        self.telefon = self.validate_phone(telefon)
        self.adres = adres

    # Геттеры и сеттеры с валидацией
    def validate_name(self, value, field_name):
        if not value or not value.isalpha():
            raise ValueError(f"{field_name} должна содержать только буквы.")
        return value

    def validate_non_empty(self, value, field_name):
        if not value:
            raise ValueError(f"{field_name} не может быть пустым.")
        return value

    def validate_date(self, value):
        if not isinstance(value, date) or value > date.today():
            raise ValueError("Некорректная дата рождения.")
        return value

    def validate_phone(self, value):
        if not value or not value.startswith("+") or not value[1:].isdigit() or len(value) < 10:
            raise ValueError("Телефон должен быть в формате +XXXXXXXXXX.")
        return value

    def __str__(self):
        return f"{self.fam} {self.imya} {self.otchestvo}, {self.professiya}, {self.kvalifikaciya}"

    def short_info(self):
        return f"{self.fam} {self.imya[0]}. {self.otchestvo[0]}."
