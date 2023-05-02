from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def make_keyboard(answers):
    buttons = []
    keyboard = InlineKeyboardMarkup()
    for answer in answers:
        buttons.append(InlineKeyboardButton(answer, callback_data=answer))
    for button in buttons:
        keyboard.add(button)
    return keyboard