from itertools import product

LANES = ["top", "jungle", "mid", "bot", "support"]


def balance_teams(players: list[dict]) -> tuple[list, list]:
    """
    10명의 플레이어를 라인 배정 후 몸값이 균형 잡힌 두 팀으로 분리.

    알고리즘:
    1. 주 라인 → 서브 라인 → 나머지 순으로 각 라인에 2명씩 배정
    2. 라인별 2명 쌍에서 2^5 = 32가지 팀 조합을 모두 시도
    3. 몸값 합산 차이가 최소인 조합 선택
    """
    if len(players) != 10:
        raise ValueError("정확히 10명이 필요합니다")

    lane_slots: dict[str, list] = {lane: [] for lane in LANES}

    # 1차: 주 라인으로 배정
    unassigned = list(players)
    for player in players:
        lane = player.get("main_lane")
        if lane and lane in lane_slots and len(lane_slots[lane]) < 2:
            lane_slots[lane].append(player)
            unassigned.remove(player)

    # 2차: 서브 라인으로 배정
    still_unassigned = []
    for player in unassigned:
        lane = player.get("sub_lane")
        if lane and lane in lane_slots and len(lane_slots[lane]) < 2:
            lane_slots[lane].append(player)
        else:
            still_unassigned.append(player)

    # 3차: 남은 빈 슬롯에 채우기
    for player in still_unassigned:
        for lane in LANES:
            if len(lane_slots[lane]) < 2:
                lane_slots[lane].append(player)
                break

    # 각 라인에 정확히 2명씩 있어야 함
    for lane in LANES:
        if len(lane_slots[lane]) != 2:
            raise ValueError(f"{lane} 라인 배정 오류")

    # 2^5 = 32가지 조합 중 몸값 차이 최소 조합 탐색
    best_diff = float("inf")
    best_team1 = None
    best_team2 = None

    lane_pairs = [lane_slots[lane] for lane in LANES]

    for choices in product([0, 1], repeat=5):
        team1 = []
        team2 = []
        for i, choice in enumerate(choices):
            p1 = dict(lane_pairs[i][choice])
            p2 = dict(lane_pairs[i][1 - choice])
            p1["assigned_lane"] = LANES[i]
            p2["assigned_lane"] = LANES[i]
            team1.append(p1)
            team2.append(p2)

        diff = abs(
            sum(p["value"] for p in team1) - sum(p["value"] for p in team2)
        )
        if diff < best_diff:
            best_diff = diff
            best_team1 = team1
            best_team2 = team2

    return best_team1, best_team2
