import { useState } from 'react'
import axios from 'axios'

const LANE_LABEL = { top: '탑', jungle: '정글', mid: '미드', bot: '원딜', support: '서폿' }
const LANE_ICON = { top: '🛡️', jungle: '🌲', mid: '⚡', bot: '🏹', support: '💊' }
const LANE_ORDER = ['top', 'jungle', 'mid', 'bot', 'support']

export default function TeamResult({ result }) {
  const [winner, setWinner] = useState(null)
  const [recorded, setRecorded] = useState(false)
  const [recording, setRecording] = useState(false)

  const sorted = (team) =>
    [...team].sort((a, b) => LANE_ORDER.indexOf(a.lane) - LANE_ORDER.indexOf(b.lane))

  const handleRecord = async () => {
    if (!winner) return
    setRecording(true)
    try {
      await axios.post('/api/matches', {
        team1: result.team1,
        team2: result.team2,
        team1_total: result.team1_total,
        team2_total: result.team2_total,
        winner,
      })
      setRecorded(true)
    } catch (e) {
      alert('기록 저장 실패: ' + (e.response?.data?.detail || e.message))
    } finally {
      setRecording(false)
    }
  }

  return (
    <div className="team-result">
      <h2>⚖️ 팀 배정 결과</h2>
      <p className="diff">
        몸값 차이: <strong>{result.diff}</strong>
        {result.diff === 0 && ' 🎯 완벽한 밸런스!'}
      </p>

      <div className="teams">
        <div className="team team1">
          <h3>🔵 팀 1 <span className="total">합계 {result.team1_total}</span></h3>
          <table>
            <tbody>
              {sorted(result.team1).map(p => (
                <tr key={p.id}>
                  <td>{LANE_ICON[p.lane]} {LANE_LABEL[p.lane]}</td>
                  <td className="summoner-name">{p.summoner_name}</td>
                  <td>{p.tier}</td>
                  <td className="value-badge">{p.value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="vs">VS</div>

        <div className="team team2">
          <h3>🔴 팀 2 <span className="total">합계 {result.team2_total}</span></h3>
          <table>
            <tbody>
              {sorted(result.team2).map(p => (
                <tr key={p.id}>
                  <td>{LANE_ICON[p.lane]} {LANE_LABEL[p.lane]}</td>
                  <td className="summoner-name">{p.summoner_name}</td>
                  <td>{p.tier}</td>
                  <td className="value-badge">{p.value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 경기 결과 기록 */}
      {!recorded ? (
        <div className="record-section">
          <p className="record-label">경기 결과 기록</p>
          <div className="winner-select">
            <button
              className={`btn-winner btn-winner-1 ${winner === 1 ? 'selected' : ''}`}
              onClick={() => setWinner(1)}
            >
              🔵 팀 1 승리
            </button>
            <button
              className={`btn-winner btn-winner-2 ${winner === 2 ? 'selected' : ''}`}
              onClick={() => setWinner(2)}
            >
              🔴 팀 2 승리
            </button>
          </div>
          <button
            className="btn-record"
            onClick={handleRecord}
            disabled={!winner || recording}
          >
            {recording ? '저장 중...' : '📝 기록 저장'}
          </button>
        </div>
      ) : (
        <div className="record-done">
          ✅ 경기 결과가 기록되었습니다! (내전 기록 탭에서 확인)
        </div>
      )}
    </div>
  )
}
