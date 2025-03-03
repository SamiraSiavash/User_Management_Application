from tkinter import Frame, Label, Entry, Button, messagebox
from BusinessLogicLayer.user_business_logic import UserBusinessLogic
from DataAccessLayer.user_data_access import UserDataAccess
from PresentationLayer.window import Window
from tkinter.ttk import Treeview, Combobox
import math


class UserManagementFrame(Frame):
    def __init__(self, window, main_view):
        super().__init__(window)

        self.user_business_logic = UserBusinessLogic()
        self.user_data_access = UserDataAccess()
        self.main_view = main_view
        self.current_page = 1

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.header = Label(self, text="User Management Page")
        self.header.grid(row=0, column=0, columnspan=4, pady=10)

        self.search_entry = Entry(self)
        self.search_entry.grid(row=1, column=0, columnspan=3, pady=(0, 10), padx=10, sticky="ew")

        self.search_button = Button(self, text="Search", command=self.search)
        self.search_button.grid(row=1, column=3, pady=(0, 10), padx=10, sticky="ew")

        self.active_button = Button(self, text="Active", state="disabled", command=self.active_user)
        self.active_button.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="ew")

        self.deactive_button = Button(self, text="Deative", state="disabled", command=self.deactive_user)
        self.deactive_button.grid(row=2, column=1, pady=(0, 10), padx=10, sticky="ew")

        self.pending_button = Button(self, text="Pending", state="disabled", command=self.pending_user)
        self.pending_button.grid(row=2, column=2, pady=(0, 10), padx=10, sticky="ew")

        self.change_role_button = Button(self, text="Change Role", state="disabled", command=self.change_role)
        self.change_role_button.grid(row=2, column=3, pady=(0, 10), padx=10, sticky="ew")

        self.user_treeview = Treeview(self, columns=("firstname", "lastname", "username", "status", "role"))
        self.user_treeview.grid(row=3, column=0, columnspan=4, pady=(0, 10), padx=10, sticky="nsew")

        self.previous_button = Button(self, text="Previous", state="disabled", command=self.previous)
        self.previous_button.grid(row=4, column=0, pady=(0, 10), padx=10, sticky="ew")

        self.page_label = Label(self, text=self.current_page)
        self.page_label.grid(row=4, column=1, pady=(0, 10), padx=10, sticky="ew")

        self.next_button = Button(self, text="Next", command=self.next)
        self.next_button.grid(row=4, column=2, pady=(0, 10), padx=10, sticky="ew")

        self.back_button = Button(self, text="Back", command=self.go_to_home)
        self.back_button.grid(row=4, column=3, pady=(0, 10), padx=10, sticky="ew")

        self.user_treeview.heading("#0", text="NO")
        self.user_treeview.heading("firstname", text="First Name")
        self.user_treeview.heading("lastname", text="Last Name")
        self.user_treeview.heading("username", text="Username")
        self.user_treeview.heading("status", text="Status")
        self.user_treeview.heading("role", text="Role")

        self.user_treeview.column("#0", width=70)

        self.row_list = []
        self.current_user = None
        self.selected_user = None

        self.user_treeview.bind("<<TreeviewSelect>>", self.manage_buttons)

    def set_current_user(self, user):
        self.current_user = user
        response = self.user_business_logic.get_user_management_list(user, self.current_page)
        if response.success:
            user_list = response.data
            self.load_data_treeview(user_list)
        else:
            messagebox.showerror(title="Error", message=response.message)
            self.main_view.switch_frame("login")

    def load_data_treeview(self, user_list):
        for row in self.row_list:
            self.user_treeview.delete(row)
        self.row_list.clear()

        row_number = 1
        for user in user_list:
            row = self.user_treeview.insert("", "end", iid=user.id, text=str(row_number),
                                            values=(user.first_name,
                                                    user.last_name,
                                                    user.username,
                                                    user.get_status(),
                                                    user.get_role()))
            self.row_list.append(row)
            row_number += 1

    def active_user(self):
        id_list = self.user_treeview.selection()
        self.user_business_logic.active_user(id_list)

        response = self.user_business_logic.get_user_management_list(self.current_user, self.current_page)
        if response.success:
            user_list = response.data
            self.load_data_treeview(user_list)
        else:
            messagebox.showerror(title="Error", message=response.message)
            self.main_view.switch_frame("login")

    def deactive_user(self):
        id_list = self.user_treeview.selection()
        self.user_business_logic.deactive_user(id_list)

        response = self.user_business_logic.get_user_management_list(self.current_user, self.current_page)
        if response.success:
            user_list = response.data
            self.load_data_treeview(user_list)
        else:
            messagebox.showerror(title="Error", message=response.message)
            self.main_view.switch_frame("login")

    def pending_user(self):
        id_list = self.user_treeview.selection()
        self.user_business_logic.pending_user(id_list)

        response = self.user_business_logic.get_user_management_list(self.current_user, self.current_page)
        if response.success:
            user_list = response.data
            self.load_data_treeview(user_list)
        else:
            messagebox.showerror(title="Error", message=response.message)
            self.main_view.switch_frame("login")

    def manage_buttons(self, event):
        select_count = len(self.user_treeview.selection())

        if select_count == 1:
            self.active_button.config(state="normal")
            self.deactive_button.config(state="normal")
            self.pending_button.config(state="normal")
            self.change_role_button.config(state="normal")
        elif select_count > 1:
            self.active_button.config(state="normal")
            self.deactive_button.config(state="normal")
            self.pending_button.config(state="normal")
            self.change_role_button.config(state="disabled")
        else:
            self.active_button.config(state="disabled")
            self.deactive_button.config(state="disabled")
            self.pending_button.config(state="disabled")
            self.change_role_button.config(state="disabled")

    def change_role(self):
        change_role_form = Window("Change Role", "300x100")

        change_role_form.grid_columnconfigure(0, weight=1)
        change_role_form.grid_columnconfigure(1, weight=1)
        change_role_form.grid_rowconfigure(0, weight=1)

        role_label = Label(change_role_form, text="Select a Role:")
        role_label.grid(row=0, column=0, pady=(10, 0), padx=(10, 0))

        role_combobox = Combobox(change_role_form, width=27)
        role_list = self.user_data_access.get_Role()
        title_list = []
        for role in role_list:
            title_list.append(role.title)
            role_combobox['values'] = title_list
        role_combobox.grid(row=0, column=1, pady=(0, 0), padx=(0, 10))
        role_combobox.current(0)

        self.selected_user = int(self.user_treeview.selection()[0])

        def submit():
            role = role_combobox.get()
            self.user_business_logic.change_role(self.selected_user, role)
            change_role_form.destroy()

            response = self.user_business_logic.get_user_management_list(self.current_user, self.current_page)
            if response.success:
                user_list = response.data
                self.load_data_treeview(user_list)
            else:
                messagebox.showerror(title="Error", message=response.message)
                self.main_view.switch_frame("login")

        submit_button = Button(change_role_form, text="Submit", command=submit)
        submit_button.grid(row=1, column=1, pady=(0, 10), padx=(0, 10), sticky="ew")

        change_role_form.mainloop()

    def search(self):
        term = self.search_entry.get()
        if term != "":
            user_list = self.user_data_access.search(term)
            self.load_data_treeview(user_list)
        else:
            response = self.user_business_logic.get_user_management_list(self.current_user, self.current_page)
            if response.success:
                user_list = response.data
                self.load_data_treeview(user_list)
            else:
                messagebox.showerror(title="Error", message=response.message)
                self.main_view.switch_frame("login")

    def go_to_home(self):
        self.main_view.switch_frame("home")
        self.set_current_user(self.current_user)
        self.current_page = 1
        self.page_label.config(text=self.current_page)

    def previous(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.page_label.config(text=self.current_page)
            self.previous_button.config(state="active")
            self.next_button.config(state="active")
            user_list = self.user_data_access.pagination(self.current_page)
            self.load_data_treeview(user_list)
            if self.current_page == 1:
                self.previous_button.config(state="disabled")
        else:
            self.next_button.config(state="active")
            self.previous_button.config(state="disabled")

    def next(self):
        end_page = int(math.ceil(len(self.user_data_access.get_user_list()) / 10))

        if self.current_page < end_page:
            self.current_page += 1
            self.page_label.config(text=self.current_page)
            self.next_button.config(state="active")
            self.previous_button.config(state="active")
            user_list = self.user_data_access.pagination(self.current_page)
            self.load_data_treeview(user_list)
            if self.current_page == end_page:
                self.next_button.config(state="disabled")
        else:
            self.previous_button.config(state="active")
            self.next_button.config(state="disabled")
