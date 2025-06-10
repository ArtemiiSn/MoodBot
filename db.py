import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def create_pool():
    return await asyncpg.create_pool(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

async def init_db(pool):
    async with pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                tg_id BIGINT UNIQUE,
                created_at TIMESTAMP DEFAULT NOW()
            );
        ''')
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS moods (
                id SERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(tg_id),
                mood TEXT,
                created_at DATE DEFAULT CURRENT_DATE
            );
        ''')
