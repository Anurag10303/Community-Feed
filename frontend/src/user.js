export function getCurrentUserId() {
  let userId = localStorage.getItem("user_id");

  if (!userId) {
    userId = Math.floor(Math.random() * 1000000).toString();
    localStorage.setItem("user_id", userId);
  }

  return userId;
}
