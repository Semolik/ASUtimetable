import os
import aiohttp

BASE_URL = "https://www.asu.ru"
DATETIME_FORMAT = "%d-%m-%Y %H:%M"
LESSON_DATETIME_FORMAT = '%d.%m.%Y'
TIMETABLE_URL_DATETIME_FORMAT = "%Y%m%d"
DAYS_OF_THE_WEEK = ['Понедельник', 'Вторник', 'Среда',
                    'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
MONTHS_IN_THE_GENITIVE_CASE = ['января', 'февраля', 'марта', 'апреля', 'мая',
                               'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
STUDENTS_BASE_LINK = f"{BASE_URL}/timetable/students/"
TIME_ZONE = 'Asia/Barnaul'
os.environ['TZ'] = TIME_ZONE
timeout_seconds = 10
session_timeout = aiohttp.ClientTimeout(
            total=None, sock_connect=timeout_seconds, sock_read=timeout_seconds)