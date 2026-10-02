#!/bin/zsh
set -u

ROOT=${0:A:h:h:h}
OUT=${1:-"$ROOT/Research/R33_REMEDIATION_20260915T2152Z/AGENT_ARCHIVE_SWEEP_20260915"}
mkdir -p "$OUT"

KNOWN_R25='6d0b14d8ab4a081b57c3762800475f8ecb67d2d7e9134a82e6f7690efc4e2957'
KNOWN_R26='df3acde273aa682642d13763a24208ff1dbb42968313cbe2a4256f7ccbc1f839'
KNOWN_R26SRC='1e87721a93666155aabc67016ccd9416684c00f1e3c02da57f2c712083fc444d'

ARCHIVES="$OUT/archives.txt"
MEMBERS="$OUT/candidate_members.tsv"
HASHES="$OUT/candidate_hashes.tsv"
EXACT="$OUT/exact_matches.tsv"
MEDIA="$OUT/media_candidates.tsv"
ERRORS="$OUT/errors.log"

: > "$ARCHIVES"
: > "$MEMBERS"
: > "$HASHES"
: > "$EXACT"
: > "$MEDIA"
: > "$ERRORS"

{
  find "$ROOT/Research" -type f \( -name '*.tar' -o -name '*.tar.gz' -o -name '*.tgz' -o -name '*.zip' \) -print 2>/dev/null
  if [[ -d /Users/Shared/micah/Documents/Codex ]]; then
    find /Users/Shared/micah/Documents/Codex -type f \( -name '*.tar' -o -name '*.tar.gz' -o -name '*.tgz' -o -name '*.zip' \) -print 2>/dev/null
  fi
} | LC_ALL=C sort -u > "$ARCHIVES"

print -r -- $'archive\ttype\tmember' > "$MEMBERS"
print -r -- $'archive\ttype\tmember\tsha256' > "$HASHES"
print -r -- $'archive\ttype\tmember\tsha256\texpectation' > "$EXACT"
print -r -- $'archive\ttype\tmember' > "$MEDIA"

is_candidate() {
  local m=$1
  case "$m" in
    *r25-accepted-state.pkl|*r26-accepted-state.pkl|*r26-accepted-policy.json|*r26_experiments.py|*smoke_r26.py|*MANIFEST.sha256|*manifest.sha256|*manifest.json) return 0 ;;
    *) return 1 ;;
  esac
}

is_media() {
  local lower=${1:l}
  case "$lower" in
    *.mp4|*.mov|*.m4v|*.avi|*.webm|*.gif|*.png|*.jpg|*.jpeg) return 0 ;;
    *) return 1 ;;
  esac
}

hash_stream() {
  shasum -a 256 | awk '{print $1}'
}

while IFS= read -r archive; do
  [[ -n "$archive" ]] || continue
  local_type=tar
  [[ "$archive" == *.zip ]] && local_type=zip

  if [[ "$local_type" == zip ]]; then
    members=$(unzip -Z1 "$archive" 2>>"$ERRORS") || { print -r -- "LIST_FAIL\t$archive" >> "$ERRORS"; continue; }
  else
    members=$(tar -tf "$archive" 2>>"$ERRORS") || { print -r -- "LIST_FAIL\t$archive" >> "$ERRORS"; continue; }
  fi

  while IFS= read -r member; do
    [[ -n "$member" ]] || continue
    if is_media "$member"; then
      print -r -- "$archive\t$local_type\t$member" >> "$MEDIA"
    fi
    is_candidate "$member" || continue
    print -r -- "$archive\t$local_type\t$member" >> "$MEMBERS"

    if [[ "$local_type" == zip ]]; then
      digest=$(unzip -p "$archive" "$member" 2>>"$ERRORS" | hash_stream) || continue
    else
      digest=$(tar -xOf "$archive" "$member" 2>>"$ERRORS" | hash_stream) || continue
    fi
    print -r -- "$archive\t$local_type\t$member\t$digest" >> "$HASHES"

    expectation=''
    [[ "$digest" == "$KNOWN_R25" ]] && expectation='r25-accepted-state.pkl'
    [[ "$digest" == "$KNOWN_R26" ]] && expectation='r26-accepted-state.pkl'
    [[ "$digest" == "$KNOWN_R26SRC" ]] && expectation='r26_experiments.py'
    if [[ -n "$expectation" ]]; then
      print -r -- "$archive\t$local_type\t$member\t$digest\t$expectation" >> "$EXACT"
    fi
  done <<< "$members"
done < "$ARCHIVES"

archive_count=$(wc -l < "$ARCHIVES" | tr -d ' ')
candidate_count=$(( $(wc -l < "$MEMBERS") - 1 ))
exact_count=$(( $(wc -l < "$EXACT") - 1 ))
media_count=$(( $(wc -l < "$MEDIA") - 1 ))

cat > "$OUT/RECEIPT.txt" <<EOF
archive_count=$archive_count
candidate_member_count=$candidate_count
exact_known_hash_matches=$exact_count
media_candidate_count=$media_count
pickle_executed=false
python_executed=false
foreign_ml_runtime_used=false
admission_rule=exact_hash_only
EOF

print -r -- "$OUT"
