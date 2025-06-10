from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def mood_inline_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="😊 Отлично", callback_data="mood:happy")],
        [InlineKeyboardButton(text="🙂 Нормально", callback_data="mood:normal")],
        [InlineKeyboardButton(text="😐 Так себе", callback_data="mood:meh")],
        [InlineKeyboardButton(text="😔 Плохо", callback_data="mood:sad")]
    ])

def profile_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Профиль", callback_data="profile")]
    ])
