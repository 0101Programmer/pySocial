import asyncio
import datetime
import os
import pathlib
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.simpledialog import askstring
import base_dir.app_windows.main_interface_window as main_interface_module
import base_dir.app_windows.elses_profile_window as elses_profile_module

from PIL import Image, ImageTk
from async_tkinter_loop import async_handler

from base_dir.config import is_not_empty, validate_email
from base_dir.db_config.db_models import User


class Friends(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        parent.withdraw()
        self.protocol("WM_DELETE_WINDOW", lambda: parent.destroy())
        self.title('Python Social')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)
        self.user = user

        main_menu = tk.Menu()
        main_menu.add_command(label="Назад", command=self.open_main_interface)
        self.config(menu=main_menu)

        friends_frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        friends_frame.pack(expand=True)

        email_lb = tk.Label(
            friends_frame,
            text="Поиск пользователя по email"
        )
        email_lb.grid()

        search_by_email_btn = tk.Button(
            friends_frame,
            text='Найти',
            command=async_handler(self.user_search_by_email),
            height=1, width=20
        )
        search_by_email_btn.grid()

        if user.friends:
            my_friends_combobox_lb = tk.Label(
                friends_frame,
                text="Список друзей:"
            )
            my_friends_combobox_lb.grid()
            self.my_friends_combobox = my_friends_combobox = ttk.Combobox(friends_frame,
                                                                          values=[v["his_email"] for k, v in
                                                                                  user.friends.items()],
                                                                          state='readonly')
            my_friends_combobox.grid()
            my_friends_combobox.bind("<<ComboboxSelected>>", async_handler(self.open_elses_profile))

    async def user_search_by_email(self):
        email = askstring('Python Social', 'Введите email пользователя')
        if email:
            if not is_not_empty(email) or not validate_email(email):
                messagebox.showinfo('Python Social', 'Пожалуйста, введите корректный email (в '
                                                     'формате "example@mail.ru")')
            else:
                is_existed_user = await User.get_or_none(email=email)
                if not is_existed_user:
                    messagebox.showinfo('Python Social', 'Пользователя с указанным email не существует')
                elif self.user.email == is_existed_user.email:
                    messagebox.showinfo('Python Social', 'Вы не можете добавить самого себя в друзья')
                elif self.user.friends and str(is_existed_user.id) in self.user.friends:
                    message = f"Открыть профиль {is_existed_user.email}?""em@mail.ru"
                    if messagebox.askyesno(message=message):
                        elses_profile_module.ElsesProfile(self, self.user, is_existed_user)
                else:
                    message = f"Добавить пользователя в друзья?\nЕсли вы хотите посмотреть профиль, нажмите 'нет'"
                    if messagebox.askyesno(message=message):
                        if not self.user.friends:
                            self.user.friends = {
                                str(is_existed_user.id): {"my_confirmation": True, "his_confirmation": False,
                                                          "his_email": is_existed_user.email}}
                        else:
                            self.user.friends[str(is_existed_user.id)] = {"my_confirmation": True,
                                                                          "his_confirmation": False,
                                                                          "his_email": is_existed_user.email}
                        if not is_existed_user.friends:
                            is_existed_user.friends = {str(self.user.id):
                                                           {"my_confirmation": False, "his_confirmation": True,
                                                            "his_email": self.user.email}}
                        else:
                            is_existed_user.friends[str(self.user.id)] = {"my_confirmation": False,
                                                                          "his_confirmation": True,
                                                                          "his_email": self.user.email}
                        await self.user.save()
                        await is_existed_user.save()
                        Friends(self, self.user)
                    else:
                        message = f"Открыть профиль?"
                        if messagebox.askyesno(message=message):
                            elses_profile_module.ElsesProfile(self, self.user, is_existed_user)

    def open_main_interface(self):
        main_interface_module.MainInterface(self, self.user)

    async def open_elses_profile(self, event):
        selected_user_email = self.my_friends_combobox.get()
        requested_user = await User.get_or_none(email=selected_user_email)
        if requested_user:
            elses_profile_module.ElsesProfile(self, self.user, requested_user)
        else:
            print("Пользователя не найдено, (удаляем из списка)")
