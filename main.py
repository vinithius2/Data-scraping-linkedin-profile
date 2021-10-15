import itertools
from time import sleep
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, JavascriptException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Class
from database.Database import Database
from database.dao.PersonDao import PersonDao
from models.Language import Language
from models.Certification import Certification
from models.Experience import Experience
from models.Person import Person
from models.Skill import Skill

database = Database()
SEE_MORE_ITEM = 'inline-show-more-text__button'
SEE_MORE_ALL_ITEMS = 'pv-profile-section__see-more-inline'
HEADER_CONTENTS = 'pv-entity__summary-info'
CONTENTS = 'inline-show-more-text'
# Mensagem
NAO_EXISTE = "NÃO EXISTE NO PERFIL"
PROFILE = 'https://www.linkedin.com/in/vinithius/'


def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get('https://www.linkedin.com/uas/login')
    driver.maximize_window()
    login(driver)


def login(driver):
    username = driver.find_element_by_id('username')
    username_text = os.environ.get('login')
    username.send_keys(username_text)
    password = driver.find_element_by_id('password')
    password_text = os.environ.get('password')
    password.send_keys(password_text)
    log_in_button = driver.find_element_by_class_name('from__button--floating')
    log_in_button.click()
    start(driver)


def start(driver):
    driver.get(PROFILE)
    try:
        scroll_down_page(driver)
    except JavascriptException as e:
        print(e)
        sleep(40)
        driver.get(PROFILE)
        scroll_down_page(driver)
    open_sections(driver)
    person = get_person(driver)
    save_database(person)
    # PRINTS
    print(person)
    print("\nOK!!!")


def save_database(person):
    database.create_tables_if_not_exists()
    PersonDao(person, database).insert()


def open_sections(driver):
    get_open_about(driver)
    get_open_experience(driver)
    get_open_certifications(driver)
    get_open_accomplishments(driver)
    get_open_skill(driver)


def get_open_about(driver):
    print("\n# SOBRE #")
    try:
        about_section = driver.find_element_by_class_name('pv-about-section')
        list_see_more_about = about_section.find_elements_by_class_name(SEE_MORE_ITEM)
        click_list(driver, list_see_more_about, about_section)
    except NoSuchElementException as e:
        print_erro(e, NAO_EXISTE)


def get_open_experience(driver):
    print("\n# EXPERIÊNCIA #")
    try:
        experience_section = driver.find_element_by_id('experience-section')
        list_all_see_more_experience = experience_section.find_elements_by_class_name(SEE_MORE_ALL_ITEMS)
        click_list(driver, list_all_see_more_experience, experience_section)
        list_item_see_more_experience = experience_section.find_elements_by_class_name(SEE_MORE_ITEM)
        click_list(driver, list_item_see_more_experience, experience_section)
    except NoSuchElementException as e:
        print_erro(e, NAO_EXISTE)


def get_open_certifications(driver):
    print("\n# CERTIFICAÇÕES #")
    try:
        certifications_section = driver.find_element_by_id('certifications-section')
        list_all_see_more_certifications = certifications_section.find_elements_by_class_name(SEE_MORE_ALL_ITEMS)
        click_list(driver, list_all_see_more_certifications, certifications_section)
    except NoSuchElementException as e:
        print_erro(e, NAO_EXISTE)


def get_open_accomplishments(driver):
    print("\n# CONQUISTAS #")
    try:
        accomplishments_section = driver.find_element_by_class_name('pv-accomplishments-section')
        accomplishments_language_section = accomplishments_section.find_element_by_class_name('languages')
        list_all_see_more_accomplishments = accomplishments_language_section.find_elements_by_class_name('pv-accomplishments-block__expand')
        click_list(driver, list_all_see_more_accomplishments, accomplishments_language_section)
    except NoSuchElementException as e:
        print_erro(e, NAO_EXISTE)


def get_open_skill(driver):
    print("\n# HABILIDADES #")
    try:
        skill_section = driver.find_element_by_class_name('pv-skill-categories-section')
        list_skill_section_see_more = skill_section.find_elements_by_class_name('pv-profile-section__card-action-bar')
        click_list(driver, list_skill_section_see_more, skill_section)
    except NoSuchElementException as e:
        print_erro(e, NAO_EXISTE)


def click_list(driver, items, element, is_except=False):
    for item in items:
        try:
            if not is_except:
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
            item.click()
            print("CLICK...")
        except ElementClickInterceptedException as e:
            print("CLICK... OPS..")
            print_erro(e)
            if not is_except:
                driver.execute_script("window.scrollTo(0, {});".format(element.location['y'] - 100))
                click_list(driver, items, element, True)


def scroll_down_page(driver, speed=8):
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")


def print_erro(e, msg="ERRO"):
    print("###### {} ######".format(msg))
    print(e)
    print("##################\n")


def get_person(driver):
    html_page = driver.page_source
    soup = BeautifulSoup(html_page, 'html.parser')
    person = get_main_info(soup)
    experiences = get_experiences(soup)
    certifications = get_certifications(soup)
    languages = get_languages(soup)
    skills = get_skills(soup)
    person.experiences = experiences
    person.certifications = certifications
    person.languages = languages
    person.skills = skills
    return person


def get_main_info(soup):
    container_main = soup.find('section', {'class': ['pv-top-card']})
    name = container_main.find('h1', {'class': ['text-heading-xlarge']}).text.strip()
    subtitle = container_main.find('div', {'class': ['text-body-medium']}).text.strip()
    local = container_main.find('span', {'class': ['text-body-small inline t-black--light break-words']}).text.strip()
    about = get_about(soup)
    return Person(name=name, subtitle=subtitle, local=local, about=about)


def get_about(soup):
    container_about = soup.find('section', {'class': ['pv-about-section']})
    about = container_about.find('div', {'class': [CONTENTS]})
    about = about.text.strip() if about else None
    print("\n## about ##")
    print(about)
    return about


def get_experiences(soup):
    experiences = list()
    container_experience = soup.find('section', {'class': ['experience-section']})
    if container_experience:
        children = container_experience.findAll('li', {'class': ['pv-entity__position-group-pager']})
        for li in children:
            experiences.append(get_data_experience(li))
            print("\n## experience ##")
            print(experiences)
    return experiences


def get_data_experience(li):
    descricao_list = list()
    descricao = li.findAll('div', {'class': ['pv-entity__description']})
    for item in descricao:
        descricao_list.append(item.text.replace("ver menos", "").strip() if item else None)

    tempo_list = list()
    tempo = li.findAll('span', {'class': ['pv-entity__bullet-item-v2']})
    for item in tempo:
        item = item.text.strip().split(" ")
        tempo_dict = dict(zip(item[1::2], list(map(int, item[::2]))))
        if "ano" in tempo_dict:
            tempo_dict["anos"] = tempo_dict["ano"]
            del tempo_dict["ano"]
        tempo_list.append(tempo_dict)

    cargo_list = list()
    class_css = 't-14 t-black t-bold' if len(tempo_list) > 1 else 't-16 t-black t-bold'
    cargo = li.findAll('h3', {'class': [class_css]})
    for item in cargo:
        cargo_list.append(item.text.replace("Cargo\n", "").strip() if item else None)

    experience_list = list()
    for item in list(itertools.zip_longest(cargo_list, tempo_list, descricao_list)):
        experience_list.append(
            Experience(item[0], item[1], item[2])
        )

    return experience_list


def get_certifications(soup):
    certifications = list()
    container_certifications = soup.find('section', {'id': ['certifications-section']})
    if container_certifications:
        children = container_certifications.findAll('li', {'class': ['pv-certification-entity']})
        for li in children:
            title = li.find('h3', {'class': ['t-16 t-bold']}).text.strip()
            certifications.append(Certification(title))
    return certifications


def get_languages(soup):
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


def get_skills(soup):
    skills = list()
    container_skill = soup.find('section', {'class': ['pv-skill-categories-section']})
    if container_skill:
        container_top_list_skill = container_skill.findAll('ol', {'class': ['pv-skill-categories-section__top-skills']})
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


if __name__ == '__main__':
    main()

