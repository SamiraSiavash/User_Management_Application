from CommonLayer.Model.response import Response
from DataAccessLayer.user_data_access import UserDataAccess
from CommonLayer.Decorators.performance_logger import performance_logger_decorator
from CommonLayer.Entities.user import User
import CommonLayer.State.user_state
import hashlib
import sqlite3


class UserBusinessLogic:
    def __init__(self):
        self.user_data_access = UserDataAccess()

    @performance_logger_decorator("UserBusinessLogic")
    def login(self, username, password):
        try:
            User(None, "first_name", "last_name", username, password, 2, 2)
        except ValueError as ex:
            return Response(False, None, ex.args[0])

        password_hash = hashlib.md5(password.encode()).hexdigest()
        user = self.user_data_access.get_user(username, password_hash)

        if user:
            match user.status:
                case 0:
                    return Response(False, None, "You account is deactived.")
                case 1:
                    CommonLayer.State.user_state.current_user_id = user.id
                    return Response(True, user, None)
                case 2:
                    return Response(False, None, "Pending.")
        else:
            return Response(False, None, "Invalid username or password(NotFound).")

    @performance_logger_decorator("UserBusinessLogic")
    def register(self, firstname, lastname, username, password):
        try:
            User(None, firstname, lastname, username, password, 2, 2)
        except ValueError as ex:
            return Response(False, None, ex.args[0])

        password_hash = hashlib.md5(password.encode()).hexdigest()

        try:
            self.user_data_access.insert_user(firstname, lastname, username, password_hash, 2, 2)
        except sqlite3.IntegrityError:
            return Response(False, None, "Username exist.")
        else:
            return Response(True, None, "Register successfully.")

    @performance_logger_decorator("UserBusinessLogic")
    def get_user_management_list(self, current_user, page):
        if current_user.role_id == 1:
            user_list = self.user_data_access.pagination(page)
            return Response(True, user_list, None)
        else:
            return Response(False, None, "Access denied.")

    @performance_logger_decorator("UserBusinessLogic")
    def active_user(self, id_list):
        for id in id_list:
            self.user_data_access.update_status(id, 1)

    @performance_logger_decorator("UserBusinessLogic")
    def deactive_user(self, id_list):
        for id in id_list:
            self.user_data_access.update_status(id, 0)

    @performance_logger_decorator("UserBusinessLogic")
    def pending_user(self, id_list):
        for id in id_list:
            self.user_data_access.update_status(id, 2)

    @performance_logger_decorator("UserBusinessLogic")
    def change_role(self, id, role_title):
        role = self.user_data_access.get_role_id(role_title)
        self.user_data_access.update_role(id, role.id)
