import json
from datetime import date, datetime

class Validator:
    @staticmethod
    def validate_non_empty(value, field_name):
        if not value or not value.strip():
            raise ValueError(f"{field_name} не может быть пустым.")
        return value.strip()

    @staticmethod
    def validate_date(value):
        if not isinstance(value, (date, datetime)):
            raise ValueError("Дата должна быть типа date.")
        if value > date.today():
            raise ValueError("Дата не может быть в будущем.")
        return value

    @staticmethod
    def validate_phone(value):
        if not value or not value.strip():
            raise ValueError("Телефон не может быть пустым.")
        if not value.isdigit() or not (10 <= len(value) <= 15):
            raise ValueError("Телефон должен содержать только цифры длиной от 10 до 15.")
        return value.strip()

class Soiskatel:
    def __init__(self, fam, imya, otchestvo, kvalifikaciya, professiya, data_rozhdeniya, telefon, adres):
        self.fam = Validator.validate_non_empty(fam, "Фамилия")
        self.imya = Validator.validate_non_empty(imya, "Имя")
        self.otchestvo = otchestvo.strip() if otchestvo else ""
        self.kvalifikaciya = Validator.validate_non_empty(kvalifikaciya, "Квалификация")
        self.professiya = Validator.validate_non_empty(professiya, "Профессия")
        self.data_rozhdeniya = Validator.validate_date(data_rozhdeniya)
        self.telefon = Validator.validate_phone(telefon)
        self.adres = Validator.validate_non_empty(adres, "Адрес")

    @classmethod
    def from_json(cls, json_str):
        try:
            data = json.loads(json_str)
            return cls(
                data["fam"], data["imya"], data.get("otchestvo", ""),
                data["kvalifikaciya"], data["professiya"],
                date.fromisoformat(data["data_rozhdeniya"]),
                data["telefon"], data["adres"]
            )
        except (KeyError, ValueError) as e:
            raise ValueError(f"Ошибка создания Soiskatel из JSON: {e}")

    def short_info(self):
        return f"{self.fam} {self.imya[0]}. {self.otchestvo[0] if self.otchestvo else ''}."

    def __str__(self):
        return (f"Soiskatel: {self.fam} {self.imya} {self.otchestvo}, "
                f"Квалификация: {self.kvalifikaciya}, Профессия: {self.professiya}, "
                f"Дата рождения: {self.data_rozhdeniya}, Телефон: {self.telefon}, Адрес: {self.adres}")

    def __eq__(self, other):
        if isinstance(other, Soiskatel):
            # Сравнение полного объекта
            return (self.fam == other.fam and
                    self.imya == other.imya and
                    self.otchestvo == other.otchestvo)
        elif isinstance(other, ShortSoiskatel):
            # Сравнение по краткой информации
            return (self.fam == other.fam and
                    self.imya[0] == other.imya[0] and
                    (self.otchestvo[0] if self.otchestvo else '') ==
                    (other.otchestvo[0] if other.otchestvo else ''))
        return False

class ShortSoiskatel(Soiskatel):
    def __init__(self, fam, imya, otchestvo):
        super().__init__(fam, imya, otchestvo, kvalifikaciya="N/A", professiya="N/A",
                         data_rozhdeniya=date(1900, 1, 1), telefon="0000000000", adres="N/A")

    def __str__(self):
        return f"ShortSoiskatel: {self.fam} {self.imya[0]}. {self.otchestvo[0] if self.otchestvo else ''}."

if __name__ == "__main__":
    # Полный объект Soiskatel
    soiskatel = Soiskatel(
        fam="Иванов",
        imya="Иван",
        otchestvo="Иванович",
        kvalifikaciya="Программист",
        professiya="Разработчик",
        data_rozhdeniya=date(1990, 5, 20),
        telefon="79991234567",
        adres="г. Москва, ул. Примерная, д. 1"
    )

    # Краткий объект ShortSoiskatel
    short_soiskatel = ShortSoiskatel("Иванов", "Иван", "Иванович")

    # Сравнение объектов
    print(soiskatel == short_soiskatel)  # True

    # Вывод полной и краткой информации
    print(soiskatel)  # Полная версия объекта
    print(short_soiskatel)  # Краткая версия объекта
