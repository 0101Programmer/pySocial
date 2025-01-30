import datetime
import tkinter as tk
from tkinter import messagebox
from async_tkinter_loop import async_handler
from tkcalendar import DateEntry
import base_dir.config as main_config_file
from base_dir.app_windows.my_profile_window import MyProfile

from base_dir.db_config.db_models import User, Dialog


class Registration(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        parent.withdraw()
        self.title('Python Social | Регистрация')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)
        self.parent = parent

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
        email_lb.grid()

        self.email_ent = tk.Entry(
            reg_frame,
        )
        self.email_ent.grid()

        password_lb = tk.Label(
            reg_frame,
            text="Придумайте надёжный пароль"
        )
        password_lb.grid()

        self.password_ent = tk.Entry(
            reg_frame,
            show="*"
        )
        self.password_ent.grid()

        password_conf_lb = tk.Label(
            reg_frame,
            text="Повторите пароль"
        )
        password_conf_lb.grid()

        self.password_conf_ent = tk.Entry(
            reg_frame,
            show="*"
        )
        self.password_conf_ent.grid()

        name_lb = tk.Label(
            reg_frame,
            text="Введите ФИО"
        )
        name_lb.grid()

        self.name_ent = tk.Entry(
            reg_frame,
        )
        self.name_ent.grid()

        birthdate_lb = tk.Label(
            reg_frame,
            text="Укажите дату рождения"
        )
        birthdate_lb.grid()

        self.birthdate_ent = DateEntry(
            reg_frame,
        )
        self.birthdate_ent.grid()

        submit_btn = tk.Button(
            reg_frame,
            text='Зарегистрироваться',
            command=async_handler(self.reg_data_validate),
            height=1, width=20
        )
        submit_btn.grid()

        back_btn = tk.Button(
            reg_frame,
            text='Назад',
            command=self.open_start_window,
            height=1, width=20
        )
        back_btn.grid()

    async def reg_data_validate(self):
        email = self.email_ent.get()
        password = self.password_ent.get()
        repeat_password = self.password_conf_ent.get()
        name = self.name_ent.get()
        birthdate = self.birthdate_ent.get()
        formated_birthdate = datetime.datetime.strptime(birthdate, '%m/%d/%y')
        password_digits_check = any(_.isdigit() for _ in password)
        name_digits_check = any(_.isdigit() for _ in name)
        if len(email) == 0 or len(password) == 0 or len(repeat_password) == 0 or len(name) == 0:
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
        elif not (datetime.datetime.now() - datetime.timedelta(365 * 100)) <= formated_birthdate <= (datetime.datetime.now() - datetime.timedelta(365 * 14)):
            messagebox.showinfo('Python Social', 'Пожалуйста, введите корректную дату (регистрация возможна с 14 лет)')
        else:
            is_existed_email = await User.get_or_none(email=email)
            if is_existed_email:
                messagebox.showinfo('Python Social', '    Пользователь с таким email уже зарегистрирован    ')
            else:
                user = await User.create(email=email, password=password, name=name, birthdate=formated_birthdate.strftime('%Y-%m-%d'),
                                         session_data={"status": "active",
                                                       "system_info": main_config_file.check_user_sys_info()})
                await Dialog.create(started_by_user=user, dialog_data={1: {
                    'text': "Здесь находится ваша личная страница для заметок",
                    'sender_id': user.id,
                    'message_sent_time': datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                }})
                MyProfile(self, user)

    def open_start_window(self):
        self.destroy()
        self.parent.deiconify()
