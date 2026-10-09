-- Pass 24 — accounts v2: passkey or password, email only to confirm and recover.
-- Additive only. Applied with D1 tracked migrations:
--   npx wrangler d1 migrations apply under-book --remote
-- (export a backup first: npx wrangler d1 export under-book --remote --output=pre-0001.sql)

-- users: confirmation + optional password
ALTER TABLE users ADD COLUMN email_verified_at   INTEGER;  -- unix ms; NULL = unconfirmed (removed after 14 days)
ALTER TABLE users ADD COLUMN password_hash       TEXT;     -- versioned string, see _lib.js hashPassword; NULL = no password
ALTER TABLE users ADD COLUMN password_updated_at INTEGER;  -- unix ms

-- Only rows that provably clicked a link are confirmed: they hold a session
-- or a saved position. (The old flow created the user row on request, before
-- any click, so typos and addresses typed by others exist and stay unconfirmed.)
UPDATE users SET email_verified_at = created_at
 WHERE email_verified_at IS NULL
   AND (id IN (SELECT user_id FROM sessions) OR id IN (SELECT user_id FROM positions));
CREATE INDEX IF NOT EXISTS idx_users_unverified ON users(created_at) WHERE email_verified_at IS NULL;

-- login_tokens: purpose-tagged. 'verify' (24 h) | 'recover' (30 min).
-- Legacy rows default to 'login' and are treated as 'recover'.
ALTER TABLE login_tokens ADD COLUMN purpose TEXT NOT NULL DEFAULT 'login';
CREATE INDEX IF NOT EXISTS idx_login_tokens_expires ON login_tokens(expires_at);

-- Passkeys: one row per WebAuthn credential.
CREATE TABLE IF NOT EXISTS credentials (
  id           TEXT PRIMARY KEY,                 -- credential ID, base64url
  user_id      TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  public_key   BLOB NOT NULL,                    -- COSE public key
  counter      INTEGER NOT NULL DEFAULT 0,
  transports   TEXT,                             -- JSON array
  backed_up    INTEGER NOT NULL DEFAULT 0,       -- synced passkey
  name         TEXT,                             -- reader's label, <= 60 chars
  created_at   INTEGER NOT NULL,
  last_used_at INTEGER
);
CREATE INDEX IF NOT EXISTS idx_credentials_user ON credentials(user_id);

-- Single-use WebAuthn challenges, looked up by the hash of the challenge itself
-- (so two tabs never overwrite each other's ceremony).
CREATE TABLE IF NOT EXISTS webauthn_challenges (
  challenge_hash TEXT PRIMARY KEY,
  user_id        TEXT REFERENCES users(id) ON DELETE CASCADE,  -- NULL for sign-in
  purpose        TEXT NOT NULL,                                -- 'register' | 'login'
  created_at     INTEGER NOT NULL,
  expires_at     INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_wa_challenges_expires ON webauthn_challenges(expires_at);

-- Fixed-window counters (rate limits, once-a-day nudges). Keys hold hashes, never raw email/IP.
CREATE TABLE IF NOT EXISTS auth_attempts (
  key          TEXT PRIMARY KEY,
  window_start INTEGER NOT NULL,   -- unix ms
  count        INTEGER NOT NULL
);

-- Small key/value store (lazy-cleanup timestamp). value is an integer.
CREATE TABLE IF NOT EXISTS meta (
  key   TEXT PRIMARY KEY,
  value INTEGER NOT NULL
);
