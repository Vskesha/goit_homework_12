# goit_homework_10
AddressBook using OOP

`assistant.py` contains classes `AddressBook`, `Record`, `Field`, `Name`, `Birthday` and `Phone`

AddressBook's iterator can return all Records in parts of given size

You can save your AddressBook to binary file using method `pickle_dump(self, filename: str = '')'`
and to json file using method `json_dump(self, filename: str = '')`.

Also you are able to unpack data from binary file with class method `pickle_load(cls, filename: str = '')`
and from json file with `json_load(cls, filename: str = '')`.

You can search some text in your Addressbook using method `search(self, phrase: str, ignore_case=True) -> list[Record]`
It returns list with matching records.

method `days_to_birthday` of class `Record` calculates and returns number of day to the next birthday.



###### P.S. Inner logic and CLI will have been developed.
