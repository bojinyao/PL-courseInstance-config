from collections.abc import MutableMapping
from collections import OrderedDict

class RoleGroups(MutableMapping):

    def __init__(self, obj : dict):
        assert obj is not None, "RoleGroups: obj is None"
        self.__instructors = OrderedDict()
        self.__tas = OrderedDict()
        self.__students = OrderedDict()

        for email, role in obj.items():
            if role == "Instructor":
                self.__instructors[email] = "Instructor"
            elif role == "TA":
                self.__tas[email] = "TA"
            elif role == "Student":
                self.__students[email] = "Student"
            else:
                raise AssertionError(f"Unknown role: \"{role}\"")

    def __getitem__(self, key : str):
        if not isinstance(key, str):
            raise TypeError(f"{key} is not of type str")
        if key in self.__instructors:
            return self.__instructors[key]
        elif key in self.__tas:
            return self.__tas[key]
        elif key in self.__students:
            return self.__students[key]
        else:
            raise KeyError(f"'{key}'")

    def __setitem__(self, key : str, value : str):
        if not isinstance(key, str):
            raise TypeError(f"{key} is not of type str")
        if not isinstance(value, str):
            raise TypeError(f"{value} is not of type str")
        if value == "Instructor":
            self.__instructors[key] = "Instructor"
        elif value == "TA":
            self.__tas[key] = "TA"
        elif value == "Student":
            self.__students[key] = "Student"
        else:
            raise TypeError(f"Unknown role \"{value}\"")

    def __delitem__(self, key : str):
        ...

    def __iter__(self):
        ...

    def __len__(self):
        ...
