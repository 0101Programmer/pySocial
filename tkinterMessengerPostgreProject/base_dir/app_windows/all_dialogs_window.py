import os
import tkinter as tk
from async_tkinter_loop import async_handler
import base_dir.app_windows.dialog_window as dialog_module
import base_dir.app_windows.main_interface_window as main_interface_module
from base_dir.db_config.db_models import User


class Dialogs(tk.Toplevel):
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

        self.messages_frame = messages_frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        messages_frame.pack(expand=True)

        check_user_btn = tk.Button(self, text="None", command=async_handler(self.get_all_dialogs))
        check_user_btn.pack()
        check_user_btn.pack_forget()
        check_user_btn.after(0, check_user_btn.invoke)

        all_dialogs_caption_lb = tk.Label(
            messages_frame,
            text="Диалоги:"
        )
        all_dialogs_caption_lb.grid()

    async def get_all_dialogs(self):
        all_dialogs = {}
        for dialog in await self.user.dialogs_started_by_user.all():
            caption = ""
            if dialog.started_by_user_id == self.user.id and dialog.second_user_id is None:
                caption = "Заметки"
            elif dialog.started_by_user_id == self.user.id and dialog.second_user_id is not None:
                caption = f"Диалог с {(await User.get(id=dialog.second_user_id)).name}"
            # elif dialog.started_by_user_id is not None and dialog.second_user_id == self.user.id:
            #     caption = f"Диалог с {(await User.get(dialog.started_by_user_id)).name}"

            all_dialogs[dialog.id] = {"dialog": dialog, "dialog_lb_caption": caption,
                                      "last_message_time": dialog.last_message_time,
                                      "dialog_btn_caption":
                                          dialog.dialog_data[max(dialog.dialog_data, key=int)]["text"][:15] if not
                                          os.path.isfile(dialog.dialog_data[max(dialog.dialog_data, key=int)]["text"])
                                          else "Изображение"}

        for dialog in await self.user.dialogs_started_with_user.all():
            caption = f"Диалог с {(await User.get(id=dialog.started_by_user_id)).name}"
            all_dialogs[dialog.id] = {"dialog": dialog, "dialog_lb_caption": caption,
                                      "last_message_time": dialog.last_message_time,
                                      "dialog_btn_caption":
                                          dialog.dialog_data[max(dialog.dialog_data, key=int)]["text"][:15] if not
                                          os.path.isfile(dialog.dialog_data[max(dialog.dialog_data, key=int)]["text"])
                                          else "Изображение"}
        all_dialogs_sorted = dict(sorted(all_dialogs.items(), key=lambda item: item[1]['last_message_time'],
                                         reverse=True))

        for k, v in all_dialogs_sorted.items():
            dialog_lb = tk.Label(
                self.messages_frame,
                text=v["dialog_lb_caption"],
            )
            dialog_lb.grid()
            dialog_btn = tk.Button(
                self.messages_frame,
                text=v["dialog_btn_caption"],
                height=1, width=20,
                command=self.open_dialog(v["dialog"])
            )
            dialog_btn.grid()

    def open_main_interface(self):
        main_interface_module.MainInterface(self, self.user)

    def open_dialog(self, dialog):
        def sub_open_dialog():
            dialog_module.Dialog(self, dialog, self.user)

        return sub_open_dialog
