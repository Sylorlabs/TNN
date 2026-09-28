#!/bin/bash
# run.sh — §4 plan-formation parallelism battery driver.
# Builds planform (pure Zag, pinned znc), forms the plan sequentially and via
# parallel shards + order-free assemble, byte-diffs everything, times each
# stage. Zero RNG. Results in results/.
set -u
cd "$(dirname "$0")"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
R=results
mkdir -p "$R"

echo "=== build ==="
$ZNC planform.zag -o planform 2> "$R/build.log" || { echo "BUILD FAILED"; tail -20 "$R/build.log"; exit 1; }
echo "build ok"

# cpu_time: prints user+sys CPU seconds for "$@"
cpu_time() { # $1 = tagfile; remaining = command
  local tag="$1"; shift
  TIMEFORMAT='%U %S'
  { time "$@" > /dev/null 2>/dev/null; } 2> "$tag.stderr"
  awk '/^[0-9]/{u=$1; s=$2} END{print u+s+0}' "$tag.stderr"
}
cputime() { # $1=label $2=reps $@=cmd...
  local label="$1"; local reps="$2"; shift 2
  local best=""
  local i
  for ((i=0;i<reps;i++)); do
    local t
    t=$(cpu_time "$R/t_$label" "$@")
    if [ -z "$best" ] || awk -v a="$t" -v b="$best" 'BEGIN{exit !(a<b)}'; then best="$t"; fi
  done
  echo "$best"
}

S=2
echo "=== seq formation (min of 3, CPU s) ==="
T_SEQ=$(cputime seq 3 ./planform seq "$R/plan_seq.bin")
./planform seq "$R/plan_seq.bin" > "$R/winner_seq.txt"
cat "$R/winner_seq.txt"

echo "=== parallel shards S=$S (min of 3, CPU s per batch) ==="
shard_batch() {
  ./planform shard 0 $S > "$R/best0.txt" &
  ./planform shard 1 $S > "$R/best1.txt" &
  wait
}
T_PARB=$(cputime parb 3 shard_batch)
echo "=== single-shard CPU (min of 5; expect ~= T_SEQ/S) ==="
./planform shard 0 $S > "$R/best0.txt"
./planform shard 1 $S > "$R/best1.txt"
T_SH0=$(cputime sh0 5 ./planform shard 0 $S)
T_SH1=$(cputime sh1 5 ./planform shard 1 $S)
shard_batch
read _ I0 S0 < "$R/best0.txt"
read _ I1 S1 < "$R/best1.txt"
echo "shard0=$T_SH0 shard1=$T_SH1 (seq=$T_SEQ)"

echo "=== assemble (normal + scrambled order) ==="
read _ I0 S0 < "$R/best0.txt"
read _ I1 S1 < "$R/best1.txt"
T_ASM=$(cputime asm 3 ./planform assemble $S "$I0" "$S0" "$I1" "$S1" "$R/plan_par.bin")
./planform assemble $S "$I0" "$S0" "$I1" "$S1" "$R/plan_par.bin" > "$R/winner_par.txt"
./planform assemble $S "$I1" "$S1" "$I0" "$S0" "$R/plan_par_scr.bin" > "$R/winner_par_scr.txt"
cat "$R/winner_par.txt"

echo "=== byte-diff proofs ==="
cmp "$R/plan_seq.bin" "$R/plan_par.bin" && echo "SEQvsPAR: byte-identical"
cmp "$R/plan_par.bin" "$R/plan_par_scr.bin" && echo "PARvsPARscrambled: byte-identical"
cmp <(cut -d' ' -f1-2 "$R/winner_seq.txt") <(cut -d' ' -f1-2 "$R/winner_par.txt") && echo "winners agree"

echo "=== DET reruns ==="
./planform seq "$R/plan_seq2.bin" > /dev/null
cmp "$R/plan_seq.bin" "$R/plan_seq2.bin" && echo "SEQ rerun: byte-identical"
shard_batch
read _ J0 T0 < "$R/best0.txt"; read _ J1 T1 < "$R/best1.txt"
./planform assemble $S "$J0" "$T0" "$J1" "$T1" "$R/plan_par2.bin" > /dev/null
cmp "$R/plan_par.bin" "$R/plan_par2.bin" && echo "PAR rerun: byte-identical"

echo "=== render (min of 3, CPU s) ==="
T_REN=$(cputime ren 3 ./planform render "$R/plan_seq.bin" "$R/render_seq.bin")
./planform render "$R/plan_seq.bin" "$R/render_seq.bin" > /dev/null
./planform render "$R/plan_par.bin" "$R/render_par.bin" > /dev/null
cmp "$R/render_seq.bin" "$R/render_par.bin" && echo "RENDER(seq-plan)vsRENDER(par-plan): byte-identical"
./planform render "$R/plan_seq.bin" "$R/render_seq2.bin" > /dev/null
cmp "$R/render_seq.bin" "$R/render_seq2.bin" && echo "RENDER rerun: byte-identical"

T_PARF_WALL=$(awk -v a="$T_PARB" -v b="$T_ASM" 'BEGIN{print a+b}')
# Projections for an unloaded machine: scoring work splits evenly (each shard
# = 1/S of candidates, verified above); reduce+emit = T_ASM (measured).
proj() { # $1 = S
  awk -v f="$T_SEQ" -v s="$1" -v a="$T_ASM" -v r="$T_REN" 'BEGIN{
    pf=f/s+a; e2e_seq=f+r; e2e_par=pf+r;
    printf "S=%-3d T_form_par=%.4f  speedup_form=%.2f  E2E=%.4f  speedup_e2e=%.2f\n", s, pf, (pf>0?f/pf:0), e2e_par, (e2e_par>0?e2e_seq/e2e_par:0)}'
}
{
echo "shards=$S  (2-CPU VM at high load; CPU seconds, min-of-N; wall batch measured under load)"
echo "T_SEQ_formation   = $T_SEQ"
echo "T_shard0          = $T_SH0   (~T_SEQ/S = $(awk -v t="$T_SEQ" 'BEGIN{print t/2}'))"
echo "T_shard1          = $T_SH1"
echo "T_assemble        = $T_ASM"
echo "T_PAR_batch_wall  = $T_PARF_WALL   (measured S=$S under load; noisy)"
echo "T_render          = $T_REN"
echo "--- projections, unloaded machine (T_form/S + T_assemble + T_render) ---"
proj 2; proj 8; proj 64
} | tee "$R/timings.txt"
echo "=== done ==="
