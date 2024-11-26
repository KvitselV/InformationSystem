class Soiskatel_rep:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_all(self):
        raise NotImplementedError()

    def write_all(self, data):
        raise NotImplementedError()

    def get_by_id(self, id):
        raise NotImplementedError()

    def get_k_n_short_list(self, k, n):
        raise NotImplementedError()

    def sort_by_field(self, field):
        raise NotImplementedError()

    def add(self, new_item):
        raise NotImplementedError()

    def replace_by_id(self, id, updated_item):
        raise NotImplementedError()

    def delete_by_id(self, id):
        raise NotImplementedError()

    def get_count(self):
        raise NotImplementedError()

class Soiskatel_rep_json(Soiskatel_rep):
    def read_all(self):
        with open(self.file_name, "r", encoding="utf-8") as file:
            return json.load(file)

    def write_all(self, data):
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            
class Soiskatel_rep_yaml(Soiskatel_rep):
    def read_all(self):
        with open(self.file_name, "r", encoding="utf-8") as file:
            return yaml.load(file)

    def write_all(self, data):
        with open(self.file_name, "w", encoding="utf-8") as file:
            yaml.dump(data, file, ensure_ascii=False, indent=4)

