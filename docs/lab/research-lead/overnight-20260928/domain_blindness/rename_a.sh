#!/bin/sh
# rename_a.sh -- DOMAIN-BLINDNESS Variant A mechanical renaming.
# Transcribed verbatim from PREREG.md Section 4.1 (frozen procedure).
# Usage: rename_a.sh <input.zag> <output.zag>
#   SKIP_COMMENTS=1 skips step 1 (used ONLY for the B5 identifier check
#   on ref_uc_uni.zag, where comment stripping is out of scope; steps
#   2-7, the identifier transformations, are identical).
set -e
export PATH="$HOME/safebin"
IN="$1"; OUT="$2"
if [ "$SKIP_COMMENTS" = "1" ]; then
  cp "$IN" "$OUT.tmp1"
else
  # Step 1: strip comment lines, prepend fixed neutral header.
  # (Pattern '^[[:space:]]*//' implements the frozen "strip every line
  # starting with //" for the indented comment lines p6_new.zag also
  # contains; audit (d) requires exactly the 3 header lines remain.)
  { printf '// db_new.zag -- DOMAIN-BLINDNESS Variant A: mechanically renamed driver.\n// Every domain/relation/entity identifier replaced by opaque tokens via\n// the frozen PREREG permutation. No hand edits.\n';
    grep -v '^[[:space:]]*//' "$IN"; } > "$OUT.tmp1"
fi
# Step 2: function names (word-boundary; _ is a word char).
sed -i 's/\bsetup_p6_noX\b/setup_w2/g; s/\bsetup_p6_noY\b/setup_w3/g; s/\bsetup_p6pipe\b/setup_w4/g; s/\bsetup_p6\b/setup_w1/g' "$OUT.tmp1"
# Step 3: string labels, longest first.
sed -i 's/P6-ABL-X/QB/g; s/P6-ABL-Y/QC/g; s/P6-PIPE/QD/g; s/P6/QA/g' "$OUT.tmp1"
# Step 4: positional tagging of identifier fields.
sed -i -E \
 -e 's/fact_add\(A,([0-9]+),([0-9]+),([0-9]+)\)/fact_add(A,E\1,R\2,E\3)/g' \
 -e 's/map_new\(A,([0-9]+),([0-9]+),([0-9]+),([0-9]+)\)/map_new(A,\1,\2,R\3,R\4)/g' \
 -e 's/teach\(A,([0-9]+),([0-9]+),([0-9]+)\)/teach(A,\1,E\2,E\3)/g' \
 -e 's/exec_map\(A,([0-9]+),([0-9]+)\)/exec_map(A,\1,E\2)/g' \
 -e 's/uni_solve\((A[23]?|C),B,c,([0-9]+),/uni_solve(\1,B,c,E\2,/g' \
 "$OUT.tmp1"
# Step 5: entity table (3-digit before 2-digit).
sed -i \
 -e 's/E101/5011/g; s/E102/5012/g; s/E103/5013/g; s/E111/5014/g; s/E112/5015/g; s/E201/5016/g; s/E202/5017/g; s/E203/5018/g; s/E211/5019/g' \
 -e 's/E21/5001/g; s/E22/5002/g; s/E61/5003/g; s/E62/5004/g; s/E63/5005/g; s/E71/5006/g; s/E81/5007/g; s/E82/5008/g; s/E83/5009/g; s/E84/5010/g' \
 "$OUT.tmp1"
# Step 6: relation table.
sed -i \
 -e 's/R81/9001/g; s/R82/9002/g; s/R91/9003/g; s/R92/9004/g; s/R93/9005/g; s/R99/9006/g' \
 "$OUT.tmp1"
# Step 7: strip tags that matched no table entry (count values).
sed -i -e 's/E\([0-9][0-9]*\)/\1/g; s/R\([0-9][0-9]*\)/\1/g' "$OUT.tmp1"
mv "$OUT.tmp1" "$OUT"
if [ "$SKIP_COMMENTS" = "1" ]; then
  echo "B5-MODE: identifier steps only, no audits"
  exit 0
fi
# Step 8: audits (fail closed).
if grep -w -E '21|22|61|62|63|71|81|82|83|84|91|92|93|99|101|102|103|111|112|201|202|203|211' "$OUT"; then
  echo "AUDIT FAIL: original identifier survives"; exit 1
fi
if grep -E 'P6|setup_p6|inbound|outbound|ABL-' "$OUT"; then
  echo "AUDIT FAIL: human label survives"; exit 1
fi
if grep -o -E '[ER][0-9]+' "$OUT"; then
  echo "AUDIT FAIL: tagging residue"; exit 1
fi
if [ "$(grep -c '//' "$OUT")" != "3" ]; then
  echo "AUDIT FAIL: comment lines != 3 header lines"; grep -n '//' "$OUT"; exit 1
fi
echo "AUDIT OK: $OUT"
