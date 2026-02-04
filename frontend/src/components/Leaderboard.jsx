import { useEffect, useState } from "react";
import { fetchLeaderboard } from "../api";

export default function Leaderboard({ refreshKey }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchLeaderboard()
      .then(setData)
      .catch(() => setData([]));
  }, [refreshKey]);

  return (
    <div className="bg-white rounded-xl shadow p-4 border">
      <h2 className="font-bold mb-3">🔥 Top Karma (24h)</h2>

      {data.length === 0 && (
        <div className="text-sm text-gray-500">No activity yet</div>
      )}

      {data.map((row, i) => (
        <div key={row.user_id} className="flex justify-between text-sm mb-1">
          <span>
            {i + 1}. {row.username}
          </span>
          <span className="font-semibold">{row.karma}</span>
        </div>
      ))}
    </div>
  );
}
