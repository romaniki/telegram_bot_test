import aiohttp
import asyncio
import emoji

import re

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from .app import dp, bot
from .post import post
from . import keyboards as kb
from . import messages as msg
from google_sheets import add_rows


class Form(StatesGroup):
    name = State() 
    phone_number = State() 
    choice = State()
    chat_id = State() 
    username = State()

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    username = message.from_user.username
    await state.update_data(chat_id=chat_id)
    await state.update_data(tg_login=username)
    await message.reply(msg.GREETING, reply_markup=kb.start_form)

# First question
@dp.callback_query_handler(lambda c: c.data == 'start_form')
async def say_hello(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await bot.send_message(chat_id=chat_id, text=f"Вопрос №1. {msg.NAME_MSG}")
    await Form.name.set()

# Second question 
@dp.message_handler(state=Form.name)
async def answer_q1(message: types.Message, state: FSMContext):
    answer1 = message.text    
    async with state.proxy() as data:
        if len(answer1) < 50:
            data["name"] = answer1.title()
        else:
            return await message.reply(msg.NAME_ERROR_MSG)

    await message.answer("Вопрос №2. " + msg.PHONE_MSG)
    await Form.phone_number.set()
    
#The last question
@dp.message_handler(state=Form.phone_number)
async def answer_q2(message: types.Message, state: FSMContext):
    answer2 = message.text
    async with state.proxy() as data:
        if re.match(r"\+\d{12}", answer2):
            data["phone_number"] = answer2
        else:
            return await message.reply(msg.PHONE_ERROR_MSG)

    await message.answer("Вопрос №3. " + msg.CHOICES_MSG, reply_markup=kb.choice_keyboard)
    await Form.choice.set()

@dp.callback_query_handler(lambda c: c.data.startswith("choice"), state=Form.choice,)
async def answer_q3(callback_query: types.CallbackQuery, state: FSMContext):

    answer3 = callback_query.data.removeprefix('choice')    
    #Get rid of clock
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    
    async with state.proxy() as data:
    
        if not "answer" in data.keys():
            data["answer"] = [int(answer3)]
            
            temp_keyboard = types.InlineKeyboardMarkup()
            btns = callback_query.message.reply_markup["inline_keyboard"]

            for i in btns:
                item = i[0]
                if item["callback_data"] == f"choice{answer3}":
                    btn = types.InlineKeyboardButton(text = emoji.emojize(":check_mark_button:" + item['text']), callback_data=item["callback_data"])
                    temp_keyboard.add(btn)
                else:
                    btn = types.InlineKeyboardButton(text = item['text'], callback_data=item["callback_data"])
                    temp_keyboard.add(btn)
                await callback_query.message.edit_reply_markup(reply_markup=temp_keyboard)

        elif "answer" in data.keys() and int(answer3) in data["answer"]:
            data["answer"].remove(int(answer3)) 
            #Remove emoji here
            temp_keyboard = types.InlineKeyboardMarkup()
            btns = callback_query.message.reply_markup["inline_keyboard"]
            for i in btns:
                item = i[0]
                if item["callback_data"] == f"choice{answer3}" and emoji.demojize(item["text"]).startswith(":check_mark_button:"):
                    btn = types.InlineKeyboardButton(text = emoji.demojize(item['text'])[19:], callback_data=item["callback_data"])
                    temp_keyboard.add(btn)
                else:
                    btn = types.InlineKeyboardButton(text = item['text'], callback_data=item["callback_data"])
                    temp_keyboard.add(btn)
                await callback_query.message.edit_reply_markup(reply_markup=temp_keyboard)
        
        elif "answer" in data.keys() and not int(answer3) in data["answer"]:
            data["answer"].append(int(answer3))
            #Add emoji here
            temp_keyboard = types.InlineKeyboardMarkup()
            btns = callback_query.message.reply_markup["inline_keyboard"]

            for i in btns:
                item = i[0]
                if item["callback_data"] == f"choice{answer3}":
                    btn = types.InlineKeyboardButton(text = emoji.emojize(":check_mark_button:" + item['text']), callback_data=item["callback_data"])
                    temp_keyboard.add(btn)
                else:
                    btn = types.InlineKeyboardButton(text = item['text'], callback_data=item["callback_data"])
                    temp_keyboard.add(btn)
                await callback_query.message.edit_reply_markup(reply_markup=temp_keyboard)

@dp.callback_query_handler(lambda c: c.data == 'submit', state=Form.choice)
async def submit(callback_query: types.CallbackQuery, state: FSMContext):
    
    chat_id = callback_query.message.chat.id
    await bot.answer_callback_query(callback_query_id=callback_query.id)

    user_data = await state.get_data()
    try:
        user_data["answer"]
        #ADD DATA TO DJANGO ADMIN PANEL
        await post(**user_data)
        #ADD DATA TO GOOGLE SHEET
        add_rows(user_data)
    except KeyError:
        user_data["answer"] = []
        #ADD DATA TO DJANGO ADMIN PANEL
        await post(**user_data)
        #ADD DATA TO GOOGLE SHEET
        add_rows(user_data)

    user_data = await state.get_data()

    await bot.send_message(chat_id=chat_id, text=f"Данные успешно сохранены. Прощай!")
    # Finish conversation
    await state.finish() 
