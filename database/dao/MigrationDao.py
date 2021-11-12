from sqlite3 import IntegrityError

from models.Migration import Migration
from utils.log_erro import log_erro


class MigrationDao:
    def __init__(self, database, migration=None):
        self.migration = migration
        self.database = database

    def insert(self):
        try:
            self.database.decryption()
            query = """INSERT INTO migration (name_file, user_version, datetime) VALUES (?,?,datetime('now'))"""
            self.database.cursor_db.execute(query, [self.migration.name_file, self.migration.user_version])
            migration_id = self.database.cursor_db.lastrowid
            self.database.connection.commit()
            self.database.cryptography()
            return migration_id
        except IntegrityError as e:
            log_erro(e)
            return None

    def select_by_name(self, name_file):
        self.database.decryption()
        migration = None
        query = """SELECT id, name_file, user_version, datetime FROM migration WHERE name_file = ?"""
        self.database.cursor_db.execute(query, [name_file])
        row = self.database.cursor_db.fetchone()
        if row:
            migration = Migration(
                name_file=row[1],
                user_version=row[2],
                datetime=row[3]
            )
        self.database.cryptography()
        return migration

    def select(self):
        self.database.decryption()
        migration_list = list()
        query = """SELECT id, name_file, user_version, datetime FROM migration ORDER BY user_version DESC"""
        self.database.cursor_db.execute(query)
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            migration_list.append(Migration(
                    name_file=row[1],
                    user_version=row[2],
                    datetime=row[3]
                )
            )
        self.database.cryptography()
        return migration_list
