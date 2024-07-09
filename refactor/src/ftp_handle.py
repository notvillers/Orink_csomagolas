'''FTP handler'''

import os
from time import sleep
from ftplib import FTP
from villog import Logger
from ping3 import ping

class Client:
    '''FTP client'''

    def __init__(self,
        hostname: str,
        username: str,
        password: str,
        do_log: bool = True,
        logger: Logger = None
    ):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.do_log = do_log
        self.logger = logger

    def __str__(self):
        return self.username + "@" + self.hostname

    def __log(self, content) -> None:
        '''logs content'''
        if self.do_log:
            if self.logger:
                self.logger.log(content)
            else:
                print(content)

    def __ping(self, wait_s: int = 10, retry_attempt: int = 10) -> bool:
        '''pings the server'''
        response_time: int = ping(self.hostname)
        if response_time or response_time == 0.0:
            self.__log(f"{self.hostname} reached")
            return True
        self.__log(f"{self.hostname} not reached, retrying in {wait_s} second(s)")
        if retry_attempt > 1:
            sleep(wait_s)
            self.__ping(retry_attempt - 1)
            self.__log(f"Can't reach {self.hostname} after {retry_attempt} attempts, aborting...")
        return False

    def ping(self):
        '''pings the server'''
        return self.__ping(wait_s = 5, retry_attempt = 1)

    def upload(self, local_file_path: str, remote_directory: str, remote_filename: str) -> str:
        '''uploads a file'''
        if self.__ping():
            with FTP(self.hostname) as ftp:
                ftp.login(user = self.username, passwd = self.password)

                ftp.cwd(remote_directory)

                with open(local_file_path, "rb") as local_file:
                    ftp.storbinary(f'STOR {remote_filename}', local_file)

                self.__log(f"File '{local_file_path}' uploaded to '{remote_directory}/{remote_filename}'")
            return f"File '{local_file_path}' uploaded to '{remote_directory}/{remote_filename}'"
        return None

    def download(self, remote_file_path: str, local_directory: str, local_filename: str) -> str:
        '''downloads a file'''
        if self.__ping():
            with FTP(self.hostname) as ftp:
                ftp.login(user = self.username, passwd = self.password)

                ftp.cwd(remote_file_path)

                with open(os.path.join(local_directory, local_filename), "wb") as local_file:
                    ftp.retrbinary(f'RETR {local_filename}', local_file.write)

                self.__log(f"File '{remote_file_path}/{local_filename}' downloaded to '{local_directory}'")
            return f"File '{remote_file_path}/{local_filename}' downloaded to '{local_directory}'"
        return None
