import asyncio
import tkinter as tk
from tkinter import messagebox

import base_dir.config as main_config_file
from base_dir.db_config.db_models import User
from base_dir.windows.my_profile_window import ProfilePage


class LogWindow(tk.Toplevel):
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
        email_lb.grid(row=3, column=1, sticky="e")

        password_lb = tk.Label(
            log_frame,
            text="Введите свой пароль"
        )
        password_lb.grid(row=4, column=1, sticky="e")

        self.email_ent = tk.Entry(
            log_frame,
        )
        self.email_ent.grid(row=3, column=2, pady=5)

        self.password_ent = tk.Entry(
            log_frame,
            show="*"
        )
        self.password_ent.grid(row=4, column=2, pady=5)

        submit_btn = tk.Button(
            log_frame,
            text='Авторизоваться',
            command=self.log_data_validate,
            height=1, width=20
        )
        submit_btn.grid(row=5, column=2)

        back_btn = tk.Button(
            log_frame,
            text='Назад',
            command=self.open_start_window,
            height=1, width=20
        )
        back_btn.grid(row=6, column=2)

    def log_data_validate(self):
        email = self.email_ent.get()
        password = str(self.password_ent.get())
        if len(email) == 0 or len(password) == 0:
            messagebox.showinfo('Python Social', '    Заполнены не все поля    ')
        elif not main_config_file.validate_email(email):
            messagebox.showinfo('Python Social', 'Пожалуйста, введите корректный email')
        else:
            async def sub_log_data_validate():
                user = await User.get_or_none(email=email)
                if not user:
                    messagebox.showinfo('Python Social', 'Пользователя с таким email не существует')
                elif user.password != password:
                    messagebox.showinfo('Python Social', '   Неверный пароль   ')
                else:
                    user.session_data = {"status": "active",
                                         "system_info": main_config_file.check_user_sys_info()}
                    await user.save()
                    ProfilePage(self, user)

            asyncio.get_event_loop().run_until_complete(sub_log_data_validate())

    def open_start_window(self):
        self.destroy()
        self.parent.deiconify()
