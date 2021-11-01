import datetime

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from database.dao.SearchDao import SearchDao
from models.Search import Search
from utils.bcolors import bcolors
from utils.log_erro import log_erro


class ScrapingSearch:
    def __init__(self, url_filter, database, driver):
        self.url_filter = url_filter
        self.database = database
        self.driver = driver

    def start(self):
        self.driver.get(self.url_filter)
        self.search()
        print(f"\n{bcolors.GREEN}Data Scraping list profiles FINISH!!!{bcolors.ENDC}")

    def search(self, count=0):
        element = self.wait_element_by_css_class('reusable-search__result-container')
        self.scroll_down_page(self.driver)
        html_page = self.driver.page_source
        soup = BeautifulSoup(html_page, 'html.parser')
        disable = self.page(soup)

        if element.is_displayed():
            profile_list = soup.findAll('li', {'class': ['reusable-search__result-container']})
            try:
                for item in profile_list:
                    profile = item.find('span', {'class': ['entity-result__title-text']})
                    if profile.find('span', {'class': ['visually-hidden']}):
                        profile.find('span', {'class': ['visually-hidden']}).replaceWith(BeautifulSoup("", "html.parser"))
                    url_profile = profile.find('a', {'class': ['app-aware-link']}).attrs['href']
                    if profile.find('span'):
                        name = profile.find('span').text.strip()
                        count = count + 1
                        print(f"({count}) {bcolors.BOLD}{name}{bcolors.ENDC} - {url_profile}")
                        SearchDao(self.database, Search(self.url_filter, url_profile)).insert_search()
                    else:
                        print(f"{bcolors.RED}{bcolors.BOLD}[NÃO CADASTRADO]{bcolors.ENDC} Usuário fora da sua rede...{bcolors.ENDC} - {url_profile}")
                self.click_next(disable, count)
            except NoSuchElementException as e:
                log_erro(e)
            except AttributeError as e:
                log_erro(e)

    def page(self, soup):
        disable = False
        element = self.wait_element_by_css_class('artdeco-pagination')
        if element.is_displayed():
            container_pages = soup.find('div', {'class': ['artdeco-pagination']})
            if container_pages:
                next_class = container_pages.find('button', {'class': 'artdeco-pagination__button--next'}).attrs['class']
                if 'artdeco-button--disabled' in next_class:
                    disable = True
                page_number = container_pages.find('li', {'class': ['selected']}).text.strip()
                print(f"\n{bcolors.HEADER}#### PAGE {page_number} ####{bcolors.ENDC}\n")
        return disable

    def wait_element_by_css_class(self, css_class, timeout=40):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, css_class)))

    def click_next(self, disable, count):
        self.scroll_down_page(self.driver)
        if not disable:
            button_next = self.driver.find_element_by_class_name('artdeco-pagination__button--next')
            button_next.click()
            self.search(count)

    def scroll_down_page(self, driver, speed=8):
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = driver.execute_script("return document.body.scrollHeight")

    def print_erro(self, e, msg="ERRO"):
        now = datetime.datetime.now()
        f = open(f"../{now.strftime('%d_%m_%Y')}.txt", "a")
        f.write("[{}] {}".format(str(now), e))
        f.close()
