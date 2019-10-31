import logging
import random

import telegram

import secret_setting
import model
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

WELCOME_MSG = f'Welcome. Please enter your free time.'
DB_INSTANCE = model.get_db()


# command /start
def start(update, context):
    context.user_data['get_txt'] = 0
    logger.info(f'start..')
    chat_id = update.effective_chat.id
    logger.info(f'chat_id: {chat_id}')
    DB_INSTANCE.add_user(chat_id)
    free_time_keyboard = model.build_keyboard_free_times(chat_id)
    num_select = len(DB_INSTANCE.get_user(chat_id).selected)
    update.message.reply_text(WELCOME_MSG + f'\nYou have selected <b>{num_select}</b> days.',
                              reply_markup=free_time_keyboard, parse_mode=telegram.ParseMode.HTML)


def help(update, context):
    update.message.reply_text("Use /start to set your free time.")
    update.message.reply_text("Use /create to create event.")
    update.message.reply_text("Use /events to show all events results.")
    update.message.reply_text("Use /participate to show all participates events results.")


def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    try:
        if context.user_data['get_txt'] == 1:
            if 'event name' not in context.user_data:
                context.user_data['event name'] = text
                update.message.reply_text("Write an event description")
                return
            elif 'dis_eve' not in context.user_data:
                dis = update.message.text
                context.user_data['dis_eve'] = dis
                update.message.reply_text("How many participants you need?")
                return
            elif 'part_eve' not in context.user_data:
                par = update.message.text
                context.user_data['part_eve'] = par

            logger.info(f"= Got on chat #{chat_id}: {text!r}")
            response = f'event created successfully,\nPlease wait while people vote for the event..'
            context.bot.send_message(chat_id=update.message.chat_id, text=response)
            model.add_to_eve_DB(model.events, {'uid': model.events.find().count(), 'chat_id': chat_id,
                                               'Name': context.user_data['event name'],
                                               'Time': context.user_data['event time'],
                                               'participants needed': int(context.user_data['part_eve']),
                                               'free members': 0, 'description': context.user_data['dis_eve'],
                                               'participants': [], 'msg_id': [], 'status': "pending"})

            model.set_free_members()
            list_of_free_mem = model.get_free_membrs(context.user_data['event time'])
            model.send_voting_request(list_of_free_mem, context,
                                      f'{context.user_data["event name"]}, {context.user_data["event time"]}.',
                                      model.events.find().count() - 1)
            del context.user_data['event name']
            del context.user_data['dis_eve']
            del context.user_data['part_eve']
            context.user_data['get_txt'] = 0

        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="Invalid Input")
    except:
        context.bot.send_message(chat_id=update.message.chat_id, text="Invalid Input")


# handler callback inline keyboard buttons
def button(update, context):
    query = update.callback_query
    choice = query.data
    print(choice)
    logger.info(f'callback data: {choice}')

    if choice.startswith("accept"):
        print(choice.split(":"))
        on_accept(update, context, int(choice.split(":")[1]))

    elif choice.startswith('reject'):
        on_reject(update, context, int(choice.split(":")[1]))

    elif choice.startswith("pop:"):
        day_time = choice.split('++')[1]
        num_of_free = choice.split('++')[0][4:]
        context.user_data['event time'] = day_time
        query.edit_message_text(
            text=f'<b>{num_of_free} mob participants are available at this time slot.</b>\nPlease select your event name:',
            parse_mode=telegram.ParseMode.HTML)

    elif not model.is_ok_button(choice):
        DB_INSTANCE.update_user_free_time(update.effective_chat.id, choice)
        num_select = len(DB_INSTANCE.get_user(update.effective_chat.id).selected)
        free_time_keyboard = model.build_keyboard_free_times(update.effective_chat.id)
        query.edit_message_text(text=WELCOME_MSG + f'\nYou have selected <b>{num_select}</b> days.',
                                reply_markup=free_time_keyboard, parse_mode=telegram.ParseMode.HTML)
    else:
        # logger.info(DB_INSTANCE.get_user(update.effective_chat.id).selected)
        free_time = '\n'.join(DB_INSTANCE.get_user(update.effective_chat.id).selected)
        model.add_to_DB(model.members, update.effective_chat.id, {'chat_id': update.effective_chat.id,
                                                                  'List of Time': DB_INSTANCE.get_user(
                                                                      update.effective_chat.id).selected})
        # my_mongo.set_free_members()
        query.edit_message_text(text=f'<b>Selected free time:</b>\n{free_time}', parse_mode=telegram.ParseMode.HTML)


# ============================================================
def create_event(update, context):
    free_time_keyboard = model.build_keyboard_event_times(update.effective_chat.id)
    update.message.reply_text("events selected ", reply_markup=free_time_keyboard)
    context.user_data['get_txt'] = 1


# =================================================================
def add_mem_to_event(chat_id, eveid, message_id):
    # for eve in my_mongo.events.find():
    model.events.update_one(
        {'uid': eveid},
        {'$push': {"participants": chat_id}}
    )
    model.events.update_one(
        {'uid': eveid},
        {'$push': {"msg_id": message_id}}
    )


def on_accept(update: Update, context: CallbackContext, eveid):
    chat_id = get_chat_id(update)
    message_id = get_message_id(update)

    event_name, event_time, event_owner = parse_event_from_request(update)

    add_mem_to_event(chat_id, eveid, message_id)
    logger.info(f"Accept #{event_owner}")
    print(eveid)
    voting_no = len(model.events.find_one({'uid': int(eveid)})['participants'])
    response = f'Thant you for join \"{event_name}\".\nThe number of the voting is: {voting_no}'

    context.bot.edit_message_text(text=response, chat_id=chat_id, message_id=message_id)
    notify_all_voting_users(context, update, int(eveid))


def on_reject(update: Update, context: CallbackContext, eveid):
    chat_id = update.effective_chat.id
    mes_id = update.effective_message.message_id
    context.bot.edit_message_text(chat_id=chat_id, message_id=mes_id, text="Tanks for voting .")


def parse_event_from_request(update: Update):
    event = update.effective_message.text.split('\n')[1]
    index = event.find(', ')
    event_name, event_time = event[:index], event[index + 2:-1]
    event_owner = update.effective_message.from_user['id']
    logger.info(f'{event_owner} {event_name} {event_time}')
    return [event_name, event_time, event_owner]


def get_message_id(update: Update):
    return update.effective_message.message_id


def get_chat_id(update: Update):
    return update.effective_chat.id


def notify_all_voting_users(context: CallbackContext, update: Update, eveid):
    db = model.events.find_one({'uid': eveid})
    voting_number = len(db['participants'])
    list_voting = db['participants']
    msg_id = db['msg_id']
    response = f'The number of volunteers in \"{db["Name"]}\" are <b>{voting_number}</b> the event status is <b>{db["status"]}</b>, Thanks.'
    logger.info("Update all voting users")
    for index, value in enumerate(list_voting):
        context.bot.edit_message_text(message_id=msg_id[index], text=response, chat_id=value,
                                      parse_mode=telegram.ParseMode.HTML)
        if voting_number >= int(db['participants needed']):
            model.events.update_one(
                {'uid': eveid},
                {'$set': {"status": "approved"}}
            )


def on_events(update: Update, context: CallbackContext):
    chat_id = get_chat_id(update)
    model.get_events_by_chat_id(chat_id, context)


def my_participates_events(update: Update, context: CallbackContext):
    chat_id = get_chat_id(update)
    model.get_participates_events_by_chat_id(chat_id, context)


# main function
def main():
    updater = Updater(secret_setting.BOT_TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('create', create_event))
    updater.dispatcher.add_handler(CommandHandler('events', on_events))
    updater.dispatcher.add_handler(CommandHandler('participate', my_participates_events))
    echo_handler = MessageHandler(Filters.text, respond)
    updater.dispatcher.add_handler(echo_handler)
    updater.dispatcher.add_handler(CommandHandler('help', help))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
