from config import VERSION
from utils.bcolors import bcolors

text_logo = f"""
    {bcolors.HEADER}######################################################################################################################{bcolors.ENDC}
    {bcolors.BOLD}#     _____                      _               _      _       _            _ _         _____            __ _ _      
    #    / ____|                    (_)             | |    (_)     | |          | (_)       |  __ \          / _(_) |     
    #   | (___   ___ _ __ __ _ _ __  _ _ __   __ _  | |     _ _ __ | | _____  __| |_ _ __   | |__) | __ ___ | |_ _| | ___ 
    #    \___ \ / __| '__/ _` | '_ \| | '_ \ / _` | | |    | | '_ \| |/ / _ \/ _` | | '_ \  |  ___/ '__/ _ \|  _| | |/ _ \\
    #    ____) | (__| | | (_| | |_) | | | | | (_| | | |____| | | | |   <  __/ (_| | | | | | | |   | | | (_) | | | | |  __/
    #   |_____/ \___|_|  \__,_| .__/|_|_| |_|\__, | |______|_|_| |_|_|\_\___|\__,_|_|_| |_| |_|   |_|  \___/|_| |_|_|\___|
    #                         | |             __/ |                                                                       
    #                         |_|            |___/ {bcolors.ENDC}                                                                  {bcolors.UNDERLINE}V {VERSION}{bcolors.ENDC}
    {bcolors.HEADER}######################################################################################################################{bcolors.ENDC} 
    """

text_closed = f"""
    {bcolors.BOLD}
    {bcolors.RED}I'll be back!{bcolors.ENDC} 
                         ______
                       <((((((\\\\
                       /      . ]\\
                       ;--..--._|]
    (\                 '--/\--'  )
     \\\\                | '-'  :'|
      \\\\               . -==- .-|
       \\\\              \.__.'   \--._
       [\\\\          __.--|       //  _/'--.
       \ \\\\       .'-._ ('-----'/ __/      \\
        \ \\\\     /   __>|      | '--.       |
         \ \\\\   |   \   |     /    /       /
          \ '\ /     \  |     |  _/       /
           \  \       \ |     | /        /
            \  \      \        /
     {bcolors.ENDC} 
     {bcolors.UNDERLINE}Exterminate... Ops... close this app of Scraping Linkedin Profile V {VERSION}...{bcolors.ENDC}
     
     {bcolors.HEADER}#################### CONTACT ####################{bcolors.ENDC}
     Dev: {bcolors.UNDERLINE}Marcos Vinithius =D{bcolors.ENDC}
     Linkedin: https://www.linkedin.com/in/vinithius/
     Github project: https://github.com/vinithius2/scraping-data-linkedin-profile
    """

text_closed_text = f"""\n
    {bcolors.UNDERLINE}Closing app Scraping Linkedin Profile V {VERSION}...{bcolors.ENDC}
"""

text_option = f"""
    {bcolors.HEADER}########## Please choose your NUMBER option: ##########{bcolors.ENDC}\n
    {bcolors.BOLD}{bcolors.BLUE}(1){bcolors.ENDC}{bcolors.ENDC} Search profiles and save list in database;\n
    {bcolors.BOLD}{bcolors.BLUE}(2){bcolors.ENDC}{bcolors.ENDC} Scraping data each profile from database;\n
    {bcolors.BOLD}{bcolors.BLUE}(3){bcolors.ENDC}{bcolors.ENDC} Weighted calculation score profiles and Export XLS;\n
    {bcolors.BOLD}{bcolors.BLUE}(4){bcolors.ENDC}{bcolors.ENDC} {bcolors.GREEN}^^{bcolors.ENDC} All of the above {bcolors.UNDERLINE}(1,2,3){bcolors.ENDC} {bcolors.GREEN}^^{bcolors.ENDC}.\n
    {bcolors.BOLD}{bcolors.BLUE}(5){bcolors.ENDC}{bcolors.ENDC} {bcolors.BLUE}?{bcolors.ENDC} Tutorial... {bcolors.BLUE}?{bcolors.ENDC}.\n
    {bcolors.BOLD}{bcolors.BLUE}(6){bcolors.ENDC}{bcolors.ENDC} {bcolors.RED}X{bcolors.ENDC} CLOSE this app {bcolors.RED}X{bcolors.ENDC}.\n
    {bcolors.BOLD}{bcolors.BLUE}(7){bcolors.ENDC}{bcolors.ENDC} {bcolors.RED}CAUTION!{bcolors.ENDC} RESET all datas {bcolors.RED}CAUTION!{bcolors.ENDC}.\n
    {bcolors.HEADER}#######################################################{bcolors.ENDC}\n
    {bcolors.BOLD}{bcolors.CYAN}* Your option (Only numbers)?{bcolors.ENDC}{bcolors.ENDC}
    """

text_new_version_start = """
    {}################################ NOTIFICATION ################################{}
    #          {}THERE IS A NEW VERSION OF Scraping Linkedin Profile.{}              #
    {}##############################################################################{}
    Release date: {}                                                               
    New version: {}{}{} > Your version: {}{}{}                                     
    Name release: {}                                                               
    {}################################# DOWNLOAD ###################################{}
    File: {}                                                                       
    Download: {}                                                                   
    {}##############################################################################{}
    Obs: After downloading the new EXE you will need to delete the EXE from the pre-
    vious version to avoid problems.
    {}##############################################################################{}
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

text_unknown_error = f"""\n
    {bcolors.FAIL}
    {bcolors.HEADER}######## ATTEMTION ########{bcolors.ENDC}
    {bcolors.FAIL}Unknown error! =({bcolors.ENDC}
    {bcolors.HEADER}###########################{bcolors.ENDC}\n
    {bcolors.ENDC}
    """

text_time_out_error = f"""\n
    {bcolors.FAIL}
    {bcolors.HEADER}######## ATTEMTION ########{bcolors.ENDC}
    {bcolors.FAIL}Profile taking too long to load, check your connection...{bcolors.ENDC}
    {bcolors.HEADER}###########################{bcolors.ENDC}\n
    {bcolors.ENDC}
    """

text_error_search = f"""\n
    {bcolors.FAIL}
    {bcolors.HEADER}######## ATTEMTION ########{bcolors.ENDC}
    {bcolors.UNDERLINE}You need to choose option number (1) to have a list for the survey...!{bcolors.ENDC}
    {bcolors.HEADER}###########################{bcolors.ENDC}\n
    {bcolors.ENDC}
    """

text_scraping_tutorial = f"""
    {bcolors.BLUE}Tutorial opened in browser!!!{bcolors.ENDC}
"""

text_out_of_your_network = """
    {}{}[NOT REGISTERED]{} User outside your network...{} - {}{}{}
"""

text_scraping_search_finish = f"""
    {bcolors.GREEN}Data Scraping list profiles FINISH!!!{bcolors.ENDC}
"""

text_scraping_profile_finish = f"""
    {bcolors.GREEN}Data Scraping FINISH!!!{bcolors.ENDC}
"""

text_scraping_profile_warning = f"""
    {bcolors.WARNING}All LinkedIn profiles have already been scraped!!!{bcolors.ENDC}
"""

text_40_seconds = f"""\n
    {bcolors.WARNING}Check your browser, human action required, you have {bcolors.BOLD}40 seconds{bcolors.ENDC}...{bcolors.ENDC}
"""

text_error_person = f"""\n
    {bcolors.FAIL}
    {bcolors.HEADER}######## ATTEMTION ########{bcolors.ENDC}
    {bcolors.UNDERLINE}You need to choose option number (2) to have Linkedin profiles to export information...!{bcolors.ENDC}
    {bcolors.HEADER}###########################{bcolors.ENDC}\n
    {bcolors.ENDC}
    """

text_error_search_and_person = f"""\n
    {bcolors.FAIL}
    {bcolors.HEADER}######## ATTEMTION ########{bcolors.ENDC}
    {bcolors.UNDERLINE}You need to choose option number (1) to have a list for the survey and after choose option number (2) to have Linkedin profiles to export information...!{bcolors.ENDC}
    {bcolors.HEADER}###########################{bcolors.ENDC}\n
    {bcolors.ENDC}
    """

text_error_filter_only_menu = f"""\n
    {bcolors.FAIL}
    {bcolors.HEADER}######## ATTEMTION ########{bcolors.ENDC}
    {bcolors.UNDERLINE}Choose only the option available in the menu!{bcolors.ENDC}
    {bcolors.BOLD}Ex:{bcolors.ENDC} 1, 2, 3, 4 or 5...
    {bcolors.HEADER}###########################{bcolors.ENDC}\n
    {bcolors.ENDC}
    """

text_menu_score = """
    [{}] ({}) - {} ({} records)
"""

text_menu_score_all = """
    [{}] Export all (approximately {} or less) database records.
"""

text_menu_score_header = """
{}{}########## Please choose your NUMBER option (only the last FIVE): ##########{}
"""

text_waiting_login = f"""
    {bcolors.BOLD}{bcolors.BLUE}Waiting login... (Look your Browser){bcolors.ENDC}{bcolors.ENDC}\n
"""

text_menu_score_header_end = """
{}{}#######################################################{}
"""

text_menu_score_option = """
    {}{}{}* Your option (Only numbers)?{}{}
"""

text_waiting_scraping_list_profiles = f"""
    {bcolors.BLUE}Waiting scraping list profiles...{bcolors.ENDC}
    """

text_waiting_export_xls = f"""
    {bcolors.BLUE}Waiting export XLS...{bcolors.ENDC}
    """

text_start_scraping = f"""
    {bcolors.BLUE}Start scraping each profiles...{bcolors.ENDC}
    """

text_already_exists_record = """
    {}Profile {} ALREADY EXISTS record: {}{}
    """

text_weighted_calculation_performed = """
    {}Weighted calculation performed!{}
    """

text_export_finished = """
    {}Export XLS Finished!{}: {}
    """

text_page = """
    {}#### PAGE {} ####{}
    """

text_count_scraping_search = """    ({}) {}{}{} - {}{}{}"""

text_count_scraping_profile_exist = """    ({}/{}) {}{}{} - {}THERE IS REGISTRATION!{}"""

text_profile_registered = """    ({}/{}) {}{} {}REGISTERED{}{}: {}{}{}"""

text_count_scraping_search_exist = """    ({}) {}{}{} - {}THERE IS REGISTRATION!{}"""

text_chrome_install = """ 
    {}{}################################################## ATTEMTION ###################################################\n
    {}

    You need installation: {}{} {}https://www.google.com/chrome/{}\n
    {}{}################################################################################################################{}{}
    """

text_chrome_install_closed = """ 
    {}{}################################################## ATTEMTION ###################################################\n
    {}

    Obs: Chrome can't close before the app is closed, don't close Chrome while it's running.

    May need installation or upgrade: {}{} {}https://www.google.com/chrome/{}\n
    {}{}################################################################################################################{}{}
    """

text_chrome_install_text_closed = f"""
    Chrome closed before the application closed, do not close Chrome at runtime or do the 
    proper installation."""

text_chrome_install_text_cannot_find = f"""
    This computer does not have the Chrome browser, for it to work correctly."""

exception_cannot_find = "unknown error: cannot find Chrome binary"

text_error_score = f"""\n
    {bcolors.FAIL}
    {bcolors.HEADER}######## ATTEMTION ########{bcolors.ENDC}
    {bcolors.UNDERLINE}Error, repeat the procedure!{bcolors.ENDC}
    
    {bcolors.HEADER}###########################{bcolors.ENDC}\n
    {bcolors.ENDC}
    """
text_option_score = f"""
    {bcolors.HEADER}########## Add comma-separated technologies to punctuation ##########{bcolors.ENDC}
    {bcolors.UNDERLINE}Example:{bcolors.ENDC} python, react, node, typescript, react native
    {bcolors.HEADER}#####################################################################{bcolors.ENDC}\n
    {bcolors.BOLD}{bcolors.CYAN}* Add your technologies: {bcolors.ENDC}{bcolors.ENDC}
    """

text_login = f"""
    {bcolors.HEADER}##################################### ATTEMTION ######################################{bcolors.ENDC}
    You need to log in to the browser that was opened, {bcolors.UNDERLINE}Y{bcolors.ENDC} to go and {bcolors.UNDERLINE}N{bcolors.ENDC} to close application.
    {bcolors.HEADER}######################################################################################{bcolors.ENDC}\n
    {bcolors.BOLD}{bcolors.CYAN}* You are logged in? (y/n): {bcolors.ENDC}{bcolors.ENDC}
    """

text_reset = f"""{bcolors.HEADER}
    {bcolors.HEADER}########################################################################## ATTEMTION #########################################################################{bcolors.ENDC}
    Following this operation, your database, logs and spreadsheets that are still in the directory of this software will be permanently deleted from the computer.
    {bcolors.HEADER}##############################################################################################################################################################{bcolors.ENDC}\n
    {bcolors.BOLD}{bcolors.CYAN}* Do you want to do this? (y/n): {bcolors.ENDC}{bcolors.ENDC}
    """

text_login_error = f"""\n
    {bcolors.FAIL}
    {bcolors.HEADER}######## ATTEMTION #########{bcolors.ENDC}
    Just {bcolors.BOLD}Y{bcolors.ENDC} or {bcolors.BOLD}N{bcolors.ENDC} for your choose!
    {bcolors.HEADER}############################{bcolors.ENDC}\n
    {bcolors.ENDC}
    """

text_reset_error = f"""\n
    {bcolors.FAIL}
    {bcolors.HEADER}######### ATTEMTION ##########{bcolors.ENDC}
    Close EXCEL or file ERROR LOG
    {bcolors.HEADER}##############################{bcolors.ENDC}\n
    {bcolors.ENDC}
    """

text_login_its_a_trap = f"""\n
    {bcolors.FAIL}
    {bcolors.HEADER}######################## ATTEMTION ########################{bcolors.ENDC}
    {bcolors.UNDERLINE}You need to login to Linkedin for this application to work.{bcolors.ENDC}
    {bcolors.HEADER}###########################################################{bcolors.ENDC}\n
    {bcolors.ENDC}
    """

text_login_url_base = f"""\n
    {bcolors.FAIL}
    {bcolors.HEADER}######################## ATTEMTION ########################{bcolors.ENDC}
    {bcolors.UNDERLINE}You need to do the linkedin people search, example base URL:{bcolors.ENDC}\n
    Ex: https://www.linkedin.com/search/results/people/
    {bcolors.HEADER}###########################################################{bcolors.ENDC}\n
    {bcolors.ENDC}
    """

text_connect_error = f"""\n
    {bcolors.FAIL}
    {bcolors.HEADER}########### ATTEMTION ###########{bcolors.ENDC}
    {bcolors.FAIL} You need an internet connection!{bcolors.ENDC}
    {bcolors.HEADER}#################################{bcolors.ENDC}\n
    {bcolors.ENDC}
    """

text_database_error = f"""\n
    {bcolors.FAIL}
    {bcolors.HEADER}############ ATTEMTION ############{bcolors.ENDC}
    {bcolors.FAIL} There is a problem in your database!{bcolors.ENDC}
    {bcolors.HEADER}###################################{bcolors.ENDC}\n
    {bcolors.ENDC}
    """
