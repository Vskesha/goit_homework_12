from datetime import date, datetime
from assistant import Birthday, Name, Record


def test():
    print("Test of method Record.days_to_birthday .....", end=' ')
    date_of_test = date(year=2023, month=8, day=21)
    delta = datetime.now().date() - date_of_test

    birth_date = date(year=2019, month=10, day=24)
    birth = Birthday(birth_date)
    rec = Record(Name('Vasya'), birthday=birth)
    assert rec.days_to_birthday() == 64 - delta.days

    birth_date = date(year=1900, month=8, day=18)
    birth.value = birth_date
    assert rec.days_to_birthday() == 363 - delta.days

    print("passed")


if __name__ == '__main__':
    test()
