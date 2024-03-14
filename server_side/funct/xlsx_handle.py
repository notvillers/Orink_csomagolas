'''Handles the creation of the .xlsx and its classes'''

import os
from datetime import date
from decimal import Decimal
from unidecode import unidecode
import xlsxwriter
import config_path
from funct.log import text_to_log

class worksheet:
    '''worksheet.name -> name of the worksheet (name of the excel's worksheet)
    worksheet.header -> header (column names)
    worksheet.data -> data of the worksheet, like:
    [
        ["col1 row1", "col2 row1"],
        ["col2 row1", "col2 row2"]
    ]
    worksheet.header_comment -> comment on the headers'''


    def __init__(self, name, header, data, header_comment = []):
        name_length = 31
        self.name = (name if len(name) <= name_length  else name[:name_length])
        self.header = header
        self.data = data
        self.header_comment = header_comment

    def __str__(self):
        return self.name
    
    # Seggesting a column width with min. and max. filter
    def suggest_width(self, col, min_width = 10, max_width = 40):
        '''return a recommended column width'''

        length = min_width
        if self.header:
            if len(str(self.header[col])) > length:
                length = len(str(self.header[col]))
        if self.data:
            for row in self.data:
                if len(str(row[col])) > length:
                    length = len(str(row[col]))

        return (length if length < max_width else max_width)

class workbook:
    '''workbook.name -> name of the workbook (the name of the .xlsx file)
    workbook.content -> worksheet(s), it can be one worksheet class or list[] of worksheet classes
    workbook.xlsx_create(file_path = "directory_path", file_name = "nameofthefile.xlsx") -> exports the workbook to the .xlsx file'''

    def __init__(self, name: str, content):
        self.name = self.remove_accents_from_name(name)
        self.content = content

    def __str__(self):
        return self.name

    # Type checking to handle single worksheet and list[] of worksheets
    def check_type(self):
        '''checks value type'''

        return type(self.content)

    def remove_accents_from_name(self, name):
        '''removes accents from file name'''

        return unidecode(name)

    # Creating the .xlsx
    def xlsx_create(self, file_path: str = config_path.path, file_name: str = ""):
        '''creates xlsx'''

        text_to_log("xlsx_create()")

        # Creating the name of the .xlsx
        file_name = ((self.name + ".xlsx") if file_name == "" else file_name)
        if not file_name.lower().endswith(".xlsx"):
            file_name += ".xlsx"
        excel_file = os.path.join(file_path, file_name)

        # Creating the .xlsx
        file = xlsxwriter.Workbook(excel_file)
        bold_format = file.add_format({"bold": True})
        date_format = file.add_format({'num_format': 'yyyy.mm.dd'})
        number_format = file.add_format({'num_format': '#,##0.00'})

        # Fetching the worksheet(s)
        worksheets = []
        if type(self.content) != list:
            worksheets.append(self.content)
        else:
            for element in self.content:
                worksheets.append(element)
        text_to_log(file_name + " is " + str(len(worksheets)) + (" worksheet:" if len(worksheets) == 1 else " worksheets:"))

        # Creating the worksheet(s)
        for wsheet in worksheets:
            text_to_log(wsheet.name)
            sheet = file.add_worksheet(wsheet.name)
            row, col = 0, 0
            last_row = row
            last_col = col

            # If available, then creating a header
            if wsheet.header:
                sheet.freeze_panes(1, 0)
                for element in wsheet.header:
                    width = wsheet.suggest_width(col)
                    sheet.set_column(col, col, width)
                    sheet.write(row, col, element, bold_format)
                    # If available, then adding comments
                    if wsheet.header_comment:
                        for comment in wsheet.header_comment:
                            if element == comment[0]:
                                sheet.write_comment(row, col, comment[1])
                    col += 1
                    last_col = (col if col > last_col else last_col)

            # If available, then creating the data
            if wsheet.data:
                row += 1
                last_row = (row if row > last_row else last_row)
                for line in wsheet.data:
                    col = 0
                    for element in line:
                        # Checking for basic types
                        if isinstance(element, date):
                            sheet.write_datetime(row, col, element, date_format)
                        elif isinstance(element, Decimal):
                            sheet.write(row, col, element, number_format)
                        else:
                            sheet.write(row, col, element)
                        col += 1
                        last_col = (col if col > last_col else last_col)
                    row += 1
                    last_row = (row if row > last_row else last_row)

            # If header is available, then adding an aoutfilter
            if wsheet.header:
                if last_col != 0:
                    last_col -= 1
                sheet.autofilter(0, 0, last_row, last_col)

        # Closing the .xlsx
        file.close()

        text_to_log("xlsx created")

        return excel_file
