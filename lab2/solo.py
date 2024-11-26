class DBConnection:
    _instance = None

    def __new__(cls, db_config):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = psycopg2.connect(**db_config)
        return cls._instance

# Пример использования:
db_config = {
    'dbname': 'test',
    'user': 'user',
    'password': 'password',
    'host': 'localhost'
}

db_connection = DBConnection(db_config)
