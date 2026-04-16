import subprocess
import re
import httpx
from urllib.parse import quote

# 챔피언 → 주 라인 매핑
CHAMPION_LANE: dict[str, str] = {
    # TOP
    "Garen": "top", "Darius": "top", "Fiora": "top", "Camille": "top",
    "Jax": "top", "Irelia": "top", "Renekton": "top", "Shen": "top",
    "Malphite": "top", "Mordekaiser": "top", "Nasus": "top", "Teemo": "top",
    "Urgot": "top", "Aatrox": "top", "Gnar": "top", "Kennen": "top",
    "Rumble": "top", "Vladimir": "top", "Sett": "top", "Wukong": "top",
    "Gangplank": "top", "Quinn": "top", "Tryndamere": "top", "Yorick": "top",
    "Illaoi": "top", "Kled": "top", "Cho'Gath": "top", "Ornn": "top",
    "Poppy": "top", "Grasp": "top", "Dr. Mundo": "top", "Riven": "top",
    "Singed": "top", "Jayce": "top", "Akali": "top", "Kayle": "top",
    "Olaf": "top", "Pantheon": "top", "Maokai": "top",

    # JUNGLE
    "Lee Sin": "jungle", "Vi": "jungle", "Jarvan IV": "jungle", "Elise": "jungle",
    "Hecarim": "jungle", "Kha'Zix": "jungle", "Kindred": "jungle", "Nidalee": "jungle",
    "Rek'Sai": "jungle", "Sejuani": "jungle", "Warwick": "jungle", "Zac": "jungle",
    "Amumu": "jungle", "Fiddlesticks": "jungle", "Gragas": "jungle", "Graves": "jungle",
    "Master Yi": "jungle", "Nunu & Willump": "jungle", "Rammus": "jungle",
    "Shyvana": "jungle", "Udyr": "jungle", "Viego": "jungle", "Volibear": "jungle",
    "Xin Zhao": "jungle", "Diana": "jungle", "Ekko": "jungle", "Evelynn": "jungle",
    "Ivern": "jungle", "Kayn": "jungle", "Lillia": "jungle", "Nocturne": "jungle",
    "Rengar": "jungle", "Shaco": "jungle", "Taliyah": "jungle", "Trundle": "jungle",
    "Briar": "jungle", "Bel'Veth": "jungle", "Wukong": "jungle",

    # MID
    "Ahri": "mid", "Syndra": "mid", "Orianna": "mid", "Ryze": "mid",
    "Zed": "mid", "Yasuo": "mid", "Yone": "mid", "Azir": "mid",
    "Lux": "mid", "Twisted Fate": "mid", "Veigar": "mid", "Cassiopeia": "mid",
    "Fizz": "mid", "LeBlanc": "mid", "Lissandra": "mid", "Malzahar": "mid",
    "Orianna": "mid", "Qiyana": "mid", "Talon": "mid", "Sylas": "mid",
    "Viktor": "mid", "Xerath": "mid", "Ziggs": "mid", "Zoe": "mid",
    "Anivia": "mid", "Annie": "mid", "Corki": "mid", "Galio": "mid",
    "Kassadin": "mid", "Katarina": "mid", "Aurelion Sol": "mid", "Hwei": "mid",
    "Naafiri": "mid", "Neeko": "mid", "Vex": "mid", "Ekko": "mid",
    "Aurora": "mid", "Smolder": "mid",

    # BOT (ADC)
    "Jinx": "bot", "Caitlyn": "bot", "Jhin": "bot", "Ezreal": "bot",
    "Ashe": "bot", "Draven": "bot", "Kalista": "bot", "Kai'Sa": "bot",
    "Lucian": "bot", "Miss Fortune": "bot", "Tristana": "bot", "Twitch": "bot",
    "Vayne": "bot", "Xayah": "bot", "Zeri": "bot", "Aphelios": "bot",
    "Kog'Maw": "bot", "Nilah": "bot", "Samira": "bot", "Sivir": "bot",
    "Varus": "bot",

    # SUPPORT
    "Thresh": "support", "Lulu": "support", "Nautilus": "support", "Blitzcrank": "support",
    "Brand": "support", "Janna": "support", "Karma": "support", "Leona": "support",
    "Morgana": "support", "Nami": "support", "Sona": "support", "Soraka": "support",
    "Taric": "support", "Vel'Koz": "support", "Zyra": "support", "Alistar": "support",
    "Bard": "support", "Braum": "support", "Pyke": "support", "Rakan": "support",
    "Seraphine": "support", "Senna": "support", "Swain": "support", "Yuumi": "support",
    "Zilean": "support", "Rell": "support", "Milio": "support", "Renata Glasc": "support",
    "Heimerdinger": "support",
}

TIER_ORDER = ["IRON","BRONZE","SILVER","GOLD","PLATINUM","EMERALD","DIAMOND","MASTER","GRANDMASTER","CHALLENGER"]

# 챔피언명 정규화 (공백·특수문자 제거) → URL 포맷과 매칭
def _norm(name: str) -> str:
    return re.sub(r"[^A-Za-z]", "", name).lower()

CHAMPION_LANE_NORM: dict[str, str] = {_norm(k): v for k, v in CHAMPION_LANE.items()}


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
}

def _fetch(url: str) -> str:
    """httpx 먼저 시도 → 실패 시 curl subprocess 폴백 (크로스플랫폼)"""
    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=15) as client:
            resp = client.get(url)
            if len(resp.text) > 1000:
                return resp.text
    except Exception:
        pass

    # curl 폴백
    result = subprocess.run(
        ["curl", "-sL", url,
         "-H", f"User-Agent: {HEADERS['User-Agent']}",
         "-H", f"Accept-Language: {HEADERS['Accept-Language']}",
         "--max-time", "15"],
        capture_output=True, text=True
    )
    return result.stdout


def _infer_lane_from_champions(champ_names: list[str]) -> str | None:
    """상위 챔피언 목록에서 주 라인 추론 (URL 포맷 정규화 후 매칭)"""
    lane_votes: dict[str, int] = {}
    for i, champ in enumerate(champ_names):
        lane = CHAMPION_LANE_NORM.get(_norm(champ))
        if lane:
            weight = len(champ_names) - i  # 상위 챔피언에 가중치
            lane_votes[lane] = lane_votes.get(lane, 0) + weight
    if not lane_votes:
        return None
    return max(lane_votes, key=lambda x: lane_votes[x])


async def scrape_summoner(summoner_name: str) -> dict:
    """op.gg에서 소환사 정보 조회 (curl 기반)"""
    try:
        return _scrape_opgg(summoner_name)
    except Exception:
        pass
    return {
        "summoner_name": summoner_name,
        "main_lane": None,
        "sub_lane": None,
        "champions": "",
        "tier": "UNRANKED",
    }


def _scrape_opgg(summoner_name: str) -> dict:
    # # → - 변환 후 한글 포함 전체 URL 인코딩
    name = summoner_name.strip().replace('#', '-')
    encoded = quote(name, safe='-')
    url = f"https://op.gg/lol/summoners/kr/{encoded}"
    html = _fetch(url)

    if len(html) < 1000:
        raise ValueError("페이지 로드 실패")

    champ_names: list[str] = []
    tier = "UNRANKED"

    # 챔피언 추출: op.gg CDN 이미지 URL에서 챔피언명 파싱
    # 형식: akamaized.net/meta/images/lol/{ver}/champion/Maokai.png
    all_champs = re.findall(
        r'akamaized\.net/meta/images/lol/[^/]+/champion/([A-Za-z0-9]+)\.png', html
    )
    # 순서 유지하며 중복 제거
    seen: set[str] = set()
    for c in all_champs:
        if c not in seen:
            seen.add(c)
            champ_names.append(c)

    # 역대 최고 티어: "first-letter:uppercase">gold 1</span> 형태
    # 티어명만 추출 (뒤의 숫자 제거)
    season_tiers = re.findall(r'first-letter:uppercase[^"]*">([a-z]+)', html)

    if season_tiers:
        valid = [t for t in season_tiers if t.upper() in TIER_ORDER]
        if valid:
            best = max(valid, key=lambda t: TIER_ORDER.index(t.upper()))
            tier = best.upper()

    main_lane = _infer_lane_from_champions(champ_names)

    return {
        "summoner_name": summoner_name,
        "main_lane": main_lane,
        "sub_lane": None,
        "champions": ", ".join(champ_names[:5]),
        "tier": tier,
    }
