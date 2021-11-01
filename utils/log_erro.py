import os
from pathlib import Path
import datetime


def __get_directory():
    path_parent = "scrapingLinkedinProfiles"
    path_absolute = Path("/")
    directory_main = os.path.join(path_absolute.parent.absolute(), path_parent)
    path_parent_logs = os.path.join(directory_main, "logs")
    directory_logs = os.path.join(path_absolute.parent.absolute(), path_parent_logs)
    name_file = datetime.datetime.now().strftime("%d_%m_%Y")
    path_logs = os.path.join(directory_logs, f"{name_file}.txt")
    return path_logs


def log_erro(e, msg="ERRO"):
    path_logs = __get_directory()
    now = datetime.datetime.now()
    f = open(path_logs, "a")
    f.write("[{}] {}".format(str(now), e))
    f.close()