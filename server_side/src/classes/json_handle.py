'''A class to handle JSON files'''

import json

class JsonHandle:
    '''A class to handle JSON files'''

    def __init__(self, json_file: str, encoding: str = "utf-8-sig") -> None:
        self.json_file = json_file
        self.encoding = encoding
        self.content = self.read()

    def read(self) -> dict:
        '''read json file'''
        with open(self.json_file, "r", encoding = self.encoding) as json_file:
            return json.load(json_file)

    def change_json_file(self, new_path: str):
        '''change json file'''
        self.json_file = new_path
        self.content = self.read()
