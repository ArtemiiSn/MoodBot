import asyncio
import aiocron
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from config import load_config
from db import create_pool, init_db
from handlers import start_handler, mood_callback, profile_callback
from keyboards import mood_inline_keyboard, profile_keyboard

config = load_config()

bot = Bot(
    token=config["BOT_TOKEN"],
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

async def start_cb(message: types.Message):
    await start_handler(message, dp["db"])

async def mood_cb(callback: types.CallbackQuery):
    await mood_callback(callback, dp["db"])

async def profile_cb(callback: types.CallbackQuery):
    await profile_callback(callback, dp["db"])

dp.message.register(start_cb, Command(commands=["start"]))
dp.callback_query.register(mood_cb, lambda c: c.data.startswith("mood:"))
dp.callback_query.register(profile_cb, lambda c: c.data == "profile")

# 🕛 Ежедневная задача в 12:00
@aiocron.crontab('0 12 * * *')
async def daily_mood_check():
    async with dp["db"].acquire() as conn:
        users = await conn.fetch("SELECT tg_id FROM users")

    for user in users:
        chat_id = user["tg_id"]
        try:
            messages = await bot.get_chat_history(chat_id, limit=20)
            for msg in messages:
                if msg.from_user.id == (await bot.me()).id:
                    try:
                        await bot.delete_message(chat_id, msg.message_id)
                    except:
                        continue
            await bot.send_message(chat_id, "👋 Привет! Как у тебя настроение сегодня?", reply_markup=mood_inline_keyboard())
        except Exception as e:
            print(f"Не удалось отправить пользователю {chat_id}: {e}")

async def main():
    pool = await create_pool()
    await init_db(pool)
    dp["db"] = pool
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
