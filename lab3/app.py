import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json

# ========================= Model ========================= #
class Soiskatel:
    def __init__(self, id, fam, imya, otchestvo, kvalifikaciya, professiya, data_rozhdeniya, telefon, adres):
        self.id = id
        self.fam = fam
        self.imya = imya
        self.otchestvo = otchestvo
        self.kvalifikaciya = kvalifikaciya
        self.professiya = professiya
        self.data_rozhdeniya = data_rozhdeniya
        self.telefon = telefon
        self.adres = adres

    @staticmethod
    def from_json(data):
        return Soiskatel(**json.loads(data))

    def to_json(self):
        return json.dumps(self.__dict__)

# ========================= Repository ========================= #
class Repository:
    def __init__(self, db_name="soiskateli.db"):
        self.db_name = db_name
        self.observers = []
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS soiskateli (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            fam TEXT NOT NULL,
                            imya TEXT NOT NULL,
                            otchestvo TEXT,
                            kvalifikaciya TEXT,
                            professiya TEXT,
                            data_rozhdeniya TEXT,
                            telefon TEXT,
                            adres TEXT)''')
        conn.commit()
        conn.close()

    def read_all(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM soiskateli")
        records = cursor.fetchall()
        conn.close()
        return [Soiskatel(*record) for record in records]

    def add(self, soiskatel):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO soiskateli (fam, imya, otchestvo, kvalifikaciya, professiya, data_rozhdeniya, telefon, adres) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (soiskatel.fam, soiskatel.imya, soiskatel.otchestvo, soiskatel.kvalifikaciya, soiskatel.professiya, soiskatel.data_rozhdeniya, soiskatel.telefon, soiskatel.adres))
        conn.commit()
        conn.close()
        self.notify_observers()

    def update(self, soiskatel):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE soiskateli SET fam=?, imya=?, otchestvo=?, kvalifikaciya=?, professiya=?, data_rozhdeniya=?, telefon=?, adres=? WHERE id=?",
                       (soiskatel.fam, soiskatel.imya, soiskatel.otchestvo, soiskatel.kvalifikaciya, soiskatel.professiya, soiskatel.data_rozhdeniya, soiskatel.telefon, soiskatel.adres, soiskatel.id))
        conn.commit()
        conn.close()
        self.notify_observers()

    def delete(self, soiskatel_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM soiskateli WHERE id=?", (soiskatel_id,))
        conn.commit()
        conn.close()
        self.notify_observers()

    def filter_by_fam(self, fam):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM soiskateli WHERE fam LIKE ?", (f"%{fam}%",))
        records = cursor.fetchall()
        conn.close()
        return [Soiskatel(*record) for record in records]

    def sort_by_field(self, field):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM soiskateli ORDER BY {field}")
        records = cursor.fetchall()
        conn.close()
        return [Soiskatel(*record) for record in records]

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer()

# ========================= Validators ========================= #
def validate_soiskatel(data):
    if not data['fam'] or not data['imya']:
        raise ValueError("Фамилия и Имя обязательны для заполнения.")
    if len(data['telefon']) < 10:
        raise ValueError("Номер телефона должен содержать не менее 10 цифр.")

# ========================= Views ========================= #
class MainView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("CRUD Soiskateli")
        self.geometry("1000x500")

        self.filter_frame = tk.Frame(self)
        self.filter_frame.pack(fill=tk.X, pady=5)

        tk.Label(self.filter_frame, text="Фильтр (Фамилия):").pack(side=tk.LEFT, padx=5)
        self.filter_entry = tk.Entry(self.filter_frame)
        self.filter_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(self.filter_frame, text="Применить", command=self.controller.apply_filter).pack(side=tk.LEFT)
        tk.Button(self.filter_frame, text="Сбросить", command=self.controller.reset_filter).pack(side=tk.LEFT)

        self.sort_frame = tk.Frame(self)
        self.sort_frame.pack(fill=tk.X, pady=5)

        tk.Label(self.sort_frame, text="Сортировать по:").pack(side=tk.LEFT, padx=5)
        self.sort_field = ttk.Combobox(self.sort_frame, values=["fam", "imya", "kvalifikaciya", "professiya"])
        self.sort_field.pack(side=tk.LEFT, padx=5)
        tk.Button(self.sort_frame, text="Сортировать", command=self.controller.apply_sort).pack(side=tk.LEFT)

        self.table = ttk.Treeview(self, columns=("id", "fam", "imya", "otchestvo", "kvalifikaciya", "professiya", "data_rozhdeniya", "telefon", "adres"), show="headings")
        for col in self.table['columns']:
            self.table.heading(col, text=col)
        self.table.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="Добавить", command=self.controller.add_record).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Редактировать", command=self.controller.edit_record).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Удалить", command=self.controller.delete_record).pack(side=tk.LEFT)

    def update_table(self, records):
        for row in self.table.get_children():
            self.table.delete(row)
        for rec in records:
            self.table.insert("", tk.END, values=(rec.id, rec.fam, rec.imya, rec.otchestvo, rec.kvalifikaciya, rec.professiya, rec.data_rozhdeniya, rec.telefon, rec.adres))

class RecordView(tk.Toplevel):
    def __init__(self, controller, soiskatel=None):
        super().__init__()
        self.controller = controller
        self.soiskatel = soiskatel
        self.title("Редактировать запись" if soiskatel else "Добавить запись")

        self.entries = {}
        fields = ["fam", "imya", "otchestvo", "kvalifikaciya", "professiya", "data_rozhdeniya", "telefon", "adres"]

        for idx, field in enumerate(fields):
            tk.Label(self, text=field).grid(row=idx, column=0, sticky=tk.W)
            entry = tk.Entry(self)
            entry.grid(row=idx, column=1, sticky=tk.EW)
            self.entries[field] = entry

        if soiskatel:
            for field in fields:
                self.entries[field].insert(0, getattr(soiskatel, field))

        tk.Button(self, text="Сохранить", command=self.save).grid(row=len(fields), column=0, columnspan=2)

    def save(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        try:
            validate_soiskatel(data)
            self.controller.save_record(data, self.soiskatel)
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

# ========================= Controllers ========================= #
class MainController:
    def __init__(self):
        self.repo = Repository()
        self.repo.add_observer(self.refresh_view)
        self.view = MainView(self)
        self.refresh_view()

    def run(self):
        self.view.mainloop()

    def refresh_view(self):
        records = self.repo.read_all()
        self.view.update_table(records)

    def apply_filter(self):
        fam = self.view.filter_entry.get()
        if fam:
            records = self.repo.filter_by_fam(fam)
            self.view.update_table(records)

    def reset_filter(self):
        self.refresh_view()

    def apply_sort(self):
        field = self.view.sort_field.get()
        if field:
            records = self.repo.sort_by_field(field)
            self.view.update_table(records)

    def add_record(self):
        RecordController(self, self.repo).open_window()

    def edit_record(self):
        selected = self.view.table.selection()
        if selected:
            record_id = self.view.table.item(selected[0], "values")[0]
            soiskatel = next((r for r in self.repo.read_all() if r.id == int(record_id)), None)
            if soiskatel:
                RecordController(self, self.repo, soiskatel).open_window()

    def delete_record(self):
        selected = self.view.table.selection()
        if selected:
            record_id = self.view.table.item(selected[0], "values")[0]
            if messagebox.askyesno("Подтверждение", "Удалить запись?"):
                self.repo.delete(int(record_id))

class RecordController:
    def __init__(self, parent_controller, repo, soiskatel=None):
        self.parent_controller = parent_controller
        self.repo = repo
        self.soiskatel = soiskatel

    def open_window(self):
        RecordView(self, self.soiskatel)

    def save_record(self, data, soiskatel):
        if soiskatel:
            soiskatel.fam = data['fam']
            soiskatel.imya = data['imya']
            soiskatel.otchestvo = data['otchestvo']
            soiskatel.kvalifikaciya = data['kvalifikaciya']
            soiskatel.professiya = data['professiya']
            soiskatel.data_rozhdeniya = data['data_rozhdeniya']
            soiskatel.telefon = data['telefon']
            soiskatel.adres = data['adres']
            self.repo.update(soiskatel)
        else:
            new_soiskatel = Soiskatel(None, data['fam'], data['imya'], data['otchestvo'], data['kvalifikaciya'],
                                      data['professiya'], data['data_rozhdeniya'], data['telefon'], data['adres'])
            self.repo.add(new_soiskatel)

# ========================= Run Application ========================= #
if __name__ == "__main__":
    app = MainController()
    app.run()
