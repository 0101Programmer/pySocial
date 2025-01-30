import tkinter as tk
from tkinter import messagebox

from async_tkinter_loop import async_handler

import base_dir.config as main_config_file
from base_dir.app_windows.my_profile_window import MyProfile
from base_dir.db_config.db_models import User


class Login(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        parent.withdraw()
        self.title('Python Social | Авторизация')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)

        self.parent = parent

        log_frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        log_frame.pack(expand=True)

        email_lb = tk.Label(
            log_frame,
            text="Введите свой email"
        )
        email_lb.grid()

        self.email_ent = tk.Entry(
            log_frame,
        )
        self.email_ent.grid()

        password_lb = tk.Label(
            log_frame,
            text="Введите свой пароль"
        )
        password_lb.grid()

        self.password_ent = tk.Entry(
            log_frame,
            show="*"
        )
        self.password_ent.grid()

        submit_btn = tk.Button(
            log_frame,
            text='Авторизоваться',
            command=async_handler(self.log_data_validate),
            height=1, width=20
        )
        submit_btn.grid()

        back_btn = tk.Button(
            log_frame,
            text='Назад',
            command=self.open_start_window,
            height=1, width=20
        )
        back_btn.grid()

    async def log_data_validate(self):
        email = self.email_ent.get()
        password = str(self.password_ent.get())
        if len(email) == 0 or len(password) == 0:
            messagebox.showinfo('Python Social', '    Заполнены не все поля    ')
        elif not main_config_file.validate_email(email):
            messagebox.showinfo('Python Social', 'Пожалуйста, введите корректный email')
        else:
            user = await User.get_or_none(email=email)
            if not user:
                messagebox.showinfo('Python Social', 'Пользователя с таким email не существует')
            elif user.password != password:
                messagebox.showinfo('Python Social', '   Неверный пароль   ')
            else:
                user.session_data = {"status": "active",
                                     "system_info": main_config_file.check_user_sys_info()}
                await user.save()
                MyProfile(self, user)

    def open_start_window(self):
        self.destroy()
        self.parent.deiconify()
