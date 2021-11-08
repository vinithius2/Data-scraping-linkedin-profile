import os
import sys
import winsound
from pathlib import Path
from time import sleep
import webbrowser
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException, WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

from config import *
from database.Database import Database
from database.dao.PersonDao import PersonDao
from database.dao.SearchDao import SearchDao
from scraping.ScoreProfile import ScoreProfile
from scraping.ScrapingProfile import ScrapingProfile
from scraping.ScrapingSearch import ScrapingSearch
from utils.log_erro import log_erro
from utils.texts import *
from webdriver_manager.chrome import ChromeDriverManager
import colorama

database = Database()
os.system('cls')
colorama.init()


def main():
    """
    Iniciar aplicação...
    """
    print(text_logo)
    __create_directory()
    database.create_tables_if_not_exists()
    try:
        driver = __config()
        print(text_waiting_login)
        winsound.Beep(250, 100)
        __login(driver)
        winsound.Beep(500, 100)
        __choose(driver)
    except WebDriverException as e:
        winsound.Beep(250, 100)
        print(text_chrome_install)
        log_erro(e)
        sleep(25)
        print(text_closed_text)
        sleep(6)


def __login(driver):
    """
    Inicia o Login do Linkedin, caso esteja com 'DEBUG=True', é usado o valor de login e senha na variável de ambiente,
    se não, o processo é manual.
    """
    result = False
    if DEBUG:
        __login_debug(driver)
        result = True
    else:
        option = input(text_login)
        if option.lower() == 'y':
            result = True
        elif option.lower() == 'n':
            result = False
            __close(driver)
        else:
            print(text_login_error)
            __login(driver)
    if result and driver.current_url != URL_LOGIN:
        return result
    else:
        print(text_login_its_a_trap)
        __login(driver)


def __create_directory():
    """
    Cria o diretório principal
    """
    path_parent = "scrapingLinkedinProfiles"
    path_absolute = Path("/")
    directory_main = os.path.join(path_absolute.parent.absolute(), path_parent)
    if not os.path.exists(directory_main):
        os.mkdir(directory_main)
    __create_directory_export(path_absolute, directory_main)
    __create_directory_logs(path_absolute, directory_main)


def __create_directory_export(path_absolute, directory_main):
    """
    Cria o diretório de arquivos exportados
    """
    path_parent_export = os.path.join(directory_main, "export")
    directory_export = os.path.join(path_absolute.parent.absolute(), path_parent_export)
    if not os.path.exists(directory_export):
        os.mkdir(directory_export)


def __create_directory_logs(path_absolute, directory_main):
    """
    Cria o diretório de LOGS
    """
    path_parent_logs = os.path.join(directory_main, "logs")
    directory_logs = os.path.join(path_absolute.parent.absolute(), path_parent_logs)
    if not os.path.exists(directory_logs):
        os.mkdir(directory_logs)


def __choose(driver):
    """
    Inicia o menu com as opções de scraping para 'Search', 'Person' e exportação para XLS.
    """
    try:
        option = input(text_option)
        option = int(option)
        if option == SEARCH_PROFILES:
            __search(driver)
            __choose(driver)
        if option == SCRAPING_PROFILES:
            __start_scraping_profiles(driver)
            __choose(driver)
        if option == SCORE_AND_EXPORT:
            __start_score_and_export(driver)
            __choose(driver)
        if option == ALL_OPTIONS:
            __start_score_all_option(driver)
            __choose(driver)
        if option == TUTORIAL:
            print(text_scraping_tutorial)
            webbrowser.open("https://drive.google.com/drive/folders/1aKO-5552TPzkPXLixR9w4Wulw_rSpVEV?usp=sharing")
            __choose(driver)
        if option == CLOSE_APP:
            __close(driver)
    except ValueError as e:
        print(text_error)
        log_erro(e)
        __choose(driver)
    except TimeoutError as e:
        print(text_time_out_error)
        log_erro(e)
        __choose(driver)
    except TimeoutException as e:
        print(text_time_out_error)
        log_erro(e)
        __choose(driver)
    except AttributeError as e:
        print(text_unknown_error)
        log_erro(e)
        __choose(driver)


def __start_scraping_profiles(driver):
    """
    Verifica se existe registro em 'Search', caso sim, faz o procedimento de Scraping em 'Profile'.
    """
    if __verify_search():
        __profile(driver)
    else:
        print(text_error_search)
        __choose(driver)


def __start_score_and_export(driver):
    """
    Verifica se existe registro, caso sim, exporta os dados.
    """
    if __print_error_verify():
        __score_and_export(driver)
    else:
        __choose(driver)


def __start_score_all_option(driver):
    """
    Verifica se existe registro, caso sim, faz o procedimento de Scraping em 'Search', 'Person' e exporta os dados.
    """
    __search(driver)
    __profile(driver)
    __score_and_export(driver)


def __print_error_verify():
    """
    Se não houver dados nas tabelas de 'Person' e 'Search' ou somente em 'Person' ou 'Search', retorna 'False'.
    """
    result = True
    if not __verify_search() and not __verify_person():
        print(text_error_search_and_person)
        result = False
    elif not __verify_search():
        print(text_error_search)
        result = False
    elif not __verify_person():
        print(text_error_person)
        result = False
    return result


def __verify_search():
    """
    Se houver dados no banco na tabela de 'Search', retorna 'True', se não, retorna 'False'.
    """
    counter = SearchDao(database).search_counter()
    if counter > 0:
        return True
    return False


def __verify_person():
    """
    Se houver dados no banco na tabela de 'Person', retorna 'True', se não, retorna 'False'.
    """
    counter = PersonDao(database).person_counter()
    if counter > 0:
        return True
    return False


def __close(driver):
    """
    Encerra o app...
    """
    print(text_closed)
    __music_terminator()
    driver.close()
    sys.exit()


def __score_and_export(driver):
    """
    Inicia o cálculo ponderado e faz a exportação dos dados para XLS
    """
    ScoreProfile(database).start()
    __choose(driver)


def __profile(driver):
    """
    Inicia o scraping da lista de perfis do banco de dados
    """
    try:
        ScrapingProfile(driver, database).start()
    except InvalidArgumentException as e:
        print(text_unknown_error)
        __choose(driver)
    except TimeoutError as e:
        print(text_unknown_error)
        __choose(driver)


def __search(driver):
    """
    Inicia o menu para add a URL do filtro de pessoas para iniciar o Scraping da lista de perfis
    """
    winsound.Beep(250, 100)
    url_filter = input(text_url_filter)
    if URL_BASE_PEOPLE in url_filter:
        try:
            ScrapingSearch(url_filter, database, driver).start()
        except InvalidArgumentException as e:
            print(e)
            __choose(driver)
        except TimeoutError as e:
            print(text_unknown_error)
            __choose(driver)
    else:
        print(text_login_url_base)
        __search(driver)


def __config():
    """
    Configuração inicial para o navegador Chrome.
    """
    chrome_options = Options()
    if DEBUG:
        chrome_options.add_experimental_option("detach", True)
    else:
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(ChromeDriverManager(log_level=0).install(), options=chrome_options)
    driver.get(URL_LOGIN)
    driver.maximize_window()
    return driver


def __login_debug(driver):
    """
    Usado quando estiver em modo Debug, agilizando o Login
    """
    username = driver.find_element_by_id('username')
    username_text = os.environ.get('login')
    username.send_keys(username_text)
    password = driver.find_element_by_id('password')
    password_text = os.environ.get('password')
    password.send_keys(password_text)
    log_in_button = driver.find_element_by_class_name('from__button--floating')
    log_in_button.click()


def __music_terminator():
    """
    Music Terminator ♪ ♫ ♬
    =D Yeahhh!
    """
    winsound.Beep(80, 390)
    winsound.Beep(90, 200)
    winsound.Beep(80, 400)
    winsound.Beep(90, 200)
    winsound.Beep(80, 400)
    winsound.Beep(80, 500)


if __name__ == '__main__':
    main()
