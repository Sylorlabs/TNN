#!/bin/sh
# run_replay.sh — REPLAY-2026-09-20-v1 runner (prereg §7, §8).
# Deterministic shell glue: runs the per-(module,run) baked binaries under
# the preregistered condition matrix, hashes stdout, decides the verdict.
# No RNG anywhere. Usage: run_replay.sh <module>
set -u
MOD="$1"
RH="/home/hatch/workspace/tnn-lab/wave12/step1a-v2/armc-rerun-2026-09-21/replay/rh"
BUILD="/tmp/rhbuild"
FIX="$HOME/workspace/tnn-lab/wave12/step1a-v2/fixtures"
STATE1="$FIX/state1.bin"; STATE2="$FIX/state2.bin"; INPUT="$FIX/input.bin"
OUT="/tmp/rhout/$MOD"; EV="$RH/evidence/$MOD.evidence.txt"
rm -rf "$OUT"; mkdir -p "$OUT"
if command -v timeout >/dev/null 2>&1; then TO="timeout 120"; else TO=""; fi

# condition matrix (§8). prints stdout to $2, exit code echoed.
run_cond() { # $1=run# $2=outfile ; echoes exit code
    r="$1"; out="$2"; bin="$BUILD/${MOD}_r$r/replay_${MOD}_r$r"
    case "$r" in
        0) env -i PATH=/usr/bin:/bin $TO "$bin" "$STATE1" "$INPUT" >"$out" 2>"$out.err"; echo $? ;;
        1) if command -v setarch >/dev/null 2>&1; then
               env -i PATH=/usr/bin:/bin setarch x86_64 -R $TO "$bin" "$STATE1" "$INPUT" >"$out" 2>"$out.err"; echo $?
           else
               echo "noaslr_unavailable" >"$OUT/noaslr_flag"; 
               env -i PATH=/usr/bin:/bin $TO "$bin" "$STATE1" "$INPUT" >"$out" 2>"$out.err"; echo $?
           fi ;;
        2) env -i PATH=/usr/bin:/bin REPLAY_A="alpha_$r" REPLAY_B=beta REPLAY_C=gamma REPLAY_D="delta_$r" \
               bash -c 'exec -a replay_alias_r2 "$0" "$1" "$2"' "$bin" "$STATE1" "$INPUT" >"$out" 2>"$out.err"; echo $? ;;
        3) ( exec 3<>/dev/null 4<>/dev/null 5<>/dev/null
             env -i PATH=/usr/bin:/bin $TO "$bin" "$STATE1" "$INPUT" >"$out" 2>"$out.err"; echo $? ) ;;
        4) ( cd /tmp && env -i PATH=/usr/bin:/bin $TO "$bin" "$STATE1" "$INPUT" >"$out" 2>"$out.err"; echo $? ) ;;
        5) ( exec 3<>/dev/null 4<>/dev/null
             env -i PATH=/usr/bin:/bin REPLAY_D="delta_$r" REPLAY_C=gamma REPLAY_B=beta REPLAY_A="alpha_$r" \
             bash -c 'exec -a a_much_longer_argv0_name_for_run_five "$0" "$1" "$2"' "$bin" "$STATE1" "$INPUT" >"$out" 2>"$out.err"; echo $? ) ;;
        6) sleep 2; env -i PATH=/usr/bin:/bin REPLAY_SKEW=1 $TO "$bin" "$STATE1" "$INPUT" >"$out" 2>"$out.err"; echo $? ;;
        7) ( cd / && exec 3<>/dev/null 4<>/dev/null
             env -i PATH=/usr/bin:/bin REPLAY_X=1 REPLAY_Y=2 REPLAY_Z=3 \
             bash -c 'exec -a replay_r7_combined "$0" "$1" "$2"' "$bin" "$STATE1" "$INPUT" >"$out" 2>"$out.err"; echo $? ) ;;
    esac
}
cond_name() { case "$1" in
    0) echo "BASE";; 1) echo "NOASLR";; 2) echo "ENV";; 3) echo "FDS";;
    4) echo "CWD";; 5) echo "ENVORDER";; 6) echo "SKEW";; 7) echo "COMBINED";; esac; }

{
echo "module=$MOD"
echo "prereg=REPLAY-2026-09-20-v1"
echo "runs=8"
verdict="PASS"; err_run=""
for r in 0 1 2 3 4 5 6 7; do
    rc=$(run_cond "$r" "$OUT/out_$r.bin")
    h=$(sha256sum "$OUT/out_$r.bin" | cut -d' ' -f1)
    echo "run_$r: tag=$r cond=$(cond_name $r) sha256=$h exit=$rc"
    eval "h_$r=$h"; eval "rc_$r=$rc"
    if [ "$rc" -ne 0 ]; then verdict="ERROR"; err_run="$err_run $r"; fi
done
if [ -f "$OUT/noaslr_flag" ]; then echo "noaslr_unavailable=1"; fi

# determinism control (§7.3, as amended 2026-09-20 item B): r=0 binary twice,
# identical conditions. Exits 0 + hash mismatch => DIVERGE (genuine per-process
# nondeterminism — the strongest divergence signal); exit != 0 => ERROR.
$TO "$BUILD/${MOD}_r0/replay_${MOD}_r0" "$STATE1" "$INPUT" >"$OUT/det_a.bin" 2>/dev/null; dca=$?
$TO "$BUILD/${MOD}_r0/replay_${MOD}_r0" "$STATE1" "$INPUT" >"$OUT/det_b.bin" 2>/dev/null; dcb=$?
ha=$(sha256sum "$OUT/det_a.bin" | cut -d' ' -f1); hb=$(sha256sum "$OUT/det_b.bin" | cut -d' ' -f1)
if [ "$dca" != "0" ] || [ "$dcb" != "0" ]; then verdict="ERROR"; dmatch=0; control_diverged=0;
elif [ "$ha" = "$hb" ]; then dmatch=1; control_diverged=0;
else dmatch=0; control_diverged=1; echo "control_mismatch=1";
     if [ "$verdict" = "PASS" ]; then verdict="DIVERGE"; fi
fi
echo "determinism_control: ha=$ha hb=$hb match=$dmatch"

# anti-triviality (§7.4): informational for dirty plants, gating for clean
$TO "$BUILD/${MOD}_r0/replay_${MOD}_r0" "$STATE2" "$INPUT" >"$OUT/alt.bin" 2>/dev/null
halt=$(sha256sum "$OUT/alt.bin" | cut -d' ' -f1)
if [ "$halt" != "$h_0" ]; then vws=1; else vws=0; fi
echo "varies_with_state=$vws"
if [ "$MOD" = "variation" ] && [ "$vws" != "1" ]; then verdict="ERROR"; echo "antitriviality_gate=FAILED"; fi

# pairwise verdict (§7.2); matrix pair stands over control pair when both exist
if [ "$verdict" != "ERROR" ]; then
    pair=""; i=0
    while [ "$i" -lt 8 ]; do
        j=$((i+1))
        while [ "$j" -lt 8 ]; do
            eval "hi=\$h_$i"; eval "hj=\$h_$j"
            if [ "$hi" != "$hj" ]; then
                verdict="DIVERGE"
                if [ -z "$pair" ]; then
                    pair="$i,$j"
                    echo "divergent_pair=$pair"
                    echo "first_diff=$(cmp -l "$OUT/out_$i.bin" "$OUT/out_$j.bin" | head -1 | tr -s ' ')"
                fi
            fi
            j=$((j+1))
        done
        i=$((i+1))
    done
    if [ -z "$pair" ]; then
        if [ "$control_diverged" = "1" ]; then echo "divergent_pair=control_a,control_b";
        else echo "divergent_pair=none"; fi
    fi
fi
[ "$verdict" = "ERROR" ] && echo "error_runs=$err_run"
echo "verdict=$verdict"

# W2 BEFORE/AFTER (§9, dirty3 only): zeroing substrate + naive pre-dirty, 8x BASE
if [ "$MOD" = "dirty3_uninit" ]; then
    echo "before_w2:"
    bh0=""
    for r in 0 1 2 3 4 5 6 7; do
        $TO "$BUILD/before_dirty3/replay_before_dirty3" "$STATE1" "$INPUT" >"$OUT/before_$r.bin" 2>/dev/null; brc=$?
        bh=$(sha256sum "$OUT/before_$r.bin" | cut -d' ' -f1)
        echo "before_run_$r: sha256=$bh exit=$brc"
        if [ -z "$bh0" ]; then bh0="$bh"; fi
        if [ "$bh" != "$bh0" ]; then echo "before_diverged=1"; fi
    done
    echo "before_all_identical_check_done"
fi
} > "$EV" 2>&1
cat "$EV" | grep -E "^(verdict|divergent_pair|error_runs|determinism_control|varies_with_state)" 
echo "evidence: $EV"
