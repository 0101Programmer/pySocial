import asyncio
import datetime
import json
import os
import pathlib
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import psycopg2
from PIL import Image, ImageTk

import base_dir.config as main_config_file
from base_dir.windows import friends_window, my_profile_window
from base_dir.windows.all_dialogs_window import MessagePage


class MainInterfaceWindow(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        # self параметры для обработки ф-ций
        self.user = user
        # ----------------------------------------------->
        self.protocol("WM_DELETE_WINDOW", lambda: parent.destroy())
        parent.withdraw()
        self.title('Python Social')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)
        self.option_add("*tearOff", False)
        main_menu = tk.Menu()
        profile_menu = tk.Menu()
        settings_menu = tk.Menu()
        settings_menu.add_command(label="Удалить профиль", command=self.delete_profile)
        profile_menu.add_command(label="Моя страница", command=self.open_my_profile_page)
        profile_menu.add_cascade(label="Настройки", menu=settings_menu)
        profile_menu.add_separator()
        profile_menu.add_command(label="Выйти", command=self.logout)

        main_menu.add_cascade(label="Профиль", menu=profile_menu)
        main_menu.add_command(label="Мессенджер", command=self.open_all_messages_page)
        main_menu.add_command(label="Друзья", command=self.open_friends_page)

        self.config(menu=main_menu)

        main_inter_frame = tk.Frame(
            self
        )
        main_inter_frame.pack(expand=True)
        # данные для работы функции по отображению погоды
        self.cities = {"Москва": 524901, "Санкт Петербург": 498817, "Самара": 499099, "Омск": 1496153,
                       "Обнинск": 516436, "Ярославль": 468902}
        self.cities_combobox = ttk.Combobox(main_inter_frame,
                                            values=[key for key, value in self.cities.items()],
                                            state='readonly')
        # ----------------------------------------------->

        user_optional_data_flag = False
        if not user.optional_data:
            city_weather_lb = tk.Label(
                main_inter_frame,
                text="Вы можете указать город проживания для отображения погоды в вашем регионе"
            )
            city_weather_lb.grid()
        else:
            user_optional_data_flag = True
            if 'city_data' in user.optional_data:

                for idx, value in enumerate([key for key, value in self.cities.items()]):
                    if value == user.optional_data['city_data']['selected_city']:
                        self.cities_combobox.current(idx)
            city_weather_lb = tk.Label(
                main_inter_frame,
                text=f"Город для отображения погоды:"
            )
            city_weather_lb.grid()

        self.cities_combobox.grid()
        self.cities_combobox.bind("<<ComboboxSelected>>", self.city_choice)

        if user_optional_data_flag and 'city_data' in user.optional_data:
            if main_config_file.weather_check(
                    user.optional_data['city_data']['selected_city_id_for_openweathermap']):
                weather_now = main_config_file.weather_check(
                    user.optional_data['city_data']['selected_city_id_for_openweathermap'])

                weather_now_lb = tk.Label(
                    main_inter_frame,
                    text=f"Сейчас {weather_now['cond']}\n"
                         f"Температура (°C): {weather_now['temperature']}\n"
                         f"Минимальная температура (°C): {weather_now['temperature_min']}\n"
                         f"Максимальная температура (°C): {weather_now['temperature_max']}"
                )
                weather_now_lb.grid()
            else:
                weather_now_lb = tk.Label(
                    main_inter_frame,
                    text=f"Невозможно получить данные для отображение погоды.\nОтсутствует подключение к интернету"
                )
                weather_now_lb.grid()

        day_time_img_path = "static/windows_pics/error_pic.jpg"
        if main_config_file.day_time_counter() == "Утро":
            day_time_img_path = "static/windows_pics/evening.png"
        elif main_config_file.day_time_counter() == "День":
            day_time_img_path = "static/windows_pics/morning.png"
        elif main_config_file.day_time_counter() == "Вечер":
            day_time_img_path = "static/windows_pics/evening.png"
        elif main_config_file.day_time_counter() == "Ночь":
            day_time_img_path = "static/windows_pics/night.png"

            #НЕ РАБОТАЕТ С НОЧНЫМ ВРМЕНЕМ КОРРЕКТНО

        self.day_time_image = Image.open(day_time_img_path)
        self.image = self.day_time_image.resize((100, 60), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(
            main_inter_frame,
            image=f'{self.image}',
            borderwidth=2,
            relief="groove"
        )
        self.image_label.grid()

        day_time_image_img_caption_lb = tk.Label(
            main_inter_frame,
            text=str(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        )
        day_time_image_img_caption_lb.grid()

    def open_my_profile_page(self):
        my_profile_window.ProfilePage(self, self.user)

    def city_choice(self, event):
        selected_city = self.cities_combobox.get()
        selected_city_id = self.cities[str(selected_city)]
        message = f"Установить г. {selected_city} в качестве вашего текущего города?"
        if messagebox.askyesno(message=message):
            async def sub_city_choice():
                if self.user.optional_data:
                    self.user.optional_data["city_data"] = {
                        'selected_city': selected_city, 'selected_city_id_for_openweathermap': selected_city_id}
                else:
                    self.user.optional_data = {'city_data': {
                        'selected_city': selected_city, 'selected_city_id_for_openweathermap': selected_city_id}}
                await self.user.save()
                MainInterfaceWindow(self, self.user)

            asyncio.get_event_loop().run_until_complete(sub_city_choice())

    def delete_profile(self):
        message = f"Вы уверены, что хотите удалить профиль?"
        if messagebox.askyesno(message=message):
            message = f"При удалении профиля вы потеряете все данные, хранящиеся в 'PySocial'.\n\nВсё равно продолжить?"
            if messagebox.askyesno(message=message):
                async def sub_delete_profile():
                    self.user.email = "DELETED"
                    self.user.session_data = {"status": "deleted", "system_info": None}
                    await self.user.save()
                    file_to_remove = pathlib.Path(self.user.profile_pic_path)
                    if file_to_remove != "static/profile_pics/default_profile.png" and os.path.isfile(file_to_remove):
                        os.remove(file_to_remove)
                    self.destroy()
                    quit()
                asyncio.get_event_loop().run_until_complete(sub_delete_profile())

    def open_all_messages_page(self):
        MessagePage(self, self.user)

    def open_friends_page(self):
        friends_window.FriendsPage(self)

    def logout(self):
        message = f"Вы уверены, что хотите выйти?"
        if messagebox.askyesno(message=message):
            async def sub_logout():
                self.user.session_data = {"status": "inactive", "system_info": None}
                await self.user.save()
                self.destroy()
                quit()
            asyncio.get_event_loop().run_until_complete(sub_logout())
