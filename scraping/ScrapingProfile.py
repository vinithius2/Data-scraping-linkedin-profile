import itertools
from time import sleep
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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
from utils.texts import text_40_seconds
from utils.texts import text_count_scraping_profile_exist
from utils.texts import text_profile_registered
from utils.texts import text_scraping_profile_finish
from utils.texts import text_scraping_profile_warning
from utils.texts import text_start_scraping


class ScrapingProfile:

    def __init__(self, driver, database):
        self.driver = driver
        self.database = database

    def start(self):
        """
        Inicia o 'Scraping' do perfil.
        """
        print(text_start_scraping)
        search_list = SearchDao(self.database).select_search_person_id_is_null()
        count_search = len(search_list)
        count_person = 0
        if search_list:
            for search in search_list:
                person = PersonDao(database=self.database).select_people_by_url(search.url_profile)
                if not person:
                    self.driver.get(search.url_profile)
                    try:
                        self.__scroll_down_page(self.driver)
                    except JavascriptException as e:
                        log_erro(e)
                        print(text_40_seconds)
                        sleep(40)
                        self.driver.get(search.url)
                        self.__scroll_down_page(self.driver)
                    self.__open_sections(self.driver)
                    person = self.__get_person(self.driver, search.url_profile)
                    count_person += 1
                    self.__save_database(person, search, count_search, count_person)
                else:
                    count_person += 1
                    print(text_count_scraping_profile_exist.format(count_person, count_search, bcolors.BOLD,
                                                                   person[0].name, bcolors.ENDC, bcolors.WARNING,
                                                                   bcolors.ENDC))
                    SearchDao(self.database).update_search_person_id(person[0].id, search.id)
        else:
            print(text_scraping_profile_warning)
        print(text_scraping_profile_finish)

    def __save_database(self, person, search, total_search, count_person):
        """
        Salva o perfil no banco de dados.
        """
        person_id = PersonDao(database=self.database, person=person).insert()
        if person_id:
            SearchDao(self.database).update_search_person_id(person_id, search.id)
            parsed_url = urlparse(person.url)
            url_profile = f"{parsed_url.hostname}{parsed_url.path}"
            print(text_profile_registered.format(count_person, total_search, bcolors.BOLD, person.name, bcolors.GREEN,
                                                 bcolors.ENDC, bcolors.ENDC, bcolors.BLUE, url_profile, bcolors.ENDC))

    def __wait_element_by_css_class(self, driver, css_class, timeout=30):
        """
        Aguarda o respectivo elemento da classe CSS carregar.
        """
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, css_class)))

    def __open_sections(self, driver):
        """
        Abre todas as seções do perfil do Linkedin.
        """
        try:
            self.__get_open_about(driver)
            self.__get_open_experience(driver)
            self.__get_open_certifications(driver)
            self.__get_open_accomplishments(driver)
            self.__get_open_skill(driver)
        except Exception as e:
            log_erro(e)

    def __get_open_about(self, driver):
        """
        Abre a seção 'Sobre' do perfil do Linkedin.
        """
        try:
            about_section = driver.find_element_by_class_name('pv-about-section')
            list_see_more_about = about_section.find_elements_by_class_name('inline-show-more-text__button')
            self.__click_list(driver, list_see_more_about, about_section)
        except NoSuchElementException as e:
            log_erro(e)

    def __get_open_experience(self, driver):
        """
        Abre a seção 'Experiência' do perfil do Linkedin.
        """
        try:
            experience_section = driver.find_element_by_id('experience-section')
            list_all_see_more_experience = experience_section.find_elements_by_class_name(
                'pv-profile-section__see-more-inline')
            self.__click_list(driver, list_all_see_more_experience, experience_section)
            list_item_see_more_experience = experience_section.find_elements_by_class_name(
                'inline-show-more-text__button')
            self.__click_list(driver, list_item_see_more_experience, experience_section)
        except NoSuchElementException as e:
            log_erro(e)

    def __get_open_certifications(self, driver):
        """
        Abre a seção 'Certificações' do perfil do Linkedin.
        """
        try:
            certifications_section = driver.find_element_by_id('certifications-section')
            list_all_see_more_certifications = certifications_section.find_elements_by_class_name(
                'pv-profile-section__see-more-inline')
            self.__click_list(driver, list_all_see_more_certifications, certifications_section)
        except NoSuchElementException as e:
            log_erro(e)

    def __get_open_accomplishments(self, driver):
        """
        Abre a seção 'Conquistas' do perfil do Linkedin.
        """
        try:
            accomplishments_section = driver.find_element_by_class_name('pv-accomplishments-section')
            accomplishments_language_section = accomplishments_section.find_element_by_class_name('languages')
            list_all_see_more_accomplishments = accomplishments_language_section.find_elements_by_class_name(
                'pv-accomplishments-block__expand')
            self.__click_list(driver, list_all_see_more_accomplishments, accomplishments_language_section)
        except NoSuchElementException as e:
            log_erro(e)

    def __get_open_skill(self, driver):
        """
        Abre a seção 'Habilidades' do perfil do Linkedin.
        """
        try:
            skill_section = driver.find_element_by_class_name('pv-skill-categories-section')
            list_skill_section_see_more = skill_section.find_elements_by_class_name(
                'pv-profile-section__card-action-bar')
            self.__click_list(driver, list_skill_section_see_more, skill_section)
        except NoSuchElementException as e:
            log_erro(e)

    def __click_list(self, driver, items, element, is_except=False):
        """
        Clica em cada item da seção.
        """
        for item in items:
            try:
                if not is_except:
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                item.click()
            except ElementClickInterceptedException as e:
                log_erro(e)
                if not is_except:
                    driver.execute_script("window.scrollTo(0, {});".format(element.location['y'] - 100))
                    self.__click_list(driver, items, element, True)

    def __scroll_down_page(self, driver, speed=8):
        """
        Faz o Scroll até o final da pagina para carregar todos os componentes.
        """
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = driver.execute_script("return document.body.scrollHeight")

    def __get_person(self, driver, url_profile):
        """
        Pega todos os dados do perfil.
        """
        try:
            html_page = driver.page_source
            soup = BeautifulSoup(html_page, 'html.parser')
            person = self.__get_main_info(driver, soup, url_profile)
            experiences = self.__get_experiences(soup)
            certifications = self.__get_certifications(soup)
            education = self.__get_education(soup)
            languages = self.__get_languages(soup)
            skills = self.__get_skills(soup)
            person.experiences = experiences
            person.certifications = certifications
            person.education = education
            person.languages = languages
            person.skills = skills
            return person
        except Exception as e:
            log_erro(e)

    def __get_main_info(self, driver, soup, url_profile):
        """
        Pega os dados de informações principais do perfil.
        """
        container_main = soup.find('section', {'class': ['pv-top-card']})

        name = self.__getText(container_main, 'h1', 'class', 'text-heading-xlarge')
        subtitle = self.__getText(container_main, 'div', 'class', 'text-body-medium')
        local = self.__getText(container_main, 'span', 'class', 'text-body-small inline t-black--light break-words')

        about = self.__get_about(soup)
        phone, email = self.__get_contact(driver, url_profile)
        return Person(name=name, subtitle=subtitle, local=local, about=about, phone_number=phone, email=email,
                      url=url_profile)

    def __get_contact(self, driver, url_profile):
        """
        Pega os dados de contato do perfil.
        """
        email = None
        phone = None
        parsed_url = urlparse(url_profile)
        driver.execute_script("window.open('{}/detail/contact-info/')".format(parsed_url.path))
        sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        html_page = driver.page_source
        soup_contact = BeautifulSoup(html_page, 'html.parser')
        sections = soup_contact.findAll('section', {'class': ['pv-contact-info__contact-type']})
        for item in sections:
            if "ci-email" in item.attrs.get("class"):
                email = self.__getText(item, 'a', 'class', 'pv-contact-info__contact-link')
            if "ci-phone" in item.attrs.get("class"):
                phone = self.__getText(item, 'span', 'class', 't-14 t-black t-normal')
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return phone, email

    def __get_about(self, soup):
        """
        Pega os dados do campo sobre do perfil.
        """
        container_about = soup.find('section', {'class': ['pv-about-section']})
        about = container_about.find('div', {'class': ['inline-show-more-text']})
        about = about.text.strip() if about else None
        return about

    def __get_experiences(self, soup):
        """
        Pega todos os dados de experiência do perfil.
        """
        experiences = list()
        container_experience = soup.find('section', {'class': ['experience-section']})
        if container_experience:
            children = container_experience.findAll('li', {'class': ['pv-entity__position-group-pager']})
            for li in children:
                experiences.append(self.__get_data_experience(li))
        return experiences

    def __get_data_experience(self, li):
        """
        Pega os dados de cada experiência individualmente do perfil.
        """
        descricao_list = list()
        empresa_list = list()
        tempo_list = list()
        cargo_list = list()
        experience_list = list()
        career = li.findAll('li', {'class': ['pv-entity__position-group-role-item']})

        if career:
            empresa_list, descricao_list = self.__get_data_description_career_experience(descricao_list, empresa_list,
                                                                                         li, career)
        else:
            empresa_list, descricao_list = self.__get_data_description_experience(descricao_list, empresa_list, li)
        tempo_list = self.__get_data_time_experience(li, tempo_list)
        cargo_list = self.__get_data_cargo_experience(li, cargo_list, tempo_list)

        for item in list(itertools.zip_longest(empresa_list, cargo_list, tempo_list, descricao_list)):
            anos = item[2].get("anos") if item[2] else 0
            meses = item[2].get("meses") if item[2] else 0
            experience_list.append(
                Experience(item[0], item[1], anos, meses, item[3])
            )
        return experience_list

    def __get_data_description_career_experience(self, descricao_list, empresa_list, li, career):
        """
        Pega informações sobre experiência caso tenha 'carreira' na empresa.
        """
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

    def __get_data_description_experience(self, descricao_list, empresa_list, li):
        """
        Pega informações sobre experiência na empresa.
        """
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

    def __get_data_time_experience(self, li, tempo_list):
        """
        Pega o tempo de experiência na empresa
        """
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

    def __get_data_cargo_experience(self, li, cargo_list, tempo_list):
        """
        Pega o cargo na empresa
        """
        class_css = 't-14 t-black t-bold' if len(tempo_list) > 1 else 't-16 t-black t-bold'
        cargo = li.findAll('h3', {'class': [class_css]})
        for item in cargo:
            cargo_list.append(item.text.replace("Cargo\n", "").strip() if item else None)
        return cargo_list

    def __get_certifications(self, soup):
        """
        Pega as certificações.
        """
        certifications = list()
        container_certifications = soup.find('section', {'id': ['certifications-section']})
        if container_certifications:
            children = container_certifications.findAll('li', {'class': ['pv-certification-entity']})
            for li in children:
                title = self.__getText(li, 'h3', 'class', 't-16 t-bold')
                certifications.append(Certification(title))
        return certifications

    def __get_education(self, soup):
        """
        Pega dados de escolaridade.
        """
        education_list = list()
        container_education = soup.find('section', {'id': ['education-section']})
        if container_education:
            children = container_education.findAll('li', {'class': ['pv-education-entity']})
            for li in children:
                college = self.__getText(li, 'h3', 'class', 'pv-entity__school-name')
                level = None
                container_level = li.find('p', {'class': ['pv-entity__degree-name']})
                if container_level:
                    level = self.__getText(container_level, 'span', 'class', 'pv-entity__comma-item')
                course = None
                container_course = li.find('p', {'class': ['pv-entity__fos']})
                if container_course:
                    course = self.__getText(container_course, 'span', 'class', 'pv-entity__comma-item')
                education_list.append(Education(college=college, level=level, course=course))
        return education_list

    def __get_languages(self, soup):
        """
        Pega dados de idiomas e nível.
        """
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

    def __get_skills(self, soup):
        """
        Pega dados de habilidades com idicações e selo do Linkedin.
        """
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
                        titulo = self.__getText(item, 'span', 'class', 'pv-skill-category-entity__name-text')
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

    def __getText(self, item, first_tag, second_tag, class_or_id):
        try:
            if item.find(first_tag, {second_tag: [class_or_id]}):
                return item.find(first_tag, {second_tag: [class_or_id]}).text.strip()
            return None
        except Exception as e:
            log_erro(e)
            return None
