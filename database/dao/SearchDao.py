from models.Search import Search


class SearchDao:
    def __init__(self, database, search=None):
        self.search = search
        self.database = database

    def insert_search(self, person_id=None):
        if person_id:
            query = """INSERT INTO search (url_filter, url_profile, person_id, datetime) VALUES (?,?,?,datetime('now'))
            """
            self.database.cursor_db.execute(query, [self.search.url_filter, self.search.url_profile, person_id])
        else:
            query = """INSERT INTO search (url_filter, url_profile, datetime) VALUES (?,?,datetime('now'))"""
            self.database.cursor_db.execute(query, [self.search.url_filter, self.search.url_profile])
        search_id = self.database.cursor_db.lastrowid
        self.database.connection.commit()
        return search_id

    def update_search_person_id(self, person_id, url_profile):
        query = """UPDATE search SET person_id = ? WHERE url_profile = ?;"""
        self.database.cursor_db.execute(query, [person_id, url_profile])
        self.database.connection.commit()

    def select_search_person_id_is_null(self):
        search_list = list()
        query = """
            SELECT id, url_filter, url_profile, text_filter, person_id, datetime FROM search WHERE person_id IS NULL
        """
        self.database.cursor_db.execute(query)
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            search_list.append(Search(
                    url_filter=row[1],
                    url_profile=row[2],
                    text_filter=row[3],
                    person_id=row[4],
                    datetime=row[5]
                )
            )
        return search_list

    def select_search_person_id_is_not_null(self):
        search_list = list()
        query = """
            SELECT id, url_filter, url_profile, text_filter, person_id, datetime FROM search WHERE person_id IS NOT NULL
        """
        self.database.cursor_db.execute(query)
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            search_list.append(Search(
                    url_filter=row[1],
                    url_profile=row[2],
                    text_filter=row[3],
                    person_id=row[4],
                    datetime=row[5]
                )
            )
        return search_list

    def select_search_by_person_id(self, person_id):
        search_list = list()
        query = """
            SELECT id, url_filter, url_profile, text_filter, person_id, datetime FROM search WHERE person_id = ?
        """
        self.database.cursor_db.execute(query, [person_id])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            search_list.append(Search(
                    url_filter=row[1],
                    url_profile=row[2],
                    text_filter=row[3],
                    person_id=row[4],
                    datetime=row[5]
                )
            )
        return search_list
    
    def select_search_by_url_filter(self, url_filter):
        search_list = list()
        query = """
            SELECT id, url_filter, url_profile, text_filter, person_id, datetime FROM search WHERE url_filter = ?
        """
        self.database.cursor_db.execute(query, [url_filter])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            search_list.append(Search(
                    url_filter=row[1],
                    url_profile=row[2],
                    text_filter=row[3],
                    person_id=row[4],
                    datetime=row[5]
                )
            )
        return search_list

    def select_search_person_group_by_url_filter(self, limit=5):
        search_list = list()
        query = """
            SELECT id, url_filter, url_profile, text_filter, person_id, datetime FROM search GROUP BY url_filter ORDER BY datetime LIMIT ?
        """
        self.database.cursor_db.execute(query, [limit])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            search_list.append(Search(
                    url_filter=row[1],
                    url_profile=row[2],
                    text_filter=row[3],
                    person_id=row[4],
                    datetime=row[5]
                )
            )
        return search_list

    def search_counter(self) -> int:
        query = """
            SELECT COUNT(*) AS counter FROM search
        """
        self.database.cursor_db.execute(query)
        rows = self.database.cursor_db.fetchall()
        return rows[0][0]
