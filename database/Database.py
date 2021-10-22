import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor_db = self.connection.cursor()

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def create_tables_if_not_exists(self):
        self.create_table_person()
        self.create_table_experience()
        self.create_table_certification()
        self.create_table_language()
        self.create_table_skill()
        self.create_table_search()

    def create_table_person(self):
        query = """CREATE TABLE IF NOT EXISTS person (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, subtitle TEXT, 
        local TEXT, url TEXT, email TEXT, phone_number TEXT, about TEXT)"""
        self.cursor_db.execute(query)

    def create_table_experience(self):
        query = """CREATE TABLE IF NOT EXISTS experience (id INTEGER PRIMARY KEY AUTOINCREMENT, empresa TEXT, 
        cargo TEXT, anos NUMBER, meses NUMBER, descricao TEXT, person_id INTEGER, FOREIGN KEY(person_id) REFERENCES 
        person(id)) """
        self.cursor_db.execute(query)

    def create_table_certification(self):
        query = """CREATE TABLE IF NOT EXISTS certification (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT,
        person_id INTEGER, FOREIGN KEY(person_id) REFERENCES person(id))"""
        self.cursor_db.execute(query)

    def create_table_language(self):
        query = """CREATE TABLE IF NOT EXISTS language (id INTEGER PRIMARY KEY AUTOINCREMENT, idioma TEXT, nivel TEXT, 
        person_id INTEGER, FOREIGN KEY(person_id) REFERENCES person(id))"""
        self.cursor_db.execute(query)

    def create_table_skill(self):
        query = """CREATE TABLE IF NOT EXISTS skill (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, 
        indications NUMBER, verify INTEGER, person_id INTEGER, FOREIGN KEY(person_id) REFERENCES person(id))"""
        self.cursor_db.execute(query)

    def create_table_search(self):
        query = """CREATE TABLE IF NOT EXISTS search (id INTEGER PRIMARY KEY AUTOINCREMENT, url_filter TEXT, 
        url_profile TEXT, datetime TEXT, person_id INTEGER, score REAL, FOREIGN KEY(person_id) REFERENCES person(id))"""
        self.cursor_db.execute(query)

