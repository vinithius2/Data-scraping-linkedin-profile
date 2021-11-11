class migration_0:
    def __init__(self, cursor_db):
        self.cursor_db = cursor_db
        self.operations_sql = [
            self.__create_table_person,
            self.__create_table_experience,
            self.__create_table_certification,
            self.__create_table_education,
            self.__create_table_language,
            self.__create_table_skill,
            self.__create_table_search,
            self.__create_table_migration
        ]

    def start(self):
        for operation in self.operations_sql:
            self.cursor_db.execute(operation.__call__())

    @staticmethod
    def __create_table_person():
        query = """CREATE TABLE IF NOT EXISTS person (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, subtitle TEXT, 
        local TEXT, url TEXT, email TEXT, phone_number TEXT, about TEXT, UNIQUE(url))"""
        return query

    @staticmethod
    def __create_table_experience():
        query = """CREATE TABLE IF NOT EXISTS experience (id INTEGER PRIMARY KEY AUTOINCREMENT, company TEXT, 
        position TEXT, years NUMBER, months NUMBER, description TEXT, person_id INTEGER, FOREIGN KEY(person_id) REFERENCES 
        person(id)) """
        return query

    @staticmethod
    def __create_table_education():
        query = """CREATE TABLE IF NOT EXISTS education (id INTEGER PRIMARY KEY AUTOINCREMENT, college TEXT, 
        level TEXT, course TEXT, person_id INTEGER, FOREIGN KEY(person_id) REFERENCES person(id))"""
        return query

    @staticmethod
    def __create_table_certification():
        query = """CREATE TABLE IF NOT EXISTS certification (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT,
        person_id INTEGER, FOREIGN KEY(person_id) REFERENCES person(id))"""
        return query

    @staticmethod
    def __create_table_language():
        query = """CREATE TABLE IF NOT EXISTS language (id INTEGER PRIMARY KEY AUTOINCREMENT, language TEXT, level TEXT, 
        person_id INTEGER, FOREIGN KEY(person_id) REFERENCES person(id))"""
        return query

    @staticmethod
    def __create_table_skill():
        query = """CREATE TABLE IF NOT EXISTS skill (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, 
        indications NUMBER, verify INTEGER, person_id INTEGER, FOREIGN KEY(person_id) REFERENCES person(id))"""
        return query

    @staticmethod
    def __create_table_search():
        query = """CREATE TABLE IF NOT EXISTS search (id INTEGER PRIMARY KEY AUTOINCREMENT, url_filter TEXT, 
        url_profile TEXT, datetime TEXT, person_id INTEGER, text_filter TEXT, FOREIGN KEY(person_id) REFERENCES person(id),
        UNIQUE(url_filter, url_profile))"""
        return query

    @staticmethod
    def __create_table_migration():
        query = """CREATE TABLE IF NOT EXISTS migration (id INTEGER PRIMARY KEY AUTOINCREMENT, name_file TEXT, 
        user_version INTEGER, datetime, UNIQUE(name_file))"""
        return query
