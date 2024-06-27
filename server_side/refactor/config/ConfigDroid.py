'''config for path'''

import os
from villog import Logger

class ConfigDroid:
    '''config class'''

    def __init__(
        self,
        root_path: str,
        ftp_name: str,
        o8_login_name: str,
        db_dir: str = None,
        db_name: str = None,
        log_dir: str = None,
        event_dir: str = None,
        event_name: str = None,
        ftp_dir: str = None,
        o8_login_dir: str = None,
        result_dir: str = None,
        user_csv_name: str = None,
        xlsx_name: str = None
    ) -> None:
        # root path
        self.path: str = root_path
        # directory of the database
        self.db_dir: str = db_dir if db_dir else "db"
        # name of the database
        self.db_name: str = db_name if db_name else "db.sqlite3"
        # path of the database directory
        self.db_dir_path: str = os.path.join(self.path, self.db_dir)
        if not os.path.exists(self.db_dir_path):
            os.makedirs(self.db_dir_path)
        # path of the database
        self.db_path: str = os.path.join(self.db_dir_path, self.db_name)
        # directory of the logs
        self.log_dir: str = log_dir if log_dir else "logs"
        # path of the logs directory
        self.log_dir_path: str = os.path.join(self.path, self.log_dir)
        if not os.path.exists(self.log_dir_path):
            os.makedirs(self.log_dir_path)
        # path of the logs backup directory
        self.log_dir_backup: str = os.path.join(self.path, f"{self.log_dir}_backup")
        # path for the event log
        if event_dir:
            event_dir_path: str = os.path.join(self.path, event_dir)
            if not os.path.exists(event_dir_path):
                os.makedirs(event_dir_path)
            self.event_name = os.path.join(event_dir_path, (event_name if event_name else "event.log"))
        else:
            self.event_name = os.path.join(self.path, (event_name if event_name else "event.log"))
        # ftp.json file
        if ftp_dir:
            self.ftp_path: str = os.path.join(self.path, ftp_dir, ftp_name)
        else:
            self.ftp_path: str = os.path.join(self.path, ftp_name)
        # o8_log.json file
        if o8_login_dir:
            self.o8_login_path: str = os.path.join(self.path, o8_login_dir, o8_login_name)
        else:
            self.o8_login_path: str = os.path.join(self.path, o8_login_name)
        # logger
        self.logger = Logger(
            file_path = self.event_name
        )
        # result dir
        if result_dir:
            self.result_path = os.path.join(self.path, result_dir)
        else:
            self.result_path = os.path.join(self.path, "result")
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)
        # csv path
        if user_csv_name:
            self.user_csv_path = os.path.join(self.result_path, user_csv_name)
        else:
            self.user_csv_path = os.path.join(self.result_path, "users.csv")
        # xlsx path
        if xlsx_name:
            self.xlsx_path = os.path.join(self.result_path, xlsx_name)
        else:
            self.xlsx_path = os.path.join(self.result_path, "users.xlsx")

    def get_db_path(self) -> str:
        '''get db path'''
        return self.db_path

    def get_log_path(self) -> str:
        '''get log path'''
        return self.log_dir_path

    def get_event_path(self) -> str:
        '''get event path'''
        return self.event_name
    
    def get_ftp_path(self) -> str:
        '''get ftp path'''
        return self.ftp_path
    
    def get_o8_login_path(self) -> str:
        '''get o8 login path'''
        return self.o8_login_path

    def get_csv_path(self) -> str:
        '''get csv path'''
        return self.user_csv_path
    
    def get_xlsx_path(self) -> str:
        '''get xlsx path'''
        return self.xlsx_path

    def log(self, content: str) -> None:
        '''log content'''
        self.logger.log(content)
