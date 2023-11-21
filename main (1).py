
import asyncio

## Импорт библиотек
from googletrans import Translator
from telebot import types
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot("6304902320:AAFDf02aBha5Ka3UTlQSpsgKYZrouTJiD0Q", parse_mode=None)

# Обработка команды /start приветствие.
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message,'------\n'
                 + 'Здравствуй, '
                 + message.from_user.first_name
                 + ' \nПереведу с русского на английский \nИ с других языков на русский '
                 +'\n------')

# Обработка команды /help.
@bot.message_handler(commands=['help'])
async def send_welcome(message):
    await bot.reply_to(message,'------\n'
                       + 'Просто вводи текст и нажимай отправить\n'
                       + 'Я сам определю какой это язык\n'
                       + 'Если не перевел, попробуй еще раз\n'
                       + 'для выбора языка напиши мне “/ setlang + язык”\n'
                       + 'Перевод гугл'
                       + '\n------')

# Обработка команды /setlang, устанавливает язык перевода.
@bot.message_handler(commands=['setlang'])
async def set_lang(message):
    # Получаем язык перевода из сообщения.
    lang = message.text.split()[1]

    # Сохраняем язык перевода в глобальной переменной.
    global lang_to
    lang_to = lang

    # Отправляем сообщение пользователю с подтверждением.
    await bot.reply_to(message, 'Язык перевода установлен на ' + lang)

# Обработка текста сообщения, если ввод на русском, то перевод на английский,
# если другой язык, то перевод на русский.
@bot.message_handler()
async def user_text(message):
    translator = Translator()

    # Определение языка ввода.
    lang = translator.detect(message.text)
    lang = lang.lang

    # Если ввод по русски, то перевести на английский по умолчанию.
    if lang == 'ru':
        send = translator.translate(message.text, dest='en')
        await bot.reply_to(message, '------\n'+ send.text +'\n------')
    else:
        if lang == 'en':
            if lang_to != 'en':
                send = translator.translate(message.text, dest=lang_to)
                await bot.reply_to(message, '------\n'+ send.text +'\n------')
            else:
                # Если язык перевода английский, то оставить как есть.
                send = message.text
                await bot.reply_to(message, '------\n'+ send +'\n------')
        else:
            # Если язык ввода не английский, то перевести на русский.
            send = translator.translate(message.text, dest='ru')
            await bot.reply_to(message, '------\n'+ send.text +'\n------')


# Обработка инлайн запросов. Инлайн режим необходимо включить в настройках бота у @BotFather.
@bot.inline_handler(lambda query: True)
async def inline_query(query):
    results = []
    translator = Translator()
    text = query.query.strip()

    # Если запрос пустой, не делаем перевод
    if not text:
        return

    # Определение языка ввода.
    lang = translator.detect(text)
    lang = lang.lang

    # Если ввод по русски, то перевести на английский по умолчанию.
    if lang == 'ru':
        send = translator.translate(text)
        results.append(types.InlineQueryResultArticle(
            id='1', title=send.text, input_message_content=types.InputTextMessageContent(
                message_text=send.text)))

    # Иначе другой язык перевести на русский {dest='ru'}.
    else:
        send = translator.translate(text, dest='ru')
        results.append(types.InlineQueryResultArticle(
            id='1', title=send.text, input_message_content=types.InputTextMessageContent(
                message_text=send.text)))

    await bot.answer_inline_query(query.id, results)

# Запуск и повторение запуска при сбое.
asyncio.run(bot.infinity_polling())