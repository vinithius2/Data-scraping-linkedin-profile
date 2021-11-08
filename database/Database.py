import os
import sqlite3
from pathlib import Path


class Database:
    def __init__(self):
        self.path = self.__create_directory()
        self.connection = sqlite3.connect(os.path.join(self.path, 'database.db'))
        self.cursor_db = self.connection.cursor()

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __create_directory(self):
        path_parent = "scrapingLinkedinProfiles"
        path_absolute = Path("/")
        directory_main = os.path.join(path_absolute.parent.absolute(), path_parent)
        if not os.path.exists(directory_main):
            os.mkdir(directory_main)
        directory_database = self.__create_directory_database(path_absolute, directory_main)
        return directory_database

    def __create_directory_database(self, path_absolute, directory_main):
        path_parent_database = os.path.join(directory_main, "database")
        directory_database = os.path.join(path_absolute.parent.absolute(), path_parent_database)
        if not os.path.exists(directory_database):
            os.mkdir(directory_database)
        return directory_database

    def create_tables_if_not_exists(self):
        self.__create_table_person()
        self.__create_table_experience()
        self.__create_table_certification()
        self.__create_table_education()
        self.__create_table_language()
        self.__create_table_skill()
        self.__create_table_search()

    def __create_table_person(self):
        query = """CREATE TABLE IF NOT EXISTS person (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, subtitle TEXT, 
        local TEXT, url TEXT, email TEXT, phone_number TEXT, about TEXT, UNIQUE(url))"""
        self.cursor_db.execute(query)

    def __create_table_experience(self):
        query = """CREATE TABLE IF NOT EXISTS experience (id INTEGER PRIMARY KEY AUTOINCREMENT, company TEXT, 
        position TEXT, years NUMBER, months NUMBER, description TEXT, person_id INTEGER, FOREIGN KEY(person_id) REFERENCES 
        person(id)) """
        self.cursor_db.execute(query)

    def __create_table_education(self):
        query = """CREATE TABLE IF NOT EXISTS education (id INTEGER PRIMARY KEY AUTOINCREMENT, college TEXT, 
        level TEXT, course TEXT, person_id INTEGER, FOREIGN KEY(person_id) REFERENCES person(id))"""
        self.cursor_db.execute(query)

    def __create_table_certification(self):
        query = """CREATE TABLE IF NOT EXISTS certification (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT,
        person_id INTEGER, FOREIGN KEY(person_id) REFERENCES person(id))"""
        self.cursor_db.execute(query)

    def __create_table_language(self):
        query = """CREATE TABLE IF NOT EXISTS language (id INTEGER PRIMARY KEY AUTOINCREMENT, language TEXT, level TEXT, 
        person_id INTEGER, FOREIGN KEY(person_id) REFERENCES person(id))"""
        self.cursor_db.execute(query)

    def __create_table_skill(self):
        query = """CREATE TABLE IF NOT EXISTS skill (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, 
        indications NUMBER, verify INTEGER, person_id INTEGER, FOREIGN KEY(person_id) REFERENCES person(id))"""
        self.cursor_db.execute(query)

    def __create_table_search(self):
        query = """CREATE TABLE IF NOT EXISTS search (id INTEGER PRIMARY KEY AUTOINCREMENT, url_filter TEXT, 
        url_profile TEXT, datetime TEXT, person_id INTEGER, text_filter TEXT, FOREIGN KEY(person_id) REFERENCES person(id),
        UNIQUE(url_filter, url_profile))"""
        self.cursor_db.execute(query)
