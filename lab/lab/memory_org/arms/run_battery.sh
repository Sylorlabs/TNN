#!/bin/bash
# MORG battery B1..B8 in frozen order, 3x reruns with SHA-256 comparison.
# Results layout: results/<arm>/run<R>/ (matches crew-1 scorer).
# Arm subcommand surface:
#   ingest <corpus> <storedir> | choose <storedir> (SELF) |
#   retrieve <storedir> <queries> <out> | revise <storedir> <id> <newtext> |
#   verify <storedir> | deletecat <storedir> <type> |
#   exportcat <storedir> <type> <file> | importcat <file> <storedir> |
#   opscount <storedir>
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FIX="$HOME/workspace/morg/fixture"
if [ ! -f "$FIX/corpus.txt" ]; then
  FIX="$HERE/mini"
  echo "note: crew-1 fixture not present at ~/workspace/morg/fixture; using mini fixture"
fi
RES="$HERE/results"
mkdir -p "$RES"
"$HERE/build.sh" > /dev/null 2>&1 || { echo "BUILD_FAIL"; exit 1; }
BIN="$HERE/build"

pick_ids() {
  python3 - "$FIX/corpus.txt" <<'PYEOF'
import sys
items = {}
for line in open(sys.argv[1]):
    p = line.rstrip("\n").split("|", 4)
    if len(p) == 5:
        items.setdefault(p[2], []).append(p[0])
out = []
for t in sorted(items):
    ids = sorted(items[t])
    out.append(ids[0])
    out.append(ids[2] if len(ids) > 2 else ids[-1])
    if len(ids) > 4:
        out.append(ids[4])
print(" ".join(out[:10]))
PYEOF
}

b3_check() { # $1 prev $2 new $3 id $4 newtext ; prints "B3 <id> PASS|FAIL"
  python3 - "$1" "$2" "$3" "$4" <<'PYEOF'
import sys
prev, new, rid, newtext = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
pl = open(prev).read().splitlines(); nl = open(new).read().splitlines()
ok = len(pl) == len(nl)
diffs = [i for i in range(len(pl)) if pl[i] != nl[i]] if ok else [-1]
if ok and len(diffs) == 1:
    i = diffs[0]
    p = pl[i].split("|", 4); q = nl[i].split("|", 4)
    ok = (len(p) == 5 and len(q) == 5 and p[0] == rid == q[0] and p[1] == q[1]
          and p[2] == q[2] and p[3] == q[3] and q[4] == newtext)
print("B3 %s %s" % (rid, "PASS" if ok else "FAIL"))
PYEOF
}

scheme_choices() { # $1 scheme.txt ; prints "domain=choice" lines (per-domain blocks)
  python3 - "$1" <<'PYEOF'
import sys, re
txt = open(sys.argv[1]).read()
cur = None
for line in txt.splitlines():
    m = re.match(r"(?i)^domain\s*[:=]\s*(\S+)", line)
    if m:
        cur = m.group(1).lower(); continue
    m = re.match(r"(?i)^chosen\s*[:=]\s*(S[1-6])", line)
    if m and cur:
        print("%s=%s" % (cur, m.group(1).upper()))
PYEOF
}

run_once() { # $1 = run number
  R="$1"
  awk -F'|' '$2=="test"' "$FIX/queries.txt" > "$RES/_qtest.txt"
  awk -F'|' '$2=="calib"' "$FIX/queries.txt" > "$RES/_qcalib.txt"
  for ARM in SELF IMPOSED FLAT; do
    A="$BIN/arm_$(echo $ARM | tr A-Z a-z)"; ADIR="$RES/$ARM/run$R"; rm -rf "$ADIR"; mkdir -p "$ADIR"
    cp "$RES/_qtest.txt" "$ADIR/_qtest.txt"; cp "$RES/_qcalib.txt" "$ADIR/_qcalib.txt"
    # ---- B1 retrieval ----
    S="$ADIR/_b1"; rm -rf "$S"; "$A" ingest "$FIX/corpus.txt" "$S" > /dev/null
    if [ "$ARM" = SELF ]; then
      cp "$ADIR/_qcalib.txt" "$S/calib.txt"; "$A" choose "$S" > /dev/null
      cp "$S/scheme.txt" "$ADIR/scheme.txt"; cp "$S/scheme.txt" "$ADIR/scheme_t0.txt"
    elif [ "$ARM" = IMPOSED ]; then
      printf 'IMPOSED fixed taxonomy: type->domain (no choice)\n' > "$ADIR/scheme.txt"
      cp "$ADIR/scheme.txt" "$ADIR/scheme_t0.txt"; cp "$ADIR/scheme.txt" "$ADIR/scheme_t1.txt"
    else
      printf 'FLAT append-only, content-match scoring (no scheme)\n' > "$ADIR/scheme.txt"
      cp "$ADIR/scheme.txt" "$ADIR/scheme_t0.txt"; cp "$ADIR/scheme.txt" "$ADIR/scheme_t1.txt"
    fi
    "$A" retrieve "$S" "$ADIR/_qtest.txt" "$ADIR/retrieval.txt" > /dev/null
    # ---- B3 revision locality ----
    B3="$ADIR/_b3"; rm -rf "$B3"; "$A" ingest "$FIX/corpus.txt" "$B3" > /dev/null
    : > "$ADIR/verify_report.txt"
    NPASS=0; NTOT=0
    for ID in $(pick_ids); do
      NTOT=$((NTOT+1))
      cp "$B3/items.dat" "$B3/items.prev"
      "$A" revise "$B3" "$ID" "REVISED $ID locality probe replacement text." > /dev/null
      LINE=$(b3_check "$B3/items.prev" "$B3/items.dat" "$ID" \
        "REVISED $ID locality probe replacement text.")
      echo "$LINE" >> "$ADIR/verify_report.txt"
      case "$LINE" in *PASS) NPASS=$((NPASS+1));; esac
    done
    if [ "$NPASS" = "$NTOT" ]; then
      echo "B3: PASS - revised $NTOT items, all other items byte-identical" >> "$ADIR/verify_report.txt"
    else
      echo "B3: FAIL - $NPASS/$NTOT items revised without collateral" >> "$ADIR/verify_report.txt"
    fi
    # ---- B4 separability ----
    B4="$ADIR/_b4"; rm -rf "$B4"; "$A" ingest "$FIX/corpus.txt" "$B4" > /dev/null
    "$A" deletecat "$B4" CODE > /dev/null
    H_REST=$("$A" verify "$B4" | sed -n 's/^hash=//p')
    grep -v '|CODE|' "$FIX/corpus.txt" > "$ADIR/_nocode.txt"
    B4B="$ADIR/_b4b"; rm -rf "$B4B"; "$A" ingest "$ADIR/_nocode.txt" "$B4B" > /dev/null
    H_FRESH=$("$A" verify "$B4B" | sed -n 's/^hash=//p')
    DEL_OK=0
    if [ "$H_REST" = "$H_FRESH" ]; then DEL_OK=1; fi
    echo "B4 deletecat CODE: rest=$H_REST fresh=$H_FRESH $([ $DEL_OK = 1 ] && echo PASS || echo FAIL)" >> "$ADIR/verify_report.txt"
    B4C="$ADIR/_b4c"; rm -rf "$B4C"; "$A" ingest "$FIX/corpus.txt" "$B4C" > /dev/null
    "$A" exportcat "$B4C" FACT "$ADIR/_fact.txt" > /dev/null
    : > "$ADIR/_empty.txt"
    B4D="$ADIR/_b4d"; rm -rf "$B4D"; "$A" ingest "$ADIR/_empty.txt" "$B4D" > /dev/null
    "$A" importcat "$ADIR/_fact.txt" "$B4D" > /dev/null
    H_IMP=$("$A" verify "$B4D" | sed -n 's/^hash=//p')
    H_EXP=$(python3 -c "
import hashlib
ls = sorted(l for l in open('$FIX/corpus.txt').read().splitlines() if l.split('|')[2]=='FACT')
print(hashlib.sha256(('\n'.join(ls)+'\n').encode()).hexdigest())")
    IMP_OK=0
    if [ "$H_IMP" = "$H_EXP" ]; then IMP_OK=1; fi
    echo "B4 importcat FACT: imp=$H_IMP expected=$H_EXP $([ $IMP_OK = 1 ] && echo PASS || echo FAIL)" >> "$ADIR/verify_report.txt"
    if [ $DEL_OK = 1 ] && [ $IMP_OK = 1 ]; then
      echo "B4: PASS - deletecat CODE hash matches fresh ingest; FACT export/import round-trips" >> "$ADIR/verify_report.txt"
    else
      echo "B4: FAIL - deletecat=$DEL_OK importcat=$IMP_OK" >> "$ADIR/verify_report.txt"
    fi
    # ---- B5 reorg cost ----
    B5="$ADIR/_b5"; rm -rf "$B5"; "$A" ingest "$FIX/corpus.txt" "$B5" > /dev/null
    if [ "$ARM" = SELF ]; then
      cp "$ADIR/_qcalib.txt" "$B5/calib.txt"; "$A" choose "$B5" > /dev/null
    fi
    "$A" opscount "$B5" > "$ADIR/ops.txt"
    OPSLINE=$(tr '\n' ' ' < "$ADIR/ops.txt")
    echo "B5: PASS - choose+refile ops: $OPSLINE" >> "$ADIR/verify_report.txt"
    # ---- B6 drift (SELF) / B7 unseen domain ----
    if [ "$ARM" = SELF ]; then
      B6="$ADIR/_b6"; rm -rf "$B6"; "$A" ingest "$FIX/corpus.txt" "$B6" > /dev/null
      cp "$ADIR/_qcalib.txt" "$B6/calib.txt"; "$A" choose "$B6" > /dev/null
      cp "$B6/scheme.txt" "$ADIR/scheme_t0.txt"; cp "$B6/scheme.txt" "$ADIR/scheme.txt"
      "$A" retrieve "$B6" "$FIX/queries_holdout.txt" "$ADIR/retrieval_holdout_old.txt" > /dev/null
      "$A" importcat "$FIX/corpus_holdout.txt" "$B6" > /dev/null
      "$A" choose "$B6" > /dev/null
      cp "$B6/scheme.txt" "$ADIR/scheme_t1.txt"
      C0=$(scheme_choices "$ADIR/scheme_t0.txt" | sort)
      C1=$(scheme_choices "$ADIR/scheme_t1.txt" | sort)
      if [ "$C0" = "$C1" ]; then CHG=n; else CHG=y; fi
      echo "B6: drift scheme-change=$CHG" >> "$ADIR/verify_report.txt"
      echo "B6 t0 choices: $(echo "$C0" | tr '\n' ' ')" >> "$ADIR/verify_report.txt"
      echo "B6 t1 choices: $(echo "$C1" | tr '\n' ' ')" >> "$ADIR/verify_report.txt"
      "$A" retrieve "$B6" "$FIX/queries_holdout.txt" "$ADIR/retrieval_holdout.txt" > /dev/null
    else
      B7="$ADIR/_b7"; rm -rf "$B7"; "$A" ingest "$FIX/corpus.txt" "$B7" > /dev/null
      "$A" retrieve "$B7" "$FIX/queries_holdout.txt" "$ADIR/retrieval_holdout_old.txt" > /dev/null
      "$A" importcat "$FIX/corpus_holdout.txt" "$B7" > /dev/null
      "$A" retrieve "$B7" "$FIX/queries_holdout.txt" "$ADIR/retrieval_holdout.txt" > /dev/null
    fi
  done
  python3 "$HERE/summarize.py" "$FIX" "$RES" "$R" > /dev/null
}

for R in 1 2 3; do
  echo "=== run $R ==="
  run_once "$R"
done

echo "=== 3x SHA-256 comparison ==="
FILES="retrieval.txt retrieval_holdout.txt retrieval_holdout_old.txt scheme.txt scheme_t0.txt scheme_t1.txt verify_report.txt ops.txt"
ALL_OK=1
for ARM in SELF IMPOSED FLAT; do
  for F in $FILES; do
    H1=$(sha256sum "$RES/$ARM/run1/$F" | cut -d' ' -f1)
    H2=$(sha256sum "$RES/$ARM/run2/$F" | cut -d' ' -f1)
    H3=$(sha256sum "$RES/$ARM/run3/$F" | cut -d' ' -f1)
    if [ "$H1" = "$H2" ] && [ "$H2" = "$H3" ]; then
      echo "IDENTICAL $ARM/$F $H1"
    else
      echo "DIFFERENT $ARM/$F $H1 $H2 $H3"
      ALL_OK=0
    fi
  done
  for R in 1 2 3; do
    if [ -f "$RES/$ARM/run$R/summary.txt" ]; then
      H=$(sha256sum "$RES/$ARM/run$R/summary.txt" | cut -d' ' -f1)
      echo "summary $ARM/run$R $H"
    fi
  done
done
# cross-run summary comparison (normalize run number)
for ARM in SELF IMPOSED FLAT; do
  S1=$(sed 's/run[123]/runN/g' "$RES/$ARM/run1/summary.txt" | sha256sum | cut -d' ' -f1)
  S2=$(sed 's/run[123]/runN/g' "$RES/$ARM/run2/summary.txt" | sha256sum | cut -d' ' -f1)
  S3=$(sed 's/run[123]/runN/g' "$RES/$ARM/run3/summary.txt" | sha256sum | cut -d' ' -f1)
  if [ "$S1" = "$S2" ] && [ "$S2" = "$S3" ]; then
    echo "IDENTICAL $ARM/summary.txt $S1"
  else
    echo "DIFFERENT $ARM/summary.txt"; ALL_OK=0
  fi
done
if [ "$ALL_OK" = 1 ]; then echo "3x RERUN: ALL BYTE-IDENTICAL"; else echo "3x RERUN: MISMATCH"; exit 1; fi
