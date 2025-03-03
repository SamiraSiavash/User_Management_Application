from tkinter import Frame, Label, Button


class HomeFrame(Frame):
    def __init__(self, window, main_view):
        super().__init__(window)

        self.main_view = main_view
        self.grid_columnconfigure(0, weight=1)

        self.header = Label(self)
        self.header.grid(row=0, column=0, pady=10, padx=10)

        self.logout_button = Button(self, text="Logout", command=self.logout)
        self.logout_button.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="ew")

        self.user_management_button = Button(self, text="User Management", command=self.go_to_usermanagement)

        self.current_user = None

    def set_current_user(self, user):
        self.current_user = user
        welcome_message = f"Welcome {user.get_fullname()} ({user.get_role()})"
        self.header.config(text=welcome_message)

        if user.role_id == 1:
            self.user_management_button.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="ew")

    def logout(self):
        self.main_view.switch_frame("login")

    def go_to_usermanagement(self):
        usermanagement_frame = self.main_view.switch_frame("usermanagement")
        usermanagement_frame.set_current_user(self.current_user)
