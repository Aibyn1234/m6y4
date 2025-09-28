import telebot
from telebot import types
from questions import * 
from config import *

bot = telebot.TeleBot(TOKEN)

user_scores = {}
user_progress = {}

@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    user_scores[chat_id] = 0
    user_progress[chat_id] = 0
    bot.send_message(chat_id, "Привет! Давай начнём викторину!")
    ask_question(chat_id)

def ask_question(chat_id):
    q_index = user_progress[chat_id]
    if q_index < len(questions):
        q = questions[q_index]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for option in q["options"]:
            markup.add(option)
        bot.send_message(chat_id, q["q"], reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(chat_id, check_answer)
    else:
        score = user_scores[chat_id]
        bot.send_message(chat_id, f"Викторина окончена!  Твои баллы: {score}/{len(questions)}")
        del user_scores[chat_id]
        del user_progress[chat_id]

def check_answer(message):
    chat_id = message.chat.id
    q_index = user_progress[chat_id]
    q = questions[q_index]

    if message.text == q["answer"]:
        user_scores[chat_id] += 1
        bot.send_message(chat_id, "Верно!")
    else:
        bot.send_message(chat_id, f"Неправильно.")

    user_progress[chat_id] += 1
    ask_question(chat_id)

bot.polling()
