import calendar
from datetime import datetime, timedelta

from pymongo import MongoClient
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

from telegram.ext import CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# User class
class User:
    """docstring for User"""

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.ls = members.find_one({'chat_id': chat_id})
        if self.ls:
            self.selected = self.ls['List of Time']
        else:
            self.selected = list()

    def update_list(self, day_time):
        if day_time in self.selected:
            self.selected.remove(day_time)
        else:
            self.selected.append(day_time)

    def is_day_time_exist(self, day_time):
        return True if day_time in self.selected else False


# ===================================== DB class

# DB class
class DB:
    def __init__(self):
        self.db_users_free_time = dict()

    # add new user with empty free time list.
    def add_user(self, chat_id):
        if chat_id not in self.db_users_free_time:
            self.db_users_free_time[chat_id] = User(chat_id)

    # return list if chat_id exist, None otherwise.
    def get_user(self, chat_id):
        return self.db_users_free_time.get(chat_id, None)

    def update_user_free_time(self, chat_id, day_time):
        self.get_user(chat_id).update_list(day_time)

    def is_day_time_exist(self, chat_id, day_time):
        return True if self.get_user(chat_id).is_day_time_exist(day_time) else False


DB_INSTANCE = DB()


def get_db():
    return DB_INSTANCE


# ==================mohamed =============================


def generate_buttons(event_id):
    def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, [header_buttons])
        if footer_buttons:
            menu.append([footer_buttons])
        return menu

    button_list = [InlineKeyboardButton("Accept", callback_data=f"accept:{event_id}"),
                   InlineKeyboardButton("Reject", callback_data=f"reject:{event_id}")]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


def send_voting_request(free_time_list, context: CallbackContext, event, eveid):
    accept_reject_btn = generate_buttons(eveid)
    voting_text = f'A new event was created:\n{event}\nWould you like to join?'
    for chat_id in free_time_list:
        context.bot.send_message(chat_id=chat_id, text=voting_text, reply_markup=accept_reject_btn)


# ==================================================

DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
TIMES = ['08:00-13:00', '13:00-20:00']
ALL_TIMES = [f'{_day} {_time}' for _day in DAYS for _time in TIMES]

OK_BUTTON = 'Ok'

EMOJIES = ['🔘', '✔']


def get_dates():
    dates = [(datetime.today() - timedelta(days=-i)).strftime('%d/%m') for i in range(1, 8)]
    for date in dates:
        yield date
        yield date


def rotate_list(count, lst):
    for _ in range(count * 2):
        lst = lst[1:] + [lst[0]]
    return lst


def find_day(date):
    born = datetime.strptime(date, '%d %m %Y').weekday()
    return calendar.day_name[born]


def build_keyboard_free_times(chat_id):
    keyboard = [InlineKeyboardButton(f"{EMOJIES[DB_INSTANCE.is_day_time_exist(chat_id, day_time)]} {day_time}",
                                     callback_data=day_time) for day_time in ALL_TIMES]
    keyboard = [keyboard[index: index + 2] for index in range(0, len(keyboard), 2)]
    keyboard.append([InlineKeyboardButton(OK_BUTTON, callback_data=OK_BUTTON)])
    return InlineKeyboardMarkup(keyboard)


def build_keyboard_event_times(chat_id):
    today = find_day(datetime.today().strftime('%d %m %Y'))
    new_times = rotate_list((DAYS.index(today[:3]) + 1) % 7, ALL_TIMES[:])
    gen_dates = get_dates()
    keyboard = [InlineKeyboardButton(f"{len(get_free_membrs(day_time))} {next(gen_dates)} {day_time}",
                                     callback_data=f'pop:{len(get_free_membrs(day_time))}++{day_time}') for day_time in
                new_times]

    keyboard = [keyboard[index: index + 2] for index in range(0, len(keyboard), 2)]
    # keyboard.append([InlineKeyboardButton(OK_BUTTON, callback_data=OK_BUTTON)])
    return InlineKeyboardMarkup(keyboard)


def is_ok_button(data):
    logger.info(f'data: {data}')
    return True if data == OK_BUTTON else False


days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


def add_to_DB(my_db, chat_id, doc):
    time_list = my_db.find_one({'chat_id': chat_id})
    if not time_list:
        my_db.insert_one(doc)
    else:
        my_db.replace_one(my_db.find_one({"chat_id": chat_id}), doc, upsert=True)


def add_to_eve_DB(my_db, doc):
    my_db.insert_one(doc)


def time_include(time1: str, time2: str):
    day_event, time_event = time1.split(" ")[0], time1.split(" ")[1]
    day_mem, time_mem = time2.split(" ")[0], time2.split(" ")[1]
    time_event_set = time_event.split("-")
    time_mem_set = time_mem.split("-")
    if days.index(day_event) == days.index(day_mem) and time_event_set[0] >= time_mem_set[0] \
            and time_event_set[1] <= time_mem_set[1]:
        return True
    else:
        return False


def get_free_membrs(time: str):
    free_mem = set()
    for mem in members.find():
        for mem_time in mem['List of Time']:
            if time_include(time, mem_time):
                free_mem.add(mem['chat_id'])
    return free_mem


def set_free_members():
    for eve in events.find():
        events.update(
            {'chat_id': eve['chat_id']},
            {'$set': {"free members": len(get_free_membrs(eve['Time']))}}
        )


def get_participants(chat_id, name):
    for x in events.find({}, {'chat_id': chat_id, 'Event Name': name}):
        return x['chat_id']


def get_events_by_chat_id(chat_id, context: CallbackContext):
    ev_list = events.find({'chat_id': chat_id})
    for ev in ev_list:
        response = f'Event name: {ev["Name"]}\n Date/Time {ev["Time"]}\n'
        response += f'event description: {ev["description"]}\n'
        response += f'Required Volunteer Number: {ev["participants needed"]}\n'
        response += f'All free members in this time: {ev["free members"]}\n'
        response += f'The voting percent: {(len(ev["participants"]) / ev["free members"])*100}%\n'
        response += f'Event Status: {ev["status"]}\n'
        context.bot.send_message(chat_id=chat_id, text=response)
    if ev_list.count() == 0:
        context.bot.send_message(chat_id=chat_id, text="no events yet")


def get_participates_events_by_chat_id(chat_id, context: CallbackContext):
    event_list = events.find()
    for ev in event_list:
        if chat_id in ev['participants']:
            response = f'Event name: {ev["Name"]}\n Date/Time {ev["Time"]}\n'
            response += f'event description: {ev["description"]}\n'
            response += f'Required Volunteer Number: {ev["participants needed"]}\n'
            response += f'All free members in this time: {ev["free members"]}\n'
            response += f'The voting percent: {(len(ev["participants"]) / ev["free members"])*100}%\n'
            response += f'Event Status: {ev["status"]}\n'
            context.bot.send_message(chat_id=chat_id, text=response)
    if event_list.count() == 0:
        context.bot.send_message(chat_id=chat_id, text="not participated in any event yet")


client = MongoClient()
db = client.get_database("MobSourcing_DB")
members = db.get_collection("membrs_DB")
events = db.get_collection("events_DB")
