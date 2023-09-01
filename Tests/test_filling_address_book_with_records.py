from random import randint, choice
from assistant import AddressBook, Birthday, Name, Phone, Record
from faker import Faker


def test():
    """
    function for testing class AddressBook.
    Fills the addressbook with fake values
    and then shows the records in сhunks of
    given size
    """
    my_address_book = AddressBook()
    fake = Faker('uk_UA')
    number_or_records = randint(40, 60)

    # populating my_address_book with fake names and birthdays
    for _ in range(number_or_records):
        name_str = fake.name()
        if 'пан' in name_str:
            continue
        name = Name(name_str)
        birth = None
        if randint(1, 10) < 8:  # not every but only 7 of 10 records will be with birthdays
            birth_date = fake.date_of_birth(minimum_age=15)
            birth = Birthday(birth_date)

        rec = Record(name, birthday=birth)
        my_address_book.add_record(rec)

    records = list(my_address_book.data.values())

    # populate records with fake phones. Some of the records will have no phones and some will have a few phones.
    for _ in range(number_or_records * 3 // 2):
        phone_str = fake.phone_number()
        phone_number = Phone(phone_str)
        choice(records).add_phone(phone_number)

    print(my_address_book)
    print('Random filling of AdressBook complete!')
    print('Enter the number N of records to show at each time: ', end='')
    while True:
        try:
            number_records_return = input()
            number_records_return = int(number_records_return)
            if number_records_return < 1:
                print('Number must be greater than zero. Enter correct number: ', end='')
                continue
            my_address_book.number_records_return = number_records_return
            break
        except ValueError:
            print('Enter correct number: ', end='')

    for n_records in my_address_book:
        input(f"\nPress Enter to show next {my_address_book.number_records_return} records: ")
        for record in n_records:
            print(str(record))


if __name__ == '__main__':
    test()
