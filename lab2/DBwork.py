import psycopg2

class Soiskatel_rep_DB:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_connection(self):
        return psycopg2.connect(**self.db_config)

    def get_by_id(self, id):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM soiskatel WHERE id = %s", (id,))
                return cursor.fetchone()

    def get_k_n_short_list(self, k, n):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM soiskatel LIMIT %s OFFSET %s", (n, k*n))
                return cursor.fetchall()

    def add(self, new_item):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO soiskatel (fam, imya, otchestvo) VALUES (%s, %s, %s) RETURNING id",
                               (new_item['fam'], new_item['imya'], new_item['otchestvo']))
                return cursor.fetchone()[0]

    def replace_by_id(self, id, updated_item):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE soiskatel SET fam = %s, imya = %s, otchestvo = %s WHERE id = %s",
                               (updated_item['fam'], updated_item['imya'], updated_item['otchestvo'], id))

    def delete_by_id(self, id):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM soiskatel WHERE id = %s", (id,))

    def get_count(self):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM soiskatel")
                return cursor.fetchone()[0]
