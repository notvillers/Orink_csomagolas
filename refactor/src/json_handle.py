'''json handle'''

import json

class JsonManager:
    '''json handle'''

    def __init__(self, path: str, encoding: str = "utf-8-sig"):
        self.path = path
        self.encoding = encoding

    def read(self) -> dict:
        '''read json'''
        with open(self.path, "r", encoding = self.encoding) as file:
            return json.load(file)
    
    def write(self, data: dict) -> None:
        '''write json'''
        with open(self.path, "w", encoding = self.encoding) as file:
            json.dump(data, file, indent = 4)

    def update(self, data: dict) -> None:
        '''update json'''
        old_data = self.read()
        old_data.update(data)
        self.write(old_data)