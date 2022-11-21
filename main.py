import telebot
from config import bot_token
from config import yuan
from telebot import types
import requests
from bs4 import BeautifulSoup as bs

bot = telebot.TeleBot(bot_token)

url = yuan
r = requests.get(url)
soup = bs(r.text, 'html.parser')
rate = soup.find_all('div', class_='converter-display__value')
rate0 = [ i.text for i in rate]
rate1 = rate0[1]


@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    cost = types.KeyboardButton('💲 Рассчитать стоимость 💲')
    question = types.KeyboardButton('❓ Задать вопрос ❓')
    start = types.KeyboardButton('⬆ В начало ⬆')
    markup.add(cost, question, start )

    manager = '@miststrix'
    mess = f'Приветствую, <b>{message.from_user.first_name}!</b>'
    disc = f'Здесь вы можете рассчитать общую стоимость товара с учетом доставки ' \
           f'из нашего магазина: https://t.me/poizonpoint 🚚\n' \
           f'' \
           f'Если вы уже определились с товаром и уже готовы сделать заказ, ' \
           f'то напишите нашему <u>менеджеру</u>: {manager} 🤓📒\n' \
           f'Он поможет вам с оформлением 💪'

    bot.send_message(message.chat.id, mess,  parse_mode='html')
    bot.send_message(message.chat.id, disc, parse_mode='html', reply_markup=markup)

@bot.message_handler()
def man(message):
    manager = '@miststrix'

    if message.text.isdigit():
        cost1 = int(message.text) * float(rate1) + 200
        bot.send_message(message.chat.id, f'Итоговая стоимость к оплате: <b>{cost1} (₽)</b>\n'
                                      f'Для заказа писать: {manager}',
                     parse_mode='html')

    elif message.text == '💲 Рассчитать стоимость 💲':
        bot.send_message(message.chat.id, f'Введите стоимость товара в <b>юанях(¥)</b>:',
                         parse_mode='html')

    elif message.text == '❓ Задать вопрос ❓':
        bot.send_message(message.chat.id, f'По вопрсам сотрудничества, а также по вопросам о товарах обращаться к нашему <u>менеджеру</u>: {manager}',
                         parse_mode='html')
    elif message.text == '⬆ В начало ⬆':
        bot.send_message(message.chat.id, f'Нажмите 👉 /start',
                         parse_mode='html')

    else:
        bot.send_message(message.chat.id, f'Не понял Вас, введите корректную команду',
                         parse_mode='html')



bot.polling(none_stop = True)
