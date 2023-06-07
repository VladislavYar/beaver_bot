import os
import logging
import json
from random import randint

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler,
    MessageHandler, ContextTypes, filters
    )

from dotenv import load_dotenv


load_dotenv()


TOKEN_BOT = os.getenv('TOKEN')

BEAVER = 'Бобёр🦫'
BEAVER_SMILES_TEXT = 'Улыбается😊'
BEAVER_SAD_TEXT = 'Грустит😥'
BACK = 'Назад'
WIKI_TEXT = 'Wiki📕'
AUDIO_BEAVER_TEXT = 'Звуки бобров🔊'
INFO_BEAVER_TEXT = 'Всё о бобрах. Почти всё👉👈'

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def load_json() -> dict[str, str]:
    """Загрузка файлов JSON."""

    with open("beaver/emotions/sad/text.json",
         "r", encoding='utf-8') as sad_text:
        sad_text = json.load(sad_text)
    with open("beaver/emotions/smile/text.json",
         "r", encoding='utf-8') as smile_text:
        smile_text = json.load(smile_text)
    with open("beaver/audio_beaver/text.json",
         "r", encoding='utf-8') as audio_beaver:
        audio_beaver = json.load(audio_beaver)
    with open("beaver/info_beaver.json", "r", encoding='utf-8') as info_beaver:
        info_beaver = json.load(info_beaver)
    return sad_text, smile_text, info_beaver, audio_beaver


sad_text, smile_text, info_beaver, audio_beaver = load_json()
sad_len = len(sad_text)
smile_len = len(smile_text)


async def info_button_beaver(update, context) -> None:
    """Выводит кнопки по выбору информации о бобре."""

    name_buttons_1 = []
    name_buttons_2 = []
    name_buttons_3 = []
    i = 0
    text = 'Что ты хочешь узнать о бобрах?🦫'
    for name_button in info_beaver:
        if i % 2 == 0 and i != 0:
            name_buttons_1.append(name_button)
        elif i % 3 == 0:
            name_buttons_2.append(name_button)
        else:
            name_buttons_3.append(name_button)
        i += 1

    button = ReplyKeyboardMarkup(
        [name_buttons_1, name_buttons_2, name_buttons_3, [BACK]],
        resize_keyboard=True)
    await update.effective_message.reply_text(text, reply_markup=button)


async def get_info_beaver(update, context) -> None:
    """Получает информацию о бобре и отправляет сообщением."""

    text = info_beaver[update.message.text]
    await update.effective_message.reply_text(text)


async def audio_button_beaver(update: Update,
                              context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выводит кнопки по выбору аудио бобра."""

    name_buttons_1 = []
    name_buttons_2 = []
    name_buttons_3 = []
    i = 0
    text = 'Какой звук бобра ты хочешь услышать?🦫'
    for name_button in audio_beaver:
        if i % 2 == 0 and i != 0:
            name_buttons_1.append(name_button)
        elif i % 3 == 0:
            name_buttons_2.append(name_button)
        else:
            name_buttons_3.append(name_button)
        i += 1

    button = ReplyKeyboardMarkup(
        [name_buttons_1, name_buttons_2, name_buttons_3, [BACK]],
        resize_keyboard=True)
    await update.effective_message.reply_text(text, reply_markup=button)


async def get_audio_beaver(update: Update,
                           context: ContextTypes.DEFAULT_TYPE) -> None:
    """Получает аудио бобра и отправляет сообщением."""
    path = f'beaver/audio_beaver/{audio_beaver[update.message.text]}.mp3'
    await update.effective_message.reply_audio(path)


async def emotion_beaver(update: Update,
                         context: ContextTypes.DEFAULT_TYPE) -> None:
    """Анализирует нажатие кнопки пользователем и отправляет фото с текстом."""

    if update.message.text == BEAVER_SMILES_TEXT:
        i = randint(1, smile_len)
        path = f'beaver/emotions/smile/{i}.jpg'
        text = smile_text[str(i)]
        photo = open(path, 'rb')
        await update.effective_message.reply_photo(photo,
                                                   caption=text)
    else:
        i = randint(1, sad_len)
        path = f'beaver/emotions/sad/{i}.jpg'
        text = sad_text[str(i)]
        photo = open(path, 'rb')
        await update.effective_message.reply_photo(photo,
                                                   caption=text)


async def wiki_beaver(update: Update,
                      context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет текст и даёт выбор из xx кнопок информации о бобрах."""

    text = 'Какую категорию о бобрах выберешь?'
    button = ReplyKeyboardMarkup([[INFO_BEAVER_TEXT,
                                   AUDIO_BEAVER_TEXT], [BACK]],
                                 resize_keyboard=True)
    await update.effective_message.reply_text(text, reply_markup=button)


async def choosing_beaver(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет текст и даёт выбор из xx кнопок эмоций бобра."""

    text = 'Какой же ты бобёр сегодня?'
    button = ReplyKeyboardMarkup([[BEAVER_SMILES_TEXT,
                                   BEAVER_SAD_TEXT], [BACK]],
                                 resize_keyboard=True)
    await update.effective_message.reply_text(text, reply_markup=button)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """При старте приветсвует и выводит кнопку."""

    button = ReplyKeyboardMarkup(
        [[BEAVER, WIKI_TEXT]], resize_keyboard=True)
    name = update.message.chat.first_name
    message = update.message.text
    if message == '/start':
        text = (
            f'Приветствую тебя, {name}! Я ботограмм-бобёр v1.0\n'
            'Пока что я мало что умею, но с преданным '
            'желанием разделю все твои эмоции(заложенные в этой версии) '
            'и немного поделюсь о себе!\n'
            'Ткни в бобра, не бойся;)'
                )
    else:
        text = 'Что теперь выберем?🦫'

    await update.effective_message.reply_text(text, reply_markup=button)


def main() -> None:
    """Старт бота."""

    application = Application.builder().token(TOKEN_BOT).build()
    back_filter = filters.Regex(BACK)
    beaver_filter = filters.Regex(BEAVER)
    wiki_button_filter = filters.Regex(WIKI_TEXT)
    info_button_filter = filters.Regex(INFO_BEAVER_TEXT)
    info_beaver_filter = (
        filters.Regex('Что едят бобры🌳?') |
        filters.Regex('Где живут бобры🏞?') |
        filters.Regex('Можно ли приручить бобра🐶?') |
        filters.Regex('Агрессивные ли бобры😡?')
        )
    audio_button_filter = filters.Regex(AUDIO_BEAVER_TEXT)
    audio_beaver_filter = (
        filters.Regex('Звук бобра в воде💦') |
        filters.Regex('Звук бобра в дикой природе🏞') |
        filters.Regex('Стоны бобра😋') |
        filters.Regex('Звук приёма пищи бобром🌿') |
        filters.Regex('Звук разгрызания дерева бобром🌳')
        )
    beaver_emotion_filter = (
        filters.Regex(BEAVER_SMILES_TEXT) | filters.Regex(BEAVER_SAD_TEXT)
        )
    application.add_handlers(
        handlers={-1: [CommandHandler('start', start),
                       MessageHandler(back_filter, start)],
                  1: [MessageHandler(beaver_filter, choosing_beaver),
                      MessageHandler(wiki_button_filter, wiki_beaver)],
                  2: [MessageHandler(beaver_emotion_filter, emotion_beaver),
                      MessageHandler(info_button_filter, info_button_beaver),
                      MessageHandler(audio_button_filter,
                                     audio_button_beaver)],
                  3: [MessageHandler(info_beaver_filter, get_info_beaver),
                      MessageHandler(audio_beaver_filter, get_audio_beaver)]}
        )

    application.run_polling()


if __name__ == "__main__":
    main()
