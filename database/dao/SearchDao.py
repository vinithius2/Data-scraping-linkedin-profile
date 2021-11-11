from sqlite3 import IntegrityError

from models.Search import Search
from utils.log_erro import log_erro


class SearchDao:
    def __init__(self, database, search=None):
        self.search = search
        self.database = database

    def insert_search(self, person_id=None):
        try:
            self.database.decryption()
            if person_id:
                query = """INSERT INTO search (url_filter, url_profile, person_id, text_filter, datetime) VALUES (?,?,?,?,datetime('now'))
                """
                self.database.cursor_db.execute(query, [self.search.url_filter, self.search.url_profile,
                                                        self.search.text_filter, person_id])
            else:
                query = """INSERT INTO search (url_filter, url_profile, text_filter, datetime) VALUES (?,?,?,datetime('now'))"""
                self.database.cursor_db.execute(query, [self.search.url_filter, self.search.url_profile,
                                                        self.search.text_filter])
            search_id = self.database.cursor_db.lastrowid
            self.database.connection.commit()
            self.database.cryptography()
            return search_id
        except IntegrityError as e:
            log_erro(e)
            return None

    def update_search_person_id(self, person_id, id_search):
        self.database.decryption()
        query = """UPDATE search SET person_id = ? WHERE id = ?;"""
        self.database.cursor_db.execute(query, [person_id, id_search])
        self.database.connection.commit()
        self.database.cryptography()

    def select_search_person_id_is_null(self):
        self.database.decryption()
        search_list = list()
        query = """
            SELECT id, url_filter, url_profile, text_filter, person_id, datetime FROM search WHERE person_id IS NULL
        """
        self.database.cursor_db.execute(query)
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            search_list.append(Search(
                    id_search=row[0],
                    url_filter=row[1],
                    url_profile=row[2],
                    text_filter=row[3],
                    person_id=row[4],
                    datetime=row[5]
                )
            )
        self.database.cryptography()
        return search_list

    def select_search_person_id_is_not_null(self):
        self.database.decryption()
        search_list = list()
        query = """
            SELECT id, url_filter, url_profile, text_filter, person_id, datetime FROM search WHERE person_id IS NOT NULL GROUP BY url_profile
        """
        self.database.cursor_db.execute(query)
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            search_list.append(Search(
                    id_search=row[0],
                    url_filter=row[1],
                    url_profile=row[2],
                    text_filter=row[3],
                    person_id=row[4],
                    datetime=row[5]
                )
            )
        self.database.cryptography()
        return search_list

    def select_search_by_person_id(self, person_id):
        self.database.decryption()
        search_list = list()
        query = """
            SELECT id, url_filter, url_profile, text_filter, person_id, datetime FROM search WHERE person_id = ?
        """
        self.database.cursor_db.execute(query, [person_id])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            search_list.append(Search(
                    id_search=row[0],
                    url_filter=row[1],
                    url_profile=row[2],
                    text_filter=row[3],
                    person_id=row[4],
                    datetime=row[5]
                )
            )
        self.database.cryptography()
        return search_list
    
    def select_search_by_url_filter(self, url_filter):
        self.database.decryption()
        search_list = list()
        query = """
            SELECT id, url_filter, url_profile, text_filter, person_id, datetime FROM search WHERE url_filter = ? AND 
            person_id IS NOT NULL GROUP BY url_profile
        """
        self.database.cursor_db.execute(query, [url_filter])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            search_list.append(Search(
                    id_search=row[0],
                    url_filter=row[1],
                    url_profile=row[2],
                    text_filter=row[3],
                    person_id=row[4],
                    datetime=row[5]
                )
            )
        self.database.cryptography()
        return search_list

    def select_search_person_by_url_profile(self, url_profile):
        self.database.decryption()
        search_list = list()
        query = """
            SELECT id, url_filter, url_profile, text_filter, person_id, datetime FROM search WHERE url_profile = ? AND 
            person_id IS NOT NULL
        """
        self.database.cursor_db.execute(query, [url_profile])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            search_list.append(Search(
                    id_search=row[0],
                    url_filter=row[1],
                    url_profile=row[2],
                    text_filter=row[3],
                    person_id=row[4],
                    datetime=row[5]
                )
            )
        self.database.cryptography()
        return search_list

    def select_search_person_group_by_url_filter(self, limit=5):
        self.database.decryption()
        search_list = list()
        query = """
            SELECT id, url_filter, url_profile, text_filter, person_id, datetime FROM search GROUP BY url_filter ORDER BY datetime LIMIT ?
        """
        self.database.cursor_db.execute(query, [limit])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            search_list.append(Search(
                    id_search=row[0],
                    url_filter=row[1],
                    url_profile=row[2],
                    text_filter=row[3],
                    person_id=row[4],
                    datetime=row[5]
                )
            )
        self.database.cryptography()
        return search_list

    def search_counter(self) -> int:
        self.database.decryption()
        query = """
            SELECT COUNT(*) AS counter FROM search
        """
        self.database.cursor_db.execute(query)
        rows = self.database.cursor_db.fetchone()
        self.database.cryptography()
        return rows[0]

    def search_counter_is_not_null(self) -> int:
        self.database.decryption()
        query = """
            SELECT COUNT(*) AS counter FROM search WHERE person_id IS NOT NULL
        """
        self.database.cursor_db.execute(query)
        rows = self.database.cursor_db.fetchone()
        self.database.cryptography()
        return rows[0]

    def search_counter_by_url_filter(self, url_filter) -> int:
        self.database.decryption()
        query = """
            SELECT COUNT(*) AS counter FROM search WHERE url_filter = ? AND person_id IS NOT NULL
        """
        self.database.cursor_db.execute(query, [url_filter])
        rows = self.database.cursor_db.fetchone()
        self.database.cryptography()
        return rows[0]
