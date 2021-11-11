import os
import sqlite3
from pathlib import Path
from sqlite3 import OperationalError

from database.dao.MigrationDao import MigrationDao
from database.migrations.migration_0 import migration_0
from models.Migration import Migration
from utils.log_erro import log_erro


class Database:
    def __init__(self):
        self.path = self.__create_directory()
        self.connection = sqlite3.connect(os.path.join(self.path, 'database.db'))
        self.cursor_db = self.connection.cursor()
        self.new_version = 1
        self.old_version = self.__get_user_version()
        self.list_migration = [
            migration_0
        ]

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __create_directory(self):
        """
        Cria diretório absoluto se não existir.
        """
        path_parent = "scrapingLinkedinProfiles"
        path_absolute = Path("/")
        directory_main = os.path.join(path_absolute.parent.absolute(), path_parent)
        if not os.path.exists(directory_main):
            os.mkdir(directory_main)
        directory_database = self.__create_directory_database(path_absolute, directory_main)
        return directory_database

    def __create_directory_database(self, path_absolute, directory_main):
        """
        Cria diretório do banco de dados se não existir.
        """
        path_parent_database = os.path.join(directory_main, "database")
        directory_database = os.path.join(path_absolute.parent.absolute(), path_parent_database)
        if not os.path.exists(directory_database):
            os.mkdir(directory_database)
        return directory_database

    def __get_user_version(self):
        """
        Pega a versão do banco
        """
        query = """PRAGMA user_version"""
        self.cursor_db.execute(query)
        user_version = self.cursor_db.fetchone()
        return user_version[0]

    def __set_user_version(self):
        """
        Atualiza a versão do banco
        """
        self.cursor_db.execute(f"PRAGMA user_version = {self.new_version}")
        self.connection.commit()

    def __migrations(self):
        """
        Executa as migrations.
        """
        if self.new_version > self.old_version:
            try:
                for migration in self.list_migration:
                    result = MigrationDao(self).select_by_name(migration.__name__)
                    if not result:
                        migration(self.cursor_db).start()
                        migration = Migration(migration.__name__, self.new_version)
                        MigrationDao(self, migration).insert()
                self.__set_user_version()
            except OperationalError as e:
                log_erro(e)
                if e.args[0] == 'no such table: migration':
                    migration_0(self.cursor_db).start()
                    migration = Migration(migration_0.__name__, self.new_version)
                    MigrationDao(self, migration).insert()
                    self.__migrations()

    def verify_migrations(self):
        """
        Inicia validação de migrations
        """
        self.__migrations()
