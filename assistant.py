from collections import UserDict
from datetime import datetime, date


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
        if not name.replace(' ', '').replace("'", '').isalnum():
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

    def add_record(self, record: Record):
        """adds record obj to address book"""
        self.data[record.name.value] = record

    def __get_records_strings(self) -> list[str]:
        """creates and returns list with numerated string representation of all Records"""
        i, lines = 1, []
        for name in sorted(self.data.keys()):
            lines.append(f'{i:>4} |' + str(self.data[name]) + '\n')
            i += 1
        return lines


if __name__ == '__main__':
    # ALL THE TESTS ARE IN SEPARATE FILES
    from Tests.test import test as test1
    from Tests.test_days_to_birthday import test as test2
    from Tests.test_str_and_repr_methods import test as test3
    from Tests.test_filling_address_book_with_records import test as test4

    test4()
    test1()
    test2()
    test3()
