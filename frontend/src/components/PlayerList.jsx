import { useState } from 'react'
import axios from 'axios'

const LANES = ['top', 'jungle', 'mid', 'bot', 'support']
const LANE_LABEL = { top: '탑', jungle: '정글', mid: '미드', bot: '원딜', support: '서폿' }
const LANE_ICON = { top: '🛡️', jungle: '🌲', mid: '⚡', bot: '🏹', support: '💊' }

export default function PlayerList({ players, onUpdate, onDelete }) {
  const handleValueChange = async (player, value) => {
    await axios.patch(`/api/players/${player.id}`, { value: parseInt(value) })
    onUpdate()
  }

  const handleLaneChange = async (player, lane) => {
    await axios.patch(`/api/players/${player.id}`, { main_lane: lane })
    onUpdate()
  }

  const handleDelete = async (id) => {
    await axios.delete(`/api/players/${id}`)
    onDelete()
  }

  return (
    <div className="player-list">
      <h2>참가자 목록</h2>
      <table>
        <thead>
          <tr>
            <th>소환사명</th>
            <th>주 라인</th>
            <th>모스트 챔피언</th>
            <th>최고 티어</th>
            <th>몸값</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {players.map(p => (
            <tr key={p.id}>
              <td className="summoner-name">{p.summoner_name}</td>
              <td>
                <select
                  value={p.main_lane || ''}
                  onChange={e => handleLaneChange(p, e.target.value)}
                >
                  <option value="">-</option>
                  {LANES.map(l => (
                    <option key={l} value={l}>
                      {LANE_ICON[l]} {LANE_LABEL[l]}
                    </option>
                  ))}
                </select>
              </td>
              <td className="champions">
                {p.champions ? p.champions : '-'}
              </td>
              <td>{p.tier}</td>
              <td>
                <div className="value-control">
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={p.value}
                    onChange={e => handleValueChange(p, e.target.value)}
                  />
                  <span className="value-num">{p.value}</span>
                </div>
              </td>
              <td>
                <button className="btn-delete" onClick={() => handleDelete(p.id)}>✕</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
