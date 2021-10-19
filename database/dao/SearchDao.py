from models.Search import Search


class SearchDao:
    def __init__(self, database, search=None):
        self.search = search
        self.database = database

    def insert_search(self, person_id=None):
        if person_id:
            query = """INSERT INTO search (url, person_id, datetime) VALUES (?,?,datetime('now'))"""
            self.database.cursor_db.execute(query, [self.search.url, person_id])
        else:
            query = """INSERT INTO search (url, datetime) VALUES (?,datetime('now'))"""
            self.database.cursor_db.execute(query, [self.search.url])
        search_id = self.database.cursor_db.lastrowid
        self.database.connection.commit()
        return search_id

    def update_search(self, person_id, url):
        query = """UPDATE search SET person_id = ? WHERE url = ?;"""
        self.database.cursor_db.execute(query, [person_id, url])
        self.database.connection.commit()

    def select_search(self):
        search_list = list()
        query = """
            SELECT id, url, person_id, datetime FROM search WHERE person_id IS NULL
        """
        self.database.cursor_db.execute(query)
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            search_list.append(Search(
                    url=row[1],
                    person_id=row[2],
                    date=row[3]
                )
            )
        return search_list
