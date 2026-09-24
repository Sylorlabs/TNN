#!/bin/bash
# Crew-4: sequential wiki splits for en14,17,19,22,24,26,27 + en1 resume.
# Run ONLY after PID 1880 (en9 split) has finished. SEQUENTIAL, low CPU.
set -u
W=~/workspace/scratch_10gb_work
BZ=~/workspace/scratch_10gb/enwiki_20260901
OUT=$W/wiki_full
LOG=$W/logs/wiki_splits_crew4.log
cd "$W" || exit 1
echo "[wiki-crew4] start $(date -u)" | tee -a "$LOG"
for k in 14 17 19 22 24 26 27; do
  f=$(ls "$BZ"/enwiki-20260901-pages-articles-multistream${k}.xml-*.bz2)
  n=$(find "$OUT" -name "en${k}_n*.xml" -type f | wc -l)
  echo "[wiki-crew4] en$k: have $n pages, splitting $f" | tee -a "$LOG"
  bzcat "$f" 2>/dev/null | python3 $W/split_wiki.py "$OUT" "en$k" 50000 >> "$LOG" 2>&1
  echo "[wiki-crew4] en$k done rc=$? total: $(find "$OUT" -name "en${k}_n*.xml" -type f | wc -l)" | tee -a "$LOG"
done
# en1 resume: 13942 files exist; skip first 13942 pages, number from 13942.
echo "[wiki-crew4] en1 resume: existing $(find "$OUT" -name 'en1_n*.xml' -type f | wc -l)" | tee -a "$LOG"
bzcat "$BZ"/enwiki-20260901-pages-articles-multistream1.xml-p1p41242.bz2 2>/dev/null | python3 $W/split_wiki.py "$OUT" "en1" 50000 13942 13942 >> "$LOG" 2>&1
echo "[wiki-crew4] en1 resume done rc=$? total: $(find "$OUT" -name 'en1_n*.xml' -type f | wc -l)" | tee -a "$LOG"
echo "[wiki-crew4] consolidating to stage/wiki_in" | tee -a "$LOG"
rm -rf $W/stage/wiki_in && mkdir -p $W/stage/wiki_in/wikipedia
find "$OUT" -path "*wikipedia/en*.xml" -print0 | while IFS= read -r -d '' f; do
  ln -sf "$f" $W/stage/wiki_in/wikipedia/$(basename $f)
done
N=$(ls $W/stage/wiki_in/wikipedia | wc -l)
echo "[wiki-crew4] consolidated: $N files" | tee -a "$LOG"
PER=$(( (N + 9) / 10 ))
echo "[wiki-crew4] batched clean ($PER per subset) -> stage/wiki_run1" | tee -a "$LOG"
python3 $W/clean_batched.py $W/stage/wiki_in $W/stage/wiki_run1 $PER >> "$LOG" 2>&1
echo "[wiki-crew4] clean rc=$? facts: $(ls $W/stage/wiki_run1/facts.dat 2>/dev/null && echo ok)" | tee -a "$LOG"
echo "[wiki-crew4] end $(date -u)" | tee -a "$LOG"
