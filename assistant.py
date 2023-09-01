from collections import UserDict
from datetime import datetime, date
from faker import Faker
import json
import pickle
from random import randint, choice


class Field:
    """parent class for fields in records such as Name, Phone, Birthday"""

    def __init__(self, value):
        self.__value = None
        self.value = value

    def __repr__(self):
        return f'Field({repr(self.value)})'

    def __str__(self):
        return f'This is Field with value: {self.value}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    """Class for name field"""

    def __init__(self, name: str):
        super().__init__(name)

    def __repr__(self):
        return f'Name({repr(self.value)})'

    def __str__(self):
        return f'Name: {self.value}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, name: str):
        if type(name) is not str:
            raise TypeError('Name must be string')
        if len(name) < 3:
            raise ValueError('Name is too short. Must be minimum 3 characters')
        if not (name
                .replace(' ', '')
                .replace("'", '')
                .replace('-', '')
                .isalnum()):
            print(name)
            raise ValueError('Name contains not allowed signs')
        self.__value = name


class Phone(Field):
    """Class for phone field"""

    def __init__(self, phone: str):
        super().__init__(phone)

    def __repr__(self):
        return f'Phone({repr(self.value)})'

    def __str__(self):
        result_string = ''
        if len(self.value) > 10:
            result_string += self.value[-15:-10]
        if len(self.value) > 7:
            result_string += f'({self.value[-10:-7]})'
        result_string += f'{self.value[-7:-4]}-{self.value[-4:-2]}-{self.value[-2:]}'
        return result_string

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, phone: str | int):
        phone = str(phone)
        phone = self._sanitize_phone_number(phone)
        if len(phone) < 7:
            raise ValueError('Phone is too short. Must be minimum 7 digits')
        if not phone.isdigit():
            raise ValueError('Phone contains not allowed signs')
        self.__value = phone

    def _sanitize_phone_number(self, phone: str) -> str:
        """
        helper function for deleting all unnecessary signs from phone number
        :param phone: string representing phone number
        :return: sanitized phone number string
        """
        new_phone = (
            phone.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace('*', "")
            .replace('x', "")
            .replace(" ", "")
        )
        return new_phone


class Birthday(Field):
    """Class for field of birthday. Birthday is stored as datetime.date object"""

    def __init__(self, birthday: date | datetime):
        super().__init__(birthday)

    def __repr__(self):
        return f'Birthday({repr(self.value)})'

    def __str__(self):
        return f'{self.value.strftime("%d.%m.%Y")}'

    @property
    def value(self) -> date:
        return self.__value

    @value.setter
    def value(self, birthday: date | datetime):
        if type(birthday) not in (date, datetime):
            raise TypeError('Birthday must be date or datetime object')
        if type(birthday) == datetime:
            birthday = birthday.date()
        curr_date = datetime.now().date()
        if birthday > curr_date:
            raise ValueError('Birthday cannot be the date after today')
        if curr_date.year - birthday.year > 150:
            raise ValueError('Person cannot be such old')
        self.__value = birthday


class Record:
    """
    Class representing the record in address book.

    Attributes:
        name (Name): the name of the contact
        phones (list[Phone]): list of phone numbers of the contact. May be empty
        birthday (Birthday): date of the birth of the contact. Optional
    """

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.__name = None
        self.__birthday = None
        self.name = name
        self.birthday = birthday

        self.phones = list()
        if phone and type(phone) is Phone:
            self.phones.append(phone)

    def __repr__(self):
        return f'Record(name={repr(self.name)}, phones={self.phones}, birthday={repr(self.birthday)})'

    def __str__(self):
        return (f'{self.name.value:<28}|  '
                f'{str(self.birthday) if self.birthday else "":<12}|  ' +
                ', '.join(str(phone) for phone in self.phones))

    @property
    def name(self) -> Name:
        return self.__name

    @name.setter
    def name(self, new_name: Name):
        if self.__name is not None:
            raise AttributeError('Name already exist for this record')
        if type(new_name) is not Name:
            raise TypeError('Wrong type of given name')
        self.__name = new_name

    @property
    def birthday(self) -> Birthday:
        return self.__birthday

    @birthday.setter
    def birthday(self, birth: Birthday):
        if type(birth) is Birthday:
            self.__birthday = birth

    def add_phone(self, phone: Phone) -> None:
        """
        Adds given Phone to list of phones of current contact
        :param phone: Phone obj with value of phone
        :return: None
        """
        self.phones.append(phone)

    def change_phone(self, phone: Phone, new_value: str) -> None:
        """
        changes value in given phone obj with new_value
        :param phone: Phone obj
        :param new_value: str representing phone
        :return: None
        """
        phone.value = new_value

    def delete_phone(self, phone: Phone) -> None:
        """
        removes given phone obj from list of phones in current Record
        :param phone: Phone obj
        :return: None
        """
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise KeyError(f'{self.name} does not have such phone number {phone.value}')

    def delete_all_phones(self) -> None:
        """
        removes all phone numbers in list of phones in current Record
        :return:
        """
        self.phones.clear()

    def days_to_birthday(self) -> int | None:
        """
        calculates and returns number of day to the next birthday.
        returns None if no birthday set in the current Record
        """
        if not self.birthday:
            return None
        curr_date = datetime.now().date()
        curr_year = curr_date.year
        birthday_in_curr_year = self.birthday.value.replace(year=curr_year)
        if curr_date <= birthday_in_curr_year:
            delta = birthday_in_curr_year - curr_date
            return delta.days
        birthday_in_next_year = birthday_in_curr_year.replace(year=curr_year + 1)
        delta = birthday_in_next_year - curr_date
        return delta.days


class AddressBook(UserDict):
    """
    Class representing address book. It is a dictionary with name of the contact as key
    and Record representing this contact as value
    """
    BINARY_FILE = 'address_book.bin'
    JSON_FILE = 'address_book.json'

    def __init__(self):
        super().__init__()
        self.number_records_return = 10

    def __iter__(self):  # implementation through generator using yield (works more efficiently with memory)
        """creating generator which returns list with 'self.number_records_return' Records each time"""
        result = []
        for id_name in self.data:
            result.append(self.data[id_name])
            if len(result) == self.number_records_return:
                yield result
                result = []
        yield result

    # def __iter__(self):  # implementation through iterator a
    #    self.__end_index = 0
    #    self.records = list(self.data.values())
    #    return self

    # def __next__(self):
    #     if self.__end_index >= len(self.records):
    #         raise StopIteration
    #     start = self.__end_index
    #     self.__end_index += self.number_records_return
    #     return self.records[start:self.__end_index]

    def __repr__(self):
        return f'AddressBook({repr(self.data)})'

    def __str__(self):
        h_line = '-----|----------------------------|--------------|------------------------------------------\n'
        result = [h_line, '  #  |            Name            |   Birthday   |  Phones\n', h_line]
        result.extend(self.__get_records_strings())
        result.append(h_line)
        return ''.join(result)

    def __get_records_strings(self) -> list[str]:
        """creates and returns list with numerated string representation of all Records"""
        i, lines = 1, []
        for name in sorted(self.data.keys()):
            lines.append(f'{i:>4} |' + str(self.data[name]) + '\n')
            i += 1
        return lines

    def add_record(self, record: Record):
        """adds Record object to address book"""
        self.data[record.name.value] = record

    def add_fake_records(self, quantity: int):
        """
        fills current address_book with given 'quantity' of fake records
        """
        fake = Faker('uk_UA')

        # populating address_book with fake names and birthdays
        for _ in range(quantity):
            name_str = fake.name()
            while 'пан' in name_str:
                name_str = fake.name()
            name = Name(name_str)
            birth = None
            if randint(1, 10) < 8:  # not every but only 7 of 10 records will be with birthdays
                birth_date = fake.date_of_birth(minimum_age=15)
                birth = Birthday(birth_date)

            rec = Record(name, birthday=birth)
            self.add_record(rec)

        records = list(self.data.values())

        # populate records with fake phones. Some of the records will have no phones and some will have a few phones.
        for _ in range(quantity * 3 // 2):
            phone_str = fake.phone_number()
            phone_number = Phone(phone_str)
            choice(records).add_phone(phone_number)

    def json_dump(self, filename: str = '') -> None:
        """
        saves current AddressBook object in json file with given 'filename'.
        :param filename: str. Optional (if not given then 'self.JSON_FILE' is used)
        :return: None
        """
        filename = filename or self.JSON_FILE

        list_to_save = []
        for rec_id, record in self.data.items():
            list_to_save.append({'name': record.name.value,
                                 'birthday': record.birthday.value.strftime('%d.%m.%Y') if record.birthday else None,
                                 'phones': [str(phone) for phone in record.phones]})

        with open(filename, 'w', encoding='utf-8') as fh:
            json.dump(list_to_save, fh, ensure_ascii=False, indent=4)

    @classmethod
    def json_load(cls, filename: str = ''):
        """
        loads and returns AddressBook object from json file with given 'filename'.
        :param filename: str. Optional (if not given then 'self.JSON_FILE' is used)
        :return: restored AddressBook object
        @rtype: AddressBook
        """
        filename = filename or cls.JSON_FILE
        with open(filename, 'r', encoding='utf-8') as fh:
            unpacked = json.load(fh)
        address_book = AddressBook()
        for user in unpacked:
            user_birthday = None
            if user['birthday']:
                user_birthday = Birthday(datetime.strptime(user['birthday'], '%d.%m.%Y'))
            record = Record(name=Name(user['name']), birthday=user_birthday)
            for phone_str in user['phones']:
                record.add_phone(Phone(phone_str))
            address_book.add_record(record)
        return address_book

    def pickle_dump(self, filename: str = '') -> None:
        """
        saves current AddressBook object in binary file with given 'filename'.
        :param filename: str. Optional (if not given then 'self.BINARY_FILE' is used)
        :return: None
        """
        filename = filename or self.BINARY_FILE
        with open(filename, 'wb') as fh:
            pickle.dump(self, fh)
        pass

    @classmethod
    def pickle_load(cls, filename: str = ''):
        """
        loads and returns AddressBook object from binary file with given 'filename'.
        :param filename: str. Optional (if not given then 'self.BINARY_FILE' is used)
        :return: restored AddressBook object
        @rtype: AddressBook
        """
        filename = filename or cls.BINARY_FILE
        with open(filename, 'rb') as fh:
            unpacked = pickle.load(fh)
        return unpacked

    def search(self, phrase: str, ignore_case=True) -> list[Record]:
        """
        searches for records in fields of which there is
        match with given 'phrase'.
        @param phrase: str that we are looking for
        @param ignore_case: bool. If True then search ignores case of phrase and values
        @return: list of matching records
        """
        result = []
        for rec_id, record in self.data.items():

            user_name = rec_id
            user_birthday = str(record.birthday)
            user_phones = '|'.join(phone.value for phone in record.phones)

            if ignore_case:
                user_name = user_name.lower()
                user_birthday = user_birthday.lower()
                user_phones = user_phones.lower()
                phrase = phrase.lower()

            if (phrase in user_name
                    or phrase in user_birthday
                    or phrase in user_phones):
                result.append(record)
        return result


if __name__ == '__main__':
    # ALL THE TESTS ARE IN SEPARATE FILES
    from Tests.test import test as test1
    from Tests.test_days_to_birthday import test as test2
    from Tests.test_str_and_repr_methods import test as test3
    from Tests.test_filling_address_book_with_records import test as test4
    from Tests.test_pickle_dump_and_pickle_load_functions import test as test5
    from Tests.test_json_dump_and_json_load_functions import test as test6
    from Tests.test_search_method import test as test7

    test4()
    test1()
    test2()
    test3()
    test5()
    test6()
    test7()
