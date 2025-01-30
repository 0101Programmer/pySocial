import json
import tkinter as tk
from tkinter import messagebox

import psycopg2
from PIL import Image, ImageTk

import base_dir.config as cnf

from base_dir.windows import friends_window


class ProfileView(tk.Toplevel):
    def __init__(self, parent, user_email):
        super().__init__(parent)
        parent.withdraw()
        self.protocol("WM_DELETE_WINDOW", lambda: parent.destroy())

        self.title('Python Social')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)

        self.user_email = user_email

        main_menu = tk.Menu()

        main_menu.add_command(label="Назад", command=self.back_)

        self.config(menu=main_menu)

        profile_view_frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        profile_view_frame.pack(expand=True)

        conn = psycopg2.connect(user="postgres", password=cnf.db_password, host="127.0.0.1", port="5432",
                                database=cnf.db_name)
        with conn.cursor() as curs:
            curs.execute("SELECT * from Users where email=%s", (user_email,))
            user_data = curs.fetchone()

            curs.execute("SELECT * from Users where is_active=%s", (True,))
            active_user_data = curs.fetchone()

            img_path = user_data[4]
            self.image = Image.open(img_path)
            self.image = ImageTk.PhotoImage(self.image)
            self.image_label = tk.Label(
                profile_view_frame,
                image=f'{self.image}',
                borderwidth=2,
                relief="groove"
            )
            self.image_label.grid(row=0, column=0, pady=5)

            full_name_data = tk.Label(
                profile_view_frame,
                text=user_data[3],
                font=("Verdana", 10, "bold")
            )
            full_name_data.grid(row=0, column=1, pady=5)

            email_data = tk.Label(
                profile_view_frame,
                text=user_data[1],
                font=("Verdana", 10, "bold")
            )
            email_data.grid(row=1, column=1, pady=5)

            if active_user_data[5] is not None and str(user_data[0]) in active_user_data[5] and \
                    active_user_data[5][str(user_data[0])]['self_is_confirmed'] is False and \
                    active_user_data[5][str(user_data[0])]['friend_is_confirmed'] is False or active_user_data[
                5] is None or str(user_data[0]) not in active_user_data[5]:
                add_friend_btn = tk.Button(
                    profile_view_frame,
                    text='Добавить в друзья',
                    command=self.add_friend,
                    height=2, width=15
                )
                add_friend_btn.grid(row=2, column=1)

        conn.close()

    def back_(self):
        friends_window.FriendsPage(self)

    def add_friend(self):
        conn = psycopg2.connect(user="postgres", password=cnf.db_password, host="127.0.0.1", port="5432",
                                database=cnf.db_name)
        with conn.cursor() as curs:
            curs.execute("SELECT * from Users where is_active=%s", (True,))
            active_user_data = curs.fetchone()
            curs.execute("SELECT * from Users where email=%s", (self.user_email,))
            add_friend_user_data = curs.fetchone()

            if active_user_data[5] is not None:
                old_data = active_user_data[5]
                new_data = {
                    add_friend_user_data[0]: {'self_is_confirmed': True, 'friend_is_confirmed': False}
                }
                curs.execute("Update Users set friends_with=%s where is_active=%s",
                             (json.dumps(old_data | new_data), True))
            else:
                new_data = {
                    add_friend_user_data[0]: {'self_is_confirmed': True, 'friend_is_confirmed': False}
                }
                curs.execute("Update Users set friends_with=%s where is_active=%s",
                             (json.dumps(new_data), True))

            if add_friend_user_data[5] is not None:
                old_data = add_friend_user_data[5]
                new_data = {
                    active_user_data[0]: {'self_is_confirmed': False, 'friend_is_confirmed': True}
                }

                curs.execute("Update Users set friends_with=%s where email=%s",
                             (json.dumps(old_data | new_data), self.user_email))
            else:
                new_data = {
                    active_user_data[0]: {'self_is_confirmed': False, 'friend_is_confirmed': True}
                }

                curs.execute("Update Users set friends_with=%s where email=%s",
                             (json.dumps(new_data), self.user_email))

            conn.commit()
            messagebox.showinfo('Python Social', 'Запрос на добавление в друзья отправлен')
            self.back_()

        conn.close()