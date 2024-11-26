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
