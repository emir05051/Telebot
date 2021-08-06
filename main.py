# Телеграм бот
import telebot
from telebot import types

# Фильтры для фото
from PIL import Image, ImageFilter, ImageDraw

# Запросы на телеграм
import requests

# Время
import datetime

# Подключаю бота
TOKEN = '1925264607:AAFPOQu3Qqectl5Mn0Ac0BlQzm9z5215F9I'
bot = telebot.TeleBot(TOKEN)

# Подключаю время
datetime = datetime.datetime

# Массив с данными
choice = ['Изменить картинку', 'Напоминание']


# Функция для загрузки фотографии на компьюетр
def download_image(message):
    image_id = message.photo[-1].file_id
    image_path = bot.get_file(image_id).file_path
    image = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{image_path}')

    with open('image.jpg', 'wb') as f:
        f.write(image.content)


# Получаю картинку image.png
def get_image():
    try:
        image = Image.open("image.jpg")
    except FileNotFoundError:
        print("Файл не найден")

    return image


# Добавляем клавиатуру для image
def add_inline_image_keyboard(message):
    keyboard = types.InlineKeyboardMarkup()

    # первый ряд
    blur = types.InlineKeyboardButton(text='Размыть', callback_data='blur')
    disable_blur = types.InlineKeyboardButton(text='Увеличить резкость', callback_data='disable_blur')
    keyboard.row(blur, disable_blur)

    # Второй ряд
    inversion = types.InlineKeyboardButton(text='Инверсия цветов', callback_data='inversion')
    greyscale = types.InlineKeyboardButton(text='Оттенок серого', callback_data='greyscale')
    keyboard.row(inversion, greyscale)

    question = 'Что сделать с фотографией ?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


# Гауссово размытие
def blur_image():
    image = get_image()

    blurred = image.filter(ImageFilter.GaussianBlur(radius=5))
    blurred.save("changed.png")


# Увеличение резкости
def disable_blur_image():
    image = get_image()

    enhanced = image.filter(ImageFilter.EDGE_ENHANCE)
    enhanced.save("changed.png")


# Инверсия цветов
def inversion_image():
    inversion = get_image()

    draw = ImageDraw.Draw(inversion)
    width = inversion.size[0]
    height = inversion.size[1]
    pix = inversion.load()

    for x in range(width):
        for y in range(height):
            r, g, b = pix[x, y]
            draw.point((x, y), (255 - r, 255 - g, 255 - b))

    inversion.save("changed.png")


# Серый цвет
def grey_image():
    greyscale = get_image()

    draw = ImageDraw.Draw(greyscale)
    width = greyscale.size[0]
    height = greyscale.size[1]
    pix = greyscale.load()

    for x in range(width):
        for y in range(height):
            r, g, b = pix[x, y]
            sr = (r + g + b) // 3  # среднее значение
            draw.point((x, y), (sr, sr, sr))  # рисуем пиксель

    greyscale.save("changed.png")


# Функция для изменения картинки
def change_image(message):
    download_image(message)

    add_inline_image_keyboard(message)

    @bot.callback_query_handler(func=lambda call: True)
    def call_back(call):
        data = call.data

        if data == 'blur':
            blur_image()

        if data == 'disable_blur':
            disable_blur_image()

        if data == 'inversion':
            inversion_image()

        if data == 'greyscale':
            grey_image()

        photo = open("changed.png", 'rb')
        bot.send_photo(call.from_user.id, photo)


# Конвертировать речь в текст
def set_reminder(message):
    options = message.text
    bot.send_message(message.chat.id, 'Напоминание. Выберите дату')


# Добавление 2 кнопок меню
@bot.message_handler(commands=['start'])
def add_keyboard(message):
    markup = types.ReplyKeyboardMarkup()

    markup_button_1 = types.KeyboardButton(choice[0])
    markup_button_2 = types.KeyboardButton(choice[1])

    markup.add(markup_button_1, markup_button_2)

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def main_function(message):
    text = message.text
    print(message.text)
    if text == choice[0]:
        bot.send_message(message.chat.id, 'Загрузите картинку')

        @bot.message_handler(content_types=['photo'])
        def upload_image(call):
            change_image(call)

    if text == choice[1]:
        set_reminder(message)


bot.polling(none_stop=True)
