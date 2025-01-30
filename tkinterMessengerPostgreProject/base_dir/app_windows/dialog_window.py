import datetime
import os
import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring

from PIL import Image, ImageTk
from async_tkinter_loop import async_handler
import base_dir.app_windows.all_dialogs_window as all_dialogs_module

from base_dir.config import is_not_empty, check_user_sys_info, image_uploader
from base_dir.db_config.db_models import User


class Dialog(tk.Toplevel):
    def __init__(self, parent, dialog, user):
        super().__init__(parent)
        parent.withdraw()
        self.protocol("WM_DELETE_WINDOW", lambda: parent.destroy())
        self.title('Python Social')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)

        get_dialog_data_btn = tk.Button(self, text="None", command=async_handler(self.get_dialog_data))
        get_dialog_data_btn.pack()
        get_dialog_data_btn.pack_forget()
        get_dialog_data_btn.after(0, get_dialog_data_btn.invoke)

        self.dialog = dialog
        self.user = user
        self.images_dict = {}
        self.message_answer_ent = tk.Entry()

        main_menu = tk.Menu()

        main_menu.add_command(label="Назад", command=self.open_all_dialogs_window)

        self.config(menu=main_menu)

        self.dialog_frame = dialog_frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        dialog_frame.pack(expand=True)

        self.message_answer_frame = message_answer_frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        message_answer_frame.pack(expand=True)

    async def get_dialog_data(self):

        self.message_answer_ent = tk.Entry(
            self.message_answer_frame,
            width=24
        )
        self.message_answer_ent.grid(pady=3)

        message_answer_btn = tk.Button(
            self.message_answer_frame,
            height=1, width=20,
            text='Отправить сообщение',
            command=async_handler(self.send_text_answer)
        )
        message_answer_btn.grid()

        pic_answer_btn = tk.Button(
            self.message_answer_frame,
            text='Отправить фото',
            height=1, width=20,
            command=async_handler(self.send_pic_answer)
        )
        pic_answer_btn.grid()

        canvas_box = tk.Canvas(
            self.dialog_frame,
        )

        vertical_bar = tk.Scrollbar(
            self.dialog_frame,
            orient='vertical',
            width=20
        )
        vertical_bar.pack(side='right', fill='y')
        vertical_bar.config(command=canvas_box.yview)

        horizontal_bar = tk.Scrollbar(
            self.dialog_frame,
            orient='horizontal'
        )
        horizontal_bar.pack(side='bottom', fill='x')
        horizontal_bar.config(command=canvas_box.xview)

        canvas_box.config(width=500, height=250,
                          xscrollcommand=horizontal_bar.set,
                          yscrollcommand=vertical_bar.set
                          )
        canvas_box.pack(expand=True, side='left', fill='both')

        start_x_coordinate = 0
        start_y_coordinate = 10
        for k, v in self.dialog.dialog_data.items():
            user = await User.get(id=v["sender_id"])
            canvas_box.create_text(start_x_coordinate, start_y_coordinate, text=("-" * 100))
            canvas_box.create_text(start_x_coordinate, start_y_coordinate + 10,
                                   text=f"{user.name}:")
            if not os.path.isfile(v["text"]):
                if len(v["text"]) < 50:
                    canvas_box.create_text(start_x_coordinate, start_y_coordinate + 25, text=v["text"],
                                           font="TimesNewRoman 10 bold", width=500)
                    canvas_box.create_text(start_x_coordinate, start_y_coordinate + 45, text=v["message_sent_time"])
                    canvas_box.create_text(start_x_coordinate, start_y_coordinate + 55, text=("-" * 100))
                    start_y_coordinate += 100
                else:
                    canvas_box.create_text(start_x_coordinate, start_y_coordinate + 30, text=v["text"],
                                           font="TimesNewRoman 10 bold", width=500)
                    canvas_box.create_text(start_x_coordinate, start_y_coordinate + 50, text=v["message_sent_time"])
                    canvas_box.create_text(start_x_coordinate, start_y_coordinate + 60, text=("-" * 100))
                    start_y_coordinate += 105
            else:
                image = Image.open(v['text'])
                image = image.resize((120, 80), Image.Resampling.LANCZOS)
                image = ImageTk.PhotoImage(image)
                self.images_dict[f"{k}"] = image
                canvas_box.create_image(start_x_coordinate, start_y_coordinate + 70, image=self.images_dict[f"{k}"])
                if v["img_caption"]:
                    canvas_box.create_text(start_x_coordinate, start_y_coordinate + 120, text=f'"{v["img_caption"]}"',
                                           font="TimesNewRoman 10 italic")
                    canvas_box.create_text(start_x_coordinate, start_y_coordinate + 140, text=v["message_sent_time"])
                    canvas_box.create_text(start_x_coordinate, start_y_coordinate + 155, text=("-" * 100))
                    start_y_coordinate += 200
                else:
                    canvas_box.create_text(start_x_coordinate, start_y_coordinate + 120, text=v["message_sent_time"])
                    canvas_box.create_text(start_x_coordinate, start_y_coordinate + 135, text=("-" * 100))
                    start_y_coordinate += 200
        canvas_box.configure(scrollregion=canvas_box.bbox("all"))
        canvas_box.yview_moveto(1.0)

    async def send_text_answer(self):
        if not is_not_empty(self.message_answer_ent.get()):
            messagebox.showinfo('Python Social', '    Нельзя отправить пустое сообщение    ')
        else:
            sender = await User.filter(
                session_data__contains={"status": "active", "system_info": check_user_sys_info()}).first()
            self.dialog.total_messages += 1
            self.dialog.dialog_data[self.dialog.total_messages] = {"text": self.message_answer_ent.get(),
                                                                   "sender_id": sender.id,
                                                                   "message_sent_time": datetime.datetime.now().strftime(
                                                                       "%d/%m/%Y, %H:%M:%S")}
            await self.dialog.save()
            Dialog(self, self.dialog, self.user)

    async def send_pic_answer(self):
        img_caption = askstring('Python Social', 'Введите подпись (по желанию)')
        path_to_save = f'../static/dialog_images/dialog_id_{self.dialog.id}_pic_number_{self.dialog.total_messages + 1}.png'
        if image_uploader(path_to_save) is True:
            sender = await User.filter(
                session_data__contains={"status": "active", "system_info": check_user_sys_info()}).first()
            self.dialog.total_messages += 1
            self.dialog.dialog_data[self.dialog.total_messages] = {"text": path_to_save,
                                                                   "img_caption": img_caption if img_caption else None,
                                                                   "img_id": self.dialog.total_messages,
                                                                   "sender_id": sender.id,
                                                                   "message_sent_time": datetime.datetime.now().strftime(
                                                                       "%d/%m/%Y, %H:%M:%S")}
            await self.dialog.save()
            Dialog(self, self.dialog, self.user)

    def open_all_dialogs_window(self):
        all_dialogs_module.Dialogs(self, self.user)
