import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CriptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(massage: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты> \
<в какую вылюту перевести> \
 <количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(massage, text)


@bot.message_handler(commands=['values'])
def values(massage: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(massage, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неправильно введены параметры.')

        quote, base, amout = values
        total_base = CriptoConverter.convert(quote, base, amout)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:

        text = f'Цена {amout} {quote} в {base} = {total_base}'
        bot.reply_to(message, text)


bot.polling()
