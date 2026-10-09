-- Pass 25 — section marks (ledger §4y). Additive only. Applied with D1
-- tracked migrations:
--   npx wrangler d1 migrations apply under-book --local|--remote
-- (export a backup first: npx wrangler d1 export under-book --remote --output=pre-0002.sql)
-- Must be applied before the code that deletes from marks (auth/delete.js)
-- deploys. /api/marks stays off until MARKS_SYNC = "1" (wrangler.toml).

-- One coloured mark per (reader, section). A removed mark stays as a
-- tombstone (x = 1, last colour kept) so the reader's other devices learn of
-- the removal; tombstones older than 180 days are purged inside /api/marks
-- requests (Pages has no cron).
CREATE TABLE IF NOT EXISTS marks (
  user_id TEXT    NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  part    TEXT    NOT NULL,               -- 'part-1'..'part-5'
  a       TEXT    NOT NULL,               -- section id, e.g. 'ch4-vonneumann'
  c       INTEGER NOT NULL,               -- colour slot 1..5
  x       INTEGER NOT NULL DEFAULT 0,     -- 1 = removed (tombstone)
  t       INTEGER NOT NULL,               -- server time of the last change, unix ms; max(now, old t + 1)
  v       INTEGER NOT NULL,               -- per-user monotonic version; the sync cursor
  PRIMARY KEY (user_id, part, a)
);
CREATE INDEX IF NOT EXISTS idx_marks_user_v ON marks(user_id, v);
CREATE INDEX IF NOT EXISTS idx_marks_tombstones ON marks(t) WHERE x = 1;
