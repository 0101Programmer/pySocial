import asyncio
import tkinter as tk

from PIL import Image, ImageTk

import base_dir.config as main_config_file
from base_dir.windows import main_interface_window
from base_dir.windows.change_my_profile_data_windows import ChangeName, ChangePassword


class ProfilePage(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        parent.withdraw()
        self.protocol("WM_DELETE_WINDOW", lambda: parent.destroy())
        self.title('Python Social')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)
        self.user = user

        async def my_profile_page():

            main_menu = tk.Menu()
            change_profile_data_menu = tk.Menu(tearoff=0)
            change_profile_data_menu.add_command(label="Сменить фотографию профиля", command=self.change_profile_pic)
            change_profile_data_menu.add_command(label="Сменить имя", command=self.change_name)
            change_profile_data_menu.add_command(label="Сменить пароль", command=self.change_password)

            main_menu.add_cascade(label="На главную", command=self.open_main_interface)
            main_menu.add_cascade(label="Изменить личные данные", menu=change_profile_data_menu)
            self.config(menu=main_menu)

            profile_frame = tk.Frame(
                self,
            )
            profile_frame.pack(expand=True)

            img_path = user.profile_pic_path
            self.image = Image.open(img_path)
            self.image = self.image.resize((100, 60), Image.Resampling.LANCZOS)
            self.image = ImageTk.PhotoImage(self.image)
            self.image_label = tk.Label(
                profile_frame,
                image=f'{self.image}',
                borderwidth=2,
                relief="groove"
            )
            self.image_label.grid(row=0, rowspan=3, pady=5)

            full_name_lb = tk.Label(
                profile_frame,
                text="Имя:"
            )
            full_name_lb.grid(row=0, column=1)

            email_lb = tk.Label(
                profile_frame,
                text="Email:"
            )
            email_lb.grid(row=1, column=1)

            password_lb = tk.Label(
                profile_frame,
                text="Пароль:"
            )
            password_lb.grid(row=2, column=1)

            user_name = tk.Label(
                profile_frame,
                text=user.name,
                font=("Verdana", 10, "bold")
            )
            user_name.grid(row=0, column=2)

            user_email = tk.Label(
                profile_frame,
                text=user.email,
                font=("Verdana", 10, "bold")
            )
            user_email.grid(row=1, column=2)

            user_password = tk.Label(
                profile_frame,
                text=user.password,
                font=("Verdana", 10, "bold")
            )
            user_password.grid(row=2, column=2)
        if asyncio.get_event_loop().is_running():
            asyncio.get_event_loop().create_task(my_profile_page())
        else:
            asyncio.get_event_loop().run_until_complete(my_profile_page())

    def open_main_interface(self):
        main_interface_window.MainInterfaceWindow(self, self.user)

    def change_name(self):
        ChangeName(self, self.user)

    def change_password(self):
        ChangePassword(self, self.user)

    def change_profile_pic(self):
        path_to_save_new_pic = f'static/profile_pics/user_id_{self.user.id}_uploaded_pic.png'
        if main_config_file.image_uploader(path_to_save_new_pic) is True:
            async def sub_change_profile_pic():
                self.user.profile_pic_path = path_to_save_new_pic
                await self.user.save()
                ProfilePage(self, self.user)

            asyncio.get_event_loop().run_until_complete(sub_change_profile_pic())

