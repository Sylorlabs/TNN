#!/bin/zsh
set -u

ROOT=${0:A:h:h:h:h}
OUT=${1:-"$ROOT/Research/R33_NATIVE_N17_R27_CONTINUITY/V91_SEMANTIC_KAT/AGENT_FRONTIER_20260915"}
mkdir -p "$OUT"

TERMS='MotifGenerator|_build_semantic_dataset|build_semantic_dataset|multinomial|manual_seed|Generator\(|GRU|bpe|BPE|merge|tokenizer|condition_dim|condition.*42|train_n|test_n|1800|1872|semantic.*dataset|sampling|sample\('

RGOUT="$OUT/repository_text_hits.txt"
ARCHIVES="$OUT/archives.txt"
AHITS="$OUT/archive_text_hits.txt"
ERRORS="$OUT/errors.log"

: > "$RGOUT"
: > "$ARCHIVES"
: > "$AHITS"
: > "$ERRORS"

rg -n -i -S --glob '!*.pkl' --glob '!*.bin' --glob '!*.mp4' --glob '!*.mov' --glob '!*.zip' --glob '!*.tar' --glob '!*.tar.gz' --glob '!*.tgz' "$TERMS" "$ROOT/Research" > "$RGOUT" 2>>"$ERRORS" || true

{
  find "$ROOT/Research" -type f \( -name '*.tar' -o -name '*.tar.gz' -o -name '*.tgz' -o -name '*.zip' \) -print 2>/dev/null
  if [[ -d /Users/Shared/micah/Documents/Codex ]]; then
    find /Users/Shared/micah/Documents/Codex -type f \( -name '*.tar' -o -name '*.tar.gz' -o -name '*.tgz' -o -name '*.zip' \) -print 2>/dev/null
  fi
} | LC_ALL=C sort -u > "$ARCHIVES"

text_member() {
  local lower=${1:l}
  case "$lower" in
    *.py|*.zag|*.md|*.txt|*.json|*.toml|*.yaml|*.yml|*.csv|*.tsv) return 0 ;;
    *) return 1 ;;
  esac
}

while IFS= read -r archive; do
  [[ -n "$archive" ]] || continue
  type=tar
  [[ "$archive" == *.zip ]] && type=zip
  if [[ "$type" == zip ]]; then
    members=$(unzip -Z1 "$archive" 2>>"$ERRORS") || continue
  else
    members=$(tar -tf "$archive" 2>>"$ERRORS") || continue
  fi
  while IFS= read -r member; do
    [[ -n "$member" ]] || continue
    text_member "$member" || continue
    if [[ "$type" == zip ]]; then
      hits=$(unzip -p "$archive" "$member" 2>>"$ERRORS" | rg -n -i -m 80 "$TERMS" 2>/dev/null) || true
    else
      hits=$(tar -xOf "$archive" "$member" 2>>"$ERRORS" | rg -n -i -m 80 "$TERMS" 2>/dev/null) || true
    fi
    if [[ -n "$hits" ]]; then
      print -r -- "===== $archive :: $member =====" >> "$AHITS"
      print -r -- "$hits" >> "$AHITS"
    fi
  done <<< "$members"
done < "$ARCHIVES"

repo_hits=$(wc -l < "$RGOUT" | tr -d ' ')
archive_sections=$(rg -c '^===== ' "$AHITS" 2>/dev/null || echo 0)
archive_count=$(wc -l < "$ARCHIVES" | tr -d ' ')

cat > "$OUT/SCAN_RECEIPT.txt" <<EOF
repository_hit_lines=$repo_hits
archives_scanned=$archive_count
archive_members_with_hits=$archive_sections
python_executed=false
pickle_executed=false
foreign_ml_runtime_used=false
historical_python_treated_as_text_only=true
EOF

print -r -- "$OUT"
