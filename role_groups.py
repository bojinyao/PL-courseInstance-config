from collections.abc import MutableMapping
from collections import OrderedDict
from itertools import chain

class RoleGroups(MutableMapping):

    def __init__(self, obj : dict):
        assert obj is not None, "RoleGroups: obj is None"
        self.__instructors = OrderedDict()
        self.__tas = OrderedDict()
        self.__students = OrderedDict()

        for email, role in obj.items():
            group = self.__fetch_group(role)
            group[email] = role

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
        try:
            cur_role = self.__getitem__(key)
            if cur_role == value:
                # not change to role
                return
            # role change
            cur_group = self.__fetch_group(cur_role)
            del cur_group[key]
            dest_group = self.__fetch_group(value)
            dest_group[key] = value
        except KeyError:
            # new key
            group = self.__fetch_group(value)
            group[key] = value


    def __delitem__(self, key : str):
        if not isinstance(key, str):
            raise TypeError(f"{key} is not of type str")
        if key in self.__instructors:
            del self.__instructors[key]
        elif key in self.__tas:
            del self.__tas[key]
        elif key in self.__students:
            del self.__students[key]
        else:
            raise KeyError(f"'{key}'")

    def __iter__(self):
        return chain(self.__instructors, self.__tas, self.__students)

    def __len__(self):
        return len(self.__instructors) + len(self.__tas) + len(self.__students)

    def __fetch_group(self, role : str):
        if role == "Instructor":
            return self.__instructors
        elif role == "TA":
            return self.__tas
        elif role == "Student":
            return self.__students
        else:
            raise AssertionError(f"Unknown role \"{role}\"")

