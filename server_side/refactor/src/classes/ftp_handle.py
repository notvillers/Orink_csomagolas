'''ftp client class'''

import os
from ftplib import FTP
from villog import Logger

class FTPHandle:
    '''ftp client class'''

    def __init__(self, hostname: str, username: str, password: str, logger: Logger = None) -> None:
        self.hostname = hostname
        self.username = username
        self.__password = password
        self.logger = logger

    def __str__(self) -> str:
        return f"{self.username}@{self.hostname}"

    def __log(self, content: str) -> None:
        '''log content'''
        if self.logger:
            self.logger.log(content)
        else:
            print(content)

    def list_files(self, remote_dir: str) -> list:
        '''list files in a directory'''
        with FTP(self.hostname) as ftp:
            ftp.login(self.username, self.__password)
            ftp.cwd(remote_dir)
            files =[]
            for item in ftp.mlsd():
                if item[1]['type'] != 'dir':
                    files.append(item[0])
            return files
        
    def list_dirs(self, remote_dir: str) -> list:
        '''list directories in a directory'''
        with FTP(self.hostname) as ftp:
            ftp.login(self.username, self.__password)
            ftp.cwd(remote_dir)
            dirs = []
            for item in ftp.mlsd():
                if item[1]['type'] == 'dir':
                    dirs.append(item[0])
            return dirs

    def upload(self, local_file: str, remote_dir: str, remote_filename: str) -> None:
        '''upload file'''
        with FTP(self.hostname) as ftp:
            ftp.login(self.username, self.__password)
            ftp.cwd(remote_dir)
            with open(local_file, "rb") as local_file:
                ftp.storbinary(f"STOR {remote_filename}", local_file)
                if self.logger:
                    self.__log(f"Uploaded {local_file} to {remote_dir}/{remote_filename}")
                else:
                    self.__log(f"Uploaded {local_file} to {remote_dir}/{remote_filename}")

    def download(self, remote_file: str, remote_dir: str, local_filename: str) -> None:
        '''download a file'''
        with FTP(self.hostname) as ftp:
            ftp.login(self.username, self.__password)
            ftp.cwd(remote_dir)
            with open(local_filename, "wb") as local_file:
                ftp.retrbinary(f"RETR {remote_file}", local_file.write)
                if self.logger:
                    self.__log(f"Downloaded {remote_dir}/{remote_file} to {local_filename}")
                else:
                    self.__log(f"Downloaded {remote_dir}/{remote_file} to {local_filename}")

    def download_files_with_extension(self, remote_dir: str, local_dir: str, extension: str) -> None:
        '''download all db files'''
        with FTP(self.hostname) as ftp:
            ftp.login(self.username, self.__password)
            ftp.cwd(remote_dir)
            extension = extension if extension.startswith(".") else f".{extension}"
            files: list = ftp.nlst()
            filtered_files: list = [file for file in files if file.lower().endswith(extension.lower())]
            for file in filtered_files:
                local_filename: str = file.split("/")[-1]
                local_file_path: str = os.path.join(local_dir, local_filename)
                with open(local_file_path, "wb") as local_file:
                    ftp.retrbinary(f"RETR {file}", local_file.write)
                    if self.logger:
                        self.__log(f"Downloaded {file} to {local_file_path}")
                    else:
                        self.__log(f"Downloaded {file} to {local_file_path}")

    def delete_file(self, remote_dir: str, remote_filename: str) -> None:
        '''delete a file'''
        with FTP(self.hostname) as ftp:
            ftp.login(self.username, self.__password)
            ftp.cwd(remote_dir)
            ftp.delete(remote_filename)
            if self.logger:
                self.__log(f"Deleted {remote_dir}/{remote_filename}")
            else:
                self.__log(f"Deleted {remote_dir}/{remote_filename}")
