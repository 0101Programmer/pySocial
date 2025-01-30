import asyncio
import datetime
import tkinter as tk
from tkinter import messagebox

import base_dir.config as main_config_file
from base_dir.db_config.db_models import User, Dialog
from base_dir.windows.my_profile_window import ProfilePage


class RegWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        parent.withdraw()
        self.title('Python Social | Регистрация')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)

        self.full_name_ent = None
        self.password_conf_ent = None
        self.password_ent = None
        self.email_ent = None
        self.parent = parent

        async def reg_window():
            reg_frame = tk.Frame(
                self,
                padx=10,
                pady=10
            )
            reg_frame.pack(expand=True)

            email_lb = tk.Label(
                reg_frame,
                text="Введите свой email"
            )
            email_lb.grid(row=3, column=1, sticky="e")

            password_lb = tk.Label(
                reg_frame,
                text="Придумайте надёжный пароль"
            )
            password_lb.grid(row=4, column=1, sticky="e")

            password_conf_lb = tk.Label(
                reg_frame,
                text="Повторите пароль"
            )
            password_conf_lb.grid(row=5, column=1, sticky="e")

            full_name_lb = tk.Label(
                reg_frame,
                text="Введите ФИО"
            )
            full_name_lb.grid(row=6, column=1, sticky="e")

            self.email_ent = tk.Entry(
                reg_frame,
            )
            self.email_ent.grid(row=3, column=2, pady=5)

            self.password_ent = tk.Entry(
                reg_frame,
                show="*"
            )
            self.password_ent.grid(row=4, column=2, pady=5)

            self.password_conf_ent = tk.Entry(
                reg_frame,
                show="*"
            )
            self.password_conf_ent.grid(row=5, column=2, pady=5)

            self.full_name_ent = tk.Entry(
                reg_frame,
            )
            self.full_name_ent.grid(row=6, column=2, pady=5)

            submit_btn = tk.Button(
                reg_frame,
                text='Зарегистрироваться',
                command=self.reg_data_validate,
                height=1, width=20
            )
            submit_btn.grid(row=7, column=2)

            back_btn = tk.Button(
                reg_frame,
                text='Назад',
                command=self.open_start_window,
                height=1, width=20
            )
            back_btn.grid(row=8, column=2)

        asyncio.get_event_loop().run_until_complete(reg_window())

    def reg_data_validate(self):
        email = self.email_ent.get()
        password = self.password_ent.get()
        repeat_password = self.password_conf_ent.get()
        full_name = self.full_name_ent.get()
        password_digits_check = any(_.isdigit() for _ in password)
        name_digits_check = any(_.isdigit() for _ in full_name)
        if len(email) == 0 or len(password) == 0 or len(repeat_password) == 0 or len(full_name) == 0:
            messagebox.showinfo('Python Social', '    Заполнены не все поля    ')
        elif password != repeat_password:
            messagebox.showinfo('Python Social', '    Пароли не совпадают    ')
        elif not main_config_file.validate_email(email):
            messagebox.showinfo('Python Social', 'Пожалуйста, введите корректный email')
        elif password_digits_check is False:
            messagebox.showinfo('Python Social', 'Пароль должен содержать не только буквы')
        elif name_digits_check is True:
            messagebox.showinfo('Python Social', 'В ФИО допускаются только буквы')
        elif len(password) < 5:
            messagebox.showinfo('Python Social', '    Слишком короткий пароль    ')
        else:
            async def sub_reg_data_validate():
                is_existed_email = await User.get_or_none(email=email)
                if is_existed_email:
                    messagebox.showinfo('Python Social', '    Пользователь с таким email уже зарегистрирован    ')
                else:
                    user = await User.create(email=email, password=password, name=full_name, birthdate="2002-12-12",
                                             session_data={"status": "active",
                                                           "system_info": main_config_file.check_user_sys_info()})
                    await Dialog.create(started_by_user=user, dialog_data={1: {
                        'text': "Здесь находится ваша личная страница для заметок",
                        'sender_id': user.id,
                        'message_sent_time': datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    }})
                    ProfilePage(self, user)

            asyncio.get_event_loop().run_until_complete(sub_reg_data_validate())

    def open_start_window(self):
        self.destroy()
        self.parent.deiconify()
