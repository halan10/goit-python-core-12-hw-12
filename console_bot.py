from entity import *

contact_book = AddressBook()
contact_book.load_from_file('contact_book.bin')
def input_error(func):
        def wrapper(*args):
                try:
                        return func(*args)
                except IndexError:
                        return "Not enough params."
                except KeyError:
                        return "Enter user name."
                except ValueError:
                        return "Give me name please."
        return wrapper

def hello(*args):
        return "Hello. How can I help You?"

@input_error
def add(*args):
        list_of_param = args[0].split()
        name = Name(list_of_param[0])
        phone = Phone(list_of_param[1])
        birthday = Birthday(list_of_param[2])
        new_user = Record(name, phone, birthday)
        contact_book.add_record(new_user)
        contact_book.save_to_file('contact_book.bin')
        if not name:
                raise KeyError()
        return f"name: {name.value}, phone: {phone.value}, birthday: {birthday.value}"

def show_all(*args):

        iter_obj = contact_book.paginator()

        for records in iter_obj:
                result = []
                for i in records:
                        result.append(f"{i}:{contact_book[i]}")
                print (result)


@input_error
def get_phone(*args):
        name = args[0]
        if name in contact_book.data:
                for k,v in contact_book.data.items():
                        record = contact_book.data[k]
                        if name == k:
                                return f"{k}:{', '.join(str(num)for num in record.phones)}"
        raise KeyError


@input_error
def change(*args):
        list_of_param = args[0].split()
        name = Name(list_of_param[0])
        phone = Phone(list_of_param[1])
        update_user  = contact_book[name.value]
        update_user.change_phone(0,phone)
        contact_book.save_to_file('contact_book.bin')
        if not name:
                raise KeyError()
        return f"User {name.value} has changed the phone to {phone.value}"

def no_command(*args):
        return "Unknown command, please try again."

def find(*args):
        contact_book.find(args[0])


COMMANDS = {hello: 'hello',
            add: 'add',
            show_all: 'show all',
            get_phone: 'phone',
            change: 'change',
            find: 'find'
        }

def command_handler(text):
        for command, kword in COMMANDS.items():
                if text.startswith(kword):
                        return command, text.replace(kword, '').strip()
        return no_command, None
def main():
        
        while True:
                user_input = input(">>>>")
                exit_commands = ['good buy', 'exit', 'close', '.']
                contact_book.save_to_file('contact_book.bin')

                if user_input.lower() in exit_commands:
                        print ("Good bye!")
                        break

                command,data = command_handler(user_input.lower())
                print(command(data))



if __name__ == '__main__':
        main()