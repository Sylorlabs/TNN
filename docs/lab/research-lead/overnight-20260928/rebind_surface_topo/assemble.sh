#!/bin/bash
# assemble.sh -- assemble full Zag sources for surface/topology tests.
# Usage: ./assemble.sh <driver> <mode>
#   <driver>: driver file (e.g., st_driver_rel.zag)
#   <mode>: treat (rebind), ctrl (fresh, vanilla), abl (A-phase, vanilla)
# Output: st_full_<name>_<mode>.zag
set -e
export PATH="$HOME/safebin"
DRIVER="$1"
MODE="$2"
NAME=$(basename "$DRIVER" .zag | sed 's/st_driver_//')
OUT="st_full_${NAME}_${MODE}.zag"
BASE="st_base.zag"
PATCH="st_patch.zag"
if [ "$MODE" = "treat" ]; then
  # Treatment: base without ev_query (lines 813-835) and without main (line 1357)
  # + patch (new ev_query) + driver
  # Patch defines phase_a_enabled()=1, so no yesa/noa needed.
  head -n 812 "$BASE" > "$OUT"
  tail -n +836 "$BASE" | head -n 521 >> "$OUT"
  tail -n +1358 "$BASE" >> "$OUT"
  cat "$PATCH" >> "$OUT"
  cat "$DRIVER" >> "$OUT"
elif [ "$MODE" = "ctrl" ]; then
  # Control: base without main (line 1357), with vanilla ev_query + driver + noa (phase_a=0)
  head -n 1356 "$BASE" > "$OUT"
  tail -n +1358 "$BASE" >> "$OUT"
  cat "$DRIVER" >> "$OUT"
  cat "st_noa.zag" >> "$OUT"
elif [ "$MODE" = "abl" ]; then
  # Ablation: base without main (line 1357), with vanilla ev_query + driver + yesa (phase_a=1)
  head -n 1356 "$BASE" > "$OUT"
  tail -n +1358 "$BASE" >> "$OUT"
  cat "$DRIVER" >> "$OUT"
  cat "st_yesa.zag" >> "$OUT"
else
  echo "Unknown mode: $MODE" >&2
  exit 1
fi
echo "Assembled $OUT"
