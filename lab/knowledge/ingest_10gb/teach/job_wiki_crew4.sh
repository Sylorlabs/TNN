#!/bin/bash
# Crew-4/5: sequential wiki splits for en14,17,19,22,24,26,27 + en1 resume.
# Run ONLY after PID 1880 (en9 split) has finished. SEQUENTIAL, low CPU.
# RESUME SAFETY (crew 5, 2026-09-24): each stem invocation computes its resume
# index via verify_split.py (highest contiguous well-formed file index from 0)
# and passes skip_n=start_n=<that>. Restarts scan past existing pages read-only
# and continue writing; a truncated last file from a mid-write kill is detected
# and rewritten (raw file-count resume would skip it forever).
# AFTER ANY KILL/RESTART just re-run this script; verification is built in.
# NOTE: run only ONE instance at a time (two concurrent instances double the
# load on this 2-vCPU box and interleave the log).
set -u
W=~/workspace/scratch_10gb_work
BZ=~/workspace/scratch_10gb/enwiki_20260901
OUT=$W/wiki_full
LOG=$W/logs/wiki_splits_crew4.log
cd "$W" || exit 1
echo "[wiki-crew4] start $(date -u)" | tee -a "$LOG"
for k in 14 17 19 22 24 26 27; do
  f=$(ls "$BZ"/enwiki-20260901-pages-articles-multistream${k}.xml-*.bz2)
  n=$(python3 $W/verify_split.py "$OUT" "en$k" 2>/dev/null | awk -F= '/^resume_index=/{print $2}')
  echo "[wiki-crew4] en$k: resume_index=$n, splitting $f" | tee -a "$LOG"
  bzcat "$f" 2>/dev/null | python3 $W/split_wiki.py "$OUT" "en$k" 50000 "$n" "$n" >> "$LOG" 2>&1
  echo "[wiki-crew4] en$k done rc=$? total: $(find "$OUT" -name "en${k}_n*.xml" -type f | wc -l)" | tee -a "$LOG"
done
# en1 resume: same verify-based resume.
N1=$(python3 $W/verify_split.py "$OUT" "en1" 2>/dev/null | awk -F= '/^resume_index=/{print $2}')
echo "[wiki-crew4] en1 resume: resume_index=$N1" | tee -a "$LOG"
bzcat "$BZ"/enwiki-20260901-pages-articles-multistream1.xml-p1p41242.bz2 2>/dev/null | python3 $W/split_wiki.py "$OUT" "en1" 50000 "$N1" "$N1" >> "$LOG" 2>&1
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
