from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from database.dao.SearchDao import SearchDao
from models.Search import Search


class ScrapingSearch:
    def __init__(self, url, database, driver):
        self.url = url
        self.database = database
        self.driver = driver

    def start(self):
        self.driver.get(self.url)
        self.search()
        print("\nData Scraping list profiles FINISH!!!")

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
                    url = profile.find('a', {'class': ['app-aware-link']}).attrs['href']
                    name = profile.find('span').text.strip()
                    count = count + 1
                    print("({}) {} - {}".format(count, name, url))
                    SearchDao(self.database, Search(url)).insert_search()
                self.click_next(disable, count)
            except NoSuchElementException as e:
                print(e)
            except AttributeError as e:
                print(e)

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
                print("\n#### PAGE {} ####\n".format(page_number))
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
