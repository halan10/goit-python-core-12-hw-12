from collections import UserDict
from datetime import datetime
import pickle

        
        
class Field:
    def __init__(self, value):
        if not isinstance(value,str):
            raise ValueError("Value must be a string")
        self._value = None
        self.value = value

    def __str__ (self)->str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)
    
    #setter and getter logic for the value attributes of the Field inheritors
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self,value):
        self._value = value

class Name(Field):
    pass

class Phone(Field):

    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value (self,value):
        if not value.isdigit() or len(value) != 12:
            raise ValueError ("Invalid phone number")
        self._value = value

class Birthday(Field):

    def __init__(self, value):
        self._value = None
        self.value = value

        @property
        def value(self):
            return self._value
        
        @value.setter
        def value(self, new_value):
            try:
                self._value = datetime.strftime(new_value, '%d.%m.%Y')
            except ValueError:
                raise ValueError('Birthday format is :"dd.mm.yyyy"')

class Record:
    def __init__(self,name, phone = None, birthday=None):
        self.name = name
        self.phones = [] 
        self._birthday = birthday if birthday else None
        if phone:
            self.add_phone(phone)

    def add_phone(self, phone):
        self.phones.append(phone)
    
    def add_birthday(self, birthday):
        self.birthday = birthday

    def change_phone(self, index, phone):
        self.phones[index]=phone

    def days_to_birthday(self):
        today = datetime.now().date()
        if not self.birthday:
            return None
        bd = datetime.strftime('%d.%m.%Y').date()
        bd = bd.replace(year = datetime.now().year)
        if today > bd:
            bd = bd.replace(year=datetime.now().year+1)
            difference = bd - today
            return difference.days


    def __repr__(self) -> str:
        return ','.join([p.value for p in self.phones])

class AddressBook(UserDict):
    def add_record(self, record:Record):
        self.data[record.name.value] = record

    def paginator(self, page = 2):
        start = 0
        while True:
            result = list(self.data)[start:start + page]
            if not result:
                break
            yield result
            start += page

    def save_to_file(self, file_name):
        with open(file_name, 'wb') as f:
           return pickle.dump(self,f)
        
    @staticmethod 
    def load_from_file(file_name):
        with open (file_name, 'rb') as f:
            return pickle.load(f)
        
    def find(self, param):
        if len(param)<3:
            return "Sorry, search parameter must be less than 3 characters"
        result = []
        for record in self.values():
            if param is str(record):
                result.append(str(record))
            return '\n'.join(result)

