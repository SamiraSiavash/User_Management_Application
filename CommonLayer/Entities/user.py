class User:
    def __init__(self, id, firstname, lastname, username, password, status, role_id):
        self.id = id
        self.first_name = firstname
        self.last_name = lastname
        self.username = username
        self.password = password
        self.status = status
        self.role_id = role_id

    def update(self, new_firstname, new_lastname, new_username, new_password, new_status, new_role):
        self.first_name = new_firstname
        self.last_name = new_lastname
        self.username = new_username
        self.password = new_password
        self.status = new_status
        self.role_id = new_role

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, new_value):
        if not isinstance(new_value, str) or len(new_value) < 3:
            raise ValueError("Invalid value for firstname.")
        self._first_name = new_value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, new_value):
        if not isinstance(new_value, str) or len(new_value) < 3:
            raise ValueError("Invalid value for lastname.")
        self._last_name = new_value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, new_value):
        if not isinstance(new_value, str) or len(new_value) < 3:
            raise ValueError("Invalid value for username.")
        self._username = new_value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_value):
        self._password = new_value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_value):
        self._status = new_value

    @property
    def role_id(self):
        return self._role_id

    @role_id.setter
    def role_id(self, new_value):
        self._role_id = new_value

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def get_role(self):
        if self.role_id == 1:
            return "Admin"
        elif self.role_id == 2:
            return "Default User"

    def get_status(self):
        if self.status == 0:
            return "Deactive"
        elif self.status == 1:
            return "Active"
        elif self.status == 2:
            return "Pending"
