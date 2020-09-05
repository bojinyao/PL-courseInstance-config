from collections.abc import MutableMapping
from collections import OrderedDict
from itertools import chain


class RoleGroups(MutableMapping):
    def __init__(self, userRoles: dict):
        assert userRoles is not None, "RoleGroups: obj is None"
        self.__instructors = OrderedDict()
        self.__tas = OrderedDict()
        self.__students = OrderedDict()

        self.__regrouped = False
        role_state = "Instructor"
        for email, role in userRoles.items():
            group = self.__fetch_group(role)
            group[email] = role
            if role != role_state:
                if (role_state == "Instructor" and role == "TA") or (
                    role_state == "TA" and role == "Student"
                ):
                    role_state = role
                else:
                    self.__regrouped = True

    def is_regrouped(self) -> bool:
        return self.__regrouped

    def __getitem__(self, key: str):
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

    def __setitem__(self, key: str, value: str):
        if not isinstance(key, str):
            raise TypeError(f"{key} is not of type str")
        if value not in ("Instructor", "TA", "Student"):
            raise AssertionError(f'Unknown role: "{value}"')
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

    def __delitem__(self, key: str):
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

    def __fetch_group(self, role: str):
        if role == "Instructor":
            return self.__instructors
        elif role == "TA":
            return self.__tas
        elif role == "Student":
            return self.__students
        else:
            raise AssertionError(f'Unknown role "{role}"')
