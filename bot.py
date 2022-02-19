# -*- coding: utf-8 -*-

import telebot
from telebot import TeleBot
import module
from telebot import types
import os
import config

token = config.token

bot = TeleBot(token)


@bot.message_handler(commands = ["start"])
def start(message):
    bot.send_message(message.from_user.id,
"Привіт👋 \n\
Я  надзвичайно зручний бот який допоможе тобі у повсякденному житті 😎\n\
Що я вмію? 🤔🤔 Ну дивись:\n\
1️⃣ Шукаю інформацію про твоє текстове повідомлення 💬 ➡️ ℹ️.\n\
2️⃣ Вибираю текст із присланної фотографії та відсилаю його тобі повідомленням 🖼️ ➡️ 💬.\n\
3️⃣ Перетворюю надіслане голосове повідомлення у текст та відсилаю його тобі 🔊 ➡️ ℹ️.\n\
4️⃣ Надіслане тобою відео перетворюю в голосове повідомлення та надсилаю тобі 📹 ➡️ 🔊.\n\
5️⃣ Скачую відео із ютуба. Просто надішли мені ссилку відео і я пришлю тобі його 🔗 ➡️ 📹.\n\
Щось не зрозуміло? Просто пропиши в чаті:\n\
👉/help👈\n\
і дізнайся більше інформації про мене 😉\n\
Є якісь пропозиції як покращити мою роботу?\n\
напиши моєму власнику: \n\
👉@skiffiks👈")
    os.system("CLS")


@bot.message_handler(commands = ["help"])
def help(message):
    bot.send_message(message.from_user.id,
"не розумію, що було не зрозуміло у стартовому повідомленні🤡🤡 \n\
Ладно, якщо ти вже нажав на допомогу то розкажу тобі пару лайфхаків😅: \
Ти можеш пересилати чужі голосові мені і я буду їх переводити у текст, (думаю це буде найчастіше використовуватись 😁). \n\
Також ніхто тобі не забороняє пересилати мої повідомлення мені ж 😂😂, для отримання якогось результату \
Допустим можеш надіслати мені силку🔗 на відео із ютуба, я надішлю тобі відео📹, \
ти можеш переслати мені це відео📹 і отримаєш голосове🔊 повідомлення із нього, \
можеш навіть переслати мені це голосове🔊 і ти отримаєш текст💬 із нього, \
таким чином ти отримаєш текст💬 із силки🔗 на ютуб відео. \n\
Також ти можеш дізнатись свій 'телеграм ID', просто пропиши у чат 👉/id👈 \n\
Круто правда ж? 😂😂")
    os.system("CLS")


@bot.message_handler(content_types = ["text"])
def get_text_messages(message):

    text = message.text
    # print(text)

    if text[:23] == "https://www.youtube.com" or text[:13] == "https://youtu":

        try:

            video_src = module.download_youtube(text)
            video = open(video_src, "rb")
            bot.send_video(message.chat.id, video)

            # os.remove(video_src) # видалення файлу, не працюэ так як процесс надсилання довго не завершуэться

        except:

            bot.send_message(message.from_user.id, "Щось не так із силкою :(, не можу знайти цього відео 😢")

    elif text == "/id":

        bot.send_message(message.from_user.id, f"твоє ID: '{message.from_user.id}'")

    else:

        try:

            if len(text) < 3:

                bot.send_message(message.from_user.id, "на повідомлення коротші 3 символів не відповідаю 😡😡")

            else:

                next_massage = module.zapros(text)

                bot.send_message(message.from_user.id, next_massage)

        except:

            bot.send_message(message.from_user.id, "не можу знайти нічого по вашому запиту 😢😢")

    os.system("CLS")


@bot.message_handler(content_types = ["photo"])
def photo(message):

    try:

        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(r"images/image.jpg", "wb") as new_file:
            new_file.write(downloaded_file)

        a = module.photo_to_text(r"images/image.jpg")
        bot.send_message(message.from_user.id, a)

    except TypeError:

        a = "🚬🗿 Не бачу тексту на цьому фото 👀"
        bot.send_message(message.from_user.id, a)

    os.system("CLS")


@bot.message_handler(content_types = ["voice"])
def voice_processing(message):

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(r"audio/audio.ogg", "wb") as new_file:
        new_file.write(downloaded_file)

    try:

        a = module.output(r"audio/audio.ogg")

        bot.send_message(message.from_user.id, a)

    except:

        bot.send_message(message.from_user.id, "Не можу розпізнати текст у цьому голосовому 😢")

    os.system("CLS")


@bot.message_handler(content_types = ["video"])
def send_text(message):

    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(r"videos/user_video.mp4", "wb") as new_file:
        new_file.write(downloaded_file)

    markup_inline = types.InlineKeyboardMarkup()

    item_1 = types.InlineKeyboardButton(text="файл .mp3", callback_data="mp3")
    item_2 = types.InlineKeyboardButton(text="Голосове", callback_data="gol")

    markup_inline.add(item_1, item_2)
    bot.send_message(message.from_user.id, "Яким способом вам надіслати аудіофайл🔊 ?",
                    reply_markup=markup_inline
                    )

    #bot.send_voice(message.from_user.id, a)
    os.system("CLS")


@bot.message_handler(content_types = ["document"])
def hz(message):

    sti = open(r"images/blet.webp", "rb")
    bot.send_sticker(message.from_user.id, sti)

    bot.reply_to(message, "🚬🗿 \nЯ незнаю що робити із цими файлами 😢 ... \nЄ якісь пропозиції?? напиши власнику 👉@skiffiks👈")

    os.system("CLS")


@bot.callback_query_handler(func = lambda call: True)
def answer(call):

    a = open(module.video_to_mp(r"videos/user_video.mp4"), "rb")

    if call.data == "mp3":

        bot.send_audio(call.from_user.id, a)

    elif call.data == "gol":

        bot.send_voice(call.from_user.id, a)

    os.system("CLS")


bot.polling(none_stop = True, interval = 0)