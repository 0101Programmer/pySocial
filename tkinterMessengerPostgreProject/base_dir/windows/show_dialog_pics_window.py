import tkinter as tk

from PIL import Image, ImageTk

from base_dir.windows import dialog_window


class ShowDialogPicsWin(tk.Toplevel):
    def __init__(self, parent, dialog_id, pics_data):
        super().__init__(parent)
        parent.withdraw()
        self.protocol("WM_DELETE_WINDOW", lambda: parent.destroy())

        self.title('Python Social')
        self.geometry('')
        self.minsize(350, 100)
        self.resizable(False, False)

        main_menu = tk.Menu()

        main_menu.add_command(label="Назад", command=self.back_to_message(dialog_id))

        self.config(menu=main_menu)

        dialog_pics_frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        dialog_pics_frame.pack(expand=True)

        y_scrollregion_coords = len(pics_data) * 100 * 2.7
        canvas_box = tk.Canvas(
            dialog_pics_frame,
            bg='#000080',
            width=500,
            height=400,
            scrollregion=(0, 0, 700, y_scrollregion_coords)
        )

        vertical_bar = tk.Scrollbar(
            dialog_pics_frame,
            orient='vertical'
        )
        vertical_bar.pack(side='right', fill='y')
        vertical_bar.config(command=canvas_box.yview)

        horizontal_bar = tk.Scrollbar(
            dialog_pics_frame,
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

        self.images = {}

        for k, v in pics_data.items():
            img_path = v['img_path']
            self.image = Image.open(img_path)
            self.image = self.image.resize((300, 200), Image.Resampling.LANCZOS)
            self.image = ImageTk.PhotoImage(self.image)
            self.images[str(k)] = {"img": self.image, "img_caption": v['img_caption'], "img_sender": v['img_sender'], "img_sent_time": v['img_sent_time'],}

        start_x_coord = 100
        start_y_coord = 30
        for k, v in self.images.items():
            canvas_box.create_image(start_x_coord, start_y_coord, anchor='nw', image=v['img'])
            canvas_caption = f'| {v['img_sender']} | {v['img_caption']} | {v['img_sent_time']} |'
            canvas_box.create_text(start_x_coord // 2, start_y_coord + 205, text=canvas_caption, anchor='nw', fill="white", font="Verdana 16")
            start_y_coord += 250

    def back_to_message(self, dialog_id):
        def sub_back_to_message():
            dialog_window.DialogPage(self, dialog_id)

        return sub_back_to_message
