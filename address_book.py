from collections import UserDict, defaultdict
from datetime import datetime
import pickle


class IncorrectPhoneError(Exception):
    pass


class DateFormatError(Exception):
    pass


class BirthdayAlreadyAddedError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.validate_phone(value)
        self.value = value

    def validate_phone(self, value):
        if len(value) != 10 or not value.isdigit():
            raise IncorrectPhoneError


class Birthday(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def edit_phone(self, old_phone, new_phone):
        new_phone = Phone(new_phone)
        for item in range(len(self.phones)):
            if self.phones[item].value == old_phone:
                self.phones[item] = new_phone

    def find_phone(self, phone):
        for item in self.phones:
            if item.value == phone:
                return phone
        return "No such phone"

    def remove_phone(self, phone):
        removed = False
        for item in self.phones:
            if item.value == phone:
                self.phones.remove(item)
                removed = True
        if not removed:
            print("No such phone for this contact.")

    def add_birthday(self, birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
            if self.birthday == None:
                self.birthday = Birthday(birthday)
            else:
                raise BirthdayAlreadyAddedError
        except ValueError:
            raise DateFormatError

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


def sort_lines_by_weekdays(lines):
    weekday_order = {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
    }
    lines = lines.split("\n")
    sorted_lines = sorted(
        lines, key=lambda line: weekday_order.get(line.split(":")[0], float("inf"))
    )
    result = "\n".join(sorted_lines)
    return result


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        for item in self.data:
            if item == name:
                return self.data[item]

    def delete(self, name):
        try:
            self.data.pop(name)
        except KeyError:
            print("No such contact in AddressBook")

    def get_birthdays_per_week(self):
        next_week_birthdays = defaultdict(list)
        next_week_birthdays_string = ""
        current_date = datetime.today().date()

        for name, record in self.data.items():
            if record.birthday == None:
                continue
            name = name
            birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = birthday.replace(year=current_date.year)
            if birthday_this_year < current_date:
                birthday_this_year = birthday_this_year.replace(
                    year=current_date.year + 1
                )

            delta_days = (birthday_this_year - current_date).days
            if delta_days < 7:
                if birthday_this_year.weekday() == 1:
                    next_week_birthdays["Tuesday"].append(name)
                elif birthday_this_year.weekday() == 2:
                    next_week_birthdays["Wednesday"].append(name)
                elif birthday_this_year.weekday() == 3:
                    next_week_birthdays["Thursday"].append(name)
                elif birthday_this_year.weekday() == 4:
                    next_week_birthdays["Friday"].append(name)
                else:
                    next_week_birthdays["Monday"].append(name)

        for weekday in next_week_birthdays:
            next_week_birthdays_string += (
                f'{weekday}: {", ".join(next_week_birthdays[weekday])}\n'
            )
        next_week_birthdays_string = sort_lines_by_weekdays(
            next_week_birthdays_string.strip()
        )

        if next_week_birthdays_string == "":
            return "Sorry, no birthdays this week"

        return next_week_birthdays_string

    def serialize(self):
        with open("data.bin", "wb") as file:
            pickle.dump(self, file)
