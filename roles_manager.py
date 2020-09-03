from util import _canvas_to_PL_roles

class RolesManager:

    def __init__(self, obj : dict):
        assert obj is not None, "ObjManager: obj cannot be None"
        # attributes
        self.__obj = obj
        self.__warnings = []
        self.__changed = False
        self.__modifid = 0
        self.__added = 0
        self.__deleted = 0
        # function calls
        self.__add_userRoles()

# ======================================================== #
# ========================== API ========================= #
# ======================================================== #

    def process_csv(self, reader : dict):
        if not reader: 
            return
        for row in reader:
            email = row["Email Address"]
            self.__update_role(email, row["Role"])

    def process_add_users(self, students : list, tas : list, instructors : list):
        new_users = {
            "Student" : students,
            "TA" : tas,
            "Instructor" : instructors
        }
        for role, emails in new_users.items():
            if emails is not None:
                for e in emails:
                    self.__update_role(e, role)

    def process_remove_users(self, emails : list):
        if not emails:
            return
        for e in emails:
            self.__remove_role(e)

    def is_changed(self) -> bool:
        return self.__changed

    def has_warnings(self) -> bool:
        return len(self.__warnings) > 0

    def iter_warnings(self):
        return self.__warnings.__iter__()

    def clear_warnings(self):
        self.__warnings = []

    def get_modified(self):
        return self.__modifid

    def get_added(self):
        return self.__added

    def get_deleted(self):
        return self.__deleted

# ======================================================== #
# ======================== Helper ======================== #
# ======================================================== #

    def __update_role(self, email : str, canvas_role : str):
        pl_roles = self.__obj["userRoles"]
        des_role = _canvas_to_PL_roles(canvas_role)
        if email in pl_roles:
            cur_role = pl_roles[email]
            if cur_role != des_role:
                self.__add_warning(f"\"{email}\" role changed from \"{cur_role}\" to \"{des_role}\"")
                pl_roles[email] = des_role
                self.__modifid += 1
                self.__changed = True
        else:
            pl_roles[email] = des_role
            self.__added += 1
            self.__changed = True

    def __remove_role(self, email : str):
        pl_roles = self.__obj["userRoles"]
        if email not in pl_roles:
            self.__add_warning(f"\"{email}\" not found in \"userRoles\"")
        else:
            del pl_roles[email]
            self.__deleted += 1
            self.__changed = True

    def __add_userRoles(self):
        if "userRoles" not in self.__obj:
            self.__obj["userRoles"] = {}
            self.__changed = True

    def __add_warning(self, msg : str):
        self.__warnings.append(msg)