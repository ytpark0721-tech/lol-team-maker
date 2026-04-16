import aiosqlite

DB_PATH = "lol.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                summoner_name TEXT NOT NULL,
                main_lane TEXT,
                sub_lane TEXT,
                champions TEXT DEFAULT '',
                tier TEXT DEFAULT 'UNRANKED',
                value INTEGER DEFAULT 5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
