from fastapi import APIRouter, HTTPException
import aiosqlite
from models.schemas import MatchRecord, Match, MatchPlayerStat, PlayerStat
from database import DB_PATH
from collections import Counter

router = APIRouter(prefix="/matches", tags=["matches"])


@router.post("", response_model=Match)
async def record_match(data: MatchRecord):
    """내전 경기 결과 기록"""
    if data.winner not in (1, 2):
        raise HTTPException(status_code=400, detail="winner는 1 또는 2여야 합니다")

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            """INSERT INTO matches (winner, team1_value, team2_value, notes)
               VALUES (?, ?, ?, ?)""",
            (data.winner, data.team1_total, data.team2_total, data.notes or "")
        )
        match_id = cursor.lastrowid

        for p in data.team1:
            await db.execute(
                """INSERT INTO match_players (match_id, summoner_name, team, lane, value, won)
                   VALUES (?, ?, 1, ?, ?, ?)""",
                (match_id, p.summoner_name, p.lane, p.value, 1 if data.winner == 1 else 0)
            )
        for p in data.team2:
            await db.execute(
                """INSERT INTO match_players (match_id, summoner_name, team, lane, value, won)
                   VALUES (?, ?, 2, ?, ?, ?)""",
                (match_id, p.summoner_name, p.lane, p.value, 1 if data.winner == 2 else 0)
            )

        await db.commit()
        row = await (await db.execute(
            "SELECT * FROM matches WHERE id = ?", (match_id,)
        )).fetchone()
        players = await (await db.execute(
            "SELECT * FROM match_players WHERE match_id = ?", (match_id,)
        )).fetchall()

        return {
            **dict(row),
            "players": [dict(p) for p in players]
        }


@router.get("", response_model=list[Match])
async def list_matches(limit: int = 20):
    """최근 경기 기록 목록"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await (await db.execute(
            "SELECT * FROM matches ORDER BY played_at DESC LIMIT ?", (limit,)
        )).fetchall()

        result = []
        for row in rows:
            players = await (await db.execute(
                "SELECT * FROM match_players WHERE match_id = ?", (row["id"],)
            )).fetchall()
            result.append({
                **dict(row),
                "players": [dict(p) for p in players]
            })
        return result


@router.delete("/{match_id}")
async def delete_match(match_id: int):
    """경기 기록 삭제"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM match_players WHERE match_id = ?", (match_id,))
        await db.execute("DELETE FROM matches WHERE id = ?", (match_id,))
        await db.commit()
    return {"ok": True}


@router.get("/stats", response_model=list[PlayerStat])
async def get_player_stats():
    """플레이어별 누적 통계"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await (await db.execute(
            """SELECT summoner_name, COUNT(*) as games,
                      SUM(won) as wins,
                      AVG(value) as avg_value,
                      GROUP_CONCAT(lane) as lanes
               FROM match_players
               GROUP BY summoner_name
               ORDER BY games DESC"""
        )).fetchall()

        stats = []
        for r in rows:
            games = r["games"]
            wins = r["wins"] or 0
            lanes = r["lanes"].split(",") if r["lanes"] else []
            most_lane = Counter(lanes).most_common(1)[0][0] if lanes else None
            stats.append({
                "summoner_name": r["summoner_name"],
                "games": games,
                "wins": wins,
                "losses": games - wins,
                "win_rate": round(wins / games * 100, 1) if games else 0,
                "avg_value": round(r["avg_value"] or 0, 1),
                "most_lane": most_lane,
            })
        return stats
