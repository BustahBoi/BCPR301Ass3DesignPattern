from pathlib import Path, PurePosixPath
from abc import ABCMeta, abstractmethod
from csv import DictReader as CSVDictReader
from openpyxl import load_workbook, utils
from datetime import datetime, date
from interpreter.validator import Validator


class FileHandler:
    def __init__(self):
        self.filename = None
        self.file_type = None

    def load(self, filename):
        self.filename = filename

    def set_file(self):
        suffix = PurePosixPath(self.filename).suffix
        print(suffix)
        file_types = {
            '.csv': CSVReader(self.filename),
            '.xlsx': XLSXReader(self.filename),
            '.txt': TXTReader(self.filename)
        }
        self.file_type = file_types[suffix]

    def get_process_data(self):
        self.set_file()
        self.file_type.do_process_data()
        return self.file_type.get_file()


class FileReader(metaclass=ABCMeta):
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def do_process_data(self):
        self.load_document()
        self.get_file_data()
        self.parse_data()
        self.validate_data()

    # hook operation
    def load_document(self):
        self.file = open(self.filename)

    @abstractmethod
    def get_file_data(self):
        pass

    @abstractmethod
    def parse_data(self):
        pass

    def validate_data(self):
        validate = Validator()
        self.file = validate.save_dict(self.file)

    def get_file(self):
        return self.file


class XLSXReader(FileReader):

    def load_document(self):
        self.file = load_workbook(self.filename)
        sheet_name = self.file.sheetnames[0]
        self.file = self.file[sheet_name]

    def get_file_data(self):
        result = list()
        for row in self.file.rows:
            result_row = list()
            for cell in row:
                result_row.append(cell.value)
            result.append(result_row)
        self.file = result

    def parse_data(self):
        result = dict()
        titles = self.file[0]
        row_num = 1
        for row in self.file:
            counter = 0
            if row is not self.file[0]:
                result_row = dict()
                for cell in row:
                    result_row[titles[counter]] = cell
                    if isinstance(cell, datetime):
                        cell = Validator.xlsx_date(cell)
                    result_row[titles[counter]] = cell
                    counter = counter + 1
                result[row_num] = result_row
                row_num = row_num + 1
        self.file = result


class CSVReader(FileReader):

    def get_file_data(self):
        self.file = CSVDictReader(self.file)

    def parse_data(self):
        result = dict()
        row_num = 1
        for row in self.file:
            result_row = dict()
            for key in row:
                result_row[key] = row.get(key)
            result[row_num] = result_row
            row_num = row_num + 1
        self.file = result


class TXTReader(FileReader):

    def get_file_data(self):
        lines = list()
        for row in self.file:
            items = row.split(',')
            items[6] = items[6].replace('\n', '')
            lines.append(items)
        self.file = lines

    def parse_data(self):
        result = dict()
        row_num = 1
        titles = self.file[0]
        for row in self.file:
            if row is not self.file[0]:
                title = 0
                result_row = dict()
                for item in row:
                    result_row[titles[title]] = item
                    title += 1
                result[row_num] = result_row
                row_num += 1
        self.file = result

