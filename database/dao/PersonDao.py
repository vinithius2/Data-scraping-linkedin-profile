import itertools

from sqlite3 import IntegrityError

from models.Certification import Certification
from models.Education import Education
from models.Experience import Experience
from models.Language import Language
from models.Person import Person
from models.Skill import Skill
from utils.bcolors import bcolors
from utils.log_erro import log_erro
from utils.texts import text_already_exists_record


class PersonDao:
    def __init__(self, database, person=None):
        self.person = person
        self.database = database
        self.person_id = None

    def person_counter(self) -> int:
        self.database.decryption()
        query = """
            SELECT COUNT(*) AS counter FROM person
        """
        self.database.cursor_db.execute(query)
        rows = self.database.cursor_db.fetchone()
        self.database.cryptography()
        return rows[0]

    # ------ INSERT ------ #
    def insert(self):
        person_list = self.select_people_by_name()
        exist = self.__person_exist(person_list)
        if not exist:
            self.__insert()
        else:
            print(text_already_exists_record.format(bcolors.WARNING, self.person.name, self.person.url, bcolors.ENDC))
        return self.person_id

    def __person_exist(self, person_list):
        exist = False
        for person in person_list:
            if person.url == self.person.url:
                exist = True
        return exist

    def __insert(self):
        self.database.decryption()
        self.person_id = self.__insert_person(self.person)
        if self.person_id:
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
        self.database.cryptography()

    def __insert_person(self, person):
        try:
            query = """INSERT INTO person (name, subtitle, local, about, url, email, phone_number)  
            VALUES (?,?,?,?,?,?,?)"""
            self.database.cursor_db.execute(query, [person.name, person.subtitle, person.local, person.about,
                                                    person.url, person.email, person.phone_number])
            person_id = self.database.cursor_db.lastrowid
            self.database.connection.commit()
            return person_id
        except IntegrityError as e:
            log_erro(e)
            return None

    def __insert_certification(self, certification, person_id):
        query = """INSERT INTO certification (title, person_id)  VALUES (?,?)"""
        self.database.cursor_db.execute(query, [certification.title, person_id])
        self.database.connection.commit()

    def __insert_education(self, education, person_id):
        query = """INSERT INTO education (college, level, course, person_id)  VALUES (?,?,?,?)"""
        self.database.cursor_db.execute(query, [education.college, education.level, education.course, person_id])
        self.database.connection.commit()

    def __insert_language(self, language, person_id):
        query = """INSERT INTO language (language, level, person_id)  VALUES (?,?,?)"""
        self.database.cursor_db.execute(query, [language.language, language.level, person_id])
        self.database.connection.commit()

    def __insert_skill(self, skill, person_id):
        query = """INSERT INTO skill (title, indications, verify, person_id)  VALUES (?,?,?,?)"""
        self.database.cursor_db.execute(query, [skill.title, skill.indications, skill.verify, person_id])
        self.database.connection.commit()

    def __insert_experience(self, experience, person_id):
        query = """INSERT INTO experience (company, position, years, months, description, person_id)  VALUES (?,?,?,
        ?,?,?) """
        self.database.cursor_db.execute(query, [
            experience.company,
            experience.position,
            experience.years,
            experience.months,
            experience.description,
            person_id
        ]
                                        )
        self.database.connection.commit()

    # ------ SELECT ------ #
    def select_people(self):
        self.database.decryption()
        query = """
            SELECT id, name, subtitle, local, about, url, email, phone_number FROM person
        """
        self.database.cursor_db.execute(query)
        rows = self.database.cursor_db.fetchall()
        person_list = self.__get_list_person(rows)
        self.database.cryptography()
        return person_list

    def select_people_by_name(self):
        self.database.decryption()
        query = """
            SELECT id, name, subtitle, local, about, url, email, phone_number FROM person WHERE name = ?
        """
        self.database.cursor_db.execute(query, [self.person.name])
        rows = self.database.cursor_db.fetchall()
        person_list = self.__get_list_person(rows)
        self.database.cryptography()
        return person_list

    def select_people_by_url(self, url):
        self.database.decryption()
        query = """
            SELECT id, name, subtitle, local, about, url, email, phone_number FROM person WHERE url = ?
        """
        self.database.cursor_db.execute(query, [url])
        rows = self.database.cursor_db.fetchall()
        person_list = self.__get_list_person(rows)
        self.database.cryptography()
        return person_list

    def select_people_by_id(self, person_id):
        self.database.decryption()
        query = """
            SELECT id, name, subtitle, local, about, url, email, phone_number FROM person WHERE id = ?
        """
        self.database.cursor_db.execute(query, [person_id])
        rows = self.database.cursor_db.fetchall()
        person = None
        if rows:
            person = self.__get_list_person(rows)[0]
        self.database.cryptography()
        return person

    def select_people_by_list_ids(self, list_ids):
        self.database.decryption()
        query = """
            SELECT id, name, subtitle, local, about, url, email, phone_number FROM person WHERE id IN {}
        """
        self.database.cursor_db.execute(query.format(tuple(list_ids)))
        rows = self.database.cursor_db.fetchall()
        person_list = self.__get_list_person(rows)
        self.database.cryptography()
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
                id=row[0],
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
            SELECT id, title, person_id FROM certification WHERE ? = person_id 
        """
        self.database.cursor_db.execute(query, [person_id])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            certification_list.append(Certification(title=row[1]))
        return certification_list

    def __select_language(self, person_id):
        language_list = list()
        query = """
            SELECT id, language, level, person_id FROM language WHERE ? = person_id 
        """
        self.database.cursor_db.execute(query, [person_id])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            language_list.append(Language(language=row[1], level=row[2]))
        return language_list

    def __select_skill(self, person_id):
        skill_list = list()
        query = """
            SELECT id, title, indications, verify, person_id person_id FROM skill WHERE ? = person_id 
        """
        self.database.cursor_db.execute(query, [person_id])
        rows = self.database.cursor_db.fetchall()
        for row in rows:
            verify = True if row[3] == 1 else False
            skill_list.append(Skill(title=row[1], indications=row[2], verify=verify))
        return skill_list

    def __select_experience(self, person_id):
        experience_list = list()
        query = """
            SELECT id, company, position, years, months, description, person_id FROM experience WHERE ? = person_id 
        """
        self.database.cursor_db.execute(query, [person_id])
        rows = self.database.cursor_db.fetchall()
        for key, group in itertools.groupby(rows, key=lambda r: r[1]):
            experience_group = list()
            for row in group:
                experience_group.append(
                    Experience(
                        company=row[1],
                        position=row[2],
                        years=row[3],
                        months=row[4],
                        description=row[5]
                    )
                )
            experience_list.append(experience_group)
        return experience_list
