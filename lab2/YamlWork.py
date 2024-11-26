import yaml
from datetime import date

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
