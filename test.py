from datetime import datetime
import json
import time

import telebot
from telebot import types
import pytz  # Для работы с часовыми поясами

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot = telebot.TeleBot('ВАШ ТОКЕН')

# Список поддерживаемых часовых поясов России
with open('timezones.json', 'br') as f:
    timezones = json.load(f)

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я крутой бот, который умеет показывать текущее время. Введите /time, чтобы узнать текущее время!")

# Команда /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Я могу выполнить следующие команды:\n"
        "/time - показать текущее время\n"
        "/timezone - выбрать часовой пояс\n"
        "/countdown - начать обратный отсчёт\n"
        "/help - показать это сообщение"
    )
    bot.send_message(message.chat.id, help_text)

# Команда /time с выбором часового пояса
@bot.message_handler(commands=['time'])
def send_time(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    buttons = [types.KeyboardButton(tz) for tz in timezones.keys()]
    markup.add(*buttons)
    msg = bot.send_message(message.chat.id, "Выберите часовой пояс:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_timezone_selection)

def process_timezone_selection(message):
    timezone = timezones.get(message.text)
    if timezone:
        now = datetime.now(pytz.timezone(timezone))
        bot.send_message(message.chat.id, f"Текущее время в {message.text}: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        bot.send_message(message.chat.id, "Неизвестный часовой пояс. Попробуйте снова.")

# Команда /countdown для создания таймера
@bot.message_handler(commands=['countdown'])
def start_countdown(message):
    msg = bot.send_message(message.chat.id, "Введите время отсчёта в секундах:")
    bot.register_next_step_handler(msg, process_countdown)

def process_countdown(message):
    try:
        countdown_time = int(message.text)
        bot.send_message(message.chat.id, f"Обратный отсчёт начался на {countdown_time} секунд!")
        bot.send_chat_action(message.chat.id, 'typing')  # Показать "печатает..." для эффекта
        bot.send_message(message.chat.id, "Время пошло! 🕒")
        for i in range(countdown_time, 0, -1):
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 2, text=f"Осталось: {i} секунд")
            time.sleep(1)
        bot.send_message(message.chat.id, "⏰ Время вышло!")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")

# Запуск бота
bot.polling(none_stop=True)
