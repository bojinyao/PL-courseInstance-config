from util import _canvas_to_PL_roles

class RolesManager:

    def __init__(self, obj : dict):
        assert obj is not None, "ObjManager: obj cannot be None"
        # attributes
        self.__obj = obj
        self.__warnings = []
        self.__changed = False
        # function calls
        self.__add_user_roles()

    def process_csv(self, reader : dict):
        if not reader: 
            return
        pl_roles = self.__obj["userRoles"]
        for row in reader:
            email = row["Email Address"]
            if email not in pl_roles:
                pl_roles[email] = _canvas_to_PL_roles(row["Role"])
                self.__changed = True

    def process_add_users(self, students : list, tas : list, instructors : list):
        new_users = {
            "Student" : students,
            "TA" : tas,
            "Instructor" : instructors
        }

        pl_roles = self.__obj["userRoles"]
        for role, emails in new_users.items():
            if emails is not None:
                for e in emails:
                    if e not in pl_roles:
                        pl_roles[e] = role
                        self.__changed = True

    def __add_user_roles(self):
        if "userRoles" not in self.__obj:
            self.__obj["userRoles"] = {}
            self.__changed = True

    def is_changed(self) -> bool:
        return self.__changed

    def has_warnings(self) -> bool:
        return len(self.__warnings) > 0

    def iter_warnings(self):
        return self.__warnings.__iter__()

    def clear_warnings(self):
        self.__warnings = []
