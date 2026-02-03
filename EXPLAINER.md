# Community Feed – Engineering Explainer

This document explains the key technical decisions behind the Community Feed backend,
with a focus on data modeling, query efficiency, and correctness under concurrency.

---

## 1. Threaded Comments (The Tree)

### How comments are modeled

Threaded comments are modeled using an **adjacency list** approach.

Each comment has an optional `parent` foreign key pointing to another comment:

- `parent = NULL` → root comment
- `parent = comment_id` → reply to another comment

This keeps the schema simple and avoids complex recursive database structures.

### How the tree is fetched efficiently

To avoid the N+1 query problem, **all comments for a post are fetched in a single query**:

- Filtered by `post_id`
- Ordered by creation time
- `select_related("author")` to avoid extra queries

The comment tree is then constructed **in memory (Python)** by:

1. Creating a map of `comment_id → comment`
2. Attaching each comment to its parent’s `children` list
3. Returning only root comments

This guarantees:

- **Exactly one SQL query**, regardless of nesting depth
- Unlimited nesting
- Predictable performance

All tree-building logic lives in `selectors.py`, not in views or serializers.

---

## 2. Likes, Concurrency, and Karma

### Preventing double likes

Likes are stored in a dedicated `Like` table with **database-level unique constraints**:

- `(user, post)` must be unique
- `(user, comment)` must be unique

This ensures that even under concurrent requests, a user cannot like the same post
or comment more than once.

The database enforces correctness, not application logic.

### Atomic like handling

All like operations are handled inside **atomic transactions** in `services.py`.

On a successful like:

- A `Like` record is created
- A corresponding `KarmaEvent` is created

If the user already liked the target:

- The unique constraint raises an `IntegrityError`
- The transaction is rolled back
- No duplicate karma is awarded

Views remain thin and simply call service functions.

---

## 3. Karma Model and Leaderboard Math

### Why karma is event-based

Instead of storing counters on the User model, karma is tracked using an
**append-only `KarmaEvent` table**.

Each event records:

- The user receiving karma
- The number of points
- The timestamp

This design:

- Avoids synchronization bugs
- Makes time-based queries trivial
- Provides a full audit trail

### Leaderboard calculation (Last 24 Hours)

The leaderboard is calculated dynamically using aggregation:

- Filter `KarmaEvent` records from the last 24 hours
- Group by user
- Sum points
- Order descending
- Limit to top 5 users

This satisfies the requirement to avoid storing “daily karma” fields
while remaining efficient and correct.

All leaderboard logic lives in `selectors.py`.

---

## 4. AI Usage Audit

AI tools were used to accelerate boilerplate generation.

One specific issue encountered:

- AI suggested storing a `daily_karma` integer field on the User model
  for performance reasons.

This approach was rejected because:

- It violates the requirement to calculate karma dynamically
- It introduces race conditions and cache invalidation problems
- It breaks correctness when likes are retried or rolled back

The final implementation uses immutable `KarmaEvent` records
and real-time aggregation instead.

---

## 5. Architectural Separation

The backend follows strict separation of concerns:

- `models.py` → data schema only
- `services.py` → write logic and transactions
- `selectors.py` → read queries and aggregation
- `serializers.py` → JSON representation
- `views.py` → HTTP request/response glue

This keeps logic testable, debuggable, and scalable.
