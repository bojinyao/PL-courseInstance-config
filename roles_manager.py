from util import _canvas_to_PL_roles
from role_groups import RoleGroups
from collections import OrderedDict


class RolesManager:
    def __init__(self, obj: dict, group_by_roles: bool):
        assert obj is not None, "ObjManager: obj cannot be None"
        # attributes
        self.__warnings = []
        self.__changed = False
        self.__modifid = 0
        self.__added = 0
        self.__deleted = 0
        # preprocess
        if "userRoles" not in obj:
            obj["userRoles"] = {}
            self.__changed = True

        if group_by_roles:
            roles = RoleGroups(obj["userRoles"])
            obj["userRoles"] = roles
            self.__changed = roles.is_regrouped()
        self.__pl_roles = obj["userRoles"]

        # DO NOT USE
        self.__obj = obj

    # ======================================================== #
    # ========================== API ========================= #
    # ======================================================== #
    # Due to difficulty of making RoleGroup serializable,
    # using finalize to simplify things
    def finalize(self):
        self.__obj["userRoles"] = OrderedDict(self.__pl_roles)

    def process_csv(self, reader: dict):
        if not reader:
            return
        for row in reader:
            email = row["Email Address"]
            self.__update_role(email, row["Role"])

    def process_add_users(self, students: list, tas: list, instructors: list):
        new_users = {"Student": students, "TA": tas, "Instructor": instructors}
        for role, emails in new_users.items():
            if emails is not None:
                for e in emails:
                    self.__update_role(e, role)

    def process_remove_users(self, emails: list):
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

    def __update_role(self, email: str, canvas_role: str):
        des_role = _canvas_to_PL_roles(canvas_role)
        if email in self.__pl_roles:
            cur_role = self.__pl_roles[email]
            if cur_role != des_role:
                self.__add_warning(
                    f'"{email}" role changed from "{cur_role}" to "{des_role}"'
                )
                self.__pl_roles[email] = des_role
                self.__modifid += 1
                self.__changed = True
        else:
            self.__pl_roles[email] = des_role
            self.__added += 1
            self.__changed = True

    def __remove_role(self, email: str):
        if email not in self.__pl_roles:
            self.__add_warning(f'"{email}" not found in "userRoles"')
        else:
            del self.__pl_roles[email]
            self.__deleted += 1
            self.__changed = True

    def __add_warning(self, msg: str):
        self.__warnings.append(msg)
