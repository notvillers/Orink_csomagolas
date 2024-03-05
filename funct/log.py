'''Logger'''

import datetime
import os
import config_path

LOGNAME = "event.txt"
LOG_PATH = os.path.join(config_path.path, LOGNAME)

# Logs to logfile
def text_to_log(text, path = LOG_PATH):
    '''logs to LOGNAME with datetime'''
    datetime_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = datetime_string + "\t" + text
    print(result)
    with open(path, "a", encoding = "utf-8") as file:
        file.write(result + "\n")

# Deletes log
def delete_log(path = LOG_PATH):
    '''deletes LOGNAME'''
    try:
        os.remove(path)
        return (path + " sikeresen törölve.")
    except FileNotFoundError:
        return (path + " nem létezik.")
    except Exception as e:
        return ("egyéb hiba: " + e)