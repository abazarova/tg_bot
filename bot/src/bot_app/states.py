from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    start = State()
    random_word = State()
    add_character = State()
    train_pinyin = State()
    train_translation= State()
    train_pinyin_write = State()
    train_translation_write = State()