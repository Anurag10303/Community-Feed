const BASE_URL = import.meta.env.VITE_API_BASE_URL?.trim();
if (!BASE_URL) {
  throw new Error("VITE_API_BASE_URL is not defined");
}

/* ===================== FEED ===================== */

export async function fetchFeed(userId = 1) {
  const res = await fetch(`${BASE_URL}/feed/?user_id=${userId}`);
  if (!res.ok) throw new Error("Failed to fetch feed");
  return res.json();
}

export async function fetchPost(postId, userId = 1) {
  const res = await fetch(`${BASE_URL}/feed/${postId}/?user_id=${userId}`);
  if (!res.ok) throw new Error("Failed to fetch post");
  return res.json();
}

export async function likeComment(commentId, userId) {
  const res = await fetch(`${BASE_URL}/api/comments/${commentId}/like/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Comment like failed");
  }

  return res.json();
}

/* ===================== LIKES ===================== */

export async function likePost(postId, userId = 1) {
  const res = await fetch(`${BASE_URL}/feed/${postId}/like/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Like failed");
  }

  return res.json();
}

/* ===================== COMMENTS ===================== */

export async function addComment(postId, content, parentId = null, userId = 1) {
  const res = await fetch(`${BASE_URL}/feed/${postId}/comment/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      content,
      parent_id: parentId,
      user_id: userId,
    }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Comment failed");
  }

  return res.json();
}

/* ===================== LEADERBOARD ===================== */

export async function fetchLeaderboard() {
  const res = await fetch(`${BASE_URL}/feed/leaderboard/`);
  if (!res.ok) throw new Error("Failed to fetch leaderboard");
  return res.json();
}
