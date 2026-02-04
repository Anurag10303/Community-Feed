import { useState } from "react";
import Feed from "./components/Feed";
import Leaderboard from "./components/Leaderboard";
import Navbar from "./components/Navbar";

export default function App() {
  const [leaderboardKey, setLeaderboardKey] = useState(0);

  return (
    <div className="max-w-6xl mx-auto px-4 py-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {/* FEED */}
        <div className="md:col-span-3">
          <Feed setLeaderboardRefresh={setLeaderboardKey} />
        </div>

        {/* LEADERBOARD */}
        <div className="md:col-span-1">
          <div className="sticky top-6">
            <Leaderboard refreshKey={leaderboardKey} />
          </div>
        </div>
      </div>
    </div>
  );
}
