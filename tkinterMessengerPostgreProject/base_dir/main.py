import asyncio
import tkinter as tk
from PIL import Image, ImageTk
from tortoise import run_async
import base_dir.config as main_config_file
from base_dir.db_config.db_connection import tortoise_init
from base_dir.db_config.db_models import User
from base_dir.windows.login_window import LogWindow
from base_dir.windows.registration_window import RegWindow
from base_dir.windows.my_profile_window import ProfilePage


class StartWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.user = None
        self.title('Python Social')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)

        async def start_window():
            start_frame = tk.Frame(
                self,
                padx=10,
                pady=10
            )
            start_frame.pack(expand=True)

            img_path = 'static/windows_pics/logo_sw.png'
            self.image = Image.open(img_path)
            self.image = self.image.resize((100, 100), Image.Resampling.LANCZOS)
            self.image = ImageTk.PhotoImage(self.image)
            self.image_label = tk.Label(
                start_frame,
                image=f'{self.image}',
                borderwidth=2,
                relief="groove"
            )
            self.image_label.grid(pady=5)

            app_name_lb = tk.Label(
                start_frame,
                text="PySocial",
                borderwidth=2,
                relief="groove",
                font=("Verdana", 10, "bold")
            )
            app_name_lb.grid(pady=5)
            current_system_data = main_config_file.check_user_sys_info()
            user = await User.filter(
                session_data__contains={"status": "active", "system_info": current_system_data}).first()
            if user:
                ProfilePage(self, user)
            else:
                reg_btn = tk.Button(
                    start_frame,
                    text="Регистрация",
                    command=self.registration,
                    height=1, width=20
                )
                reg_btn.grid()

                log_btn = tk.Button(
                    start_frame,
                    text="Авторизация",
                    command=self.login,
                    height=1, width=20
                )
                log_btn.grid()
        asyncio.get_event_loop().run_until_complete(start_window())

    def registration(self):
        RegWindow(self)

    def login(self):
        LogWindow(self)

    def my_profile(self):
        ProfilePage(self, self.user)


if __name__ == "__main__":
    run_async(tortoise_init())
    app = StartWindow()
    app.mainloop()
