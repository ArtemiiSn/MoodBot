from aiogram import types
from keyboards import mood_inline_keyboard, profile_keyboard

async def start_handler(message: types.Message, pool):
    await message.delete()  # ← Удаляем команду /start

    user_id = message.from_user.id
    async with pool.acquire() as conn:
        exists = await conn.fetchrow("SELECT 1 FROM users WHERE tg_id = $1", user_id)
        if not exists:
            await conn.execute("INSERT INTO users (tg_id) VALUES ($1)", user_id)

    await message.answer("Как у тебя настроение сегодня?", reply_markup=mood_inline_keyboard())


async def mood_callback(callback: types.CallbackQuery, pool):
    mood = callback.data.split(":")[1]
    user_id = callback.from_user.id

    async with pool.acquire() as conn:
        today = await conn.fetchval(
            "SELECT 1 FROM moods WHERE user_id = $1 AND created_at = CURRENT_DATE",
            user_id
        )
        if today:
            await callback.answer("Ты уже выбирал настроение сегодня 🙃", show_alert=True)
        else:
            await conn.execute(
                "INSERT INTO moods (user_id, mood) VALUES ($1, $2)",
                user_id, mood
            )
            await callback.message.edit_text("✅ Спасибо! Ты выбрал настроение.", reply_markup=profile_keyboard())
            await callback.answer()

async def profile_callback(callback: types.CallbackQuery, pool):
    user_id = callback.from_user.id
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT mood, created_at FROM moods 
            WHERE user_id = $1 
            ORDER BY created_at DESC 
            LIMIT 31
        """, user_id)
    if rows:
        text = "<b>📊 Твои последние 31 настроения:</b>\n\n"
        for r in rows:
            text += f"{r['created_at'].strftime('%d.%m')}: {r['mood']}\n"
    else:
        text = "У тебя пока нет сохранённых настроений."
    await callback.message.answer(text)
