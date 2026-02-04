import { likeComment } from "../api";
import { getCurrentUserId } from "../user";

const USER_ID = getCurrentUserId();

export default function Comment({ comment, onRefresh }) {
  async function handleLike() {
    await likeComment(comment.id, USER_ID);
    onRefresh(); // 🔥 THIS TRIGGERS LEADERBOARD TOO
  }

  return (
    <div className="bg-gray-100 rounded px-3 py-2 text-sm">
      <span className="font-semibold">{comment.author.username}</span>{" "}
      {comment.content}
      <div className="text-xs text-gray-600 mt-1 flex gap-3">
        <button onClick={handleLike} className="hover:text-blue-600">
          👍 Like
        </button>
        <span>{comment.like_count} likes</span>
      </div>
    </div>
  );
}
