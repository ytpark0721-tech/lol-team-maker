from pydantic import BaseModel
from typing import Optional

LANES = ["top", "jungle", "mid", "bot", "support"]

class PlayerCreate(BaseModel):
    summoner_name: str
    main_lane: Optional[str] = None
    sub_lane: Optional[str] = None
    champions: Optional[str] = ""
    tier: Optional[str] = "UNRANKED"
    value: int = 5

class PlayerUpdate(BaseModel):
    main_lane: Optional[str] = None
    sub_lane: Optional[str] = None
    value: Optional[int] = None

class Player(BaseModel):
    id: int
    summoner_name: str
    main_lane: Optional[str]
    sub_lane: Optional[str]
    champions: str
    tier: str
    value: int

class TeamRequest(BaseModel):
    player_ids: list[int]

class TeamPlayer(BaseModel):
    id: int
    summoner_name: str
    lane: str
    value: int
    tier: str

class TeamResult(BaseModel):
    team1: list[TeamPlayer]
    team2: list[TeamPlayer]
    team1_total: int
    team2_total: int
    diff: int
