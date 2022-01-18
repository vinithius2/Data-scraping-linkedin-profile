import os
import sqlite3
import sys
from pathlib import Path
from sqlite3 import OperationalError

import keyring
from cryptography.fernet import Fernet

from config import DEBUG
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
        self.__generate_credentials()
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

    def resource_path(self, relative_path):
        """ Obtenha o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath("__file__")))
        return os.path.join(base_path, relative_path)

    def cryptography(self):
        """
        Efetua a criptografia do arquivo SQLite.
        """
        if not DEBUG:
            if self.__is_sqlite_file():
                path_database = os.path.join(self.path, 'database.db')
                fernet = Fernet(self.__get_credentials())
                with open(path_database, 'rb') as file:
                    original = file.read()
                    encrypted = fernet.encrypt(original)
                with open(path_database, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted)

    def decryption(self):
        """
        Desfaz a criptografia do arquivo SQLite.
        """
        if not DEBUG:
            if not self.__is_sqlite_file():
                path_database = os.path.join(self.path, 'database.db')
                fernet = Fernet(self.__get_credentials())
                with open(path_database, 'rb') as file:
                    encrypted = file.read()
                    original = fernet.decrypt(encrypted)
                with open(path_database, 'wb') as dec_file:
                    dec_file.write(original)

    def __is_sqlite_file(self):
        """
        Verifica se o arquivo SQLite está criptografado ou não.
        """
        path_database = os.path.join(self.path, 'database.db')
        with open(path_database, 'rb') as file:
            size = os.path.getsize(file.name)
            if size > 0:
                original = file.read()
                if "SQLite" in str(original):
                    return True
                else:
                    return False
            else:
                return True

    def __get_secret_user(self):
        secret_username = None
        try:
            with open(self.resource_path("secret_username.key"), 'rb') as file:
                secret_username = file.read().decode('utf-8')
        except FileNotFoundError as e:
            log_erro(e)
        return secret_username

    def __generate_credentials(self):
        """
        Gera a chave aleatória de criptografia.
        """
        secret_username = self.__get_secret_user()
        if secret_username and not keyring.get_password("database", secret_username):
            key = Fernet.generate_key()
            keyring.set_password("database", secret_username, key.decode('utf-8'))

    def __get_credentials(self):
        """
        Retorna a chave de criptografia.
        """
        secret_username = self.__get_secret_user()
        return keyring.get_password("database", secret_username)

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
        self.decryption()
        query = """PRAGMA user_version"""
        self.cursor_db.execute(query)
        user_version = self.cursor_db.fetchone()
        self.cryptography()
        return user_version[0]

    def __set_user_version(self):
        """
        Atualiza a versão do banco
        """
        self.decryption()
        self.cursor_db.execute(f"PRAGMA user_version = {self.new_version}")
        self.connection.commit()
        self.cryptography()

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
        self.decryption()
        self.__migrations()
        self.cryptography()
