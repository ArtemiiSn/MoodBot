import asyncio
import asyncpg

async def test_connection():
    try:
        conn = await asyncpg.connect(
            user="postgres",
            password="1234",
            database="mood_db",
            host="localhost"
        )
        print("✅ Успешное подключение к базе данных!")

        # Попробуем выполнить простой запрос
        result = await conn.fetch("SELECT 1 AS test")
        print("Результат запроса:", result)

        await conn.close()
    except Exception as e:
        print("❌ Ошибка подключения:", e)

asyncio.run(test_connection())
