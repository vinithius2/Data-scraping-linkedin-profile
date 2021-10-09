from time import sleep
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, JavascriptException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

SEE_MORE_ITEM = 'inline-show-more-text__button'
SEE_MORE_ALL_ITEMS = 'pv-profile-section__see-more-inline'


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
    show_data(driver)


def show_data(driver):
    profile = 'https://www.linkedin.com/in/ilyabrotzky/'
    driver.get(profile)
    try:
        # sleep(2)
        # if driver.current_url == profile:
        #     driver.execute_script("document.body.style.zoom='zoom 25%'")
        scroll_down_page(driver)
    except JavascriptException as e:
        print(e)
        sleep(40)
        driver.get(profile)
        sleep(2)
        driver.execute_script("document.body.style.zoom='zoom 25%'")
        scroll_down_page(driver)
    get_open_about(driver)
    get_open_experience(driver)
    get_open_certifications(driver)
    get_open_accomplishments(driver)
    get_open_skill(driver)
    print("ok")


def get_open_about(driver):
    print("get_open_about")
    try:
        about_section = driver.find_element_by_class_name('pv-about-section')
        # x = about_section.location['x']
        # y = about_section.location['y']
        list_see_more_about = about_section.find_elements_by_class_name(SEE_MORE_ITEM)
        click_list(driver, list_see_more_about, about_section)
    except NoSuchElementException as e:
        print(e)


def get_open_experience(driver):
    print("get_open_experience")
    try:
        experience_section = driver.find_element_by_id('experience-section')
        list_item_see_more_experience = experience_section.find_elements_by_class_name(SEE_MORE_ITEM)
        list_all_see_more_experience = experience_section.find_elements_by_class_name(SEE_MORE_ALL_ITEMS)
        # x = experience_section.location['x']
        # y = experience_section.location['y']
        click_list(driver, list_item_see_more_experience, experience_section)
        click_list(driver, list_all_see_more_experience, experience_section)
    except NoSuchElementException as e:
        print(e)


def get_open_certifications(driver):
    print("get_open_certifications")
    try:
        certifications_section = driver.find_element_by_id('certifications-section')
        list_all_see_more_certifications = certifications_section.find_elements_by_class_name(SEE_MORE_ALL_ITEMS)
        # x = certifications_section.location['x']
        # y = certifications_section.location['y']
        click_list(driver, list_all_see_more_certifications, certifications_section)
    except NoSuchElementException as e:
        print(e)


def get_open_accomplishments(driver):
    print("get_open_accomplishments")
    try:
        accomplishments_section = driver.find_element_by_class_name('pv-accomplishments-section')
        accomplishments_language_section = accomplishments_section.find_element_by_class_name('languages')
        list_all_see_more_accomplishments = accomplishments_language_section.find_elements_by_class_name('pv-accomplishments-block__expand')
        # x = accomplishments_language_section.location['x']
        # y = accomplishments_language_section.location['y']
        click_list(driver, list_all_see_more_accomplishments, accomplishments_section)
    except NoSuchElementException as e:
        print(e)


def get_open_skill(driver):
    print("get_open_skill")
    try:
        skill_section = driver.find_element_by_class_name('pv-skill-categories-section')
        list_skill_section_see_more = skill_section.find_elements_by_class_name('pv-profile-section__card-action-bar')
        # x = skill_section.location['x']
        # y = skill_section.location['y']
        click_list(driver, list_skill_section_see_more, skill_section)
    except NoSuchElementException as e:
        print(e)


def click_list(driver, items, element_position):
    # print("X: {}, Y: {}".format(x, y))
    # x, y = scroll_smooth_page(driver, y)
    # driver.execute_script("window.scrollTo({}, {});".format(x, y))
    for item in items:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", element_position)
            sleep(2)
            item.click()
        except ElementClickInterceptedException as e:
            print(e)
            # y = driver.execute_script("return document.body.scrollHeight")
            # x, y = scroll_smooth_page(driver, y)
            # click_list(driver, items, x, y)


def scroll_down_page(driver, speed=8):
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")


# def scroll_smooth_page(driver, y, speed=8):
#     current_scroll_position, new_height = y, driver.execute_script("return document.body.scrollHeight")
#     while current_scroll_position <= new_height:
#         current_scroll_position += speed
#         driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
#         new_height = driver.execute_script("return document.body.scrollHeight")
#     return current_scroll_position, new_height


if __name__ == '__main__':
    main()

