import json
import yaml
import psycopg2
from datetime import date, datetime


# Класс Soiskatel
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


# Репозиторий для работы с JSON
class Soiskatel_rep_json:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_all(self):
        with open(self.file_name, "r", encoding="utf-8") as file:
            return json.load(file)

    def write_all(self, data):
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_by_id(self, id):
        data = self.read_all()
        return next((item for item in data if item["id"] == id), None)

    def get_k_n_short_list(self, k, n):
        data = self.read_all()
        start = k * n
        end = start + n
        return [Soiskatel.from_json(json.dumps(item)) for item in data[start:end]]

    def sort_by_field(self, field):
        data = self.read_all()
        data.sort(key=lambda x: x.get(field))
        self.write_all(data)

    def add(self, new_item):
        data = self.read_all()
        new_item["id"] = len(data) + 1  # Генерация нового ID
        data.append(new_item)
        self.write_all(data)

    def replace_by_id(self, id, updated_item):
        data = self.read_all()
        for i, item in enumerate(data):
            if item["id"] == id:
                data[i] = updated_item
                self.write_all(data)
                return
        raise ValueError("Элемент не найден")

    def delete_by_id(self, id):
        data = self.read_all()
        data = [item for item in data if item["id"] != id]
        self.write_all(data)

    def get_count(self):
        data = self.read_all()
        return len(data)


# Репозиторий для работы с YAML
class Soiskatel_rep_yaml:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_all(self):
        with open(self.file_name, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def write_all(self, data):
        with open(self.file_name, "w", encoding="utf-8") as file:
            yaml.dump(data, file, allow_unicode=True)

    def get_by_id(self, id):
        data = self.read_all()
        return next((item for item in data if item["id"] == id), None)

    def get_k_n_short_list(self, k, n):
        data = self.read_all()
        start = k * n
        end = start + n
        return [Soiskatel.from_json(json.dumps(item)) for item in data[start:end]]

    def sort_by_field(self, field):
        data = self.read_all()
        data.sort(key=lambda x: x.get(field))
        self.write_all(data)

    def add(self, new_item):
        data = self.read_all()
        new_item["id"] = len(data) + 1  # Генерация нового ID
        data.append(new_item)
        self.write_all(data)

    def replace_by_id(self, id, updated_item):
        data = self.read_all()
        for i, item in enumerate(data):
            if item["id"] == id:
                data[i] = updated_item
                self.write_all(data)
                return
        raise ValueError("Элемент не найден")

    def delete_by_id(self, id):
        data = self.read_all()
        data = [item for item in data if item["id"] != id]
        self.write_all(data)

    def get_count(self):
        data = self.read_all()
        return len(data)


# Реализация паттерна одиночка для работы с БД
class DBConnection:
    _instance = None

    def __new__(cls, db_config):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = psycopg2.connect(**db_config)
        return cls._instance


# Репозиторий для работы с БД
class Soiskatel_rep_DB:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_connection(self):
        return DBConnection(self.db_config).connection

    def get_by_id(self, id):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM soiskatel WHERE id = %s", (id,))
                return cursor.fetchone()

    def get_k_n_short_list(self, k, n):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM soiskatel LIMIT %s OFFSET %s", (n, k * n))
                return cursor.fetchall()

    def add(self, new_item):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO soiskatel (fam, imya, otchestvo, kvalifikaciya, professiya, data_rozhdeniya, telefon, adres) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                    (new_item['fam'], new_item['imya'], new_item['otchestvo'], new_item['kvalifikaciya'], new_item['professiya'],
                     new_item['data_rozhdeniya'], new_item['telefon'], new_item['adres'])
                )
                return cursor.fetchone()[0]  # возвращает id нового объекта

    def replace_by_id(self, id, updated_item):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE soiskatel SET fam = %s, imya = %s, otchestvo = %s, kvalifikaciya = %s, professiya = %s, "
                    "data_rozhdeniya = %s, telefon = %s, adres = %s WHERE id = %s",
                    (updated_item['fam'], updated_item['imya'], updated_item['otchestvo'], updated_item['kvalifikaciya'],
                     updated_item['professiya'], updated_item['data_rozhdeniya'], updated_item['telefon'],
                     updated_item['adres'], id)
                )

    def delete_by_id(self, id):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM soiskatel WHERE id = %s", (id,))

    def get_count(self):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM soiskatel")
                return cursor.fetchone()[0]

if __name__ == "__main__":
        # Настройки подключения к базе данных
        db_config = {
            "dbname": "postgres",
            "user": "postgres",
            "password": "123",
            "host": "localhost",
            "port": "5432"
        }

        # Создание репозитория для работы с БД
        repo_db = Soiskatel_rep_DB(db_config)

        # Пример данных соискателя
        soiskatel_data = {
            "fam": "Сидоров",
            "imya": "Сидор",
            "otchestvo": "Сидорович",
            "kvalifikaciya": "Математик",
            "professiya": "Преподаватель",
            "data_rozhdeniya": "1970-12-12",
            "telefon": "1112233445",
            "adres": "Екатеринбург, ул. Чапаева, д. 10"
        }

        # Добавление нового соискателя в БД
        new_id = repo_db.add(soiskatel_data)
        print(f"Добавлен соискатель с ID: {new_id}")

        # Получение соискателя по ID
        soiskatel_by_id = repo_db.get_by_id(new_id)
        print(soiskatel_by_id)

        # Получение списка соискателей с пагинацией
        short_list = repo_db.get_k_n_short_list(0, 2)
        print(short_list)

        # Обновление данных соискателя
        updated_data = soiskatel_data.copy()
        updated_data["fam"] = "Сидоровский"
        repo_db.replace_by_id(new_id, updated_data)

        # Удаление соискателя по ID
        repo_db.delete_by_id(new_id)
        print(f"Соискатель с ID {new_id} удален.")
