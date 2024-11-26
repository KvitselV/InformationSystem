class Validator:
    @staticmethod
    def validate_name(value, field_name):
        if not value or not value.isalpha():
            raise ValueError(f"{field_name} должна содержать только буквы.")
        return value

    @staticmethod
    def validate_non_empty(value, field_name):
        if not value:
            raise ValueError(f"{field_name} не может быть пустым.")
        return value

    @staticmethod
    def validate_date(value):
        if not isinstance(value, date) or value > date.today():
            raise ValueError("Некорректная дата рождения.")
        return value

    @staticmethod
    def validate_phone(value):
        if not value or not value.startswith("+") or not value[1:].isdigit() or len(value) < 10:
            raise ValueError("Телефон должен быть в формате +XXXXXXXXXX.")
        return value
