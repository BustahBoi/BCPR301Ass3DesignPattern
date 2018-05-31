import re
from copy import deepcopy
from abc import ABCMeta, abstractmethod


class Strategy(metaclass=ABCMeta):

    @abstractmethod
    def check(self, data):
        pass


class CheckID(Strategy):

    def check(self, data):
        data = str(data)
        reg_exp = "^[A-Z][\d]{3}$"
        match = re.match(reg_exp, data)
        if match:
            return data
        else:
            return False


class CheckSales(Strategy):

    def check(self, data):
        data = str(data)
        reg_exp = "^[\d]{3}$"
        match = re.match(reg_exp, data)
        if match:
            return data
        else:
            return False


class CheckSalary(Strategy):

    def check(self, data):
        data = str(data)
        reg_exp = "^([\d]{2}|[\d]{3})$"
        match = re.match(reg_exp, data)
        if match:
            return data
        else:
            return False


class CheckAge(Strategy):

    def check(self, data):
        data = str(data)
        reg_exp = "^[\d]{2}$"
        match = re.match(reg_exp, data)
        if match:
            return data
        else:
            return False


class CheckGender(Strategy):

    def check(self, data):
        data = str(data)
        reg_exp = "^(M|F)$"
        match = re.match(reg_exp, data)
        if match:
            return data
        else:
            male = re.match("((m|M)ale)$", data)
            if male:
                return "M"
            female = re.match("((f|F)emale)$", data)
            if female:
                return "F"
            else:
                return False


class CheckBMI(Strategy):

    def check(self, data):
        reg_exp = "^(Normal|Overweight|Obesity|Underweight)$"
        match = re.match(reg_exp, data.capitalize())
        if match:
            return data.capitalize()
        else:
            return False


class CheckBirthday(Strategy):

    def check(self, data):
        reg_exp = "^(0[1-9]|[1-2][0-9]|3(0|1))(-|/)(0[1-9]|1[0-2])(-|/)(19|20)[0-9]{2}$"
        match = re.match(reg_exp, data)
        if match:
            return data
        else:
            match = re.compile("(/|\\|.|:|;|,|_)")
            if match.search(data):
                data = match.sub('-', data)
                return data
            else:
                return False


class CheckContext:
    def __init__(self, strategy):
        self.__strategy = strategy

    def check(self, value):
        return self.__strategy.check(value)


class Validator:
    def __init__(self):
        self.temp_dict = dict()
        self.valid_dict = dict()

    def checker(self, row):
        result = False
        for key, value in row.items():
            result = self.check(key, value)
            if result:
                self.push_value(key, result)
                result = True
            else:
                break
        return result

    def check(self, key, value):
        key = key.lower()
        strategy = self.get_strategy(key)
        if strategy:
            context = CheckContext(strategy)
            result = context.check(value)
            if result:
                return result
            else:
                return False
        else:
            return False

    def get_strategy(self, key):
        strategies = {"id": CheckID(),
                      "gender": CheckGender(),
                      "age": CheckAge(),
                      "sales": CheckSales(),
                      "bmi": CheckBMI(),
                      "salary": CheckSalary(),
                      "birthday": CheckBirthday()}
        try:
            return strategies[key]
        except KeyError:
            return False

    @staticmethod
    def xlsx_date(a_date):
        return a_date.date().strftime("%d-%m-%Y")

    def save_dict(self, loaded_dict):
        for empno, row in loaded_dict.items():
            b = self.checker(row)
            if b is False:
                print("Error at entry: " + str(empno))
            else:
                self.push_row(empno)
        return self.return_dict()

    def push_value(self, key, value):
        self.temp_dict[key] = value

    def push_row(self, empno):
        temp = deepcopy(self.temp_dict)
        if len(temp) == 7:
            self.valid_dict[empno] = temp
        self.temp_dict = dict()

    def return_dict(self):
        return self.valid_dict

