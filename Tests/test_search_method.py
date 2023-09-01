from assistant import AddressBook, Record, Name, Birthday, Phone
from datetime import date


def test():
    address_book = AddressBook()
    address_book.add_record(Record(name=Name('abc'),
                                   phone=Phone("1(972)2664875")))
    address_book.add_record(Record(name=Name('def'),
                                   phone=Phone('451-972-22')))
    address_book.add_record(Record(name=Name('ab1972c'),
                                   birthday=Birthday(date(year=1988, month=3, day=5))))
    address_book.add_record(Record(name=Name('ghi'),
                                   phone=Phone('4536456446'),
                                   birthday=Birthday(date(year=1972, month=5, day=3))))
    address_book.add_fake_records(1000)
    search_result = address_book.search('1972')
    print('\nResults for searching "1972" in records:')
    for record in search_result:
        print(str(record))
    assert len(search_result) >= 4
    print("Test of method AddressBook.search ... passed")

    while True:
        phrase = input("\nType something to search for ('e' or 'q' to exit): ")
        if phrase in ('e', 'q'):
            break
        search_result = address_book.search(phrase)
        if search_result:
            print(f'Results for searching "{phrase}" in records:')
            for record in search_result:
                print(str(record))
        else:
            print(f'There is not result for "{phrase}".')


if __name__ == '__main__':
    test()
