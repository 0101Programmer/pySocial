import tkinter as tk
from tkinter import simpledialog, messagebox

from PIL import Image, ImageTk
from async_tkinter_loop import async_handler
import base_dir.app_windows.main_interface_window as main_interface_module
from base_dir.config import is_not_empty, image_uploader


class MyProfile(tk.Toplevel):
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
        change_profile_data_menu = tk.Menu(tearoff=0)
        change_profile_data_menu.add_command(label="Сменить фотографию профиля", command=async_handler(self.change_profile_pic))
        change_profile_data_menu.add_command(label="Сменить имя", command=async_handler(self.change_name))
        change_profile_data_menu.add_command(label="Сменить пароль", command=async_handler(self.change_password))

        main_menu.add_cascade(label="На главную", command=self.open_main_interface)
        main_menu.add_cascade(label="Изменить личные данные", menu=change_profile_data_menu)
        self.config(menu=main_menu)

        profile_frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        profile_frame.pack(expand=True)

        img_path = user.profile_pic_path
        self.image = Image.open(img_path)
        self.image = self.image.resize((120, 80), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(
            profile_frame,
            image=f'{self.image}',
            borderwidth=2,
            relief="groove"
        )
        self.image_label.grid(row=0, rowspan=4, pady=5, padx=5)

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

        birthdate_lb = tk.Label(
            profile_frame,
            text="Дата рождения:"
        )
        birthdate_lb.grid(row=3, column=1)

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

        user_birthdate = tk.Label(
            profile_frame,
            text=user.birthdate,
            font=("Verdana", 10, "bold")
        )
        user_birthdate.grid(row=3, column=2)

    def open_main_interface(self):
        main_interface_module.MainInterface(self, self.user)

    async def change_name(self):
        new_name = simpledialog.askstring("PyS", "Введите ваше ФИО")
        if new_name:
            name_digits_check = any(_.isdigit() for _ in new_name)
            if name_digits_check is True or not is_not_empty(new_name):
                messagebox.showinfo('Python Social', 'Пожалуйста, введите корректное значение. Имя не должно содержать цифры или быть пустой строкой')
            else:
                self.user.name = new_name
                await self.user.save()
                MyProfile(self, self.user)

    async def change_password(self):
        new_password = simpledialog.askstring("PyS", "Введите новый пароль")
        if new_password:
            password_digits_check = any(_.isdigit() for _ in new_password)
            if not password_digits_check or not is_not_empty(new_password) or len(new_password) < 5:
                messagebox.showinfo('Python Social',
                                    'Пожалуйста, введите корректное значение. Пароль должен состоять из более, чем 5-ти символов, содержать не только буквы, не быть пустой строкой')
            else:
                new_password_confirmation = simpledialog.askstring("PyS", "Повторите пароль")
                if new_password_confirmation:
                    if new_password != new_password_confirmation:
                        messagebox.showinfo('Python Social',"Пароли не совпадают")
                    else:
                        self.user.password = new_password
                        await self.user.save()
                        MyProfile(self, self.user)

    async def change_profile_pic(self):
        path_to_save_new_pic = f'../static/profile_pics/user_id_{self.user.id}_uploaded_profile_pic.png'
        if image_uploader(path_to_save_new_pic) is True:
            self.user.profile_pic_path = path_to_save_new_pic
            await self.user.save()
            MyProfile(self, self.user)
