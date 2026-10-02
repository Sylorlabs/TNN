#!/bin/sh
# k2_hardened_replay.sh — hardened N=8 replay for K2' plants (REPLAY-2026-09-20-v1).
# Faithful adaptation of replay-hardening/runner/{build_replay,run_replay}.sh:
# per-run baked adversarial substrate (ADV_TAG 0..7) + the plant's OWN main
# (the red-team harness contract calls entropy_mix from main, after
# vary_expr, before print_hex — so the plant's own main IS the unit under test).
# Usage: k2_hardened_replay.sh <NN> [argv0fix]
#   argv0fix=1 forces identical argv0 on all runs (isolates argv0-path artifacts, plant20).
set -u
NN="$1"; FIX0="${2:-0}"
LAB="$HOME/workspace/tnn-lab"
PL="$LAB/wave12/step1a-v2/thin-certifier/k2prime-redteam/plants/plant$NN"
RH="$LAB/wave12/step1a-v2/replay-hardening"
ZNC="$LAB/toolchain/bin/znc_linux_x86_64_abed8aa1"
ZFLAGS="--no-zagd --no-analyze --no-foreground-cache"
BUILD="/tmp/k2hr/pl$NN"; OUT="/tmp/k2hr/out_pl$NN"
FIX="$LAB/wave12/step1a-v2/fixtures"
STATE1="$FIX/state1.bin"; STATE2="$FIX/state2.bin"; INPUT="$FIX/input.bin"
EVDIR="/tmp/k2prime/plant$NN"
mkdir -p "$EVDIR"
EV="$EVDIR/replay_hardened.evidence"
if [ "$FIX0" = "1" ]; then EV="$EVDIR/replay_hardened_argv0fix.evidence"; fi
rm -rf "$BUILD" "$OUT"; mkdir -p "$BUILD" "$OUT"
LOG="$EVDIR/hardened_build.log"; : > "$LOG"
if command -v timeout >/dev/null 2>&1; then TO="timeout 120"; else TO=""; fi

fail() { echo "HARDENED_BUILD_FAIL: $1" | tee -a "$LOG"; echo "verdict=BUILDFAIL" > "$EV"; exit 4; }

# --- per-run builds: plant sources + adversarial substrate (baked tag r) ---
for r in 0 1 2 3 4 5 6 7; do
    d="$BUILD/r$r"; mkdir -p "$d"
    for f in "$PL"/*.zag; do
        base=$(basename "$f")
        if [ "$base" = "R33_NATIVE_IO_V1.zag" ]; then continue; fi
        cp "$f" "$d/$base"
    done
    cp "$RH/substrate/adv_substrate_r$r.zag" "$d/R33_NATIVE_IO_V1.zag"
    ( cd "$d" && $TO $ZNC variation.zag $ZFLAGS -o "plant${NN}_r$r" >>"$LOG" 2>&1 ) \
        || fail "compile plant$NN run $r"
done
echo "built plant$NN x8 (adversarial substrate, tags 0..7)" >>"$LOG"

# --- condition matrix (prereg §8), binaries = plant's own main ---
run_cond() { # $1=run# $2=outfile ; echoes exit code
    r="$1"; out="$2"; bin="$BUILD/r$r/plant${NN}_r$r"
    if [ "$FIX0" = "1" ]; then
        env -i PATH=/usr/bin:/bin bash -c 'exec -a k2plant_fixed_argv0 "$0" "$1" "$2"' "$bin" "$STATE1" "$INPUT" >"$out" 2>"$out.err"; echo $?
        return
    fi
    case "$r" in
        0) env -i PATH=/usr/bin:/bin $TO "$bin" "$STATE1" "$INPUT" >"$out" 2>"$out.err"; echo $? ;;
        1) if command -v setarch >/dev/null 2>&1; then
               env -i PATH=/usr/bin:/bin setarch x86_64 -R $TO "$bin" "$STATE1" "$INPUT" >"$out" 2>"$out.err"; echo $?
           else
               echo "noaslr_unavailable" >"$OUT/noaslr_flag"
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
echo "module=plant$NN"
echo "prereg=REPLAY-2026-09-20-v1"
echo "runs=8"
echo "substrate=adversarial-baked-tags-0..7"
echo "argv0_normalized=$FIX0"
verdict="PASS"; err_run=""
for r in 0 1 2 3 4 5 6 7; do
    rc=$(run_cond "$r" "$OUT/out_$r.bin")
    h=$(sha256sum "$OUT/out_$r.bin" | cut -d' ' -f1)
    echo "run_$r: tag=$r cond=$(cond_name $r) sha256=$h exit=$rc"
    eval "h_$r=$h"; eval "rc_$r=$rc"
    if [ "$rc" -ne 0 ]; then verdict="ERROR"; err_run="$err_run $r"; fi
done
if [ -f "$OUT/noaslr_flag" ]; then echo "noaslr_unavailable=1"; fi

# determinism control: r=0 binary twice, identical conditions
$TO "$BUILD/r0/plant${NN}_r0" "$STATE1" "$INPUT" >"$OUT/det_a.bin" 2>/dev/null; dca=$?
$TO "$BUILD/r0/plant${NN}_r0" "$STATE1" "$INPUT" >"$OUT/det_b.bin" 2>/dev/null; dcb=$?
ha=$(sha256sum "$OUT/det_a.bin" | cut -d' ' -f1); hb=$(sha256sum "$OUT/det_b.bin" | cut -d' ' -f1)
if [ "$dca" != "0" ] || [ "$dcb" != "0" ]; then verdict="ERROR"; dmatch=0; control_diverged=0;
elif [ "$ha" = "$hb" ]; then dmatch=1; control_diverged=0;
else dmatch=0; control_diverged=1; echo "control_mismatch=1";
     if [ "$verdict" = "PASS" ]; then verdict="DIVERGE"; fi
fi
echo "determinism_control: ha=$ha hb=$hb match=$dmatch"

# anti-triviality (informational for plants): state2 run
$TO "$BUILD/r0/plant${NN}_r0" "$STATE2" "$INPUT" >"$OUT/alt.bin" 2>/dev/null
halt=$(sha256sum "$OUT/alt.bin" | cut -d' ' -f1)
if [ "$halt" != "$h_0" ]; then vws=1; else vws=0; fi
echo "varies_with_state=$vws"

# pairwise verdict (§7.2)
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
} > "$EV" 2>&1
grep -E "^(verdict|divergent_pair|error_runs|determinism_control|varies_with_state)" "$EV"
echo "evidence: $EV"
