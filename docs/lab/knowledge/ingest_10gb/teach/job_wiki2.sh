#!/bin/bash
# Wiki splits for en9-en27 (en1 already done: 25,232 pages).
# Then consolidate -> stage/wiki_in, batched clean -> stage/wiki_run1.
set -u
W=~/workspace/scratch_10gb_work
BZ=~/workspace/scratch_10gb/enwiki_20260901
OUT=$W/wiki_full
for k in 9 14 17 19 22 24 26 27; do
  f=$(ls "$BZ"/enwiki-20260901-pages-articles-multistream${k}.xml-*.bz2)
  echo "[wiki] splitting $f"
  bzcat "$f" 2>/dev/null | python3 $W/split_wiki.py "$OUT" "en$k" 50000
  echo "[wiki] en$k rc=$? total pages: $(find $OUT -name "en*.xml" | wc -l)"
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
