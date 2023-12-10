from address_book import (
    IncorrectPhoneError,
    DateFormatError,
    BirthdayAlreadyAddedError,
    Record,
    AddressBook,
    pickle,
)
import os


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "No such contact."
        except IndexError:
            return "Please enter contact name."
        except AttributeError:
            return "Please double check entering information and try again."
        except IncorrectPhoneError:
            return "Phone must be 10 digits."
        except DateFormatError:
            return "Date must be in DD.MM.YYYY format."
        except BirthdayAlreadyAddedError:
            return "Birthday already added to this contact."

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book):
    name, phone = args
    new_record = Record(name)
    new_record.add_phone(phone)
    book.add_record(new_record)
    return "Contact added."


@input_error
def change_contact(args, book):
    name, new_phone = args
    contact_to_change = book.find(name)
    old_phone = contact_to_change.phones[0].value
    contact_to_change.edit_phone(old_phone, new_phone)
    return "Contact changed."


@input_error
def get_phone(args, book):
    name = args[0]
    record = book.find(name)
    return f'phones: {"; ".join(p.value for p in record.phones)}'


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    return record.birthday.value


@input_error
def get_all_contacts(book):
    if book.data == {}:
        return "You have no contacts."
    result = ""
    for record in book.data.values():
        result += str(record) + "\n"
    return result.rstrip()


@input_error
def show_next_week_birthdays(book):
    if book.data == {}:
        return "You have no contacts."
    return book.get_birthdays_per_week()


def main():
    if os.path.getsize("data.bin") == 0:
        book = AddressBook()
    else:
        with open("data.bin", "rb") as file:
            book = pickle.load(file)
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            book.serialize()
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_phone(args, book))
        elif command == "all":
            print(get_all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(show_next_week_birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
