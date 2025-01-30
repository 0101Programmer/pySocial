import datetime
import re
from tkinter import filedialog, messagebox
import platform

import requests
from PIL import Image



def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    match = re.match(pattern, email)
    if match:
        return True
    else:
        return False


def img_resizer(img_path, new_img_path, size_tuple):
    image = Image.open(img_path)
    image.thumbnail(size_tuple)
    image.save(new_img_path)


def image_uploader(path_to_save):
    img_types = [('image files', '*.png *.jpg *.jpeg')]
    img_path = filedialog.askopenfilename(filetypes=img_types)
    if img_path != "":
        image = Image.open(img_path)
        image.save(path_to_save)
        return True
    else:
        messagebox.showinfo('Python Social', '  Пожалуйста, выберите изображение для загрузки  ')
        return False


# функция для отображения погоды


appid = APIKey
msc_city_id = 524901
spb_city_id = 498817
samara_city_id = 499099
omsk_city_id = 1496153
obninsk_city_id = 516436
yaroslavl_city_id = 468902


def weather_check(city_id):
    url = "http://api.openweathermap.org"
    timeout = 2
    try:
        requests.get(url, timeout=timeout)
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        return {'cond': data['weather'][0]['description'],
                'temperature': data['main']['temp'],
                'temperature_min': data['main']['temp_min'],

                'temperature_max': data['main']['temp_max']}
    except (requests.ConnectionError, requests.Timeout):
        return None


# ----------------------------------------------->


def is_not_empty(string):
    return bool(string.strip())


def check_user_sys_info():
    current_sys_info = {"system": platform.uname().system,
                        "node_name": platform.uname().node,
                        "release": platform.uname().release,
                        "version": platform.uname().version,
                        "machine": platform.uname().machine,
                        "processor": platform.uname().processor,
                        }
    return current_sys_info


def day_time_counter():
    min_morning_target_time = datetime.datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)
    max_morning_target_time = datetime.datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)

    min_afternoon_target_time = datetime.datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    max_afternoon_target_time = datetime.datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)

    min_evening_target_time = datetime.datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)
    max_evening_target_time = datetime.datetime.now().replace(hour=21, minute=0, second=0, microsecond=0)

    min_night_target_time = datetime.datetime.now().replace(hour=21, minute=0, second=0, microsecond=0)
    max_night_target_time = datetime.datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)

    if min_morning_target_time <= datetime.datetime.now() < max_morning_target_time:
        return "Утро"
    elif min_afternoon_target_time <= datetime.datetime.now() < max_afternoon_target_time:
        return "День"
    elif min_evening_target_time <= datetime.datetime.now() < max_evening_target_time:
        return "Вечер"
    else:
        return "Ночь"


def nested_lists_maker(nested_lists_len: int, original_list: list):
    new_list = []
    final_sub_list = []
    if len(original_list) > nested_lists_len:
        while len(original_list) >= nested_lists_len:
            sub_list = original_list[:nested_lists_len]
            for i in sub_list:
                original_list.remove(i)
            new_list.append(sub_list)
        if len(original_list) != 0:
            for j in original_list:
                final_sub_list.append(j)
            new_list.append(final_sub_list)
        return new_list
    else:
        return original_list
