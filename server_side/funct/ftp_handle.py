'''FTP handler'''

import os
from ftplib import FTP
from funct.log import text_to_log

class Client:
    '''FTP client'''

    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
    
    def __str__(self):
        return self.username + "@" + self.hostname
    
    def upload(self, local_file_path, remote_directory, remote_filename):
        '''uploads a file'''
        if remote_directory is None:
            remote_directory = '/'
        with FTP(self.hostname) as ftp:
            ftp.login(user = self.username, passwd = self.password)

            ftp.cwd(remote_directory or '/')

            with open(local_file_path, "rb") as local_file:
                ftp.storbinary(f'STOR {remote_filename}', local_file)

            text_to_log(f"File '{local_file_path}' uploaded to '{remote_directory}/{remote_filename}'")

            return True


    def download(self, remote_file_path, local_directory, local_filename):
        '''downloads a file'''
        with FTP(self.hostname) as ftp:
            ftp.login(user = self.username, passwd = self.password)

            ftp.cwd(remote_file_path)

            with open(local_directory + local_filename, "wb") as local_file:
                ftp.retrbinary(f'RETR {local_filename}', local_file.write)

            text_to_log(f"File '{remote_file_path}/{local_filename}' downloaded to '{local_directory}'")

            return True


    def download_all_db_files(self, remote_directory, local_directory):
        '''downloads all .db files from the remote directory'''
        with FTP(self.hostname) as ftp:
            ftp.login(user=self.username, passwd=self.password)
            ftp.cwd(remote_directory)
            file_list = ftp.nlst()
            db_files = [file for file in file_list if file.endswith('.db')]
            for db_file in db_files:
                local_filename = db_file.split('/')[-1]
                local_file_path = os.path.join(local_directory, local_filename)
                with open(local_file_path, "wb") as local_file:
                    ftp.retrbinary(f'RETR {db_file}', local_file.write)
                text_to_log(f"File '{db_file}' downloaded to '{local_file_path}'")
            return True