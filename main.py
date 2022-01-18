import os
import shutil
import sys
import webbrowser
import winsound
from datetime import datetime
from pathlib import Path
from time import sleep

import colorama
import requests
from requests.exceptions import ConnectionError as ConnectionErrorVersion
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException, WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from config import *
from database.Database import Database
from database.dao.PersonDao import PersonDao
from database.dao.SearchDao import SearchDao
from scraping.ScoreProfile import ScoreProfile
from scraping.ScrapingProfile import ScrapingProfile
from scraping.ScrapingSearch import ScrapingSearch
from utils.log_erro import log_erro
from utils.texts import *

database = Database()
os.system('cls')
colorama.init()


def main():
    """
    Iniciar aplicação...
    """
    try:
        print(text_logo)
        __verify_version()
        __create_directory()
        database.verify_migrations()
        driver = __config()
        print(text_waiting_login)
        winsound.Beep(250, 100)
        __login(driver)
        winsound.Beep(500, 100)
        __choose(driver)
    except WebDriverException as e:
        winsound.Beep(250, 100)
        if exception_cannot_find in e.msg:
            print(text_chrome_install.format(
                bcolors.FAIL, bcolors.BOLD, text_chrome_install_text_cannot_find, bcolors.ENDC, bcolors.ENDC,
                bcolors.BLUE, bcolors.ENDC, bcolors.FAIL, bcolors.BOLD, bcolors.ENDC, bcolors.ENDC
            )
            )
        else:
            print(text_chrome_install_closed.format(
                bcolors.FAIL, bcolors.BOLD, e, bcolors.ENDC, bcolors.ENDC, bcolors.BLUE, bcolors.ENDC, bcolors.FAIL,
                bcolors.BOLD, bcolors.ENDC, bcolors.ENDC
            )
            )
        log_erro(e)
        sleep(25)
        print(text_closed_text)
        sleep(6)
        database.cryptography()
    except ConnectionError as e:
        log_erro(e)
        print(text_connect_error)
        database.cryptography()
    except ConnectionErrorVersion as e:
        log_erro(e)
        print(text_connect_error)
        database.cryptography()
    except Exception as e:
        log_erro(e)
        print(text_unknown_error)
        database.cryptography()


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
        if option == RESET_APP:
            __reset(driver)
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
    database.cryptography()
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


def __reset(driver):
    option = input(text_reset)
    if option.lower() == 'y':
        database.connection.close()
        path_parent = "scrapingLinkedinProfiles"
        path_absolute = Path("/")
        directory_main = os.path.join(path_absolute.parent.absolute(), path_parent)
        shutil.rmtree(directory_main)
    elif option.lower() == 'n':
        __choose(driver)
    else:
        print(text_login_error)
        __reset(driver)


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


def __verify_version():
    """
    Gera notificação para atualização em caso de nova versão.
    """
    try:
        response = requests.get(URL_RELEASES)
        if response.status_code == 200:
            last_release = response.json()[0]
            if last_release and 'tag_name' in last_release and 'name' in last_release:
                tag = last_release['tag_name'].replace("v", "")
                name = last_release['name']
                if float(tag) > VERSION:
                    if 'assets' in last_release and len(last_release['assets']) >= 1:
                        asset_name_file = last_release['assets'][-1]['name']
                        asset_browser_download_url = last_release['assets'][-1]['browser_download_url']
                        asset_updated_at = last_release['assets'][-1]['updated_at']
                        updated_at = datetime.strptime(asset_updated_at.replace("Z", ""), '%Y-%m-%dT%H:%M:%S')
                        print(text_new_version_start.format(
                            bcolors.HEADER,
                            bcolors.ENDC,
                            bcolors.BOLD,
                            bcolors.ENDC,
                            bcolors.HEADER,
                            bcolors.ENDC,
                            updated_at.strftime("%B %d, %Y"),
                            bcolors.GREEN,
                            tag,
                            bcolors.ENDC,
                            bcolors.RED,
                            VERSION,
                            bcolors.ENDC,
                            name,
                            bcolors.HEADER,
                            bcolors.ENDC,
                            asset_name_file,
                            asset_browser_download_url,
                            bcolors.HEADER,
                            bcolors.ENDC,
                            bcolors.HEADER,
                            bcolors.ENDC,
                        )
                        )
    except IndexError as e:
        log_erro(e)
    except ValueError as e:
        log_erro(e)


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
