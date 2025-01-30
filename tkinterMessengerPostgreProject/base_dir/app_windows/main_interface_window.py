import asyncio
import datetime
import os
import pathlib
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from PIL import Image, ImageTk
from async_tkinter_loop import async_handler
import base_dir.app_windows.friends_window as friends_module
import base_dir.app_windows.all_dialogs_window as all_dialogs_module
import base_dir.app_windows.my_profile_window as my_profile_module
import base_dir.config as main_config_file


class MainInterface(tk.Toplevel):
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
        # меню навигации
        main_menu = tk.Menu()
        profile_menu = tk.Menu()
        settings_menu = tk.Menu()
        settings_menu.add_command(label="Удалить профиль", command=self.delete_profile)
        profile_menu.add_command(label="Моя страница", command=self.open_my_profile_page)
        profile_menu.add_cascade(label="Настройки", menu=settings_menu)
        profile_menu.add_separator()
        profile_menu.add_command(label="Выйти", command=async_handler(self.logout))

        main_menu.add_cascade(label="Профиль", menu=profile_menu)
        main_menu.add_command(label="Мессенджер", command=self.open_all_dialogs_window)
        main_menu.add_command(label="Друзья", command=self.open_friends_window)

        self.config(menu=main_menu)
        # ----------------------------------------------->
        main_inter_frame = tk.Frame(
            self,
            padx=10,
            pady=10
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
        self.cities_combobox.bind("<<ComboboxSelected>>", async_handler(self.city_choice))

        if user_optional_data_flag and 'city_data' in user.optional_data:
            get_city_weather_btn = tk.Button(self, text="None", command=async_handler(self.get_city_weather))
            get_city_weather_btn.pack()
            get_city_weather_btn.pack_forget()
            get_city_weather_btn.after(0, get_city_weather_btn.invoke)
            if user.optional_data['city_data']["weather_now"]:
                weather_now_lb = tk.Label(
                    main_inter_frame,
                    text=f"Сейчас {user.optional_data['city_data']["weather_now"]['cond']}\n"
                         f"Температура (°C): {user.optional_data['city_data']["weather_now"]['temperature']}\n"
                         f"Минимальная температура (°C): {user.optional_data['city_data']["weather_now"]['temperature_min']}\n"
                         f"Максимальная температура (°C): {user.optional_data['city_data']["weather_now"]['temperature_max']}"
                )
                weather_now_lb.grid()
            else:
                weather_now_lb = tk.Label(
                    main_inter_frame,
                    text=f"При отображении погоды что-то пошло не так и мы уже работаем над этим"
                )
                weather_now_lb.grid()

        day_time_img_path = "../static/windows_pics/error_pic.jpg"
        if main_config_file.day_time_counter() == "Утро":
            day_time_img_path = "../static/windows_pics/evening.png"
        elif main_config_file.day_time_counter() == "День":
            day_time_img_path = "../static/windows_pics/morning.png"
        elif main_config_file.day_time_counter() == "Вечер":
            day_time_img_path = "../static/windows_pics/evening.png"
        elif main_config_file.day_time_counter() == "Ночь":
            day_time_img_path = "../static/windows_pics/night.png"

        self.day_time_image = Image.open(day_time_img_path)
        self.image = self.day_time_image.resize((120, 80), Image.Resampling.LANCZOS)
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
        my_profile_module.MyProfile(self, self.user)

    async def get_city_weather(self):
        if datetime.datetime.now() - datetime.timedelta(minutes=30) > datetime.datetime.strptime(self.user.optional_data['city_data']["updated_at"], "%Y-%m-%d %H:%M:%S.%f"):
            if main_config_file.weather_check(
                    self.user.optional_data['city_data']['selected_city_id_for_openweathermap']):
                weather_now = main_config_file.weather_check(
                    self.user.optional_data['city_data']['selected_city_id_for_openweathermap'])
                if weather_now:
                    self.user.optional_data["city_data"]["weather_now"] = weather_now
                    self.user.optional_data["city_data"]["updated_at"] = str(datetime.datetime.now())
                else:
                    self.user.optional_data["city_data"]["weather_now"] = False
            else:
                self.user.optional_data["city_data"]["weather_now"] = False
            await self.user.save()


    async def city_choice(self, event):
        selected_city = self.cities_combobox.get()
        selected_city_id = self.cities[str(selected_city)]
        weather_now = False
        message = f"Установить г. {selected_city} в качестве вашего текущего города?"
        if messagebox.askyesno(message=message):
            if main_config_file.weather_check(selected_city_id):
                weather_now = main_config_file.weather_check(selected_city_id)
            if self.user.optional_data:
                self.user.optional_data["city_data"] = {
                    'selected_city': selected_city, 'selected_city_id_for_openweathermap': selected_city_id,
                    "updated_at": str(datetime.datetime.now()), "weather_now": weather_now}
            else:
                self.user.optional_data = {'city_data': {
                    'selected_city': selected_city, 'selected_city_id_for_openweathermap': selected_city_id,
                    "updated_at": str(datetime.datetime.now()), "weather_now": weather_now}}
            await self.user.save()
            MainInterface(self, self.user)

    def delete_profile(self):
        pass
        # message = f"Вы уверены, что хотите удалить профиль?"
        # if messagebox.askyesno(message=message):
        #     message = f"При удалении профиля вы потеряете все данные, хранящиеся в 'PySocial'.\n\nВсё равно продолжить?"
        #     if messagebox.askyesno(message=message):
        #         async def sub_delete_profile():
        #             self.user.email = "DELETED"
        #             self.user.session_data = {"status": "deleted", "system_info": None}
        #             await self.user.save()
        #             file_to_remove = pathlib.Path(self.user.profile_pic_path)
        #             if file_to_remove != "static/profile_pics/default_profile.png" and os.path.isfile(file_to_remove):
        #                 os.remove(file_to_remove)
        #             self.destroy()
        #             quit()
        #
        #         asyncio.get_event_loop().run_until_complete(sub_delete_profile())

    def open_all_dialogs_window(self):
        all_dialogs_module.Dialogs(self, self.user)

    def open_friends_window(self):
        friends_module.Friends(self, self.user)

    async def logout(self):
        message = f"Вы уверены, что хотите выйти?"
        if messagebox.askyesno(message=message):
            self.user.session_data = {"status": "inactive", "system_info": None}
            await self.user.save()
            self.destroy()
