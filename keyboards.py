from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def send_main_buttons() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Qidirish")]
        ]
    )

def send_stop_button():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Stop")]
        ]
    )
