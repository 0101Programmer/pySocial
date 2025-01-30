import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import psycopg2

import base_dir.config as cnf
from base_dir.windows import main_interface_window, other_profile_window


class FriendsPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        parent.withdraw()
        self.protocol("WM_DELETE_WINDOW", lambda: parent.destroy())

        self.title('Python Social')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)

        main_menu = tk.Menu()

        main_menu.add_command(label="Назад", command=self.open_main_interface)

        self.config(menu=main_menu)

        friends_page_frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        friends_page_frame.pack(expand=True)

        conn = psycopg2.connect(user="postgres", password=cnf.db_password, host="127.0.0.1", port="5432",
                                database=cnf.db_name)
        with conn.cursor() as curs:
            curs.execute('SELECT * FROM Users WHERE is_active=%s', (True,))
            user_data = curs.fetchone()

            search_friend_lb = tk.Label(
                friends_page_frame,
                text="Посмотреть профиль или найти друга по email:"
            )
            search_friend_lb.grid(row=0, column=0, sticky="e")

            if user_data[5] is not None:

                self_confirmed = []
                friend_confirmed = []
                confirmed = []

                for k, v in user_data[5].items():
                    if v['self_is_confirmed'] is True and v['friend_is_confirmed'] is False:
                        self_confirmed.append(k)
                    elif v['self_is_confirmed'] is False and v['friend_is_confirmed'] is True:
                        friend_confirmed.append(k)
                    else:
                        confirmed.append(k)

                print('self_confirmed:', len(self_confirmed), 'friend_confirmed:', len(friend_confirmed), 'confirmed:',
                      len(confirmed))

                if len(confirmed) != 0:

                    if len(self_confirmed) == 0 and len(friend_confirmed) == 0:

                        my_friends_lb = tk.Label(
                            friends_page_frame,
                            text="Убрать пользователя из списка друзей:"
                        )
                        my_friends_lb.grid(row=1, column=0, sticky="e")

                        friends_email_list = []
                        for user_id in confirmed:
                            curs.execute('SELECT email FROM Users WHERE id=%s', (user_id,))
                            _ = curs.fetchone()[0]
                            if _ != 'DELETED':
                                friends_email_list.append(_)

                        self.friends_combobox = ttk.Combobox(friends_page_frame,
                                                             values=friends_email_list,
                                                             width=22,
                                                             state="readonly")
                        self.friends_combobox.grid(row=1, column=1)
                        self.friends_combobox.bind("<<ComboboxSelected>>", self.delete_friend)

                    elif len(self_confirmed) != 0 and len(friend_confirmed) == 0:

                        my_friends_lb = tk.Label(
                            friends_page_frame,
                            text="Убрать пользователя из списка друзей:"
                        )
                        my_friends_lb.grid(row=1, column=0, sticky="e")

                        friends_email_list = []
                        for user_id in confirmed:
                            curs.execute('SELECT email FROM Users WHERE id=%s', (user_id,))
                            _ = curs.fetchone()[0]
                            if _ != 'DELETED':
                                friends_email_list.append(_)

                        self.friends_combobox = ttk.Combobox(friends_page_frame,
                                                             values=friends_email_list,
                                                             width=22,
                                                             state="readonly")
                        self.friends_combobox.grid(row=1, column=1)
                        self.friends_combobox.bind("<<ComboboxSelected>>", self.delete_friend)

                        my_applications_friends_lb = tk.Label(
                            friends_page_frame,
                            text="Отправленные заявки в друзья:"
                        )
                        my_applications_friends_lb.grid(row=2, column=0, sticky="e")

                        my_applications_friends_email_list = []
                        for user_id in self_confirmed:
                            curs.execute('SELECT email FROM Users WHERE id=%s', (user_id,))
                            _ = curs.fetchone()[0]
                            my_applications_friends_email_list.append(_)

                        self.my_applications_combobox = ttk.Combobox(friends_page_frame,
                                                                     values=my_applications_friends_email_list,
                                                                     width=22,
                                                                     state="readonly")
                        self.my_applications_combobox.grid(row=2, column=1)
                        self.my_applications_combobox.bind("<<ComboboxSelected>>", self.cancel_my_friend_application)

                    elif len(self_confirmed) == 0 and len(friend_confirmed) != 0:

                        my_friends_lb = tk.Label(
                            friends_page_frame,
                            text="Убрать пользователя из списка друзей:"
                        )
                        my_friends_lb.grid(row=1, column=0, sticky="e")

                        friends_email_list = []
                        for user_id in confirmed:
                            curs.execute('SELECT email FROM Users WHERE id=%s', (user_id,))
                            _ = curs.fetchone()[0]
                            if _ != 'DELETED':
                                friends_email_list.append(_)

                        self.friends_combobox = ttk.Combobox(friends_page_frame,
                                                             values=friends_email_list,
                                                             width=22,
                                                             state="readonly")
                        self.friends_combobox.grid(row=1, column=1)
                        self.friends_combobox.bind("<<ComboboxSelected>>", self.delete_friend)

                        friends_applications_lb = tk.Label(
                            friends_page_frame,
                            text="Заявки, ожидающие вашего подтверждения:"
                        )
                        friends_applications_lb.grid(row=2, column=0, sticky="e")

                        friends_applications_email_list = []
                        for user_id in friend_confirmed:
                            curs.execute('SELECT email FROM Users WHERE id=%s', (user_id,))
                            _ = curs.fetchone()[0]
                            if _ != "DELETED":
                                friends_applications_email_list.append(_)

                        self.friends_applications_combobox = ttk.Combobox(friends_page_frame,
                                                                          values=friends_applications_email_list,
                                                                          width=22,
                                                                          state="readonly")
                        self.friends_applications_combobox.grid(row=2, column=1)
                        self.friends_applications_combobox.bind("<<ComboboxSelected>>", self.accept_friend_application)

                    elif len(self_confirmed) != 0 and len(friend_confirmed) != 0:

                        my_friends_lb = tk.Label(
                            friends_page_frame,
                            text="Убрать пользователя из списка друзей:"
                        )
                        my_friends_lb.grid(row=1, column=0, sticky="e")

                        friends_email_list = []
                        for user_id in confirmed:
                            curs.execute('SELECT email FROM Users WHERE id=%s', (user_id,))
                            _ = curs.fetchone()[0]
                            if _ != 'DELETED':
                                friends_email_list.append(_)

                        self.friends_combobox = ttk.Combobox(friends_page_frame,
                                                             values=friends_email_list,
                                                             width=22,
                                                             state="readonly")
                        self.friends_combobox.grid(row=1, column=1)
                        self.friends_combobox.bind("<<ComboboxSelected>>", self.delete_friend)

                        my_applications_friends_lb = tk.Label(
                            friends_page_frame,
                            text="Отправленные заявки в друзья:"
                        )
                        my_applications_friends_lb.grid(row=2, column=0, sticky="e")

                        my_applications_friends_email_list = []
                        for user_id in self_confirmed:
                            curs.execute('SELECT email FROM Users WHERE id=%s', (user_id,))
                            _ = curs.fetchone()[0]
                            if _ != "DELETED":
                                my_applications_friends_email_list.append(_)

                        my_applications_combobox = ttk.Combobox(friends_page_frame,
                                                                values=my_applications_friends_email_list,
                                                                width=22,
                                                                state="readonly")
                        my_applications_combobox.grid(row=2, column=1)

                        friends_applications_lb = tk.Label(
                            friends_page_frame,
                            text="Заявки, ожидающие вашего подтверждения:"
                        )
                        friends_applications_lb.grid(row=3, column=0, sticky="e")

                        friends_applications_email_list = []
                        for user_id in friend_confirmed:
                            curs.execute('SELECT email FROM Users WHERE id=%s', (user_id,))
                            _ = curs.fetchone()[0]
                            if _ != "DELETED":
                                friends_applications_email_list.append(_)

                        self.friends_applications_combobox = ttk.Combobox(friends_page_frame,
                                                                          values=friends_applications_email_list,
                                                                          width=22,
                                                                          state="readonly")
                        self.friends_applications_combobox.grid(row=3, column=1)
                        self.friends_applications_combobox.bind("<<ComboboxSelected>>", self.accept_friend_application)

                else:

                    if len(self_confirmed) != 0 and len(friend_confirmed) == 0:

                        my_applications_friends_lb = tk.Label(
                            friends_page_frame,
                            text="Отправленные заявки в друзья:"
                        )
                        my_applications_friends_lb.grid(row=1, column=0, sticky="e")

                        my_applications_friends_email_list = []
                        for user_id in self_confirmed:
                            curs.execute('SELECT email FROM Users WHERE id=%s', (user_id,))
                            _ = curs.fetchone()[0]
                            my_applications_friends_email_list.append(_)

                        self.my_applications_combobox = ttk.Combobox(friends_page_frame,
                                                                     values=my_applications_friends_email_list,
                                                                     width=22,
                                                                     state="readonly")
                        self.my_applications_combobox.grid(row=1, column=1)
                        self.my_applications_combobox.bind("<<ComboboxSelected>>", self.cancel_my_friend_application)

                    elif len(self_confirmed) != 0 and len(friend_confirmed) != 0:

                        my_applications_friends_lb = tk.Label(
                            friends_page_frame,
                            text="Отправленные заявки друзья:"
                        )
                        my_applications_friends_lb.grid(row=1, column=0, sticky="e")

                        friends_applications_lb = tk.Label(
                            friends_page_frame,
                            text="Заявки, ожидающие вашего подтверждения:"
                        )
                        friends_applications_lb.grid(row=2, column=0, sticky="e")

                    elif len(self_confirmed) == 0 and len(friend_confirmed) != 0:

                        friends_applications_lb = tk.Label(
                            friends_page_frame,
                            text="Заявки, ожидающие вашего подтверждения:"
                        )
                        friends_applications_lb.grid(row=1, column=0, sticky="e")

                        friends_applications_email_list = []
                        for user_id in friend_confirmed:
                            curs.execute('SELECT email FROM Users WHERE id=%s', (user_id,))
                            _ = curs.fetchone()[0]
                            friends_applications_email_list.append(_)

                        self.friends_applications_combobox = ttk.Combobox(friends_page_frame,
                                                                          values=friends_applications_email_list,
                                                                          width=22,
                                                                          state="readonly")
                        self.friends_applications_combobox.grid(row=1, column=1)
                        self.friends_applications_combobox.bind("<<ComboboxSelected>>", self.accept_friend_application)

            else:
                my_friends_lb = tk.Label(
                    friends_page_frame,
                    text="Добавьте новых друзей на этой странице!"
                )
                my_friends_lb.grid(row=1, column=0, columnspan=3, sticky="ew")

            self.friend_email_ent = tk.Entry(
                friends_page_frame,
                width=25
            )
            self.friend_email_ent.grid(row=0, column=1, pady=5)

            search_friend_btn = tk.Button(
                friends_page_frame,
                text='Поиск',
                command=self.search_friend_data_validate,
                height=1, width=15
            )
            search_friend_btn.grid(row=0, column=2, padx=5)

        conn.close()

    def cancel_my_friend_application(self, event):
        selected_email = self.my_applications_combobox.get()
        message = f"Отозвать заявку на добавление {selected_email} в друзья?"
        if messagebox.askyesno(message=message):
            conn = psycopg2.connect(user="postgres", password=cnf.db_password, host="127.0.0.1", port="5432",
                                    database=cnf.db_name)
            with conn.cursor() as curs:
                curs.execute("SELECT * from Users where is_active=%s", (True,))
                active_user_data = curs.fetchone()

                curs.execute("SELECT * from Users where email=%s", (selected_email,))
                friend_to_cancel_data = curs.fetchone()

                curs.execute("SELECT friends_with from Users where is_active=%s",
                             (True,))
                self_dict_to_upd = curs.fetchone()[0]

                self_dict_to_upd.pop(str(friend_to_cancel_data[0]), None)
                if len(self_dict_to_upd) == 0:
                    self_dict_to_upd = None
                curs.execute("Update Users set friends_with=%s where is_active=%s",
                             (json.dumps(self_dict_to_upd), True))

                curs.execute("SELECT friends_with from Users where email=%s",
                             (selected_email,))
                friend_dict_to_upd = curs.fetchone()[0]

                friend_dict_to_upd.pop(str(active_user_data[0]), None)
                if len(friend_dict_to_upd) == 0:
                    friend_dict_to_upd = None
                curs.execute("Update Users set friends_with=%s where email=%s",
                             (json.dumps(friend_dict_to_upd), selected_email))
                conn.commit()
            conn.close()
            messagebox.showinfo('Python Social', '   Заявка отозвана   ')
            FriendsPage(self)

    def delete_friend(self, event):
        selected_email = self.friends_combobox.get()

        conn = psycopg2.connect(user="postgres", password=cnf.db_password, host="127.0.0.1", port="5432",
                                database=cnf.db_name)
        message = f"Удалить {selected_email} из вашего списка друзей?"
        if messagebox.askyesno(message=message):
            with conn.cursor() as curs:
                curs.execute("SELECT * from Users where is_active=%s", (True,))
                active_user_data = curs.fetchone()

                curs.execute("SELECT * from Users where email=%s", (selected_email,))
                friend_to_delete_data = curs.fetchone()

                curs.execute("SELECT friends_with from Users where is_active=%s",
                             (True,))
                self_dict_to_upd = curs.fetchone()[0]

                self_dict_to_upd.pop(str(friend_to_delete_data[0]), None)
                if len(self_dict_to_upd) == 0:
                    self_dict_to_upd = None
                curs.execute("Update Users set friends_with=%s where is_active=%s",
                             (json.dumps(self_dict_to_upd), True))

                curs.execute("SELECT friends_with from Users where email=%s",
                             (selected_email,))
                friend_dict_to_upd = curs.fetchone()[0]

                friend_dict_to_upd.pop(str(active_user_data[0]), None)
                if len(friend_dict_to_upd) == 0:
                    friend_dict_to_upd = None
                curs.execute("Update Users set friends_with=%s where email=%s",
                             (json.dumps(friend_dict_to_upd), selected_email))
                conn.commit()
            conn.close()
            messagebox.showinfo('Python Social', 'Пользователь удалён из вашего списка друзей')
            FriendsPage(self)

    def accept_friend_application(self, event):
        selected_email = self.friends_applications_combobox.get()

        conn = psycopg2.connect(user="postgres", password=cnf.db_password, host="127.0.0.1", port="5432",
                                database=cnf.db_name)
        message = f"Добавить {selected_email} в ваш список друзей?"

        if messagebox.askyesno(message=message):
            with conn.cursor() as curs:
                curs.execute("SELECT * from Users where is_active=%s", (True,))
                active_user_data = curs.fetchone()

                curs.execute("SELECT * from Users where email=%s", (selected_email,))
                friend_to_confirm_data = curs.fetchone()

                old_self_data = active_user_data[5]
                new_self_data = {
                    friend_to_confirm_data[0]: {'self_is_confirmed': True, 'friend_is_confirmed': True}
                }

                curs.execute("Update Users set friends_with=%s where is_active=%s",
                             (json.dumps(old_self_data | new_self_data), True))

                old_other_data = friend_to_confirm_data[5]
                new_other_data = {
                    active_user_data[0]: {'self_is_confirmed': True, 'friend_is_confirmed': True}
                }

                curs.execute("Update Users set friends_with=%s where email=%s",
                             (json.dumps(old_other_data | new_other_data), selected_email))
                conn.commit()
            conn.close()
            messagebox.showinfo('Python Social', 'Пользователь добавлен в ваш список друзей')
            FriendsPage(self)

        else:
            message = f"Отклонить заявку от {selected_email}?"
            if messagebox.askyesno(message=message):

                with conn.cursor() as curs:
                    curs.execute("SELECT * from Users where is_active=%s", (True,))
                    active_user_data = curs.fetchone()

                    curs.execute("SELECT * from Users where email=%s", (selected_email,))
                    friend_to_confirm_data = curs.fetchone()

                    curs.execute("SELECT friends_with from Users where is_active=%s",
                                 (True,))
                    self_dict_to_upd = curs.fetchone()[0]

                    self_dict_to_upd.pop(str(friend_to_confirm_data[0]), None)
                    if len(self_dict_to_upd) == 0:
                        self_dict_to_upd = None
                    curs.execute("Update Users set friends_with=%s where is_active=%s",
                                 (json.dumps(self_dict_to_upd), True))

                    curs.execute("SELECT friends_with from Users where email=%s",
                                 (selected_email,))
                    friend_dict_to_upd = curs.fetchone()[0]

                    friend_dict_to_upd.pop(str(active_user_data[0]), None)
                    if len(friend_dict_to_upd) == 0:
                        friend_dict_to_upd = None
                    curs.execute("Update Users set friends_with=%s where email=%s",
                                 (json.dumps(friend_dict_to_upd), selected_email))
                    conn.commit()
                conn.close()
                messagebox.showinfo('Python Social', '   Заявка отклонена   ')
                FriendsPage(self)

    def open_main_interface(self):
        main_interface_window.MainInterfaceWindow(self)

    def open_user_profile(self, user_email):
        other_profile_window.ProfileView(self, user_email)

    def search_friend_data_validate(self):
        friend_email = str(self.friend_email_ent.get())
        if len(friend_email) == 0:
            messagebox.showinfo('Python Social', '    Заполнены не все поля    ')
        elif not cnf.validate_email(friend_email):
            messagebox.showinfo('Python Social', 'Пожалуйста, введите корректный email')
        else:
            conn = psycopg2.connect(user="postgres", password=cnf.db_password, host="127.0.0.1", port="5432",
                                    database=cnf.db_name)
            with conn.cursor() as curs:
                curs.execute("SELECT email from Users where email=%s", (friend_email,))
                friend_data = curs.fetchone()
                if not friend_data:
                    messagebox.showinfo('Python Social', 'Пользователя с таким email не существует')
                else:
                    curs.execute("SELECT email from Users where is_active=%s", (True,))
                    active_user_data = curs.fetchone()
                    if friend_data[0] == active_user_data[0]:
                        messagebox.showinfo('Python Social',
                                            'Нельзя отправить запрос на добавление в друзья самому себе')
                    else:
                        self.open_user_profile(friend_email)
            conn.close()