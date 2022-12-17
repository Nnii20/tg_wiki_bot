import os
import re

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import wikipedia


# Создаем экземпляр бота
bot = Bot(token=os.environ.get('BOT_TOKEN'))
dp = Dispatcher(bot)
wikipedia.set_lang("ru")


def getwiki(s):
    """Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов"""
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext = ny.content[:1000]
        # Разделяем по точкам. Отбрасываем все после последней точки
        wikimas = wikitext.split('.')[:-1]
        # Создаем пустую переменную для текста
        wikitext_res = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if '==' not in x:
                # Если в строке осталось больше трех символов, добавляем ее к нашей переменной
                # и возвращаем утерянные при разделении строк точки на место
                if len(x.strip()) > 3:
                    wikitext_res += x + '.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext_res = re.sub(r'(\([^()]*\))|(\{[^\{\}]*\})', '', wikitext_res)
        return wikitext_res
    except Exception:
        return "Не удалось получить информацию по запросу."


@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    """handler команды /start"""
    await msg.reply("Отправьте мне любое слово, и я найду его значение на Wikipedia.")


@dp.message_handler(commands=['set_lang', 'change_lang'])
async def change_language(msg: types.Message):
    """handler команд /set_lang и /change_lang"""
    lang = msg.text.split()[-1]
    wikipedia.set_lang(lang)
    await msg.answer(f"Язык поиска изменен на {lang}")


@dp.message_handler(content_types=['text'])
async def handle_text(msg: types.Message):
    """handler получения любых сообщений от пользователя"""
    await msg.answer(getwiki(msg.text))
