# Naplózó

import config_path
import datetime
import os

logname = "event.txt"

# Logolás .txt-be
def text_to_log(text, path = config_path.path):
    datetime_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = datetime_string + "\t" + text
    print(result)
    with open(os.path.join(path, logname), "a") as file:
        file.write(result + "\n")

# Log törlése
def delete_log(path = config_path.path):
    path = os.path.join(config_path.path, logname)
    try:
        os.remove(path)
        return (path + " sikeresen törölve.")
    except FileNotFoundError:
        return (path + " nem létezik.")
    except Exception as e:
        return ("egyéb hiba: " + e)