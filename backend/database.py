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
        # 내전 경기 기록
        await db.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                winner INTEGER NOT NULL,        -- 1 or 2
                team1_value INTEGER NOT NULL,
                team2_value INTEGER NOT NULL,
                notes TEXT DEFAULT ''
            )
        """)
        # 경기별 플레이어 기록
        await db.execute("""
            CREATE TABLE IF NOT EXISTS match_players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER NOT NULL,
                summoner_name TEXT NOT NULL,
                team INTEGER NOT NULL,          -- 1 or 2
                lane TEXT NOT NULL,
                value INTEGER NOT NULL,
                won INTEGER NOT NULL,           -- 0 or 1
                FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE
            )
        """)
        await db.commit()
