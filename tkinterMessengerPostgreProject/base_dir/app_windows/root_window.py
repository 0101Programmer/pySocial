import asyncio
import tkinter as tk

from PIL import Image, ImageTk
from async_tkinter_loop import async_handler, async_mainloop
from tortoise import Tortoise
from tortoise.connection import connections

from base_dir.app_windows.login_window import Login
from base_dir.app_windows.my_profile_window import MyProfile
from base_dir.app_windows.registration_window import Registration
from base_dir.config import db_password, db_name, check_user_sys_info
from base_dir.db_config.db_models import User

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def tortoise_init():
    await Tortoise.init(db_url=f'asyncpg://postgres:{db_password}@localhost:5432/{db_name}',
                        modules={"app": ["base_dir.db_config.db_models"]})
    await Tortoise.generate_schemas(safe=True)


class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Python Social')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)

        self.root_frame = root_frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        root_frame.pack(expand=True)

        img_path = '../static/windows_pics/logo_sw.png'
        self.image = Image.open(img_path)
        self.image = self.image.resize((100, 100), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(
            root_frame,
            image=f'{self.image}',
            borderwidth=2,
            relief="groove"
        )
        self.image_label.grid(pady=5)

        app_name_lb = tk.Label(
            root_frame,
            text="PySocial",
            borderwidth=2,
            relief="groove",
            font=("Verdana", 10, "bold")
        )
        app_name_lb.grid(pady=5)

        check_user_btn = tk.Button(self, text="None", command=async_handler(self.check_user))
        check_user_btn.pack()
        check_user_btn.pack_forget()
        check_user_btn.after(0, check_user_btn.invoke)

    async def check_user(self):
        current_system_data = check_user_sys_info()
        user = await User.filter(
            session_data__contains={"status": "active", "system_info": current_system_data}).first()
        if user:
            MyProfile(self, user)
        else:
            reg_btn = tk.Button(
                self.root_frame,
                text="Регистрация",
                command=self.registration,
                height=1, width=20
            )
            reg_btn.grid()

            log_btn = tk.Button(
                self.root_frame,
                text="Авторизация",
                command=self.login,
                height=1, width=20
            )
            log_btn.grid()

    def registration(self):
        Registration(self)

    def login(self):
        Login(self)


root = Root()
if __name__ == '__main__':
    try:
        loop.run_until_complete(tortoise_init())
        async_mainloop(root)
    finally:
        loop.run_until_complete(connections.close_all())
        loop.close()
