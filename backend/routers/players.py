from fastapi import APIRouter, HTTPException
import aiosqlite
from models.schemas import PlayerCreate, PlayerUpdate, Player
from services.scraper import scrape_summoner
from database import DB_PATH

router = APIRouter(prefix="/players", tags=["players"])


@router.get("", response_model=list[Player])
async def list_players():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await (await db.execute(
            "SELECT * FROM players ORDER BY created_at DESC"
        )).fetchall()
        return [dict(r) for r in rows]


@router.post("/scrape", response_model=Player)
async def add_player_by_scrape(summoner_name: str):
    """소환사명으로 op.gg 조회 후 플레이어 추가"""
    info = await scrape_summoner(summoner_name)
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            """INSERT INTO players (summoner_name, main_lane, sub_lane, champions, tier, value)
               VALUES (?, ?, ?, ?, ?, 5)""",
            (info["summoner_name"], info["main_lane"], info["sub_lane"],
             info["champions"], info["tier"])
        )
        await db.commit()
        row = await (await db.execute(
            "SELECT * FROM players WHERE id = ?", (cursor.lastrowid,)
        )).fetchone()
        return dict(row)


@router.post("", response_model=Player)
async def add_player(data: PlayerCreate):
    """수동으로 플레이어 추가"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            """INSERT INTO players (summoner_name, main_lane, sub_lane, champions, tier, value)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (data.summoner_name, data.main_lane, data.sub_lane,
             data.champions, data.tier, data.value)
        )
        await db.commit()
        row = await (await db.execute(
            "SELECT * FROM players WHERE id = ?", (cursor.lastrowid,)
        )).fetchone()
        return dict(row)


@router.patch("/{player_id}", response_model=Player)
async def update_player(player_id: int, data: PlayerUpdate):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        player = await (await db.execute(
            "SELECT * FROM players WHERE id = ?", (player_id,)
        )).fetchone()
        if not player:
            raise HTTPException(status_code=404, detail="플레이어를 찾을 수 없습니다")

        fields = {k: v for k, v in data.model_dump().items() if v is not None}
        if fields:
            sets = ", ".join(f"{k} = ?" for k in fields)
            await db.execute(
                f"UPDATE players SET {sets} WHERE id = ?",
                (*fields.values(), player_id)
            )
            await db.commit()

        row = await (await db.execute(
            "SELECT * FROM players WHERE id = ?", (player_id,)
        )).fetchone()
        return dict(row)


@router.delete("/{player_id}")
async def delete_player(player_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM players WHERE id = ?", (player_id,))
        await db.commit()
    return {"ok": True}


@router.delete("")
async def clear_players():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM players")
        await db.commit()
    return {"ok": True}
