# Обработка голоса и перевод его в wav
# voice_message = bot.get_file(message.voice.file_id)
# voice_message_path = voice_message.file_path
# file = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{voice_message_path}')
#
# with open('voice.wav', 'wb') as f:
#     f.write(file.content)

# Распознавание
# filename = '16-122828-0002.wav'
#
# with sr.AudioFile(filename) as source:
#     audio_data = r.record(source)
#     # Распознавание из аудио
#     try:
#         text = r.recognize_google(audio_data, language='en')
#         print(text)
#     except:
#         print('Err')
# from PIL import Image, ImageFilter
#
# try:
#     original = Image.open("image.jpg")
# except FileNotFoundError:
#     print("Файл не найден")
#
#
# blurred = original.filter(ImageFilter.GaussianBlur(radius=3))
#
# original.show()
# blurred.show()
# # сохраняем изображение
# blurred.save("blurred.png")

from fuzzywuzzy import fuzz

fuzz.token_sort_ratio("я люблю спать", "но надо работать")