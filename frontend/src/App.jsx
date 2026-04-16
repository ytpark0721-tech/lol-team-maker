import { useState } from 'react'
import PlayerInput from './components/PlayerInput'
import PlayerList from './components/PlayerList'
import TeamResult from './components/TeamResult'
import MatchHistory from './components/MatchHistory'
import axios from 'axios'
import './App.css'

export default function App() {
  const [players, setPlayers] = useState([])
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [page, setPage] = useState('main')  // 'main' | 'history'

  const refreshPlayers = async () => {
    const res = await axios.get('/api/players')
    setPlayers(res.data)
  }

  const handleGenerate = async () => {
    if (players.length !== 10) {
      setError('정확히 10명이 필요합니다')
      return
    }
    setLoading(true)
    setError('')
    try {
      const res = await axios.post('/api/teams/generate', {
        player_ids: players.map(p => p.id),
      })
      setResult(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || '팀 구성 실패')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = async () => {
    await axios.delete('/api/players')
    setPlayers([])
    setResult(null)
  }

  return (
    <div className="app">
      <h1>⚔️ LOL 내전 팀 메이커</h1>

      <div className="nav-tabs">
        <button
          className={`nav-tab ${page === 'main' ? 'nav-tab-active' : ''}`}
          onClick={() => setPage('main')}
        >🏠 팀 구성</button>
        <button
          className={`nav-tab ${page === 'history' ? 'nav-tab-active' : ''}`}
          onClick={() => setPage('history')}
        >📊 내전 기록</button>
      </div>

      {page === 'main' && (
        <>
          <PlayerInput onAdded={refreshPlayers} />

          {players.length > 0 && (
            <>
              <PlayerList
                players={players}
                onUpdate={refreshPlayers}
                onDelete={refreshPlayers}
              />

              <div className="actions">
                <span className="count">{players.length} / 10명</span>
                <button
                  className="btn-generate"
                  onClick={handleGenerate}
                  disabled={players.length !== 10 || loading}
                >
                  {loading ? '팀 구성 중...' : '⚖️ 팀 자동 배정'}
                </button>
                <button className="btn-clear" onClick={handleClear}>
                  전체 초기화
                </button>
              </div>

              {error && <p className="error">{error}</p>}
            </>
          )}

          {result && <TeamResult result={result} />}
        </>
      )}

      {page === 'history' && <MatchHistory />}
    </div>
  )
}
