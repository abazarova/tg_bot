import random

from aiogram import types
from aiogram.dispatcher import FSMContext

from .app import bot, dp
from .keyboards import make_keyboard
from .messages import GAME_OVER_LOSE, GAME_OVER_WIN, WELCOME, ENTER_THE_CHARACTER_TO_ADD, WORD_ADDED, \
    ENTER_THE_CHARACTER_TO_TRANSLATE, ENTER_THE_CHARACTER_TO_PINYIN
from .send_signals import add_word_to_db, get_all, get_random
from .states import States


@dp.message_handler(commands=['start', 'help'], state="*")
async def send_welcome(message: types.Message):
    await message.answer(WELCOME, parse_mode='Markdown')


@dp.message_handler(commands=['random_character'], state="*")
async def add_character(message: types.Message, state: FSMContext):
    await States.random_word.set()
    res = await get_random()
    await message.answer("Word: " + res['word'] + "\n" + "Pinyin: " + res['pinyin'] + "\n" \
                         + "Translation: " + res['translation'])
    

@dp.message_handler(commands=['add_character'], state="*")
async def add_character(message: types.Message, state: FSMContext):
    await States.add_character.set()
    await message.answer(ENTER_THE_CHARACTER_TO_ADD, parse_mode='Markdown')


@dp.message_handler(state=States.add_character)
async def add_word(message: types.Message, state: FSMContext):
    data = message.text
    word, _, _ = str.split(data, sep=" ")
    await add_word_to_db(data)
    await message.answer(WORD_ADDED.format(word))
    await States.start.set()


@dp.message_handler(commands=['train_pinyin_mul'], state="*")
async def train_pinyin(message: types.Message, state: FSMContext):
    await States.train_pinyin.set()
    res = await get_random()
    async with state.proxy() as data:
        data['step'] = 1
        data['answer'] = res['pinyin']
        data['word'] = res['word']
    
    all_words = await get_all()
    all_answers = [w['pinyin'] for w in all_words]
    all_answers.remove(res['pinyin'])

    random.shuffle(all_answers)
    answers = [data['answer']] + all_answers[:2]
    random.shuffle(answers)

    kbrd = make_keyboard(answers)

    await message.answer("Word: " + data['word'], reply_markup=kbrd)


@dp.callback_query_handler(state=States.train_pinyin)
async def button_callback_train_pinyin(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data
    async with state.proxy() as data:
        if answer == data['answer']:
            res = await get_random()
            data['step'] += 1
            data['answer'] = res['pinyin']
            data['word'] = res['word']
            if data['step'] > 5:
                await bot.send_message(callback_query.from_user.id, GAME_OVER_WIN, parse_mode='Markdown')
                await States.start.set()
            else:
                all_words = await get_all()
                all_answers = [w['pinyin'] for w in all_words]
                all_answers.remove(res['pinyin'])

                random.shuffle(all_answers)
                answers = [data['answer']] + all_answers[:2]
                random.shuffle(answers)


                kbrd = make_keyboard(answers)

                await bot.send_message(callback_query.from_user.id, "Correct! \n" +  "Word: " + data['word'],
                                       reply_markup=kbrd)
        else:
            await States.start.set()
            await bot.send_message(callback_query.from_user.id, GAME_OVER_LOSE, parse_mode='Markdown')
            

@dp.message_handler(commands=['train_pinyin_write'], state="*")
async def train_pinyin_write(message: types.Message, state: FSMContext):
    await States.train_pinyin_write.set()
    res = await get_random()
    async with state.proxy() as data:
        data['step'] = 1
        data['answer'] = res['pinyin']
        data['word'] = res['word']

    await message.answer(ENTER_THE_CHARACTER_TO_PINYIN.format(data['word']))


@dp.message_handler(state=States.train_pinyin_write)
async def check_pinyin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        answer = message.text
        if answer == data['answer']:
            if data['step'] > 5: 
                await message.answer(GAME_OVER_WIN, parse_mode='Markdown')
                await States.start.set()
            else:
                res = await get_random()
                data['step'] += 1
                data['answer'] = res['pinyin']
                data['word'] = res['word']

                await message.reply('Correct!')
                await message.answer(ENTER_THE_CHARACTER_TO_PINYIN.format(data['word']))
        else:
            await message.reply(GAME_OVER_LOSE, parse_mode='Markdown')
            await States.start.set()


@dp.message_handler(commands=['train_transl_write'], state="*")
async def train_translation_write(message: types.Message, state: FSMContext):
    await States.train_translation_write.set()
    res = await get_random()
    async with state.proxy() as data:
        data['step'] = 1
        data['answer'] = res['translation']
        data['word'] = res['word']

    await message.answer(ENTER_THE_CHARACTER_TO_TRANSLATE.format(data['word']))


@dp.message_handler(state=States.train_translation_write)
async def check_translation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        answer = message.text
        if answer == data['answer']:
            if data['step'] > 5: 
                await message.answer(GAME_OVER_WIN, parse_mode='Markdown')
                await States.start.set()
            else:
                res = await get_random()
                data['step'] += 1
                data['answer'] = res['translation']
                data['word'] = res['word']

                await message.reply('Correct!')
                await message.answer(ENTER_THE_CHARACTER_TO_TRANSLATE.format(data['word']))
        else:
            await message.reply(GAME_OVER_LOSE, parse_mode='Markdown')
            await States.start.set()


@dp.message_handler(commands=['train_translation_mul'], state="*")
async def train_translation(message: types.Message, state: FSMContext):
    await States.train_translation.set()
    res = await get_random()
    async with state.proxy() as data:
        data['step'] = 1
        data['answer'] = res['translation']
        data['word'] = res['word']
    
    all_words = await get_all()
    all_answers = [w['translation'] for w in all_words]
    all_answers.remove(res['translation'])

    random.shuffle(all_answers)
    answers = [data['answer']] + all_answers[:2]
    random.shuffle(answers)

    kbrd = make_keyboard(answers)

    await message.answer("Word: " + data['word'], reply_markup=kbrd)


@dp.callback_query_handler(state=States.train_translation)
async def button_callback_train_translation(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data
    async with state.proxy() as data:
        if answer == data['answer']:
            res = await get_random()
            data['step'] += 1
            data['answer'] = res['translation']
            data['word'] = res['word']
            if data['step'] > 5:
                await bot.send_message(callback_query.from_user.id, GAME_OVER_WIN, parse_mode='Markdown')
                await States.start.set()
            else:
                all_words = await get_all()
                all_answers = [w['translation'] for w in all_words]
                all_answers.remove(res['translation'])

                random.shuffle(all_answers)
                answers = [data['answer']] + all_answers[:2]
                random.shuffle(answers)

                kbrd = make_keyboard(answers)

                await bot.send_message(callback_query.from_user.id, "Correct! \n" +  "Word: " + data['word'],
                                       reply_markup=kbrd)
        else:
            await States.start.set()
            await bot.send_message(callback_query.from_user.id, GAME_OVER_LOSE, parse_mode='Markdown')
            