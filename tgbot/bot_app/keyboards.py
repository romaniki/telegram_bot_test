from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData
import emoji
import operator

from aiogram_dialog.widgets.kbd import Multiselect
from aiogram_dialog.widgets.text import Format


#keyboard to greet a user
start_form = InlineKeyboardMarkup()
start_form_btn = InlineKeyboardButton(text="Пройти анкету", callback_data="start_form")
start_form.add(start_form_btn)

#keyboard to choose a choice
choice_keyboard = InlineKeyboardMarkup(row_width=1)

choice_btns = (
        InlineKeyboardButton(
            text="Вариант №1",
            callback_data="choice1"
        ),
        InlineKeyboardButton(
            text="Вариант №2",
            callback_data="choice2",
        ),
        InlineKeyboardButton(
            text="Вариант №3",
            callback_data="choice3"
        ),
        InlineKeyboardButton(text="Отправить анкету", callback_data="submit")
)
choice_keyboard.add(*choice_btns)

submit_kb = ReplyKeyboardMarkup()
submit_btn = InlineKeyboardButton(text="Отправить анкету", callback_data="submit")
submit_kb.add(submit_btn)

