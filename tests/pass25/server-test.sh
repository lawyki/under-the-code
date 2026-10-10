#!/usr/bin/env bash
# Pass 25 server test — /api/marks, /api/position (src/cid/seq), auth/delete.
# LOCAL ONLY: a fresh D1 in the scratch dir, wrangler pages dev on PORT.
# Re-runnable:  bash tests/pass25/server-test.sh
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd)
S=${UTC_SCRATCH:-${TMPDIR:-/tmp}/utc-pass25}; mkdir -p "$S"
W=${WRANGLER:-npx wrangler}
PORT=${PORT:-8798}
B=http://localhost:$PORT
STATE=$S/d1state
LOG=$S/pages-dev.log
PASS=0; FAIL=0; FAILS=()
SERVER_PID=

cd "$REPO" || exit 1

ok()   { PASS=$((PASS+1)); echo "  ok   $1"; }
bad()  { FAIL=$((FAIL+1)); FAILS+=("$1 :: $2"); echo "  FAIL $1 :: $2"; }
check(){ # name, condition-result(0/1), detail
  if [ "$2" = 0 ]; then ok "$1"; else bad "$1" "$3"; fi; }

sha() { printf '%s' "$1" | shasum -a 256 | cut -d' ' -f1; }
db_file() { ls "$STATE"/v3/d1/miniflare-D1DatabaseObject/*.sqlite 2>/dev/null | grep -v metadata | head -1; }
sql() { sqlite3 "$(db_file)" "$1"; }

new_user() { # id email token -> inserts user + fresh session
  local now; now=$(($(date +%s)*1000))
  sql "INSERT INTO users (id,email,created_at,email_verified_at) VALUES ('$1','$2',$now,$now);
       INSERT INTO sessions (token_hash,user_id,created_at,expires_at) VALUES ('$(sha "$3")','$1',$now,$((now+86400000)));"
}

# req METHOD PATH TOKEN BODY [ORIGIN]  -> sets CODE and BODY_OUT
req() {
  local origin=${5-$B}
  local args=(-s -o "$S/resp.json" -w '%{http_code}' -X "$1" "$B$2")
  [ -n "$3" ] && args+=(-H "Cookie: __Host-under_session=$3")
  [ -n "$origin" ] && args+=(-H "Origin: $origin")
  if [ -n "$4" ]; then args+=(-H 'Content-Type: application/json' --data-binary "$4"); fi
  CODE=$(curl "${args[@]}"); BODY_OUT=$(cat "$S/resp.json")
}
jq_() { node -e 'let d=JSON.parse(require("fs").readFileSync(0,"utf8")); const f=new Function("d","return ("+process.argv[1]+")"); const r=f(d); console.log(typeof r==="object"?JSON.stringify(r):r)' "$1" <<<"$BODY_OUT"; }

start_server() { # flag
  stop_server
  "$W" pages dev public --port "$PORT" --inspector-port 9339 --persist-to "$STATE" \
    --binding MARKS_SYNC="$1" --binding SITE_ORIGIN="$B" >"$LOG.$1" 2>&1 &
  SERVER_PID=$!
  for i in $(seq 1 60); do
    curl -s -o /dev/null "$B/api/position" && break; sleep 0.5
  done
}
stop_server() {
  if [ -n "$SERVER_PID" ]; then pkill -P "$SERVER_PID" 2>/dev/null; kill "$SERVER_PID" 2>/dev/null; wait "$SERVER_PID" 2>/dev/null; SERVER_PID=; fi
  # anything left on our port (workerd child)
  for p in $(lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null); do kill "$p" 2>/dev/null; done
}
trap stop_server EXIT

echo "wrangler: $W ($("$W" --version | tail -1))"
lsof -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1 && { echo "port $PORT busy"; exit 1; }

# ---- fresh local database ----
rm -rf "$STATE"
"$W" d1 execute under-book --local --persist-to "$STATE" --file=schema.sql >/dev/null 2>&1
CI=1 "$W" d1 migrations apply under-book --local --persist-to "$STATE" >/dev/null 2>&1
[ -n "$(db_file)" ] || { echo "no local db"; exit 1; }

TA=tokenAAAAAAAAAAAAAAAAAAAAAAAAAAAA
TB=tokenBBBBBBBBBBBBBBBBBBBBBBBBBBBB
TL=tokenLLLLLLLLLLLLLLLLLLLLLLLLLLLL
new_user u-alice alice@example.test "$TA"
new_user u-bob   bob@example.test   "$TB"
new_user u-limit lim@example.test   "$TL"

# =============================== MARKS_SYNC=1 ===============================
echo "== MARKS_SYNC=1"; start_server 1

echo "-- marks: guards"
req GET /api/marks "" ""; check "GET signed out -> 401" $([ "$CODE" = 401 ]; echo $?) "$CODE $BODY_OUT"
req POST /api/marks "" '{"v":1,"ops":[{"part":"part-1","a":"ch1-context","c":1}]}'; check "POST signed out -> 401" $([ "$CODE" = 401 ]; echo $?) "$CODE"
req POST /api/marks "$TA" '{"v":1,"ops":[{"part":"part-1","a":"ch1-context","c":1}]}' "https://evil.example"; check "POST bad origin -> 403" $([ "$CODE" = 403 ]; echo $?) "$CODE"
big=$(node -e 'console.log(JSON.stringify({v:1,ops:[{part:"part-1",a:"ch1-context",c:1}],pad:"x".repeat(8200)}))')
req POST /api/marks "$TA" "$big"; check "POST >8KB -> 413" $([ "$CODE" = 413 ]; echo $?) "$CODE"
for bodyname in 'not-json|{nope' 'array|[1]' 'null|null' 'v2|{"v":2,"ops":[{"part":"part-1","a":"ch1-context","c":1}]}' \
  'no-ops|{"v":1,"ops":[]}' 'ops-not-array|{"v":1,"ops":{}}' \
  'bad-part|{"v":1,"ops":[{"part":"part-6","a":"ch1-context","c":1}]}' \
  'bad-a|{"v":1,"ops":[{"part":"part-1","a":"fig-1-1","c":1}]}' \
  'bad-a-long|{"v":1,"ops":[{"part":"part-1","a":"ch1-'"$(printf 'x%.0s' $(seq 1 100))"'","c":1}]}' \
  'c6|{"v":1,"ops":[{"part":"part-1","a":"ch1-context","c":6}]}' \
  'c-float|{"v":1,"ops":[{"part":"part-1","a":"ch1-context","c":1.5}]}' \
  'c-string|{"v":1,"ops":[{"part":"part-1","a":"ch1-context","c":"1"}]}' \
  'client-t-only|{"v":1,"ops":[{"part":"part-1","a":"ch1-context"}]}'; do
  n=${bodyname%%|*}; b=${bodyname#*|}
  req POST /api/marks "$TA" "$b"; check "POST 400 $n" $([ "$CODE" = 400 ]; echo $?) "$CODE $BODY_OUT"
done
ops51=$(node -e 'console.log(JSON.stringify({v:1,ops:Array.from({length:51},(_,i)=>({part:"part-1",a:"ch1-s"+i,c:1}))}))')
req POST /api/marks "$TA" "$ops51"; check "POST 51 ops -> 400" $([ "$CODE" = 400 ]; echo $?) "$CODE"
cnt=$(sql "SELECT COUNT(*) FROM marks"); check "nothing written by rejected requests" $([ "$cnt" = 0 ]; echo $?) "count=$cnt"
req PUT /api/marks "$TA" ""; check "PUT -> 405" $([ "$CODE" = 405 ]; echo $?) "$CODE"

echo "-- marks: happy path"
req GET /api/marks "$TA" ""
check "GET empty -> 200" $([ "$CODE" = 200 ]; echo $?) "$CODE $BODY_OUT"
own=$(sha u-alice | cut -c1-16)
check "owner = sha256(id)[:16]" $([ "$(jq_ 'd.owner')" = "$own" ]; echo $?) "$(jq_ 'd.owner') vs $own"
check "empty: cursor 0, rows []" $([ "$(jq_ 'd.cursor+"/"+d.rows.length')" = "0/0" ]; echo $?) "$BODY_OUT"
req GET '/api/marks?since=abc' "$TA" ""; check "since invalid -> treated as 0" $([ "$CODE" = 200 ] && [ "$(jq_ 'd.cursor')" = 0 ]; echo $?) "$BODY_OUT"

req POST /api/marks "$TA" '{"v":1,"ops":[{"part":"part-1","a":"ch1-context","c":1},{"part":"part-1","a":"chBridge-mode","c":3},{"part":"part-4","a":"ch13-codd","c":5,"t":1}]}'
check "POST 3 ops -> 200" $([ "$CODE" = 200 ]; echo $?) "$CODE $BODY_OUT"
check "POST returns 3 rows" $([ "$(jq_ 'd.rows.length')" = 3 ]; echo $?) "$BODY_OUT"
check "rows carry part,a,c,x,t,v" $([ "$(jq_ 'd.rows.every(r=>["part","a","c","x","t","v"].every(k=>k in r))')" = true ]; echo $?) "$BODY_OUT"
check "versions distinct and increasing within one batch" $([ "$(jq_ 'd.rows[0].v<d.rows[1].v&&d.rows[1].v<d.rows[2].v')" = true ]; echo $?) "$BODY_OUT"
check "client-sent t ignored (server time)" $([ "$(jq_ 'd.rows[2].t>1e12')" = true ]; echo $?) "$BODY_OUT"
V1=$(jq_ 'd.rows[0].v'); V3=$(jq_ 'd.rows[2].v'); T1=$(jq_ 'd.rows[0].t')

req GET /api/marks "$TA" ""
check "GET all -> 3 rows ordered by v" $([ "$(jq_ 'd.rows.length===3&&d.rows[0].v<d.rows[1].v&&d.rows[1].v<d.rows[2].v')" = true ]; echo $?) "$BODY_OUT"
check "cursor = max v" $([ "$(jq_ 'd.cursor')" = "$V3" ]; echo $?) "$BODY_OUT"
req GET "/api/marks?since=$V1" "$TA" ""
check "since=v1 -> 2 rows" $([ "$(jq_ 'd.rows.length')" = 2 ]; echo $?) "$BODY_OUT"
req GET "/api/marks?since=$V3" "$TA" ""
check "since=cursor -> 0 rows, cursor unchanged" $([ "$(jq_ 'd.rows.length+"/"+d.cursor')" = "0/$V3" ]; echo $?) "$BODY_OUT"

echo "-- marks: same-ms writes cannot be skipped"
# Two marks in one batch share the same 'now' (same ms) but get distinct v.
req POST /api/marks "$TA" '{"v":1,"ops":[{"part":"part-2","a":"ch6-complexity","c":2},{"part":"part-2","a":"ch6-stroustrup","c":4}]}'
check "same-ms rows: same t floor, distinct v" $([ "$(jq_ 'd.rows[0].v!==d.rows[1].v')" = true ]; echo $?) "$BODY_OUT"
VA=$(jq_ 'd.rows[0].v')
req GET "/api/marks?since=$VA" "$TA" ""
check "cursor at the first same-ms row still returns the second" $([ "$(jq_ 'd.rows.length===1&&d.rows[0].a==="ch6-stroustrup"')" = true ]; echo $?) "$BODY_OUT"
# Simulate rows written in the same ms as a cursor taken earlier: force identical t and check versions still order them.
sql "UPDATE marks SET t = 1700000000000 WHERE user_id='u-alice' AND part='part-2'"
req GET "/api/marks?since=$VA" "$TA" ""
check "identical t does not hide rows (cursor is v)" $([ "$(jq_ 'd.rows.length')" = 1 ]; echo $?) "$BODY_OUT"

echo "-- marks: dedupe, recolour, t monotonic"
req POST /api/marks "$TA" '{"v":1,"ops":[{"part":"part-1","a":"ch1-context","c":2},{"part":"part-1","a":"ch1-context","c":4}]}'
check "dedupe keeps last op (c=4), one row" $([ "$(jq_ 'd.rows.length===1&&d.rows[0].c===4')" = true ]; echo $?) "$BODY_OUT"
# Push the stored t into the future (as if the server clock had been ahead): next write must still increase t.
FUT=$(( $(date +%s)*1000 + 3600000 ))
sql "UPDATE marks SET t = $FUT WHERE user_id='u-alice' AND a='ch1-context'"
req POST /api/marks "$TA" '{"v":1,"ops":[{"part":"part-1","a":"ch1-context","c":5}]}'
check "t = max(now, old.t+1) when stored t is ahead" $([ "$(jq_ 'd.rows[0].t')" = "$((FUT+1))" ]; echo $?) "$BODY_OUT"
VPREV=$(jq_ 'd.rows[0].v')
req POST /api/marks "$TA" '{"v":1,"ops":[{"part":"part-1","a":"ch1-context","c":1}]}'
check "t keeps increasing (+1 again)" $([ "$(jq_ 'd.rows[0].t')" = "$((FUT+2))" ]; echo $?) "$BODY_OUT"
check "v increases on every write" $([ "$(jq_ "d.rows[0].v>$VPREV")" = true ]; echo $?) "$BODY_OUT"

echo "-- marks: remove -> tombstone"
req GET /api/marks "$TA" ""; CUR=$(jq_ 'd.cursor')
req POST /api/marks "$TA" '{"v":1,"ops":[{"part":"part-1","a":"chBridge-mode","c":0}]}'
check "remove -> x=1, keeps last c (3)" $([ "$(jq_ 'd.rows[0].x===1&&d.rows[0].c===3')" = true ]; echo $?) "$BODY_OUT"
req GET "/api/marks?since=$CUR" "$TA" ""
check "tombstone visible to since" $([ "$(jq_ 'd.rows.length===1&&d.rows[0].a==="chBridge-mode"&&d.rows[0].x===1')" = true ]; echo $?) "$BODY_OUT"
req POST /api/marks "$TA" '{"v":1,"ops":[{"part":"part-3","a":"ch9-circuits","c":0}]}'
check "remove of unknown mark writes nothing (review: no unbounded tombstones)" $([ "$(jq_ 'd.rows.length')" = 0 ]; echo $?) "$BODY_OUT"
req POST /api/marks "$TA" '{"v":1,"ops":[{"part":"part-1","a":"chBridge-mode","c":2}]}'
check "re-mark revives tombstone (x=0,c=2)" $([ "$(jq_ 'd.rows[0].x===0&&d.rows[0].c===2')" = true ]; echo $?) "$BODY_OUT"

echo "-- marks: isolation between users"
req GET /api/marks "$TB" ""
check "bob sees none of alice's rows" $([ "$(jq_ 'd.rows.length')" = 0 ]; echo $?) "$BODY_OUT"
check "bob's owner differs" $([ "$(jq_ 'd.owner')" != "$own" ]; echo $?) "$BODY_OUT"

echo "-- marks: limit 250"
seed=""
# two real sections among the seeded 250 (recolour / swap need ids the book has)
seed="('u-limit','part-5','ch16-threads',1,0,1,1),('u-limit','part-5','ch16-races',1,0,1,2),"
for i in $(seq 3 250); do seed="$seed('u-limit','part-5','ch18-s$i',1,0,1,$i),"; done
sql "INSERT INTO marks (user_id,part,a,c,x,t,v) VALUES ${seed%,};"
req POST /api/marks "$TL" '{"v":1,"ops":[{"part":"part-5","a":"ch16-lockfree","c":2}]}'
check "mark 251 -> 409 mark_limit" $([ "$CODE" = 409 ] && [ "$(jq_ 'd.error+"/"+d.limit')" = "mark_limit/250" ]; echo $?) "$CODE $BODY_OUT"
check "409 applied nothing" $([ "$(sql "SELECT COUNT(*) FROM marks WHERE user_id='u-limit'")" = 250 ]; echo $?) "count"
req POST /api/marks "$TL" '{"v":1,"ops":[{"part":"part-5","a":"ch16-threads","c":3}]}'
check "recolour at the limit -> 200" $([ "$CODE" = 200 ]; echo $?) "$CODE $BODY_OUT"
req POST /api/marks "$TL" '{"v":1,"ops":[{"part":"part-5","a":"ch16-threads","c":0},{"part":"part-5","a":"ch16-lockfree","c":2}]}'
check "swap (remove one, add one) at the limit -> 200" $([ "$CODE" = 200 ]; echo $?) "$CODE $BODY_OUT"
check "still 250 live" $([ "$(sql "SELECT COUNT(*) FROM marks WHERE user_id='u-limit' AND x=0")" = 250 ]; echo $?) "count"
# Atomic guard: drop to 248 live, then 2 parallel POSTs each adding 2 new marks (each passes the pre-check alone).
sql "UPDATE marks SET x=1 WHERE user_id='u-limit' AND a IN ('ch16-races','ch18-s3')"
PIDS=(); for k in 1 2; do
  curl -s -o "$S/par$k.json" -w '%{http_code}\n' -X POST "$B/api/marks" -H "Cookie: __Host-under_session=$TL" -H "Origin: $B" \
    --data-binary "{\"v\":1,\"ops\":[{\"part\":\"part-4\",\"a\":\"$( [ $k = 1 ] && echo ch13-codd || echo ch13-sql )\",\"c\":1},{\"part\":\"part-4\",\"a\":\"$( [ $k = 1 ] && echo ch13-algebra || echo ch13-acid )\",\"c\":1}]}" > "$S/par$k.code" &
  PIDS+=($!); done; wait "${PIDS[@]}"
live=$(sql "SELECT COUNT(*) FROM marks WHERE user_id='u-limit' AND x=0")
check "parallel adds never exceed 250 (codes $(cat "$S"/par1.code) $(cat "$S"/par2.code))" $([ "$live" -le 250 ]; echo $?) "live=$live"

echo "-- marks: 180-day purge"
NOW=$(( $(date +%s)*1000 )); DAY=86400000
sql "INSERT INTO marks (user_id,part,a,c,x,t,v) VALUES
     ('u-bob','part-2','ch5-old181',1,1,$((NOW-181*DAY)),1),
     ('u-bob','part-2','ch5-old179',1,1,$((NOW-179*DAY)),2),
     ('u-bob','part-2','ch5-live300',1,0,$((NOW-300*DAY)),3);"
sql "DELETE FROM meta WHERE key='marks_purge'"
req GET /api/marks "$TB" ""
check "purge: 181-day tombstone gone" $([ "$(sql "SELECT COUNT(*) FROM marks WHERE a='ch5-old181'")" = 0 ]; echo $?) "still there"
check "purge: 179-day tombstone kept" $([ "$(sql "SELECT COUNT(*) FROM marks WHERE a='ch5-old179'")" = 1 ]; echo $?) "gone"
check "purge: old live mark kept" $([ "$(sql "SELECT COUNT(*) FROM marks WHERE a='ch5-live300'")" = 1 ]; echo $?) "gone"
# at most 100 per request
seed=""
for i in $(seq 1 130); do seed="$seed('u-bob','part-3','ch9-dead$i',1,1,$((NOW-200*DAY)),$((10+i))),"; done
sql "INSERT INTO marks (user_id,part,a,c,x,t,v) VALUES ${seed%,};"
req POST /api/marks "$TB" '{"v":1,"ops":[{"part":"part-3","a":"ch9-arpanet","c":1}]}'
left=$(sql "SELECT COUNT(*) FROM marks WHERE a LIKE 'ch9-dead%'")
check "POST also purges, at most 100 per request (30 left)" $([ "$left" = 30 ]; echo $?) "left=$left"
check "v after purge exceeds every v issued before" $([ "$(jq_ 'd.rows[0].v>140')" = true ]; echo $?) "$BODY_OUT"

echo "-- verification fixes (Sonnet 5.5)"
req POST /api/marks "$TA" '{"v":1,"ops":[{"part":"part-1","a":"ch1-nonexistent","c":1}]}'
check "a section the book does not have -> 400 bad_op" $([ "$CODE" = 400 ]; echo $?) "$CODE $BODY_OUT"
req POST /api/marks "$TA" '{"v":1,"ops":[{"part":"part-2","a":"ch1-context","c":1}]}'
check "a real id in the wrong part -> 400" $([ "$CODE" = 400 ]; echo $?) "$CODE $BODY_OUT"
req POST /api/marks "$TA" '{"v":1,"ops":[{"part":"part-1","a":"ch1-transistor","c":2}]}'
req POST /api/marks "$TA" '{"v":1,"ops":[{"part":"part-1","a":"ch1-transistor","c":0}]}'
T1=$(sql "SELECT t FROM marks WHERE user_id='u-alice' AND a='ch1-transistor'")
req POST /api/marks "$TA" '{"v":1,"ops":[{"part":"part-1","a":"ch1-transistor","c":0}]}'
T2=$(sql "SELECT t FROM marks WHERE user_id='u-alice' AND a='ch1-transistor'")
check "removing a removed mark writes nothing (tombstone clock not reset)" $([ "$(jq_ 'd.rows.length')" = 0 ] && [ "$T1" = "$T2" ]; echo $?) "$T1 vs $T2 $BODY_OUT"
sql "INSERT OR REPLACE INTO meta (key,value) VALUES ('marks_purge', $(( $(date +%s)*1000 )))"
CH=$(sql "SELECT total_changes()")
req GET /api/marks "$TA" ""
check "GET within the hour does not purge (no write)" $([ "$CODE" = 200 ]; echo $?) "$CODE"
req GET /api/position "$TA" ""
check "GET position carries the account tag" $([ "$(jq_ 'typeof d.owner==="string"&&d.owner.length===16')" = true ]; echo $?) "$BODY_OUT"
req POST /api/position "$TA" '{"part":"part-1","anchor":"ch1-kernel-p2","fraction":0.1}'
req DELETE /api/position "$TA" ""
check "DELETE position -> 204" $([ "$CODE" = 204 ]; echo $?) "$CODE"
req GET /api/position "$TA" ""
check "after DELETE the place is gone" $([ "$(jq_ 'd.position===null')" = true ]; echo $?) "$BODY_OUT"
req DELETE /api/position "" ""
check "DELETE signed out -> 401" $([ "$CODE" = 401 ]; echo $?) "$CODE"
req DELETE /api/position "$TA" "" "https://evil.example"
check "DELETE bad origin -> 403" $([ "$CODE" = 403 ]; echo $?) "$CODE"

echo "-- position: src/cid/seq (flag on)"
P='"part":"part-1","anchor":"ch1-context-p2","fraction":0.25,"section":"ch1-context"'
req POST /api/position "$TA" "{$P,\"src\":\"set\",\"cid\":\"abcd1234\",\"seq\":5}"
check "POST position with cid/seq -> 200, seq echoed" $([ "$CODE" = 200 ] && [ "$(jq_ 'd.ok&&d.seq===5&&d.updated_at>0')" = true ]; echo $?) "$CODE $BODY_OUT"
stored=$(sql "SELECT data FROM positions WHERE user_id='u-alice'")
check "src/cid/seq stored" $(node -e 'const d=JSON.parse(process.argv[1]); process.exit(d.src==="set"&&d.cid==="abcd1234"&&d.seq===5?0:1)' "$stored"; echo $?) "$stored"
UPD=$(sql "SELECT updated_at FROM positions WHERE user_id='u-alice'")
req POST /api/position "$TA" "{$P,\"fraction\":0.9,\"src\":\"auto\",\"cid\":\"abcd1234\",\"seq\":4}"
check "same cid older seq -> 409 stale with stored updated_at" $([ "$CODE" = 409 ] && [ "$(jq_ 'd.error+"/"+d.updated_at')" = "stale/$UPD" ]; echo $?) "$CODE $BODY_OUT"
req POST /api/position "$TA" "{$P,\"src\":\"auto\",\"cid\":\"abcd1234\",\"seq\":5}"
check "same cid equal seq -> 409" $([ "$CODE" = 409 ]; echo $?) "$CODE $BODY_OUT"
check "stale writes left the row untouched" $([ "$(sql "SELECT data FROM positions WHERE user_id='u-alice'")" = "$stored" ]; echo $?) "changed"
req POST /api/position "$TA" "{$P,\"src\":\"auto\",\"cid\":\"abcd1234\",\"seq\":6}"
check "same cid newer seq -> 200" $([ "$CODE" = 200 ] && [ "$(jq_ 'd.seq')" = 6 ]; echo $?) "$CODE $BODY_OUT"
req POST /api/position "$TA" "{$P,\"src\":\"set\",\"cid\":\"zzzz9999\",\"seq\":0}"
check "different cid (lower seq) overwrites -> 200" $([ "$CODE" = 200 ]; echo $?) "$CODE $BODY_OUT"
check "stored cid now zzzz9999" $([ "$(sql "SELECT json_extract(data,'\$.cid') FROM positions WHERE user_id='u-alice'")" = zzzz9999 ]; echo $?) "x"
req POST /api/position "$TA" "{$P}"
check "no cid (old client) always writes -> 200, no seq echoed" $([ "$CODE" = 200 ] && [ "$(jq_ '"seq" in d')" = false ]; echo $?) "$CODE $BODY_OUT"
req POST /api/position "$TA" "{$P,\"src\":\"pinned\",\"cid\":\"BAD!\",\"seq\":-1}"
stored=$(sql "SELECT data FROM positions WHERE user_id='u-alice'")
check "invalid src/cid/seq ignored, not stored" $([ "$CODE" = 200 ] && node -e 'const d=JSON.parse(process.argv[1]); process.exit(!("src" in d)&&!("cid" in d)&&!("seq" in d)?0:1)' "$stored"; echo $?) "$CODE $stored"
req POST /api/position "$TA" "{$P,\"cid\":\"abcd1234\",\"seq\":1}"
check "after a cid-less write, any cid writes" $([ "$CODE" = 200 ]; echo $?) "$CODE $BODY_OUT"
req POST /api/position "$TB" "{$P,\"cid\":\"bobbob12\",\"seq\":3}"
check "first write for a user (insert) -> 200" $([ "$CODE" = 200 ] && [ "$(jq_ 'd.seq')" = 3 ]; echo $?) "$CODE $BODY_OUT"
req GET /api/position "$TA" ""
check "GET position still works" $([ "$CODE" = 200 ] && [ "$(jq_ 'd.position.part')" = part-1 ]; echo $?) "$CODE $BODY_OUT"

echo "-- auth/delete removes marks"
cntA=$(sql "SELECT COUNT(*) FROM marks WHERE user_id='u-alice'")
req POST /api/auth/delete "$TA" ""
check "delete -> 200" $([ "$CODE" = 200 ]; echo $?) "$CODE $BODY_OUT"
check "alice's marks gone (had $cntA)" $([ "$(sql "SELECT COUNT(*) FROM marks WHERE user_id='u-alice'")" = 0 ] && [ "$cntA" -gt 0 ]; echo $?) "left"
check "alice's user row gone" $([ "$(sql "SELECT COUNT(*) FROM users WHERE id='u-alice'")" = 0 ]; echo $?) "left"
check "bob's marks untouched" $([ "$(sql "SELECT COUNT(*) FROM marks WHERE user_id='u-bob'")" -gt 0 ]; echo $?) "gone"
req POST /api/auth/delete "$TL" ""
check "delete works for a user with 250+ rows" $([ "$CODE" = 200 ] && [ "$(sql "SELECT COUNT(*) FROM marks WHERE user_id='u-limit'")" = 0 ]; echo $?) "$CODE"

stop_server

# =============================== MARKS_SYNC=0 ===============================
echo "== MARKS_SYNC=0"; start_server 0
TC=tokenCCCCCCCCCCCCCCCCCCCCCCCCCCCC
new_user u-carol carol@example.test "$TC"
for m in GET POST PUT DELETE; do
  req $m /api/marks "" ""
  check "flag 0: $m signed out -> 404 disabled" $([ "$CODE" = 404 ] && [ "$(jq_ 'd.error')" = disabled ]; echo $?) "$CODE $BODY_OUT"
done
req GET /api/marks "$TC" ""; check "flag 0: GET signed in -> 404" $([ "$CODE" = 404 ]; echo $?) "$CODE"
req POST /api/marks "$TC" '{"v":1,"ops":[{"part":"part-1","a":"ch1-context","c":1}]}' "https://evil.example"
check "flag 0: POST bad origin -> 404 (gate first)" $([ "$CODE" = 404 ]; echo $?) "$CODE"
req POST /api/position "$TC" "{$P,\"src\":\"set\",\"cid\":\"abcd1234\",\"seq\":5}"
check "flag 0: position POST -> {ok,updated_at} only" $([ "$CODE" = 200 ] && [ "$(jq_ 'Object.keys(d).join()')" = "ok,updated_at" ]; echo $?) "$CODE $BODY_OUT"
stored=$(sql "SELECT data FROM positions WHERE user_id='u-carol'")
check "flag 0: src/cid/seq not stored" $(node -e 'const d=JSON.parse(process.argv[1]); process.exit(!("src" in d)&&!("cid" in d)&&!("seq" in d)?0:1)' "$stored"; echo $?) "$stored"
req POST /api/position "$TC" "{$P,\"cid\":\"abcd1234\",\"seq\":1}"
check "flag 0: no stale check (older seq still 200)" $([ "$CODE" = 200 ]; echo $?) "$CODE $BODY_OUT"
req POST /api/position "$TC" "$(node -e 'console.log(JSON.stringify({part:"part-1",anchor:"x1",fraction:0.1,pad:"y".repeat(2100)}))')"
check "flag 0: 413 unchanged" $([ "$CODE" = 413 ]; echo $?) "$CODE"
req POST /api/position "$TC" '{"part":"part-9","anchor":"a","fraction":0}'
check "flag 0: 400 bad_part unchanged" $([ "$CODE" = 400 ] && [ "$(jq_ 'd.error')" = bad_part ]; echo $?) "$CODE"
req POST /api/position "$TC" "{$P}" "https://evil.example"
check "flag 0: 403 bad origin unchanged" $([ "$CODE" = 403 ]; echo $?) "$CODE"
req POST /api/position "" "{$P}"
check "flag 0: 401 signed out unchanged" $([ "$CODE" = 401 ]; echo $?) "$CODE"
# delete.js works with the flag off as long as the table exists
req POST /api/auth/delete "$TB" ""
check "flag 0: delete still removes marks" $([ "$CODE" = 200 ] && [ "$(sql "SELECT COUNT(*) FROM marks WHERE user_id='u-bob'")" = 0 ]; echo $?) "$CODE"
stop_server

echo
echo "PASS $PASS  FAIL $FAIL"
for f in "${FAILS[@]+"${FAILS[@]}"}"; do echo "  - $f"; done
[ "$FAIL" = 0 ]
