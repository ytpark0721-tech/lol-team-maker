import { useState } from 'react'
import axios from 'axios'

const LANES = ['top', 'jungle', 'mid', 'bot', 'support']
const LANE_LABEL = { top: '탑', jungle: '정글', mid: '미드', bot: '원딜', support: '서폿' }

export default function PlayerInput({ onAdded }) {
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [manual, setManual] = useState(false)
  const [manualLane, setManualLane] = useState('top')

  const handleAdd = async () => {
    if (!name.trim()) return
    setLoading(true)
    setError('')
    try {
      if (manual) {
        await axios.post('/api/players', {
          summoner_name: name.trim(),
          main_lane: manualLane,
          value: 5,
        })
      } else {
        await axios.post(`/api/players/scrape?summoner_name=${encodeURIComponent(name.trim())}`)
      }
      setName('')
      onAdded()
    } catch (e) {
      setError(e.response?.data?.detail || '추가 실패')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="player-input">
      <div className="input-row">
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleAdd()}
          placeholder="소환사명 입력"
          disabled={loading}
        />
        {manual && (
          <select value={manualLane} onChange={e => setManualLane(e.target.value)}>
            {LANES.map(l => (
              <option key={l} value={l}>{LANE_LABEL[l]}</option>
            ))}
          </select>
        )}
        <button onClick={handleAdd} disabled={loading || !name.trim()}>
          {loading ? '조회 중...' : '추가'}
        </button>
      </div>
      <label className="manual-toggle">
        <input
          type="checkbox"
          checked={manual}
          onChange={e => setManual(e.target.checked)}
        />
        수동 입력 (op.gg 조회 안 됨)
      </label>
      {error && <p className="error">{error}</p>}
    </div>
  )
}
