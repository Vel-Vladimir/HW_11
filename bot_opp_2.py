from collections import UserDict
from datetime import datetime

class Birthday:
    def __init__(self, day_birth: str):
        self.__value = None
        self.value = day_birth

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, day_birth):
        """
        :param day_birth: day.month (23.07)
        :return:
        """
        day_month = day_birth.split(".")
        if len(day_month) == 2 and 0 < int(day_month[0]) < 32 and 0 < int(day_month[1]) < 13:
            self.__value = (int(day_month[0]), int(day_month[1]))
        else:
            return f"Birthday {day_birth} not in right format. Right format 'Day.Month' (31.12)"

    def __repr__(self):
        return str(self.__value)

class Phone:
    def __init__(self, phone_number: str):
        self.__value = None
        self.value = phone_number

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone_number):
        if phone_number.isdigit() and len(phone_number) == 10:
            self.__value = phone_number
        else:
            return f"Phone number {phone_number} not in right format. Right format 0501234567"

    def __repr__(self):
        return self.__value


class Name:
    def __init__(self, name: str):
        self.value = name

    def __repr__(self):
        return self.value


class Record:
    def __init__(self, name: Name, phone: Phone = None, birth_day: Birthday = None):
        self.phones = [phone]
        self.name = name
        self.birthday = birth_day

    def __repr__(self):
        return f'Record({self.name}, {[ph.value for ph in self.phones]}, {self.birthday})'

    def add_phone(self, phone_to_add: Phone):
        for exist_phone in self.phones:
            if phone_to_add.value == exist_phone.value:
                return f"You try to add phone {phone_to_add} that already exists"
        self.phones.append(phone_to_add)

    def del_phone(self, phone: Phone):
        try:
            self.phones.remove(phone)
        except ValueError:
            return f"You try to delete number {phone} that is absent in the list!"

    def edit_phone(self, current_phone: Phone, new_phone: Phone):
        try:
            index = self.phones.index(current_phone)
            self.phones[index] = new_phone
        except ValueError:
            return f"You try to edit number {current_phone} that is absent in the list!"

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birth_day = datetime(year=today.year + 1, month=self.birthday.value[1], day=self.birthday.value[0])
            delta = next_birth_day - today
            return f"{delta.days} days left to the next birth day."

class AddressBookIterator:
    def __init__(self, number_records, address_book):
        self.number_records = number_records
        self.address_book = address_book
        self.start = 0
        self.stop = number_records
        self.keys = tuple(address_book.keys())


    def __next__(self):
        res = []
        for key in self.keys[self.start:self.stop]:
            res.append((key, self.address_book[key]))
        if res == []:
            raise StopIteration
        self.start = self.stop
        self.stop += self.number_records
        return res


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def iterator(self, number_records):
        return AddressBookIterator(number_records, self.data)

if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('1234567890')
    day = Birthday("24.07")
    rec = Record(name, phone, day)

    name2 = Name('Ted')
    phone2 = Phone('4444444')
    rec2 = Record(name2, phone2)

    name3 = Name('Bob')
    phone3 = Phone('55555555')
    rec3 = Record(name3, phone3)

    name4 = Name('Clod')
    phone4 = Phone('6666666')
    rec4 = Record(name4, phone4)
    ab = AddressBook()
    ab.add_record(rec)
    ab.add_record(rec2)
    ab.add_record(rec3)
    ab.add_record(rec4)
    print(rec.days_to_birthday())
    print(ab)
    iter = ab.iterator(2)
    while True:
        try:
            print(next(iter))
        except StopIteration:
            break

    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'
