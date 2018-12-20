import telebot
from telebot import types

token = ''
saved_users_massege = {} # сюда сохраняем сообщения пользователя в формате id:[mes1, mes2, mes3]

bot = telebot.TeleBot(token)

def save_message(message):
    """ функция сохраняет сообщения пользователя
    для идентефикации используется message.chat.id
    при количестве сообщений больше 3 удаляет самое старое """
    id_user = message.chat.id
    text = message.text
    try:
        saved_users_massege[id_user].append(text)
    except KeyError:
        saved_users_massege[id_user] = [text]
    if len(saved_users_massege[id_user])>3:
        saved_users_massege[id_user].remove(saved_users_massege[id_user][0])


def send_battom(message):
    """функция отправляет клавиатуру с 3 последними сообщениями
    при отсутствие сообщений отсылает одну кнопку"""
    try:
        data = saved_users_massege[message.chat.id]
    except KeyError:
        data = ['you do not have message']
    for i in range(len(data)):
        data[i] = types.KeyboardButton(data[i])
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key.add(*data)
    bot.send_message(message.chat.id, 'last 3 message', reply_markup=key)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, 'send message for me :)')

@bot.message_handler(content_types = ['text'])
def communication(message):
    if message.text.lower() == 'старт':
        send_battom(message)
    else:
        bot.send_message(message.chat.id, message.text)
        save_message(message)

if __name__ == '__main__':
    bot.polling()