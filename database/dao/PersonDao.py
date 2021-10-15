from models.Certification import Certification
from models.Experience import Experience
from models.Language import Language
from models.Person import Person
from models.Skill import Skill


class PersonDao:
    def __init__(self, person, database):
        self.person = person
        self.database = database

    # ------ INSERT ------ #

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
        query = """INSERT INTO person (name, subtitle, local, about, url, email, phone_number)  
        VALUES (?,?,?,?,?,?,?)"""
        self.database.cursor_db.execute(query, [person.name, person.subtitle, person.local, person.about,
                                                None, None, None])
        # TODO: Pegar dados de URL, EMAIL e TELEFONE
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

    # ------ SELECT ------ #

    def select_all_people(self):
        person_list = list()
        query = """
            SELECT id, name, subtitle, local, about, url, email, phone_number FROM person
        """
        self.database.cursor_db.execute(query)
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            certification_list = self.__select_certification(row[0])
            language_list = self.__select_language(row[0])
            skill_list = self.__select_skill(row[0])
            experience_list = self.__select_experience(row[0])
            person_list.append(Person(
                name=row[1],
                subtitle=row[2],
                local=row[3],
                about=row[4],
                url=row[5],
                email=row[6],
                phone_number=row[7],
                experiences=experience_list,
                languages=language_list,
                skills=skill_list,
                certifications=certification_list
                )
            )
        return person_list

    def __select_certification(self, person_id):
        certification_list = list()
        query = """
            SELECT id, titulo, person_id FROM certification WHERE ? = person_id 
        """
        self.database.cursor_db.execute(query, [person_id])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            certification_list.append(Certification(titulo=row[1]))
        return certification_list

    def __select_language(self, person_id):
        language_list = list()
        query = """
            SELECT id, idioma, nivel, person_id FROM language WHERE ? = person_id 
        """
        self.database.cursor_db.execute(query, [person_id])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            language_list.append(Language(idioma=row[1], nivel=row[2]))
        return language_list

    def __select_skill(self, person_id):
        skill_list = list()
        query = """
            SELECT id, titulo, indications, verify, person_id person_id FROM skill WHERE ? = person_id 
        """
        self.database.cursor_db.execute(query, [person_id])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            verify = True if row[3] == 1 else False
            skill_list.append(Skill(titulo=row[1], indications=row[2], verify=verify))
        return skill_list

    def __select_experience(self, person_id):
        experience_list = list()
        query = """
            SELECT id, cargo, anos, meses, descricao, person_id FROM experience WHERE ? = person_id 
        """
        self.database.cursor_db.execute(query, [person_id])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            experience_list.append(Experience(cargo=row[1], anos=row[2], meses=row[3], descricao=row[4]))
        return experience_list
