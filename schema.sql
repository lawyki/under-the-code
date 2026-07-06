-- Under the Code — accounts + reading-position sync.
-- Apply with:
--   npx wrangler d1 execute under-book --local  --file=schema.sql   (dev)
--   npx wrangler d1 execute under-book --remote --file=schema.sql   (production)

CREATE TABLE IF NOT EXISTS users (
  id         TEXT PRIMARY KEY,             -- crypto.randomUUID()
  email      TEXT NOT NULL UNIQUE,         -- lowercased
  created_at INTEGER NOT NULL              -- unix ms
);

-- One-time magic-link tokens. Only the SHA-256 of the token is stored;
-- the plaintext lives solely in the emailed link. 15-minute expiry,
-- consumed (deleted) on first successful use.
CREATE TABLE IF NOT EXISTS login_tokens (
  token_hash TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  next_path  TEXT,                         -- same-origin path to return to
  created_at INTEGER NOT NULL,
  expires_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_login_tokens_user ON login_tokens(user_id);

-- Sessions. Same hashed-token scheme; 180-day expiry.
CREATE TABLE IF NOT EXISTS sessions (
  token_hash TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at INTEGER NOT NULL,
  expires_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);

-- One reading position per user — the whole point of the account.
CREATE TABLE IF NOT EXISTS positions (
  user_id    TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  data       TEXT NOT NULL,                -- JSON snapshot (part, anchor, fraction, labels)
  updated_at INTEGER NOT NULL
);
