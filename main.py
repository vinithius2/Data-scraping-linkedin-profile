import os
import sys

from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.options import Options

from ScoreProfile import ScoreProfile
from ScrapingProfile import ScrapingProfile
from ScrapingSearch import ScrapingSearch
from database.Database import Database

text_option = """
    ########## Please choose your NUMBER option: ##########\n
    (1) Search profiles and save list in database;\n
    (2) Scraping data each profile from database;\n
    (3) Score profiles;\n
    (4) Export profiles for XLS file with predeterminted filter;\n
    (5) CLOSE this app.
    * Your option (Only numbers)? 
    """

text_url_filter = """
    Example of URL: https://www.linkedin.com/search/results/people/?keywords=desenvolvedor&origin=FACETED_SEARCH&position=1&searchId=0e12d907-9848-40fb-8bc4-d0ec3c3c48c0&sid=nO4\n\n
    Add URL filter for Linkedin Profiles:
    """

text_error = """\n
    ######## ATTEMTION ########
    Just NUMBERS for your choose!
    Ex: 1, 2, 3 or 4...
    ###########################\n
    """

database = Database()


def main():
    database.create_tables_if_not_exists()
    driver = config()
    login(driver)
    print("Waiting...")
    choose(driver)


def choose(driver):
    try:
        option = input(text_option)
        option = int(option)
        if option == 1:
            search(driver)
        if option == 2:
            profile(driver)
        if option == 3:
            score(driver)
        if option == 4:
            export(driver)
        if option == 5:
            close(driver)
    except ValueError as e:
        print(text_error)
        choose(driver)


def close(driver):
    print("I'll be back! =]")
    driver.close()
    sys.exit()


def score(driver):
    print("\n # Score # \n")
    ScoreProfile(database).start()
    choose(driver)


def export(driver):
    print("\n # Export # \n")
    choose(driver)


def profile(driver):
    print("\n # Scraping # \n")
    ScrapingProfile(driver, database).start()
    choose(driver)


def search(driver):
    url_filter = input(text_url_filter)
    print("\n # Search # \n")
    try:
        ScrapingSearch(url_filter, database, driver).start()
    except InvalidArgumentException as e:
        print(e)
    choose(driver)


def config():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=r"./chromedriver.exe", options=chrome_options)
    driver.get('https://www.linkedin.com/uas/login')
    driver.maximize_window()
    return driver


def login(driver):
    username = driver.find_element_by_id('username')
    username_text = os.environ.get('login')
    username.send_keys(username_text)
    password = driver.find_element_by_id('password')
    password_text = os.environ.get('password')
    password.send_keys(password_text)
    log_in_button = driver.find_element_by_class_name('from__button--floating')
    log_in_button.click()


if __name__ == '__main__':
    main()
