import os
import sys
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.options import Options

from database.Database import Database
from scraping.ScoreProfile import ScoreProfile
from scraping.ScrapingProfile import ScrapingProfile
from scraping.ScrapingSearch import ScrapingSearch
from utils.texts import *

database = Database()
SEARCH_PROFILES = 1
SCRAPING_PROFILES = 2
SCORE_AND_EXPORT = 3
ALL_OPTIONS = 4
CLOSE_APP = 5


def main():
    print(text_logo)
    create_directory()
    database.create_tables_if_not_exists()
    driver = config()
    print(text_waiting_login)
    login(driver)
    choose(driver)


def create_directory():
    path_parent = "scrapingLinkedinProfiles"
    path_absolute = Path("/")
    directory_main = os.path.join(path_absolute.parent.absolute(), path_parent)
    if not os.path.exists(directory_main):
        os.mkdir(directory_main)
    create_directory_database(path_absolute, directory_main)
    create_directory_export(path_absolute, directory_main)


def create_directory_database(path_absolute, directory_main):
    path_parent_database = os.path.join(directory_main, "database")
    directory_database = os.path.join(path_absolute.parent.absolute(), path_parent_database)
    if not os.path.exists(directory_database):
        os.mkdir(directory_database)


def create_directory_export(path_absolute, directory_main):
    path_parent_export = os.path.join(directory_main, "export")
    directory_export = os.path.join(path_absolute.parent.absolute(), path_parent_export)
    if not os.path.exists(directory_export):
        os.mkdir(directory_export)


def choose(driver):
    try:
        option = input(text_option)
        option = int(option)
        if option == SEARCH_PROFILES:
            search(driver)
        if option == SCRAPING_PROFILES:
            profile(driver)
        if option == SCORE_AND_EXPORT:
            score_and_export(driver)
        if option == ALL_OPTIONS:
            search(driver)
            profile(driver)
            score_and_export(driver)
        if option == CLOSE_APP:
            close(driver)
    except ValueError as e:
        print(text_error)
        choose(driver)


def close(driver):
    print(text_closed)
    driver.close()
    sys.exit()


def score_and_export(driver):
    print("\n # Score # \n")
    ScoreProfile(database).start()
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
