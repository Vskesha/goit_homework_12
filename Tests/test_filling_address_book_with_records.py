from random import randint
from assistant import AddressBook


def test():
    """
    function for testing class AddressBook.
    Fills the addressbook with fake values
    and then shows the records in сhunks of
    given size
    """
    my_address_book = AddressBook()
    number_of_records = randint(40, 60)
    my_address_book.add_fake_records(number_of_records)

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
