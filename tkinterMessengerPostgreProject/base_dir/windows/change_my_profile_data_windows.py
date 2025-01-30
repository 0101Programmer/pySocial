import asyncio
import tkinter as tk
from tkinter import messagebox

from base_dir.windows import my_profile_window


class ChangeName(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        parent.withdraw()
        self.protocol("WM_DELETE_WINDOW", lambda: parent.destroy())
        self.title('Python Social')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)

        change_name_frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        change_name_frame.pack(expand=True)

        change_name_lb = tk.Label(
            change_name_frame,
            text="Введите ваше имя:"
        )
        change_name_lb.grid()

        self.change_name_ent = tk.Entry(
            change_name_frame,
        )
        self.change_name_ent.grid()

        submit_btn = tk.Button(
            change_name_frame,
            text='Подтвердить',
            command=self.data_validator,
            height=1, width=15
        )
        submit_btn.grid()

        back_btn = tk.Button(
            change_name_frame,
            text='Назад',
            command=self.back_to_profile_page,
            height=1, width=15
        )
        back_btn.grid()

    def data_validator(self):
        new_name = self.change_name_ent.get()
        digits_check = any(_.isdigit() for _ in new_name)
        if len(new_name) == 0:
            messagebox.showinfo('Python Social', '    Заполнены не все поля    ')
        elif digits_check is True:
            messagebox.showinfo('Python Social', 'В имени допускаются только буквы')
        else:
            async def sub_data_validator():
                self.user.name = new_name
                await self.user.save()
                my_profile_window.ProfilePage(self, self.user)
            asyncio.get_event_loop().run_until_complete(sub_data_validator())

    def back_to_profile_page(self):
        my_profile_window.ProfilePage(self, self.user)


class ChangePassword(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        parent.withdraw()
        self.protocol("WM_DELETE_WINDOW", lambda: parent.destroy())
        self.title('Python Social')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)

        change_password_frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        change_password_frame.pack(expand=True)

        new_password_lb = tk.Label(
            change_password_frame,
            text="Введите новый пароль:"
        )
        new_password_lb.grid()

        self.new_password_ent = tk.Entry(
            change_password_frame,
        )
        self.new_password_ent.grid()

        confirm_new_password_lb = tk.Label(
            change_password_frame,
            text="Повторите пароль:"
        )
        confirm_new_password_lb.grid()

        self.confirm_new_password_ent = tk.Entry(
            change_password_frame
        )
        self.confirm_new_password_ent.grid(pady=(0, 5))

        submit_btn = tk.Button(
            change_password_frame,
            text='Подтвердить',
            command=self.data_validator,
            height=1, width=15
        )
        submit_btn.grid()

        back_btn = tk.Button(
            change_password_frame,
            text='Назад',
            command=self.back_to_profile_page,
            height=1, width=15
        )
        back_btn.grid()

    def data_validator(self):
        new_password = self.new_password_ent.get()
        confirm_password = self.confirm_new_password_ent.get()
        digits_check = any(_.isdigit() for _ in new_password)
        if len(new_password) == 0 or len(confirm_password) == 0:
            messagebox.showinfo('Python Social', '    Заполнены не все поля    ')
        elif digits_check is False:
            messagebox.showinfo('Python Social', 'Пароль должен содержать не только буквы')
        elif len(new_password) < 5:
            messagebox.showinfo('Python Social', '    Слишком короткий пароль    ')
        elif new_password != confirm_password:
            messagebox.showinfo('Python Social', '    Пароли не совпадают    ')
        else:
            async def sub_data_validator():
                self.user.password = new_password
                await self.user.save()
                my_profile_window.ProfilePage(self, self.user)
            asyncio.get_event_loop().run_until_complete(sub_data_validator())

    def back_to_profile_page(self):
        my_profile_window.ProfilePage(self, self.user)