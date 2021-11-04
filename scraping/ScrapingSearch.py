from urllib.parse import parse_qs
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from database.dao.PersonDao import PersonDao
from database.dao.SearchDao import SearchDao
from models.Search import Search
from utils.bcolors import bcolors
from utils.log_erro import log_erro
from utils.texts import text_out_of_your_network
from utils.texts import text_scraping_search_finish


class ScrapingSearch:
    def __init__(self, url_filter, database, driver):
        self.url_filter = url_filter
        self.database = database
        self.driver = driver

    def start(self):
        """
        Iniciar o scraping search...
        """
        self.driver.get(self.url_filter)
        captured_value = self.__get_keywords(self.url_filter)
        self.__search(captured_value)
        print(text_scraping_search_finish)

    def __get_keywords(self, url_filter):
        """
        Captura as palavras usadas no filtro
        """
        parsed_url = urlparse(url_filter)
        captured_value = None
        if "keywords" in parse_qs(parsed_url.query).keys():
            captured_value = parse_qs(parsed_url.query)["keywords"][0]
        return captured_value

    def __search(self, captured_value, count=0):
        """
        Iniciar o scraping search...
        """
        element = self.__wait_element_by_css_class('reusable-search__result-container')
        self.__scroll_down_page(self.driver)
        html_page = self.driver.page_source
        soup = BeautifulSoup(html_page, 'html.parser')
        disable = self.__page(soup)

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
                        count += 1
                        print(f"({count}) {bcolors.BOLD}{name}{bcolors.ENDC} - {url_profile}")
                        SearchDao(self.database, Search(
                                    url_filter=self.url_filter,
                                    url_profile=url_profile,
                                    text_filter=captured_value
                                )).insert_search()
                    else:
                        print(f"{text_out_of_your_network} - {url_profile}")
                self.__click_next(disable, count)
            except NoSuchElementException as e:
                log_erro(e)
            except AttributeError as e:
                log_erro(e)

    def __page(self, soup):
        """
        Verifica se o botão da paginação está desabilitado ou não para seguir a próxima página.
        """
        disable = False
        element = self.__wait_element_by_css_class('artdeco-pagination')
        if element.is_displayed():
            container_pages = soup.find('div', {'class': ['artdeco-pagination']})
            if container_pages:
                next_class = container_pages.find('button', {'class': 'artdeco-pagination__button--next'}).attrs['class']
                if 'artdeco-button--disabled' in next_class:
                    disable = True
                page_number = container_pages.find('li', {'class': ['selected']}).text.strip()
                print(f"\n{bcolors.HEADER}#### PAGE {page_number} ####{bcolors.ENDC}\n")
        return disable

    def __wait_element_by_css_class(self, css_class, timeout=40):
        """
        Aguarda o respectivo elemento da classe CSS carregar.
        """
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, css_class)))

    def __click_next(self, disable, count):
        """
        Clica no botão NEXT caso exista para seguir para a próxima página.
        """
        self.__scroll_down_page(self.driver)
        if not disable:
            button_next = self.driver.find_element_by_class_name('artdeco-pagination__button--next')
            button_next.click()
            self.__search(count)

    def __scroll_down_page(self, driver, speed=8):
        """
        Faz o Scroll até o final da pagina para carregar todos os componentes.
        """
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = driver.execute_script("return document.body.scrollHeight")
