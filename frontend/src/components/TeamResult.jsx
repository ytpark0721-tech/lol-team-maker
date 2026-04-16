const LANE_LABEL = { top: '탑', jungle: '정글', mid: '미드', bot: '원딜', support: '서폿' }
const LANE_ICON = { top: '🛡️', jungle: '🌲', mid: '⚡', bot: '🏹', support: '💊' }
const LANE_ORDER = ['top', 'jungle', 'mid', 'bot', 'support']

export default function TeamResult({ result }) {
  const sorted = (team) =>
    [...team].sort((a, b) => LANE_ORDER.indexOf(a.lane) - LANE_ORDER.indexOf(b.lane))

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
    </div>
  )
}
