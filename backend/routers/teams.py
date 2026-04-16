from fastapi import APIRouter, HTTPException
import aiosqlite
from models.schemas import TeamRequest, TeamResult, TeamPlayer
from services.balancer import balance_teams
from database import DB_PATH

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("/generate", response_model=TeamResult)
async def generate_teams(req: TeamRequest):
    if len(req.player_ids) != 10:
        raise HTTPException(status_code=400, detail="정확히 10명을 선택해야 합니다")

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        placeholders = ",".join("?" * len(req.player_ids))
        rows = await (await db.execute(
            f"SELECT * FROM players WHERE id IN ({placeholders})",
            req.player_ids
        )).fetchall()

    players = [dict(r) for r in rows]
    if len(players) != 10:
        raise HTTPException(status_code=404, detail="일부 플레이어를 찾을 수 없습니다")

    try:
        team1, team2 = balance_teams(players)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    def to_team_player(p: dict) -> TeamPlayer:
        return TeamPlayer(
            id=p["id"],
            summoner_name=p["summoner_name"],
            lane=p["assigned_lane"],
            value=p["value"],
            tier=p["tier"],
        )

    t1 = [to_team_player(p) for p in team1]
    t2 = [to_team_player(p) for p in team2]
    t1_total = sum(p.value for p in t1)
    t2_total = sum(p.value for p in t2)

    return TeamResult(
        team1=t1,
        team2=t2,
        team1_total=t1_total,
        team2_total=t2_total,
        diff=abs(t1_total - t2_total),
    )
