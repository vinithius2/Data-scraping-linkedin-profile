import itertools

from models.Certification import Certification
from models.Education import Education
from models.Experience import Experience
from models.Language import Language
from models.Person import Person
from models.Skill import Skill
from utils.bcolors import bcolors


class PersonDao:
    def __init__(self, database, person=None):
        self.person = person
        self.database = database
        self.person_id = None

    # ------ INSERT ------ #
    def insert(self):
        person_list = self.select_people_by_name()
        exist = self.person_exist(person_list)
        if not exist:
            self.__insert()
        else:
            print(f"{bcolors.WARNING}Perfil {self.person.name} JÁ EXISTE registro: {self.person.url}{bcolors.ENDC}")
        return self.person_id

    def person_exist(self, person_list):
        exist = False
        for person in person_list:
            if person.url == self.person.url:
                exist = True
        return exist

    def __insert(self):
        self.person_id = self.__insert_person(self.person)
        for certification in self.person.certifications:
            self.__insert_certification(certification, self.person_id)
        for education in self.person.education:
            self.__insert_education(education, self.person_id)
        for language in self.person.languages:
            self.__insert_language(language, self.person_id)
        for skill in self.person.skills:
            self.__insert_skill(skill, self.person_id)
        for experience_list in self.person.experiences:
            for experience in experience_list:
                self.__insert_experience(experience, self.person_id)

    def __insert_person(self, person):
        query = """INSERT INTO person (name, subtitle, local, about, url, email, phone_number)  
        VALUES (?,?,?,?,?,?,?)"""
        self.database.cursor_db.execute(query, [person.name, person.subtitle, person.local, person.about,
                                                person.url, person.email, person.phone_number])
        person_id = self.database.cursor_db.lastrowid
        self.database.connection.commit()
        return person_id

    def __insert_certification(self, certification, person_id):
        query = """INSERT INTO certification (titulo, person_id)  VALUES (?,?)"""
        self.database.cursor_db.execute(query, [certification.titulo, person_id])
        self.database.connection.commit()

    def __insert_education(self, education, person_id):
        query = """INSERT INTO education (college, level, course, person_id)  VALUES (?,?,?,?)"""
        self.database.cursor_db.execute(query, [education.college, education.level, education.course, person_id])
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
        query = """INSERT INTO experience (empresa, cargo, anos, meses, descricao, person_id)  VALUES (?,?,?,?,?,?)"""
        self.database.cursor_db.execute(query, [
                experience.empresa,
                experience.cargo,
                experience.anos,
                experience.meses,
                experience.descricao,
                person_id
            ]
        )
        self.database.connection.commit()

    # ------ SELECT ------ #
    def select_people(self):
        query = """
            SELECT id, name, subtitle, local, about, url, email, phone_number FROM person
        """
        self.database.cursor_db.execute(query)
        rows = self.database.cursor_db.fetchall()
        person_list = self.__get_list_person(rows)
        return person_list

    def select_people_by_name(self):
        query = """
            SELECT id, name, subtitle, local, about, url, email, phone_number FROM person WHERE name = ?
        """
        self.database.cursor_db.execute(query, [self.person.name])
        rows = self.database.cursor_db.fetchall()
        person_list = self.__get_list_person(rows)
        return person_list

    def select_people_by_id(self, person_id):
        query = """
            SELECT id, name, subtitle, local, about, url, email, phone_number FROM person WHERE id = ?
        """
        self.database.cursor_db.execute(query, [person_id])
        rows = self.database.cursor_db.fetchall()
        person = None
        if rows:
            person = self.__get_list_person(rows)[0]
        return person

    def select_people_by_list_ids(self, list_ids):
        query = """
            SELECT id, name, subtitle, local, about, url, email, phone_number FROM person WHERE id IN {}
        """
        self.database.cursor_db.execute(query.format(tuple(list_ids)))
        rows = self.database.cursor_db.fetchall()
        person_list = self.__get_list_person(rows)
        return person_list

    def __get_list_person(self, rows):
        person_list = list()
        for row in rows:
            certification_list = self.__select_certification(row[0])
            education_list = self.__select_education(row[0])
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
                certifications=certification_list,
                education=education_list
                )
            )
        return person_list

    def __select_education(self, person_id):
        education_list = list()
        query = """
            SELECT id, college, level, course, person_id FROM education WHERE ? = person_id 
        """
        self.database.cursor_db.execute(query, [person_id])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            education_list.append(Education(college=row[1], level=row[2], course=row[3]))
        return education_list

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
            SELECT id, empresa, cargo, anos, meses, descricao, person_id FROM experience WHERE ? = person_id 
        """
        self.database.cursor_db.execute(query, [person_id])
        rows = self.database.cursor_db.fetchall()
        for key, group in itertools.groupby(rows, key=lambda r: r[1]):
            experience_group = list()
            for row in group:
                experience_group.append(
                    Experience(
                        empresa=row[1],
                        cargo=row[2],
                        anos=row[3],
                        meses=row[4],
                        descricao=row[5]
                    )
                )
            experience_list.append(experience_group)
        return experience_list
