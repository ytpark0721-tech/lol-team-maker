import { useState, useEffect } from 'react'
import axios from 'axios'

const LANE_LABEL = { top: '탑', jungle: '정글', mid: '미드', bot: '원딜', support: '서폿' }
const LANE_ICON = { top: '🛡️', jungle: '🌲', mid: '⚡', bot: '🏹', support: '💊' }
const LANE_ORDER = ['top', 'jungle', 'mid', 'bot', 'support']

function formatDate(str) {
  const d = new Date(str.replace(' ', 'T') + 'Z')
  return d.toLocaleString('ko-KR', {
    month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit'
  })
}

export default function MatchHistory() {
  const [matches, setMatches] = useState([])
  const [stats, setStats] = useState([])
  const [tab, setTab] = useState('history')
  const [expanded, setExpanded] = useState(null)

  const load = async () => {
    const [mRes, sRes] = await Promise.all([
      axios.get('/api/matches'),
      axios.get('/api/matches/stats'),
    ])
    setMatches(mRes.data)
    setStats(sRes.data)
  }

  useEffect(() => { load() }, [])

  const handleDelete = async (id) => {
    if (!confirm('이 경기 기록을 삭제하시겠습니까?')) return
    await axios.delete(`/api/matches/${id}`)
    load()
  }

  const getTeamPlayers = (match, team) =>
    match.players
      .filter(p => p.team === team)
      .sort((a, b) => LANE_ORDER.indexOf(a.lane) - LANE_ORDER.indexOf(b.lane))

  return (
    <div className="match-history">
      <h2>📊 내전 기록</h2>

      <div className="history-tabs">
        <button
          className={`htab ${tab === 'history' ? 'htab-active' : ''}`}
          onClick={() => setTab('history')}
        >경기 히스토리</button>
        <button
          className={`htab ${tab === 'stats' ? 'htab-active' : ''}`}
          onClick={() => setTab('stats')}
        >플레이어 통계</button>
      </div>

      {tab === 'history' && (
        <div className="history-list">
          {matches.length === 0 && (
            <p className="empty-msg">아직 기록된 내전이 없습니다.</p>
          )}
          {matches.map(m => {
            const t1 = getTeamPlayers(m, 1)
            const t2 = getTeamPlayers(m, 2)
            const isOpen = expanded === m.id
            return (
              <div key={m.id} className="match-card">
                <div className="match-header" onClick={() => setExpanded(isOpen ? null : m.id)}>
                  <span className="match-date">{formatDate(m.played_at)}</span>
                  <span className={`match-winner ${m.winner === 1 ? 'blue' : 'red'}`}>
                    {m.winner === 1 ? '🔵 팀1 승' : '🔴 팀2 승'}
                  </span>
                  <span className="match-values">{m.team1_value} vs {m.team2_value}</span>
                  <button className="btn-expand">{isOpen ? '▲' : '▼'}</button>
                  <button className="btn-delete-match" onClick={e => { e.stopPropagation(); handleDelete(m.id) }}>✕</button>
                </div>

                {isOpen && (
                  <div className="match-detail">
                    <div className="match-teams">
                      <div className={`match-team ${m.winner === 1 ? 'win' : 'lose'}`}>
                        <div className="team-tag">🔵 팀 1 {m.winner === 1 ? '✓승' : '패'}</div>
                        {t1.map((p, i) => (
                          <div key={i} className="match-player">
                            <span>{LANE_ICON[p.lane]} {LANE_LABEL[p.lane]}</span>
                            <span className="mp-name">{p.summoner_name}</span>
                            <span className="mp-val">{p.value}</span>
                          </div>
                        ))}
                      </div>
                      <div className="match-vs-small">VS</div>
                      <div className={`match-team ${m.winner === 2 ? 'win' : 'lose'}`}>
                        <div className="team-tag">🔴 팀 2 {m.winner === 2 ? '✓승' : '패'}</div>
                        {t2.map((p, i) => (
                          <div key={i} className="match-player">
                            <span>{LANE_ICON[p.lane]} {LANE_LABEL[p.lane]}</span>
                            <span className="mp-name">{p.summoner_name}</span>
                            <span className="mp-val">{p.value}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}

      {tab === 'stats' && (
        <div className="stats-table-wrap">
          {stats.length === 0 && (
            <p className="empty-msg">내전 기록이 쌓이면 통계가 표시됩니다.</p>
          )}
          {stats.length > 0 && (
            <table className="stats-table">
              <thead>
                <tr>
                  <th>소환사명</th>
                  <th>게임</th>
                  <th>승</th>
                  <th>패</th>
                  <th>승률</th>
                  <th>평균 몸값</th>
                  <th>주 라인</th>
                </tr>
              </thead>
              <tbody>
                {stats.map(s => (
                  <tr key={s.summoner_name}>
                    <td className="summoner-name">{s.summoner_name}</td>
                    <td>{s.games}</td>
                    <td className="wins">{s.wins}</td>
                    <td className="losses">{s.losses}</td>
                    <td>
                      <span className={`wr-badge ${s.win_rate >= 50 ? 'wr-good' : 'wr-bad'}`}>
                        {s.win_rate}%
                      </span>
                    </td>
                    <td>{s.avg_value}</td>
                    <td>{s.most_lane ? `${LANE_ICON[s.most_lane]} ${LANE_LABEL[s.most_lane]}` : '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  )
}
