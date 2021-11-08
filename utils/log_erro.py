import datetime
import os
from pathlib import Path


def __get_directory():
    path_parent = "scrapingLinkedinProfiles"
    path_absolute = Path("/")
    directory_main = os.path.join(path_absolute.parent.absolute(), path_parent)
    path_parent_logs = os.path.join(directory_main, "logs")
    directory_logs = os.path.join(path_absolute.parent.absolute(), path_parent_logs)
    name_file = datetime.datetime.now().strftime("%d_%m_%Y_%H")
    path_logs = os.path.join(directory_logs, f"{name_file}.txt")
    return path_logs


def log_erro(e):
    path_logs = __get_directory()
    now = datetime.datetime.now()
    f = open(path_logs, "a")
    f.write("[{}] {}\n".format(str(now), e))
    f.close()
