import os

from dotenv import load_dotenv

load_dotenv()

# BOT_TOKEN = os.getenv("BOT_TOKEN_TEST") if not os.getenv("DEBUGE") else os.getenv("BOT_TOKEN")
BOT_TOKEN: str = os.getenv("BOT_TOKEN")
admins: list[int] = [
    420624020
]
EVENT_FORM: str = """
*{0}*
{1}
Дата проведения: *{2}*
"""

REGISTER_FORM: str = """
📇ФИО: *{0}*
🏢Почта: *{1}*
👥ВУЗ: *{2}*
📱Телефон: *{3}*
"""

HUMAN_MONTHS: list[str] = [
    "Unknown",
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь"
]

HUMAN_MONTHS_TWO: list[str] = ["Unknown",
          "Января",
          "Февраля",
          "Марта",
          "Апреля",
          "Мая",
          "Июня",
          "Июля",
          "Августа",
          "Сентября",
          "Октября",
          "Ноября",
          "Декабря"]

# REGISTER_FORM: str = """
# ФИО: <b>{0}</b>
# Факультет: <b>{1}</b>
# Группа: <b>{2}</b>
# Тел.: <b>{3}</b>
# """
# FACULTY_MASS = [
#     'ФТС',
#     'ИЭФ',
#     'ФЭИП',
#     'СПФ',
#     'ФИТИМ',
# ]
FACULTY_MASS: list[str] = [
    'ФТС',
    'ИЭФ',
    'ФЭиП',
    'СПФ',
    'ФИИЦТ',
]

HIDE_TITLE: str = '🚫Скрыто🚫   '

CONTACT: str = '@Ya_Kobets'

DB_URL: str = os.getenv('MONGO_DB') if os.getenv('MONGO_DB') else 'mongodb://localhost:27017/tg_oso'
