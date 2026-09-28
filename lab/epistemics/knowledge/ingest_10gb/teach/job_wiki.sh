#!/bin/bash
# Wiki split (run 1): en1 fast-resume (skip 13942, start 13942) + en9/14/17/19/22/24/26/27,
# then consolidate -> stage/wiki_in, batched clean -> stage/wiki_run1.
# Zero RNG. Deterministic.
set -u
W=~/workspace/scratch_10gb_work
BZ=~/workspace/scratch_10gb/enwiki_20260901
OUT=$W/wiki_full
mkdir -p "$OUT"
echo "[wiki] en1 fast resume (skip 13942, start 13942)"
bzcat "$BZ/enwiki-20260901-pages-articles-multistream1.xml-p1p41242.bz2" 2>/dev/null | \
  python3 $W/split_wiki.py "$OUT" en1 50000 13942 13942
echo "[wiki] en1 rc=$? pages: $(ls $OUT/shard_00/wikipedia 2>/dev/null | wc -l)"
for k in 9 14 17 19 22 24 26 27; do
  f=$(ls "$BZ"/enwiki-20260901-pages-articles-multistream${k}.xml-*.bz2)
  echo "[wiki] splitting $f"
  bzcat "$f" 2>/dev/null | python3 $W/split_wiki.py "$OUT" "en$k" 50000
  echo "[wiki] en$k rc=$?"
done
echo "[wiki] consolidating to stage/wiki_in"
rm -rf $W/stage/wiki_in && mkdir -p $W/stage/wiki_in/wikipedia
find "$OUT" -path "*wikipedia/en*.xml" -print0 | while IFS= read -r -d '' f; do
  ln -sf "$f" $W/stage/wiki_in/wikipedia/$(basename $f)
done
N=$(ls $W/stage/wiki_in/wikipedia | wc -l)
echo "[wiki] consolidated: $N files"
PER=$(( (N + 9) / 10 ))
echo "[wiki] batched clean ($PER per subset)"
python3 $W/clean_batched.py $W/stage/wiki_in $W/stage/wiki_run1 $PER
echo "[wiki] clean rc=$?"
