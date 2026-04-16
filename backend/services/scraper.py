import subprocess
import re

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


def _curl_get(url: str) -> str:
    result = subprocess.run(
        ["curl", "-sL", url,
         "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
         "-H", "Accept-Language: ko-KR,ko;q=0.9",
         "--max-time", "10"],
        capture_output=True, text=True
    )
    return result.stdout


def _infer_lane_from_champions(champ_names: list[str]) -> str | None:
    """상위 챔피언 목록에서 주 라인 추론"""
    lane_votes: dict[str, int] = {}
    for i, champ in enumerate(champ_names):
        lane = CHAMPION_LANE.get(champ)
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
        "champion_pool": 0,
        "tier": "UNRANKED",
    }


def _scrape_opgg(summoner_name: str) -> dict:
    # 소환사명에 태그 없으면 -KR1 추가 시도
    name = summoner_name.strip()
    url = f"https://op.gg/lol/summoners/kr/{name.replace(' ', '%20')}"
    html = _curl_get(url)

    if len(html) < 1000:
        raise ValueError("페이지 로드 실패")

    # 메타 description에서 티어 + 챔피언 파싱
    # 예: "Hide on bush#KR1 / Challenger 1 1799LP / 187Win 136Lose Win rate 58% / Aurora - 18Win 13Lose..."
    desc_match = re.search(
        r'name.*?description.*?content.*?"([^"]{30,})"',
        html
    )

    tier = "UNRANKED"
    champ_names: list[str] = []

    if desc_match:
        desc = desc_match.group(1)
        # 티어 추출
        tier_match = re.search(
            r'/\s*(Challenger|Grandmaster|Master|Diamond|Emerald|Platinum|Gold|Silver|Bronze|Iron)',
            desc, re.IGNORECASE
        )
        if tier_match:
            tier = tier_match.group(1).upper()

        # 챔피언 추출: "Aurora - 18Win..."
        champs = re.findall(r"([A-Za-z][A-Za-z\s'\.&!]+?)\s*-\s*\d+Win", desc)
        champ_names = [c.strip() for c in champs if c.strip() and len(c.strip()) > 1]

    main_lane = _infer_lane_from_champions(champ_names)
    champion_pool = len(champ_names)

    return {
        "summoner_name": summoner_name,
        "main_lane": main_lane,
        "sub_lane": None,
        "champion_pool": champion_pool,
        "tier": tier,
    }
