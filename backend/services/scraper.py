import httpx
from bs4 import BeautifulSoup
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
}

LANE_MAP = {
    "TOP": "top",
    "JUNGLE": "jungle",
    "MID": "mid",
    "BOTTOM": "bot",
    "SUPPORT": "support",
    "ADC": "bot",
}

TIER_ORDER = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "EMERALD", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]


async def scrape_summoner(summoner_name: str) -> dict:
    """op.gg에서 소환사 정보 조회"""
    try:
        return await _scrape_opgg(summoner_name)
    except Exception:
        pass

    return {
        "summoner_name": summoner_name,
        "main_lane": None,
        "sub_lane": None,
        "champion_pool": 0,
        "tier": "UNRANKED",
    }


async def _scrape_opgg(summoner_name: str) -> dict:
    url = f"https://www.op.gg/summoners/kr/{summoner_name}"
    async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
        resp = await client.get(url, headers=HEADERS)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    script = soup.find("script", id="__NEXT_DATA__")
    if not script:
        raise ValueError("__NEXT_DATA__ not found")

    data = json.loads(script.string)
    props = data.get("props", {}).get("pageProps", {}).get("data", {})

    # 티어 추출
    tier = "UNRANKED"
    lp_info = props.get("summoner_leagues", [])
    for league in lp_info:
        if league.get("queue_info", {}).get("game_type") == "SOLORANKED":
            tier = league.get("tier_info", {}).get("tier", "UNRANKED")
            break

    # 챔피언 통계에서 라인 추출
    champion_stats = props.get("champion_stats", [])
    lane_counts: dict[str, int] = {}
    champion_set = set()

    for stat in champion_stats:
        champ = stat.get("id")
        if champ:
            champion_set.add(champ)
        position = stat.get("position", "").upper()
        if position in LANE_MAP:
            lane = LANE_MAP[position]
            lane_counts[lane] = lane_counts.get(lane, 0) + stat.get("play", 0)

    lanes_sorted = sorted(lane_counts.items(), key=lambda x: x[1], reverse=True)
    main_lane = lanes_sorted[0][0] if lanes_sorted else None
    sub_lane = lanes_sorted[1][0] if len(lanes_sorted) > 1 else None

    return {
        "summoner_name": summoner_name,
        "main_lane": main_lane,
        "sub_lane": sub_lane,
        "champion_pool": len(champion_set),
        "tier": tier,
    }
