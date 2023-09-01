from assistant import AddressBook


def test():
    print("Testing 'pickle_dump' and 'pickle_load' methods of AddressBook ... ", end='')
    my_address_book = AddressBook()
    my_address_book.add_fake_records(1000)
    my_address_book.pickle_dump()
    my_address_book_restored = AddressBook.pickle_load()
    assert str(my_address_book) == str(my_address_book_restored)
    print('passed')
    print("1000 of fake contacts saved in 'address_book.bin")


if __name__ == '__main__':
    test()
