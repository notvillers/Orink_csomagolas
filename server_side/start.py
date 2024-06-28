'''start script'''

from os import path as ospath
from config.ConfigDroid import ConfigDroid
from src.main import main as main_main


def main() -> None:
    '''main function'''
    droideka = ConfigDroid(
        root_path = ospath.dirname(__file__),
        db_name = "csomagolas.db",
        log_dir = "logs",
        ftp_dir = "config",
        ftp_name = "ftp.json",
        o8_login_dir = "config",
        o8_login_name = "login.json"
    )

    droideka.log("start")

    main_main(droideka)

if __name__ == "__main__":
    main()
