from time import sleep
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, JavascriptException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Class
SEE_MORE_ITEM = 'inline-show-more-text__button'
SEE_MORE_ALL_ITEMS = 'pv-profile-section__see-more-inline'
# Mensagem
NAO_EXISTE = "NÃO EXISTE NO PERFIL"


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
    profile = 'https://www.linkedin.com/in/vinithius/'
    driver.get(profile)
    try:
        scroll_down_page(driver)
    except JavascriptException as e:
        print(e)
        sleep(40)
        driver.get(profile)
        scroll_down_page(driver)
    open_section(driver)
    print("\nOK!!!")


def open_section(driver):
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
        print_erro(e)


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


if __name__ == '__main__':
    main()

