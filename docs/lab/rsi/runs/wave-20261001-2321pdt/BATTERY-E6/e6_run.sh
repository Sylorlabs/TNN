#!/bin/sh
# e6_run.sh -- BATTERY-E6 runner. Shell only: hash checks, staged runs of the
# frozen binary, inspector reports, ablation probes, byte-identity gates,
# and the PREREG_E6 section 4 decision rule as byte comparisons.
# No transcript transformation; no logic keyed on world ids, subjects,
# relations, or CHOICE values beyond the section 4 rule and gates.
# Usage: sh e6_run.sh
set -u
LANE=docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E6
SHIM=docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin
TNN2=docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag
SHIM_WANT=9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
TNN2_WANT=a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
PREREG=$LANE/PREREG_E6.md
FREEZE_COMMIT=58811f3a5
PREREG_WANT=80ea66f7f9cf292b0d15f5b586e968fea280a39d303c1698985a8d5f3c7f87a0
W_S0_WANT=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
W_S1_WANT=a12acfe5989e04e26ccf505f75b600b0a715ad601ef741593d567530d02888d0
W_ACT_WANT=8c0222254050b10cc247418dfecc1424c6dd0326480b413632adad57bc380d87
W_S3_WANT=e10ac056d807a0d8aea07611dc8b0be6bbaea527554b75fcc330c11f5c4fa920
W_S5_WANT=a38bd1ebd64e97ef14a2ef4a26b19ec416aac971bfbc42c00351b8eb616c4f22

check_hash() {
  got=$(sha256sum "$1" | cut -d' ' -f1)
  if [ "$got" != "$2" ]; then
    echo "HASH-MISMATCH $1 want=$2 got=$got"
    exit 1
  fi
  echo "HASH-OK $1"
}

echo "== E6-K1 prereg ordering =="
check_hash "$PREREG" "$PREREG_WANT"
if git diff "$FREEZE_COMMIT" HEAD -- "$PREREG" | grep -q .; then
  echo "E6-K1 FAIL: prereg changed after freeze commit"
  exit 1
fi
echo "E6-K1 PASS (prereg frozen at $FREEZE_COMMIT, unchanged)"

echo "== E6-K3 pre-run frozen binary check =="
check_hash "$SHIM" "$SHIM_WANT"
check_hash "$TNN2" "$TNN2_WANT"

echo "== E6-K6 anti-smuggling (frozen sources, E6 id set) =="
if grep -r "95001\|95101\|95011\|95002\|95202\|95012" \
    docs/lab/research-lead/overnight-20260928/tnn2_build/ \
    docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/ 2>/dev/null; then
  echo "LEAK-FOUND"; exit 1
fi
echo "E6-K6 PASS (zero matches)"

echo "== worldgen =="
mkdir -p "$LANE/e6_worlds" "$LANE/e6_runs"
(cd "$LANE" && ./e6_worldgen_bin e6_worlds)
echo "== E6-K4 seal integrity (world hashes vs prereg section 2) =="
check_hash "$LANE/e6_worlds/e6_s0_world.txt" "$W_S0_WANT"
check_hash "$LANE/e6_worlds/e6_s1_world.txt" "$W_S1_WANT"
check_hash "$LANE/e6_worlds/e6_act_world.txt" "$W_ACT_WANT"
check_hash "$LANE/e6_worlds/e6_s3_world.txt" "$W_S3_WANT"
check_hash "$LANE/e6_worlds/e6_s5_world.txt" "$W_S5_WANT"
(cd "$LANE/e6_worlds" && sha256sum e6_s0_world.txt e6_s1_world.txt \
  e6_act_world.txt e6_s3_world.txt e6_s5_world.txt > E6_MANIFEST.sha256 \
  && cat E6_MANIFEST.sha256)
echo "E6-K4 PASS"

echo "== staged chains (3 fresh-state chains, stages s0..s6 + degenerate) =="
for r in 1 2 3; do
  st="$LANE/e6_runs/e6_chain_r${r}.bin"
  rm -f "$st"
  # s0: init baseline (empty world)
  ./$SHIM "$LANE/e6_worlds/e6_s0_world.txt" "$st" > "$LANE/e6_runs/e6_t${r}_s0.trans"
  cp "$st" "$LANE/e6_runs/e6_d${r}_s0.bin"
  # s1: create two guides
  ./$SHIM "$LANE/e6_worlds/e6_s1_world.txt" "$st" > "$LANE/e6_runs/e6_t${r}_s1.trans"
  cp "$st" "$LANE/e6_runs/e6_d${r}_s1.bin"
  # s2: ACT with 2 live guides
  ./$SHIM "$LANE/e6_worlds/e6_act_world.txt" "$st" > "$LANE/e6_runs/e6_t${r}_s2.trans"
  cp "$st" "$LANE/e6_runs/e6_d${r}_s2.bin"
  # s3: resolve guide 1
  ./$SHIM "$LANE/e6_worlds/e6_s3_world.txt" "$st" > "$LANE/e6_runs/e6_t${r}_s3.trans"
  cp "$st" "$LANE/e6_runs/e6_d${r}_s3.bin"
  # s4: ACT after 1 resolution
  ./$SHIM "$LANE/e6_worlds/e6_act_world.txt" "$st" > "$LANE/e6_runs/e6_t${r}_s4.trans"
  cp "$st" "$LANE/e6_runs/e6_d${r}_s4.bin"
  # s5: resolve guide 2
  ./$SHIM "$LANE/e6_worlds/e6_s5_world.txt" "$st" > "$LANE/e6_runs/e6_t${r}_s5.trans"
  cp "$st" "$LANE/e6_runs/e6_d${r}_s5.bin"
  # s6: ACT after both resolved
  ./$SHIM "$LANE/e6_worlds/e6_act_world.txt" "$st" > "$LANE/e6_runs/e6_t${r}_s6.trans"
  cp "$st" "$LANE/e6_runs/e6_d${r}_s6.bin"
  # d: degenerate ACT on fresh state
  dst="$LANE/e6_runs/e6_dg_r${r}.bin"
  rm -f "$dst"
  ./$SHIM "$LANE/e6_worlds/e6_act_world.txt" "$dst" > "$LANE/e6_runs/e6_tdg${r}.trans"
  echo "CHAIN-OK r$r"
done

echo "== inspector reports =="
for r in 1 2 3; do
  for s in s0 s1 s2 s3 s4 s5 s6; do
    (cd "$LANE" && ./e6_inspect_bin "e6_runs/e6_d${r}_${s}.bin" > "e6_runs/e6_rep${r}_${s}.txt")
  done
done
echo "INSPECT-DONE"

echo "== E6-K2 determinism (dumps + transcripts byte-identical across chains) =="
for s in s0 s1 s2 s3 s4 s5 s6; do
  if cmp -s "$LANE/e6_runs/e6_d1_${s}.bin" "$LANE/e6_runs/e6_d2_${s}.bin" && \
     cmp -s "$LANE/e6_runs/e6_d1_${s}.bin" "$LANE/e6_runs/e6_d3_${s}.bin" && \
     cmp -s "$LANE/e6_runs/e6_t1_${s}.trans" "$LANE/e6_runs/e6_t2_${s}.trans" && \
     cmp -s "$LANE/e6_runs/e6_t1_${s}.trans" "$LANE/e6_runs/e6_t3_${s}.trans"; then
    echo "E6-K2 PASS stage $s (3/3 byte-identical dumps + transcripts)"
  else
    echo "E6-K2 FAIL stage $s"; exit 1
  fi
done
if cmp -s "$LANE/e6_runs/e6_tdg1.trans" "$LANE/e6_runs/e6_tdg2.trans" && \
   cmp -s "$LANE/e6_runs/e6_tdg1.trans" "$LANE/e6_runs/e6_tdg3.trans"; then
  echo "E6-K2 PASS degenerate (3/3 byte-identical)"
else
  echo "E6-K2 FAIL degenerate"; exit 1
fi

echo "== lifecycle: GUIDE/UNCERT lines across resolution events =="
for r in 1 2 3; do
  for s in s2 s3 s4 s5; do
    grep -E '^(GUIDE|UNCERT) ' "$LANE/e6_runs/e6_rep${r}_${s}.txt" > "$LANE/e6_runs/e6_gu${r}_${s}.txt"
  done
  if cmp -s "$LANE/e6_runs/e6_gu${r}_s2.txt" "$LANE/e6_runs/e6_gu${r}_s3.txt"; then
    echo "r$r resolution-1: GUIDE/UNCERT lines UNCHANGED (sticky)"
  else
    echo "r$r resolution-1: GUIDE/UNCERT lines CHANGED"; diff "$LANE/e6_runs/e6_gu${r}_s2.txt" "$LANE/e6_runs/e6_gu${r}_s3.txt" || true
  fi
  if cmp -s "$LANE/e6_runs/e6_gu${r}_s4.txt" "$LANE/e6_runs/e6_gu${r}_s5.txt"; then
    echo "r$r resolution-2: GUIDE/UNCERT lines UNCHANGED (sticky)"
  else
    echo "r$r resolution-2: GUIDE/UNCERT lines CHANGED"; diff "$LANE/e6_runs/e6_gu${r}_s4.txt" "$LANE/e6_runs/e6_gu${r}_s5.txt" || true
  fi
done

echo "== ablation battery (5 classes x 3 chains, ACT probe on mutated d1) =="
for r in 1 2 3; do
  for c in NONE F4 F20 UC PRES; do
    (cd "$LANE" && ./e6_ablate_bin "e6_runs/e6_d${r}_s1.bin" "$c" "e6_runs/e6_m${r}_${c}.bin" > /dev/null)
    ./$SHIM "$LANE/e6_worlds/e6_act_world.txt" "$LANE/e6_runs/e6_m${r}_${c}.bin" > "$LANE/e6_runs/e6_ta${r}_${c}.trans"
  done
  echo "ABLATE-OK r$r"
done
echo "== E6-K2 ablation transcripts byte-identical across chains =="
for c in NONE F4 F20 UC PRES; do
  if cmp -s "$LANE/e6_runs/e6_ta1_${c}.trans" "$LANE/e6_runs/e6_ta2_${c}.trans" && \
     cmp -s "$LANE/e6_runs/e6_ta1_${c}.trans" "$LANE/e6_runs/e6_ta3_${c}.trans"; then
    echo "E6-K2 PASS ablation $c (3/3 byte-identical)"
  else
    echo "E6-K2 FAIL ablation $c"; exit 1
  fi
done

echo "== section 4 decision rule (byte comparisons of CHOICE lines) =="
c2=$(grep '^CHOICE ' "$LANE/e6_runs/e6_t1_s2.trans")
c4=$(grep '^CHOICE ' "$LANE/e6_runs/e6_t1_s4.trans")
c6=$(grep '^CHOICE ' "$LANE/e6_runs/e6_t1_s6.trans")
cd0=$(grep '^CHOICE ' "$LANE/e6_runs/e6_tdg1.trans")
echo "natural s2: [$c2] s4: [$c4] s6: [$c6] degenerate: [$cd0]"
a_none=$(grep '^CHOICE ' "$LANE/e6_runs/e6_ta1_NONE.trans")
a_f4=$(grep '^CHOICE ' "$LANE/e6_runs/e6_ta1_F4.trans")
a_f20=$(grep '^CHOICE ' "$LANE/e6_runs/e6_ta1_F20.trans")
a_uc=$(grep '^CHOICE ' "$LANE/e6_runs/e6_ta1_UC.trans")
a_pres=$(grep '^CHOICE ' "$LANE/e6_runs/e6_ta1_PRES.trans")
echo "ablate NONE: [$a_none] F4: [$a_f4] F20: [$a_f20] UC: [$a_uc] PRES: [$a_pres]"
if [ "$c2" = "$c4" ] && [ "$c4" = "$c6" ]; then
  echo "NATURAL-INVARIANCE holds (action invariant across contents/resolutions)"
else
  echo "NATURAL-INVARIANCE broken"
fi
if cmp -s "$LANE/e6_runs/e6_gu1_s2.txt" "$LANE/e6_runs/e6_gu1_s3.txt" && \
   cmp -s "$LANE/e6_runs/e6_gu1_s4.txt" "$LANE/e6_runs/e6_gu1_s5.txt"; then
  echo "H2C-LIFECYCLE: H2C-STICKY (guide records unchanged by both resolutions)"
else
  echo "H2C-LIFECYCLE: H2C-RETIRED (a resolution changed a guide record)"
fi
if [ "$a_f4" = "$a_none" ] && [ "$a_uc" = "$a_none" ] && [ "$a_pres" != "$a_none" ]; then
  echo "VERDICT: E6-DEAD-CONTENT"
elif { [ "$a_f4" != "$a_none" ] || [ "$a_uc" != "$a_none" ]; } && [ "$c2" = "$c4" ] && [ "$c4" = "$c6" ]; then
  echo "VERDICT: E6-CONTENT-READ"
else
  echo "VERDICT: E6-INCONCLUSIVE"
fi
if [ "$cd0" = "CHOICE 0" ]; then
  echo "E6-K5 PASS (degenerate control CHOICE 0)"
else
  echo "E6-K5 FAIL (degenerate control [$cd0] != CHOICE 0)"
fi

echo "== E6-K3 post-run frozen binary check =="
check_hash "$SHIM" "$SHIM_WANT"
check_hash "$TNN2" "$TNN2_WANT"
echo "== evidence hashes =="
(cd "$LANE/e6_runs" && sha256sum e6_d1_s0.bin e6_d1_s1.bin e6_d1_s2.bin \
  e6_d1_s3.bin e6_d1_s4.bin e6_d1_s5.bin e6_d1_s6.bin \
  e6_t1_s0.trans e6_t1_s1.trans e6_t1_s2.trans e6_t1_s3.trans \
  e6_t1_s4.trans e6_t1_s5.trans e6_t1_s6.trans e6_tdg1.trans \
  e6_ta1_NONE.trans e6_ta1_F4.trans e6_ta1_F20.trans e6_ta1_UC.trans \
  e6_ta1_PRES.trans \
  e6_rep1_s0.txt e6_rep1_s1.txt e6_rep1_s2.txt e6_rep1_s3.txt \
  e6_rep1_s4.txt e6_rep1_s5.txt e6_rep1_s6.txt | tee E6_EVIDENCE_SHA256.txt)
echo E6-RUN-DONE
