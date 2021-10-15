class PersonDao:
    def __init__(self, person, database):
        self.person = person
        self.database = database

    def insert(self):
        person_id = self.__insert_person(self.person)
        for certification in self.person.certifications:
            self.__insert_certification(certification, person_id)
        for language in self.person.languages:
            self.__insert_language(language, person_id)
        for skill in self.person.skills:
            self.__insert_skill(skill, person_id)
        for experience_list in self.person.experiences:
            for experience in experience_list:
                self.__insert_experience(experience, person_id)

    def __insert_person(self, person):
        query = """INSERT INTO person (name, subtitle, local, about)  VALUES (?,?,?,?)"""
        self.database.cursor_db.execute(query, [person.name, person.subtitle, person.local, person.about])
        person_id = self.database.cursor_db.lastrowid
        self.database.connection.commit()
        return person_id

    def __insert_certification(self, certification, person_id):
        query = """INSERT INTO certification (titulo, person_id)  VALUES (?,?)"""
        self.database.cursor_db.execute(query, [certification.titulo, person_id])
        self.database.connection.commit()

    def __insert_language(self, language, person_id):
        query = """INSERT INTO language (idioma, nivel, person_id)  VALUES (?,?,?)"""
        self.database.cursor_db.execute(query, [language.idioma, language.nivel, person_id])
        self.database.connection.commit()

    def __insert_skill(self, skill, person_id):
        query = """INSERT INTO skill (titulo, indications, verify, person_id)  VALUES (?,?,?,?)"""
        self.database.cursor_db.execute(query, [skill.titulo, skill.indications, skill.verify, person_id])
        self.database.connection.commit()

    def __insert_experience(self, experience, person_id):
        query = """INSERT INTO experience (cargo, anos, meses, descricao, person_id)  VALUES (?,?,?,?,?)"""
        self.database.cursor_db.execute(query, [experience.cargo, experience.anos, experience.meses,
                                                experience.descricao, person_id])
        self.database.connection.commit()

    def select_all_people(self):
        pass
