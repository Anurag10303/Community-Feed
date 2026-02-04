import { useState } from "react";

export default function PostCard({ post, onLike, onComment, onLikeComment }) {
  const [text, setText] = useState("");
  const [showBox, setShowBox] = useState(false);

  async function submitComment(e) {
    e.preventDefault();
    if (!text.trim()) return;

    await onComment(post.id, text);
    setText("");
    setShowBox(false);
  }

  return (
    <div className="bg-white rounded-xl shadow-md p-5 mb-6 border text-black">
      {/* HEADER */}
      <div className="font-semibold text-gray-900">{post.author.username}</div>

      {/* CONTENT */}
      <div className="my-2 text-gray-800">{post.content}</div>

      {/* STATS */}
      <div className="text-sm text-gray-600 mb-2">
        {post.like_count} likes · {post.comments.length} comments
      </div>

      {/* POST ACTIONS */}
      <div className="flex gap-6 border-t border-b py-2 mb-3">
        <button
          disabled={post.is_liked_by_user}
          onClick={() => onLike(post.id)}
          className={`font-semibold ${
            post.is_liked_by_user
              ? "text-blue-600 cursor-not-allowed"
              : "text-gray-600 hover:text-blue-600"
          }`}
        >
          👍 {post.is_liked_by_user ? "Liked" : "Like"}
        </button>

        <button
          onClick={() => setShowBox((v) => !v)}
          className="font-semibold text-blue-600"
        >
          💬 Comment
        </button>
      </div>

      {/* COMMENTS */}
      <div className="space-y-2">
        {post.comments.map((comment) => (
          <div
            key={comment.id}
            className="bg-gray-100 rounded-lg px-3 py-2 text-sm"
          >
            <div>
              <span className="font-semibold">{comment.author.username}</span>{" "}
              {comment.content}
            </div>

            <div className="flex gap-4 mt-1 text-xs text-gray-600">
              <span>{comment.like_count || 0} likes</span>

              <button
                disabled={comment.is_liked_by_user}
                onClick={() => onLikeComment(comment.id)}
                className={`font-semibold ${
                  comment.is_liked_by_user
                    ? "text-blue-600 cursor-not-allowed"
                    : "hover:text-blue-600"
                }`}
              >
                👍 {comment.is_liked_by_user ? "Liked" : "Like"}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* COMMENT INPUT */}
      {showBox && (
        <form onSubmit={submitComment} className="flex gap-2 mt-3">
          <input
            className="flex-1 border rounded px-3 py-2"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Write a comment…"
          />
          <button className="bg-blue-600 text-white px-4 rounded">Post</button>
        </form>
      )}
    </div>
  );
}
