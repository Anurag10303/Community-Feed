import { useEffect, useState } from "react";
import { fetchFeed, likePost, addComment, likeComment } from "../api";
import PostCard from "./PostCard";
import { getCurrentUserId } from "../user";

export default function Feed({ setLeaderboardRefresh }) {
  const [posts, setPosts] = useState([]);
  const userId = getCurrentUserId();

  useEffect(() => {
    fetchFeed(userId).then(setPosts);
  }, [userId]);

  /* ================= POST LIKE ================= */

  async function handlePostLike(postId) {
    await likePost(postId, userId);

    setPosts((prev) =>
      prev.map((p) =>
        p.id === postId
          ? {
              ...p,
              is_liked_by_user: true,
              like_count: p.like_count + 1,
            }
          : p,
      ),
    );

    setLeaderboardRefresh((k) => k + 1);
  }

  /* ================= COMMENT ADD ================= */

  async function handleAddComment(postId, content) {
    await addComment(postId, content, null, userId);

    setPosts((prev) =>
      prev.map((p) =>
        p.id === postId
          ? {
              ...p,
              comments: [
                ...p.comments,
                {
                  id: Date.now(),
                  content,
                  author: { username: "You" },
                  like_count: 0,
                  is_liked_by_user: false,
                },
              ],
            }
          : p,
      ),
    );

    setLeaderboardRefresh((k) => k + 1);
  }

  /* ================= COMMENT LIKE ================= */

  async function handleCommentLike(commentId) {
    await likeComment(commentId, userId);

    setPosts((prev) =>
      prev.map((p) => ({
        ...p,
        comments: p.comments.map((c) =>
          c.id === commentId
            ? {
                ...c,
                is_liked_by_user: true,
                like_count: (c.like_count || 0) + 1,
              }
            : c,
        ),
      })),
    );

    setLeaderboardRefresh((k) => k + 1);
  }

  return (
    <div className="space-y-6">
      {posts.map((post) => (
        <PostCard
          key={post.id}
          post={post}
          onLike={handlePostLike}
          onComment={handleAddComment}
          onLikeComment={handleCommentLike}
        />
      ))}
    </div>
  );
}
