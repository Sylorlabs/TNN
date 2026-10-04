#!/bin/sh
# stagecost.sh -- comparisons spent per stage (count of DET-CMP + DET-NCMP
# events, which is exactly what slog_cmp/slog_ncmp charge to the turn-cost
# accumulator 16650). Splits the battery into LEARNED stages (S1-S11) and
# LESIONED stages (S12-S14, whose strategy tables are hand-written by
# main's strat_lesion_*).
set -eu
cd "$(dirname "$0")"
for t in "$@"; do
  awk -v T="$t" '
    /^STAGE /{ st=$2 }
    /^DET-CMP /{ n[st]++; tot++ }
    /^DET-NCMP /{ n[st]++; tot++ }
    END{
      les=0; lr=0;
      for (s in n) { if (s=="S12"||s=="S13"||s=="S14") les+=n[s]; else lr+=n[s]; }
      printf "%-6s total=%-4d learned(S1-S11)=%-4d LESIONED(S12-S14)=%-3d\n", T, tot+0, lr+0, les+0;
    }' "out/$t.txt"
done
