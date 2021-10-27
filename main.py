import os
import sys

from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.options import Options

from database.Database import Database
from scraping.ScoreProfile import ScoreProfile
from scraping.ScrapingProfile import ScrapingProfile
from scraping.ScrapingSearch import ScrapingSearch
from utils.bcolors import bcolors

text_option = f"""
    {bcolors.HEADER}########## Please choose your NUMBER option: ##########{bcolors.ENDC}\n
    {bcolors.BOLD}{bcolors.BLUE}(1){bcolors.ENDC}{bcolors.ENDC} Search profiles and save list in database;\n
    {bcolors.BOLD}{bcolors.BLUE}(2){bcolors.ENDC}{bcolors.ENDC} Scraping data each profile from database;\n
    {bcolors.BOLD}{bcolors.BLUE}(3){bcolors.ENDC}{bcolors.ENDC} Score profiles;\n
    {bcolors.BOLD}{bcolors.BLUE}(4){bcolors.ENDC}{bcolors.ENDC} Export profiles for XLS file with predeterminted filter;\n
    {bcolors.BOLD}{bcolors.BLUE}(5){bcolors.ENDC}{bcolors.ENDC} CLOSE this app.\n
    {bcolors.HEADER}###########################{bcolors.ENDC}\n
    {bcolors.BOLD}{bcolors.CYAN}* Your option (Only numbers)?{bcolors.ENDC}{bcolors.ENDC}
    """

text_url_filter = f"""
    {bcolors.UNDERLINE}Example of URL:{bcolors.ENDC} https://www.linkedin.com/search/results/people/?keywords=desenvolvedor&origin=FACETED_SEARCH&position=1&searchId=0e12d907-9848-40fb-8bc4-d0ec3c3c48c0&sid=nO4\n\n
    {bcolors.BOLD}{bcolors.CYAN}Add URL filter for Linkedin Profiles:{bcolors.ENDC}{bcolors.ENDC}
    """

text_error = f"""\n
    {bcolors.FAIL}
    {bcolors.HEADER}######## ATTEMTION ########{bcolors.ENDC}
    {bcolors.UNDERLINE}Just NUMBERS for your choose!{bcolors.ENDC}
    {bcolors.BOLD}Ex:{bcolors.ENDC} 1, 2, 3 or 4...
    {bcolors.HEADER}###########################{bcolors.ENDC}\n
    {bcolors.ENDC}
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
