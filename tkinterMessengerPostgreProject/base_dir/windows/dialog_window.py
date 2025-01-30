import asyncio
import datetime
import json
import os
import tkinter as tk
from tkinter import messagebox

import psycopg2
from tkinter.simpledialog import askstring

from base_dir.config import is_not_empty, check_user_sys_info
from base_dir.db_config.db_models import Dialog, User

from base_dir.windows import all_dialogs_window, show_dialog_pics_window


class DialogPage(tk.Toplevel):
    def __init__(self, parent, dialog):
        super().__init__(parent)
        parent.withdraw()
        self.protocol("WM_DELETE_WINDOW", lambda: parent.destroy())
        self.title('Python Social')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)
        self.dialog = dialog
        self.message_answer_ent = tk.Entry()
        self.user_id = ""

        async def get_dialog_data():

            main_menu = tk.Menu()

            main_menu.add_command(label="Назад")

            self.config(menu=main_menu)

            dialog_frame = tk.Frame(
                self
            )
            dialog_frame.pack(expand=True)

            message_answer_frame = tk.Frame(self)
            message_answer_frame.pack(expand=True)

            self.message_answer_ent = tk.Entry(
                message_answer_frame,
                width=24
            )
            self.message_answer_ent.grid(pady=3)

            message_answer_btn = tk.Button(
                message_answer_frame,
                height=1, width=20,
                text='Отправить сообщение',
                command=self.send_answer
            )
            message_answer_btn.grid()

            pic_answer_btn = tk.Button(
                message_answer_frame,
                text='Отправить фото',
                height=1, width=20
            )
            pic_answer_btn.grid()

            last_scroll_coord = self.dialog.total_messages * 100
            print(last_scroll_coord)

            canvas_box = tk.Canvas(
                dialog_frame,
                # width=500,
                # height=400,
                scrollregion=(0, 0, 700, last_scroll_coord)
            )

            vertical_bar = tk.Scrollbar(
                dialog_frame,
                orient='vertical'
            )
            vertical_bar.pack(side='right', fill='y')
            vertical_bar.config(command=canvas_box.yview)

            horizontal_bar = tk.Scrollbar(
                dialog_frame,
                orient='horizontal'
            )
            horizontal_bar.pack(side='bottom', fill='x')
            horizontal_bar.config(command=canvas_box.xview)

            canvas_box.config(width=500, height=400)

            canvas_box.config(
                xscrollcommand=horizontal_bar.set,
                yscrollcommand=vertical_bar.set
            )
            canvas_box.pack(expand=True, side='left', fill='both')

            start_x_coordinate = 250
            start_y_coordinate = 10
            for k, v in dialog.dialog_data.items():

                self.user_id = v["sender_id"]
                self.user_name()

                # пропадание содержимого кроется тут:


                # user = await User.get(id=v["sender_id"])
                # canvas_box.create_text(start_x_coordinate, start_y_coordinate,
                #                        text=f"{user.name}:")

                canvas_box.create_text(start_x_coordinate, start_y_coordinate + 15, text=v["text"])
                canvas_box.create_text(start_x_coordinate, start_y_coordinate + 30, text=v["message_sent_time"])
                start_y_coordinate += 60

        if asyncio.get_event_loop().is_running():
            asyncio.get_event_loop().create_task(get_dialog_data())
        else:
            asyncio.get_event_loop().run_until_complete(get_dialog_data())

    # def open_message_page(self):
    #     messages_window.MessagePage(self)

    def user_name(self):
        async def sub_user_name():
            user_name = await User.get(id=self.user_id)
            print(user_name.name)
        asyncio.get_event_loop().create_task(sub_user_name())

    def send_answer(self):
        if not is_not_empty(self.message_answer_ent.get()):
            messagebox.showinfo('Python Social', '    Нельзя отправить пустое сообщение    ')
        else:
            async def async_send_answer():
                sender = await User.filter(
                    session_data__contains={"status": "active", "system_info": check_user_sys_info()}).first()
                self.dialog.total_messages += 1
                self.dialog.dialog_data[self.dialog.total_messages] = {"text": self.message_answer_ent.get(),
                                                                       "sender_id": sender.id,
                                                                       "message_sent_time": datetime.datetime.now().strftime(
                                                                           "%d/%m/%Y, %H:%M:%S")}
                await self.dialog.save()
                DialogPage(self, self.dialog)

            asyncio.get_event_loop().run_until_complete(async_send_answer())

    # def send_pic(self, dialog_id):
    #     def sub_send_pic():
    #         img_caption = askstring('Python Social', 'Введите подпись')
    #
    #         if img_caption:
    #
    #             if len(img_caption) <= 0:
    #                 messagebox.showinfo('Python Social', 'Нельзя отправить изображение без подписи')
    #             elif not cnf.is_not_empty(img_caption):
    #                 messagebox.showinfo('Python Social', 'Нельзя отправить изображение без подписи')
    #             else:
    #
    #                 conn = psycopg2.connect(user="postgres", password=cnf.db_password, host="127.0.0.1", port="5432",
    #                                         database=cnf.db_name)
    #                 with conn.cursor() as curs:
    #                     curs.execute("SELECT * from Users where is_active=%s", (True,))
    #                     user_data = curs.fetchone()
    #                     curs.execute("SELECT * from Dialogs where uniq_dialog_id=%s", (str(dialog_id),))
    #                     dialog_data = curs.fetchone()
    #                     messages_num = dialog_data[4]
    #                     messages_num += 1
    #
    #                     path_to_save = f'static/dialog_images/dialog_id_{dialog_id}_pic_number_{messages_num}.png'
    #                     curs.execute(
    #                         """Update Dialogs set messages_counter=%s, last_message_time=%s where uniq_dialog_id=%s""",
    #                         (messages_num, datetime.datetime.now(), dialog_id))
    #                     curs.execute(
    #                         f"""Update Dialogs set dialog_data[{str(messages_num)}]=%s where uniq_dialog_id=%s""",
    #                         (json.dumps({"text": path_to_save, "sender_id": user_data[0],
    #                                      "message_sent_time": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
    #                                      "img_caption": img_caption}), dialog_id))
    #                     if cnf.image_uploader(path_to_save) is True:
    #                         cnf.img_resizer(path_to_save, path_to_save, (400, 400))
    #                         conn.commit()
    #                         DialogPage(self, dialog_id)
    #                 conn.close()
    #
    #     return sub_send_pic
