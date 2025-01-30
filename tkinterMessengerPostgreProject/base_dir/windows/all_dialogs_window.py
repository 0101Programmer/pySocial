import asyncio
import datetime
import json
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.simpledialog import askstring

import psycopg2
from base_dir.db_config.db_models import Dialog, User
from base_dir.windows import main_interface_window, dialog_window


class MessagePage(tk.Toplevel):
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

        main_menu.add_command(label="На главную", command=self.open_main_interface)

        self.config(menu=main_menu)

        messages_frame = tk.Frame(
            self
        )
        messages_frame.pack(expand=True)

        async def get_all_dialogs():

            all_dialogs_caption_lb = tk.Label(
                messages_frame,
                text="Диалоги:"
            )
            all_dialogs_caption_lb.grid()

            for dialog in await user.dialogs_started_by_user.all():
                dialog_lb = tk.Label(
                    messages_frame,
                    text=f"Диалог с {sub_user.name if (sub_user := await User.get(id=dialog.started_by_user_id)) else "error"}",
                )
                dialog_lb.grid()

                dialog_btn = tk.Button(
                    messages_frame,
                    text=f"{dialog.dialog_data[max(dialog.dialog_data, key=int)]["text"][:15]}...",
                    height=1, width=20,
                    command=self.open_dialog(dialog)
                )
                dialog_btn.grid()

        if asyncio.get_event_loop().is_running():
            asyncio.get_event_loop().create_task(get_all_dialogs())
        else:
            asyncio.get_event_loop().run_until_complete(get_all_dialogs())

        # conn = psycopg2.connect(user="postgres", password=cnf.db_password, host="127.0.0.1", port="5432",
        #                         database=cnf.db_name)
        # with conn.cursor() as curs:
        #     curs.execute("SELECT * from Users where is_active=%s", (True,))
        #     active_user_data = curs.fetchone()
        #
        #     curs.execute("SELECT * from Dialogs where started_by_user_id=%s or user2_id=%s",
        #                  (active_user_data[0], active_user_data[0]))
        #     messages_data = curs.fetchall()
        #
        #     dialog_id_last_message_time_dict = {}
        #
        #     for i, val in enumerate(messages_data):
        #         dialog_id_last_message_time_dict[val[0]] = val[5]
        #         sorted_items = sorted(dialog_id_last_message_time_dict.items(), key=lambda item: item[1], reverse=True)
        #         sorted_dialog_id_last_message_time_dict = dict(sorted_items)
        #
        #     for dialog_id in [k for k, v in sorted_dialog_id_last_message_time_dict.items()]:
        #         curs.execute("SELECT * from Dialogs where uniq_dialog_id=%s",
        #                      (dialog_id,))
        #         dialog_data = curs.fetchall()[0]
        #
        #         last_message_sender_id = dialog_data[3][f'{max(dialog_data[3], key=int)}']['sender_id']
        #         curs.execute(f"SELECT full_name from Users where id={last_message_sender_id}")
        #         last_message_sender_full_name = curs.fetchone()[0]
        #
        #         message_btn = tk.Button(
        #             messages_frame,
        #             text=f'{last_message_sender_full_name}: {dialog_data[3][f'{max(dialog_data[3], key=int)}']['text'][:15]}...',
        #             height=1, width=25,
        #             command=self.open_message(dialog_data[0])
        #         )
        #
        #         message_txt = ''
        #
        #         if int(dialog_data[1]) == active_user_data[0] and dialog_data[2] is None:
        #             message_txt = 'Заметки'
        #         elif int(dialog_data[1]) == active_user_data[0] and int(dialog_data[2]) is not None:
        #             curs.execute("SELECT full_name from Users where id=%s", (dialog_data[2],))
        #             result = curs.fetchone()[0]
        #             message_txt = f"Диалог с {result}"
        #         else:
        #             curs.execute("SELECT full_name from Users where id=%s", (dialog_data[1],))
        #             result = curs.fetchone()[0]
        #             message_txt = f"Диалог с {result}"
        #
        #         message_lb = tk.Label(
        #             messages_frame,
        #             text=message_txt,
        #             font=("Verdana", 8, "bold")
        #         )
        #
        #         message_lb.grid()
        #         message_btn.grid()
        #
        #     if active_user_data[5] is not None:
        #         dialog_not_exist_with = []
        #
        #         for k, v in active_user_data[5].items():
        #             if v['self_is_confirmed'] is True and v['friend_is_confirmed'] is True:
        #                 curs.execute(
        #                     'SELECT * from Dialogs where (started_by_user_id=%s and user2_id=%s) or '
        #                     '(started_by_user_id=%s and user2_id=%s)',
        #                     (active_user_data[0], int(k), int(k), active_user_data[0]))
        #                 check = curs.fetchone()
        #                 if not check:
        #                     dialog_not_exist_with.append(k)
        #
        #         if len(dialog_not_exist_with) != 0:
        #
        #             new_dialog_with_lb = tk.Label(
        #                 messages_frame,
        #                 text="Начать новый диалог с:"
        #             )
        #             new_dialog_with_lb.grid()
        #
        #             friends_email_list = []
        #             for user_id in dialog_not_exist_with:
        #                 curs.execute('SELECT email FROM Users WHERE id=%s', (user_id,))
        #                 _ = curs.fetchone()[0]
        #                 friends_email_list.append(_)
        #
        #             self.friends_combobox = ttk.Combobox(messages_frame,
        #                                                  values=friends_email_list,
        #                                                  state="readonly")
        #             self.friends_combobox.grid()
        #             self.friends_combobox.bind("<<ComboboxSelected>>", self.start_dialog)
        #
        # conn.close()

    def start_dialog(self, event):
        selected_email = self.friends_combobox.get()

        conn = psycopg2.connect(user="postgres", password=cnf.db_password, host="127.0.0.1", port="5432",
                                database=cnf.db_name)
        with conn.cursor() as curs:

            curs.execute("SELECT * from Users where is_active=%s", (True,))
            active_user_data = curs.fetchone()

            curs.execute("SELECT * from Users where email=%s", (selected_email,))
            start_dialog_with_user_data = curs.fetchone()

            curs.execute(
                "SELECT * from Dialogs where started_by_user_id=%s and user2_id=%s or started_by_user_id=%s and "
                "user2_id=%s",
                (active_user_data[0], start_dialog_with_user_data[0],
                 start_dialog_with_user_data[0], active_user_data[0]))
            messages_exist_check = curs.fetchone()

            if not messages_exist_check:
                start_message = askstring('Python Social', 'Введите сообщение для отправки')

                if len(start_message) <= 0:
                    messagebox.showinfo('Python Social', 'Нельзя отправить пустое сообщение')
                elif not cnf.is_not_empty(start_message):
                    messagebox.showinfo('Python Social', 'Нельзя отправить пустое сообщение')
                else:
                    message = f"Начать диалог с {start_dialog_with_user_data[1]}?"
                    if messagebox.askyesno(message=message):
                        num = random.randint(0, 999999)
                        dialog_id = hash(str(num))
                        start_message_dict = {
                            1: {
                                "text": start_message,
                                "sender_id": active_user_data[0],
                                "message_sent_time": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                            }
                        }
                        curs.execute("""INSERT INTO Dialogs (uniq_dialog_id, started_by_user_id, user2_id, dialog_data, messages_counter, last_message_time) 
                                                            VALUES (%s, %s, %s, %s, %s, %s)""",
                                     (dialog_id, active_user_data[0], start_dialog_with_user_data[0],
                                      json.dumps(start_message_dict), 1, datetime.datetime.now()))
                        conn.commit()
                        dialog_window.DialogPage(self, dialog_id)
        conn.close()

    def open_main_interface(self):
        main_interface_window.MainInterfaceWindow(self)

    def open_dialog(self, dialog):
        def sub_function():
            dialog_window.DialogPage(self, dialog)

        return sub_function
