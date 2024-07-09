'''csv handle class'''

import os

class CsvMaster:
    '''csv handle class'''

    def __init__(self, path: str, encoding: str = "utf-8-sig"):
        self.path = path
        self.encoding = encoding

    def __is_file_there(self) -> bool:
        '''is file there'''
        return os.path.exists(self.path)

    def __get_file_content(self) -> list[str]:
        '''get file content'''
        if not self.__is_file_there():
            return None
        with open(self.path, "r", encoding=self.encoding) as file:
            content: list[str] = file.readlines()
        return content

    def read(self, separator: str = ",") -> list[list[str]]:
        '''get file as matrix'''
        content: list[str] = self.__get_file_content()
        if not content:
            return None
        matrix: list = []
        for line in content:
            matrix.append(line.strip().split(separator))
        return matrix

    def order_by_element(self, order_by: int = 0) -> None:
        '''order matrix by second element'''
        matrix = self.read()
        if not matrix:
            return None
        sorted_matrix = sorted(matrix, key=lambda x: x[order_by])
        return sorted_matrix
    
    def search_in_line(self, search: str) -> list[list[str]]:
        '''search in line'''
        matrix = self.read()
        if not matrix:
            return None
        new_matrix: list[list[str]] = []
        for line in matrix:
            line_content: str = "".join(line)
            if search in line_content.lower():
                new_matrix.append(line)
        return new_matrix
    
    def search_in_line_by_order(self, search: str, order_by: int = 0) -> list[list[str]]:
        '''search in line by order'''
        matrix = self.search_in_line(search)
        sorted_matrix = sorted(matrix, key=lambda x: x[order_by])
        return sorted_matrix

    def change_path(self, new_path: str) -> None:
        '''change path'''
        self.path = new_path

    def change_encoding(self, new_encoding: str) -> None:
        '''change encoding'''
        self.encoding = new_encoding
