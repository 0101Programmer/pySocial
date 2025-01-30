import asyncio
import datetime
import os
import pathlib
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.simpledialog import askstring
import base_dir.app_windows.friends_window as friends_module
import base_dir.app_windows.dialog_window as dialog_module

from PIL import Image, ImageTk
from async_tkinter_loop import async_handler

from base_dir.config import is_not_empty, validate_email
from base_dir.db_config.db_models import User, Dialog


class ElsesProfile(tk.Toplevel):
    def __init__(self, parent, user, requested_user):
        super().__init__(parent)
        parent.withdraw()
        self.protocol("WM_DELETE_WINDOW", lambda: parent.destroy())
        self.title('Python Social')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)
        self.user = user
        self.requested_user = requested_user

        main_menu = tk.Menu()
        main_menu.add_command(label="Назад", command=self.open_friends_window)
        self.config(menu=main_menu)

        requested_user_profile_frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        requested_user_profile_frame.pack(expand=True)

        requested_user_pic_path = requested_user.profile_pic_path
        self.image = Image.open(requested_user_pic_path)
        self.image = self.image.resize((120, 80), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(
            requested_user_profile_frame,
            image=f'{self.image}',
            borderwidth=2,
            relief="groove"
        )
        self.image_label.grid()

        name_lb = tk.Label(
            requested_user_profile_frame,
            text="Имя:"
        )
        name_lb.grid()

        user_name = tk.Label(
            requested_user_profile_frame,
            text=requested_user.name,
            font=("Verdana", 10, "bold")
        )
        user_name.grid()

        email_lb = tk.Label(
            requested_user_profile_frame,
            text="Email:"
        )
        email_lb.grid()

        user_email = tk.Label(
            requested_user_profile_frame,
            text=requested_user.email,
            font=("Verdana", 10, "bold")
        )
        user_email.grid()

        if user.friends:
            if str(requested_user.id) in user.friends:
                if (user.friends[str(requested_user.id)]["my_confirmation"] and
                        user.friends[str(requested_user.id)]["his_confirmation"]):
                    friendship_check_lb = tk.Label(
                        requested_user_profile_frame,
                        text="Пользователь в вашем списке друзей"
                    )
                    friendship_check_lb.grid()

                    cancel_friend_request_btn = tk.Button(
                        requested_user_profile_frame,
                        text='Удалить',
                        height=1, width=20
                    )
                    cancel_friend_request_btn.grid()

                    write_a_message_btn = tk.Button(
                        requested_user_profile_frame,
                        text='Написать сообщение',
                        command=async_handler(self.write_a_message),
                        height=1, width=20
                    )
                    write_a_message_btn.grid()

                elif (user.friends[str(requested_user.id)]["my_confirmation"] and not
                        user.friends[str(requested_user.id)]["his_confirmation"]):
                    friendship_check_lb = tk.Label(
                        requested_user_profile_frame,
                        text="Заявка на добавления в друзья отправлена",
                    )
                    friendship_check_lb.grid()

                    cancel_friend_request_btn = tk.Button(
                        requested_user_profile_frame,
                        text='Отозвать заявку',
                        command=async_handler(self.cancel_my_request),
                        height=1, width=20
                    )
                    cancel_friend_request_btn.grid()

                elif (not user.friends[str(requested_user.id)]["my_confirmation"] and
                      user.friends[str(requested_user.id)]["his_confirmation"]):
                    friendship_check_lb = tk.Label(
                        requested_user_profile_frame,
                        text="Заявка на добавления в друзья ожидает вашего подтверждения")
                    friendship_check_lb.grid()

                    cancel_friend_request_btn = tk.Button(
                        requested_user_profile_frame,
                        text='Отклонить заявку',
                        height=1, width=20
                    )
                    cancel_friend_request_btn.grid()
            else:
                friendship_check_lb = tk.Label(
                    requested_user_profile_frame,
                    text="Пользователя нет в вашем списке друзей"
                )
                friendship_check_lb.grid()

                cancel_friend_request_btn = tk.Button(
                    requested_user_profile_frame,
                    text='Добавить',
                    command=async_handler(self.add_friend),
                    height=1, width=20
                )
                cancel_friend_request_btn.grid()
        else:
            friendship_check_lb = tk.Label(
                requested_user_profile_frame,
                text="Пользователя нет в вашем списке друзей",
            )
            friendship_check_lb.grid()

            cancel_friend_request_btn = tk.Button(
                requested_user_profile_frame,
                text='Добавить',
                command=async_handler(self.add_friend),
                height=1, width=20
            )
            cancel_friend_request_btn.grid()

    def open_friends_window(self):
        friends_module.Friends(self, self.user)

    async def delete_friend(self):
        pass

    async def write_a_message(self):
        existed_dialog_started_by_user = await Dialog.get_or_none(started_by_user=self.user, second_user=self.requested_user)
        existed_dialog_started_by_requested_user = await Dialog.get_or_none(started_by_user=self.requested_user, second_user=self.user)
        if not existed_dialog_started_by_user or existed_dialog_started_by_requested_user:
            message = askstring('Python Social', 'Введите сообщение')
            if message:
                if is_not_empty(message):
                    await Dialog.create(started_by_user=self.user, second_user=self.requested_user,
                                        dialog_data={1: {
                                            'text': message,
                                            'sender_id': self.user.id,
                                            'message_sent_time': datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                                        }})
                    dialog = await Dialog.get(started_by_user=self.user, second_user=self.requested_user)
                    dialog_module.Dialog(self, dialog, self.user)


    async def cancel_my_request(self):
        message = f"Вы уверены, что хотите отозвать свою заявку?"
        if messagebox.askyesno(message=message):
            del self.user.friends[str(self.requested_user.id)]
            if len(self.user.friends) == 0:
                self.user.friends = None
            del self.requested_user.friends[str(self.user.id)]
            if len(self.requested_user.friends) == 0:
                self.requested_user.friends = None
            await self.user.save()
            await self.requested_user.save()
            ElsesProfile(self, self.user, self.requested_user)

    async def cancel_friend_request(self):
        pass

    async def add_friend(self):
        if not self.user.friends:
            self.user.friends = {
                str(self.requested_user.id): {"my_confirmation": True, "his_confirmation": False,
                                              "his_email": self.requested_user.email}}
        else:
            self.user.friends[str(self.requested_user.id)] = {"my_confirmation": True,
                                                              "his_confirmation": False,
                                                              "his_email": self.requested_user.email}
        if not self.requested_user.friends:
            self.requested_user.friends = {str(self.user.id):
                                               {"my_confirmation": False, "his_confirmation": True,
                                                "his_email": self.user.email}}
        else:
            self.requested_user.friends[str(self.user.id)] = {"my_confirmation": False,
                                                              "his_confirmation": True,
                                                              "his_email": self.user.email}
        await self.user.save()
        await self.requested_user.save()
        ElsesProfile(self, self.user, self.requested_user)
