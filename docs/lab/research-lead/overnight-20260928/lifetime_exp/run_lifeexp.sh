#!/bin/bash
# run_lifeexp.sh: build, measure, and baseline the lifetime-experience test.
# Pure bash + znc + sqlite3. No Python.
set -u
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
D=docs/lab/research-lead/overnight-20260928/lifetime_exp
SQ=/tmp/lifeexp_sql
cd ~/workspace/tnn-rsi || exit 1

"$ZNC" "$D/lifeexp.zag" -o "$D/lifeexp_bin" 2> "$D/build.err"
if [ ! -x "$D/lifeexp_bin" ]; then echo "zag build failed"; exit 1; fi

for r in 1 2 3; do
  ./"$D/lifeexp_bin" run > "$D/LIFEXP_RAW_$r.txt" 2> "$D/LIFEXP_ERR_$r.txt"
done
echo "== zag stdout md5 (must match) =="
md5sum "$D"/LIFEXP_RAW_*.txt

rm -rf "$SQ" && mkdir -p "$SQ"
./"$D/lifeexp_bin" emit_sql "$SQ" || exit 1

ms_now() { date +%s%N; }
for r in 1 2 3; do
  DB="$SQ/life_$r.db"
  rm -f "$DB"
  s=$(ms_now); sqlite3 "$DB" < "$SQ/world.sql"; e=$(ms_now)
  t_ingest=$(( (e - s) / 1000000 ))
  # serious-baseline variant: single transaction around the same INSERTs
  DB2="$SQ/life_txn_$r.db"
  rm -f "$DB2"
  s=$(ms_now); { echo "BEGIN;"; cat "$SQ/world.sql"; echo "COMMIT;"; } | sqlite3 "$DB2"; e=$(ms_now)
  t_ingest_txn=$(( (e - s) / 1000000 ))
  s=$(ms_now); sqlite3 "$DB" < "$SQ/index.sql"; e=$(ms_now)
  t_index=$(( (e - s) / 1000000 ))
  s=$(ms_now); sqlite3 "$DB" < "$SQ/reabstract.sql"; e=$(ms_now)
  t_reabstract=$(( (e - s) / 1000000 ))
  s=$(ms_now); sqlite3 "$DB" < "$SQ/queries.sql" > "$SQ/sqlite_out_$r.txt" 2> "$SQ/sqlite_err_$r.txt"; e=$(ms_now)
  t_queries=$(( (e - s) / 1000000 ))
  echo "rep$r ingest_ms=$t_ingest ingest_txn_ms=$t_ingest_txn index_ms=$t_index reabstract_ms=$t_reabstract queries_ms=$t_queries"
  ls -la "$DB" | awk '{print "rep'$r' db_bytes="$5}'
done

echo "== sqlite outputs md5 (must match) =="
md5sum "$SQ"/sqlite_out_*.txt

# cross-check: zag query lines vs sqlite output
grep -E "^(Q1SUM|Q2_[0-9]+|Q3A_[0-9]+|Q3B_MATCH|Q4_[0-9]+) " "$D/LIFEXP_RAW_1.txt" | sed 's/ /|/' | sort > "$SQ/zag_q.txt"
sort "$SQ/sqlite_out_1.txt" > "$SQ/sql_q.txt"
if diff -q "$SQ/zag_q.txt" "$SQ/sql_q.txt" > /dev/null; then
  echo "CROSSCHECK rep1: all $(wc -l < "$SQ/zag_q.txt") query results match"
else
  echo "CROSSCHECK rep1: MISMATCH"; diff "$SQ/zag_q.txt" "$SQ/sql_q.txt" | head -20
fi
sort "$SQ/sqlite_out_2.txt" > "$SQ/sql_q2.txt"
sort "$SQ/sqlite_out_3.txt" > "$SQ/sql_q3.txt"
diff -q "$SQ/sql_q.txt" "$SQ/sql_q2.txt" && diff -q "$SQ/sql_q.txt" "$SQ/sql_q3.txt" && echo "sqlite reps 2,3 identical to rep1"
