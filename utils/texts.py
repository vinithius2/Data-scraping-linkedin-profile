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
    #                         |_|            |___/ {bcolors.ENDC}
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
     {bcolors.UNDERLINE}...closing app{bcolors.ENDC}
    """

text_option = f"""
    {bcolors.HEADER}########## Please choose your NUMBER option: ##########{bcolors.ENDC}\n
    {bcolors.BOLD}{bcolors.BLUE}(1){bcolors.ENDC}{bcolors.ENDC} Search profiles and save list in database;\n
    {bcolors.BOLD}{bcolors.BLUE}(2){bcolors.ENDC}{bcolors.ENDC} Scraping data each profile from database;\n
    {bcolors.BOLD}{bcolors.BLUE}(3){bcolors.ENDC}{bcolors.ENDC} Weighted calculation score profiles and Export XLS;\n
    {bcolors.BOLD}{bcolors.BLUE}(4){bcolors.ENDC}{bcolors.ENDC} {bcolors.GREEN}🠕🠕{bcolors.ENDC} All of the above {bcolors.UNDERLINE}(1,2,3){bcolors.ENDC} {bcolors.GREEN}🠕🠕{bcolors.ENDC}.\n
    {bcolors.BOLD}{bcolors.BLUE}(5){bcolors.ENDC}{bcolors.ENDC} {bcolors.RED}✖{bcolors.ENDC} CLOSE this app {bcolors.RED}✖{bcolors.ENDC}.\n
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

text_waiting_login = f"{bcolors.BOLD}{bcolors.BLUE}Waiting login...{bcolors.ENDC}{bcolors.ENDC}"
