import itertools
from time import sleep

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, JavascriptException

from database.Database import Database
from database.dao.PersonDao import PersonDao
from database.dao.SearchDao import SearchDao
from models.Certification import Certification
from models.Education import Education
from models.Experience import Experience
from models.Language import Language
from models.Person import Person
from models.Skill import Skill
from utils.bcolors import bcolors
from utils.log_erro import log_erro

database = Database()
SEE_MORE_ITEM = 'inline-show-more-text__button'
SEE_MORE_ALL_ITEMS = 'pv-profile-section__see-more-inline'


class ScrapingProfile:

    def __init__(self, driver, database):
        self.driver = driver
        self.database = database

    def start(self):
        search_list = SearchDao(self.database).select_search_person_id_is_null()
        for search in search_list:
            self.driver.get(search.url_profile)
            try:
                self.scroll_down_page(self.driver)
            except JavascriptException as e:
                log_erro(e)
                print(f"{bcolors.WARNING}Verifique o navegador, necessário ação humana, você tem {bcolors.BOLD}40 segundos{bcolors.ENDC}...{bcolors.ENDC}")
                sleep(40)
                self.driver.get(search.url)
                self.scroll_down_page(self.driver)
            self.open_sections(self.driver)
            person = self.get_person(self.driver, search.url_profile)
            self.save_database(person)
        print(f"\n{bcolors.GREEN}Data Scraping FINISH!!!{bcolors.ENDC}")

    def save_database(self, person):
        person_id = PersonDao(database=database, person=person).insert()
        if person_id:
            SearchDao(self.database).update_search_person_id(person_id, person.url)
            print(f"({person_id}) {bcolors.BOLD}{person.name}{bcolors.ENDC} {bcolors.BOLD}{bcolors.GREEN}CADASTRADO{bcolors.ENDC}{bcolors.ENDC}: {person.url}")

    def open_sections(self, driver):
        self.get_open_about(driver)
        self.get_open_experience(driver)
        self.get_open_certifications(driver)
        self.get_open_accomplishments(driver)
        self.get_open_skill(driver)

    def get_open_about(self, driver):
        try:
            about_section = driver.find_element_by_class_name('pv-about-section')
            list_see_more_about = about_section.find_elements_by_class_name(SEE_MORE_ITEM)
            self.click_list(driver, list_see_more_about, about_section)
        except NoSuchElementException as e:
            log_erro(e)

    def get_open_experience(self, driver):
        try:
            experience_section = driver.find_element_by_id('experience-section')
            list_all_see_more_experience = experience_section.find_elements_by_class_name(SEE_MORE_ALL_ITEMS)
            self.click_list(driver, list_all_see_more_experience, experience_section)
            list_item_see_more_experience = experience_section.find_elements_by_class_name(SEE_MORE_ITEM)
            self.click_list(driver, list_item_see_more_experience, experience_section)
        except NoSuchElementException as e:
            log_erro(e)

    def get_open_certifications(self, driver):
        try:
            certifications_section = driver.find_element_by_id('certifications-section')
            list_all_see_more_certifications = certifications_section.find_elements_by_class_name(SEE_MORE_ALL_ITEMS)
            self.click_list(driver, list_all_see_more_certifications, certifications_section)
        except NoSuchElementException as e:
            log_erro(e)

    def get_open_accomplishments(self, driver):
        try:
            accomplishments_section = driver.find_element_by_class_name('pv-accomplishments-section')
            accomplishments_language_section = accomplishments_section.find_element_by_class_name('languages')
            list_all_see_more_accomplishments = accomplishments_language_section.find_elements_by_class_name(
                'pv-accomplishments-block__expand')
            self.click_list(driver, list_all_see_more_accomplishments, accomplishments_language_section)
        except NoSuchElementException as e:
            log_erro(e)

    def get_open_skill(self, driver):
        try:
            skill_section = driver.find_element_by_class_name('pv-skill-categories-section')
            list_skill_section_see_more = skill_section.find_elements_by_class_name(
                'pv-profile-section__card-action-bar')
            self.click_list(driver, list_skill_section_see_more, skill_section)
        except NoSuchElementException as e:
            log_erro(e)

    def click_list(self, driver, items, element, is_except=False):
        for item in items:
            try:
                if not is_except:
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                item.click()
            except ElementClickInterceptedException as e:
                log_erro(e)
                if not is_except:
                    driver.execute_script("window.scrollTo(0, {});".format(element.location['y'] - 100))
                    self.click_list(driver, items, element, True)

    def scroll_down_page(self, driver, speed=8):
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = driver.execute_script("return document.body.scrollHeight")

    def get_person(self, driver, url_profile):
        html_page = driver.page_source
        soup = BeautifulSoup(html_page, 'html.parser')
        person = self.get_main_info(driver, soup, url_profile)
        experiences = self.get_experiences(soup)
        certifications = self.get_certifications(soup)
        education = self.get_education(soup)
        languages = self.get_languages(soup)
        skills = self.get_skills(soup)
        person.experiences = experiences
        person.certifications = certifications
        person.education = education
        person.languages = languages
        person.skills = skills
        return person

    def get_main_info(self, driver, soup, url_profile):
        container_main = soup.find('section', {'class': ['pv-top-card']})
        name = container_main.find('h1', {'class': ['text-heading-xlarge']}).text.strip()
        subtitle = container_main.find('div', {'class': ['text-body-medium']}).text.strip()
        local = container_main.find('span',
                                    {'class': ['text-body-small inline t-black--light break-words']}).text.strip()
        about = self.get_about(soup)
        phone, email = self.get_contact(driver, url_profile)
        return Person(name=name, subtitle=subtitle, local=local, about=about, phone_number=phone, email=email, url=url_profile)

    def get_contact(self, driver, url_profile):
        email = None
        phone = None
        driver.execute_script("window.open('{}detail/contact-info/')".format(url_profile))
        sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        html_page = driver.page_source
        soup_contact = BeautifulSoup(html_page, 'html.parser')
        sections = soup_contact.findAll('section', {'class': ['pv-contact-info__contact-type']})
        for item in sections:
            if "ci-email" in item.attrs.get("class"):
                email = item.find('a', {'class': ['pv-contact-info__contact-link']}).text.strip()
            if "ci-phone" in item.attrs.get("class"):
                phone = item.find('span', {'class': ['t-14 t-black t-normal']}).text.strip()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return phone, email

    def get_about(self, soup):
        container_about = soup.find('section', {'class': ['pv-about-section']})
        about = container_about.find('div', {'class': ['inline-show-more-text']})
        about = about.text.strip() if about else None
        return about

    def get_experiences(self, soup):
        experiences = list()
        container_experience = soup.find('section', {'class': ['experience-section']})
        if container_experience:
            children = container_experience.findAll('li', {'class': ['pv-entity__position-group-pager']})
            for li in children:
                experiences.append(self.get_data_experience(li))
        return experiences

    def get_data_experience(self, li):
        descricao_list = list()
        empresa_list = list()
        tempo_list = list()
        cargo_list = list()
        experience_list = list()
        career = li.findAll('li', {'class': ['pv-entity__position-group-role-item']})

        if career:
            empresa_list, descricao_list = self.get_data_description_career_experience(descricao_list, empresa_list, li, career)
        else:
            empresa_list, descricao_list = self.get_data_description_experience(descricao_list, empresa_list, li)
        tempo_list = self.get_data_time_experience(li, tempo_list)
        cargo_list = self.get_data_cargo_experience(li, cargo_list, tempo_list)

        for item in list(itertools.zip_longest(empresa_list, cargo_list, tempo_list, descricao_list)):
            anos = item[2].get("anos") if item[2] else 0
            meses = item[2].get("meses") if item[2] else 0
            experience_list.append(
                Experience(item[0], item[1], anos, meses, item[3])
            )
        return experience_list

    def get_data_description_career_experience(self, descricao_list, empresa_list, li, career):
        for item in career:
            try:
                empresa = li.find('div', {'class': ['pv-entity__company-summary-info']}).findAll(
                    'span', attrs={'class': None})[0]
                empresa_list.append(empresa.text.strip())
            except IndexError as e:
                empresa_list.append(None)
                log_erro(e)
            descricao = item.find('div', {'class': ['pv-entity__description']})
            if descricao:
                descricao_list.append(descricao.text.replace("ver menos", "").strip() if item else None)
            else:
                descricao_list.append(None)
        return empresa_list, descricao_list

    def get_data_description_experience(self, descricao_list, empresa_list, li):
        try:
            empresa = li.find('p', {'class': ['pv-entity__secondary-title']})
            if empresa.find('span', {'class': ['separator']}):
                empresa.find('span', {'class': ['separator']}).replaceWith(BeautifulSoup("", "html.parser"))
            descricao = li.findAll('div', {'class': ['pv-entity__description']})
            if descricao:
                for item in descricao:
                    empresa_list.append(empresa.text.strip())
                    descricao_list.append(item.text.replace("ver menos", "").strip() if item else None)
            else:
                empresa_list.append(empresa.text.strip())
        except TypeError as e:
            log_erro(e)
        except Exception as e:
            log_erro(e)
        return empresa_list, descricao_list

    def get_data_time_experience(self, li, tempo_list):
        tempo = li.findAll('span', {'class': ['pv-entity__bullet-item-v2']})
        for item in tempo:
            if item.text == "menos de um ano":
                item = item.text.replace("menos de um ano", "1 ano").split(" ")
            else:
                item = item.text.strip().split(" ")
            tempo_dict = dict(zip(item[1::2], list(map(int, item[::2]))))
            if "ano" in tempo_dict:
                tempo_dict["anos"] = tempo_dict["ano"]
                del tempo_dict["ano"]
            if "mês" in tempo_dict:
                tempo_dict["meses"] = tempo_dict["mês"]
                del tempo_dict["mês"]
            tempo_list.append(tempo_dict)
        return tempo_list

    def get_data_cargo_experience(self, li, cargo_list, tempo_list):
        class_css = 't-14 t-black t-bold' if len(tempo_list) > 1 else 't-16 t-black t-bold'
        cargo = li.findAll('h3', {'class': [class_css]})
        for item in cargo:
            cargo_list.append(item.text.replace("Cargo\n", "").strip() if item else None)
        return cargo_list

    def get_certifications(self, soup):
        certifications = list()
        container_certifications = soup.find('section', {'id': ['certifications-section']})
        if container_certifications:
            children = container_certifications.findAll('li', {'class': ['pv-certification-entity']})
            for li in children:
                title = li.find('h3', {'class': ['t-16 t-bold']}).text.strip()
                certifications.append(Certification(title))
        return certifications

    def get_education(self, soup):
        education_list = list()
        container_education = soup.find('section', {'id': ['education-section']})
        if container_education:
            children = container_education.findAll('li', {'class': ['pv-education-entity']})
            for li in children:
                college = li.find('h3', {'class': ['pv-entity__school-name']}).text.strip()
                level = None
                container_level = li.find('p', {'class': ['pv-entity__degree-name']})
                if container_level:
                    level = container_level.find('span', {'class': ['pv-entity__comma-item']}).text.strip()
                course = None
                container_course = li.find('p', {'class': ['pv-entity__fos']})
                if container_course:
                    course = container_course.find('span', {'class': ['pv-entity__comma-item']}).text.strip()
                education_list.append(Education(college=college, level=level, course=course))
        return education_list

    def get_languages(self, soup):
        languages = list()
        container_accomplishments = soup.find('div', {'id': ['languages-expandable-content']})
        if container_accomplishments:
            list_accomplishments = container_accomplishments.findAll('li', {'class': ['pv-accomplishment-entity']})
            for li in list_accomplishments:
                idioma = li.find('h4', {'class': ['pv-accomplishment-entity__title']}).contents[2].strip()
                nivel = li.find('p', {'class': ['pv-accomplishment-entity__proficiency']})
                nivel = nivel.text.strip() if nivel else None
                languages.append(Language(idioma, nivel))
        return languages

    def get_skills(self, soup):
        skills = list()
        container_skill = soup.find('section', {'class': ['pv-skill-categories-section']})
        if container_skill:
            container_top_list_skill = container_skill.findAll('ol',
                                                               {'class': ['pv-skill-categories-section__top-skills']})
            container_list_skill = container_skill.findAll('ol', {'class': ['pv-skill-category-list__skills_list']})
            all_list_skill = [container_top_list_skill, container_list_skill]
            for item in all_list_skill:
                for ol in item:
                    list_li = ol.findAll('li', {'class': ['pv-skill-category-entity']})
                    for li in list_li:
                        titulo = li.find('span', {'class': ['pv-skill-category-entity__name-text']}).text.strip()
                        indications = li.find('span', {'class': ['pv-skill-category-entity__endorsement-count']})
                        if indications:
                            if indications.text.strip() == '+ de 99':
                                indications = 99
                            else:
                                indications = int(indications.text.strip())
                        else:
                            indications = 0
                        verify = True if li.find('div', {'class': ['pv-skill-entity__verified-icon']}) else False
                        skills.append(Skill(titulo, indications, verify))
        return skills
