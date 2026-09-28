#!/bin/sh
# build_replay.sh — REPLAY-2026-09-20-v1 build (prereg §5).
# Generates per-(module,run) build dirs in /tmp, compiles with znc.
# Binaries are NEVER committed. Fails fast on any unit-derivation mismatch.
set -u
RH="$HOME/workspace/tnn-lab/wave12/step1a-v2/replay-hardening"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
BUILD="/tmp/rhbuild"
LOG="$RH/evidence/build.log"
FIX="$HOME/workspace/tnn-lab/wave12/step1a-v2/fixtures"
: > "$LOG"

fail() { echo "BUILD_FAIL: $1" | tee -a "$LOG"; exit 1; }

# --- unit derivation checks (prereg §5) ---
for m in dirty1_urandom dirty2_clock dirty3_uninit dirty4_hash dirty5_aslr; do
    # only delta vs frozen module may be the removed @import line (+3 header lines)
    if [ "$(diff "$HOME/workspace/tnn-lab/wave12/step1a-v2/modules/$m.zag" "$RH/units/$m.zag" | grep -c '^<')" -ne 1 ]; then
        fail "unit $m derivation mismatch"
    fi
    if ! diff "$HOME/workspace/tnn-lab/wave12/step1a-v2/modules/$m.zag" "$RH/units/$m.zag" | grep '^<' | grep -q '@import("harness.zag")'; then
        fail "unit $m removed line is not the harness import"
    fi
done
# variation unit: must equal frozen vary_expr (lines 6-30) exactly
sed -n '6,30p' "$HOME/workspace/tnn-lab/wave12/step1a-v2/modules/variation.zag" > /tmp/vary_frozen.txt
tail -n +4 "$RH/units/variation.zag" > /tmp/vary_unit.txt
if ! diff /tmp/vary_frozen.txt /tmp/vary_unit.txt >/dev/null; then
    fail "variation unit mismatch"
fi
rm -f /tmp/vary_frozen.txt /tmp/vary_unit.txt
# adversarial substrates: r0 must equal template; rN differ only in ADV_TAG line
for r in 0 1 2 3 4 5 6 7; do
    if [ "$r" = "0" ]; then
        cmp -s "$RH/substrate/R33_NATIVE_IO_V1_ADVERSARIAL.zag.template" "$RH/substrate/adv_substrate_r0.zag" \
            || fail "adv_substrate_r0 != template"
    else
        ndiff=$(diff "$RH/substrate/adv_substrate_r0.zag" "$RH/substrate/adv_substrate_r$r.zag" | grep -c '^[<>]') || true
        [ "$ndiff" = "2" ] || fail "adv_substrate_r$r delta != 1 line"
        grep -q "const ADV_TAG:i64 = $r;" "$RH/substrate/adv_substrate_r$r.zag" || fail "adv_substrate_r$r tag wrong"
    fi
done
echo "derivation checks OK" | tee -a "$LOG"

rm -rf "$BUILD"; mkdir -p "$BUILD"
ZFLAGS="--no-zagd --no-analyze --no-foreground-cache"

# --- AFTER builds: adversarial substrate, 8 modules x 8 runs ---
for m in dirty1_urandom dirty2_clock dirty3_uninit dirty4_hash dirty5_aslr variation dirty1b_entropy_read dirty2b_clock_read; do
    for r in 0 1 2 3 4 5 6 7; do
        d="$BUILD/${m}_r$r"; mkdir -p "$d"
        cp "$RH/substrate/adv_substrate_r$r.zag" "$d/adv.zag"
        cp "$RH/units/$m.zag" "$d/unit.zag"
        cp "$RH/replay_driver.zag" "$d/replay_driver.zag"
        ( cd "$d" && $ZNC replay_driver.zag $ZFLAGS -o "replay_${m}_r$r" >>"$LOG" 2>&1 ) \
            || fail "compile ${m}_r$r"
    done
    echo "built $m x8" | tee -a "$LOG"
done

# --- BEFORE build: real zeroing substrate + naive pre-dirty, dirty3 only ---
d="$BUILD/before_dirty3"; mkdir -p "$d"
cp "$HOME/workspace/tnn-lab/wave12/step1a-v2/substrate/R33_NATIVE_IO_V1.zag" "$d/adv.zag"
cp "$RH/units/dirty3_uninit.zag" "$d/unit.zag"
cp "$RH/replay_driver_zeroing.zag" "$d/replay_driver_zeroing.zag"
( cd "$d" && $ZNC replay_driver_zeroing.zag $ZFLAGS -o replay_before_dirty3 >>"$LOG" 2>&1 ) \
    || fail "compile before_dirty3"
echo "built before_dirty3" | tee -a "$LOG"

# --- record substrate hashes (prereg §4/§11) ---
{
    echo "real_substrate_sha256=$(sha256sum "$HOME/workspace/tnn-lab/wave12/step1a-v2/substrate/R33_NATIVE_IO_V1.zag" | cut -d' ' -f1)"
    echo "adv_template_sha256=$(sha256sum "$RH/substrate/R33_NATIVE_IO_V1_ADVERSARIAL.zag.template" | cut -d' ' -f1)"
    for r in 0 1 2 3 4 5 6 7; do
        echo "adv_r${r}_sha256=$(sha256sum "$RH/substrate/adv_substrate_r$r.zag" | cut -d' ' -f1)"
    done
    echo "driver_sha256=$(sha256sum "$RH/replay_driver.zag" | cut -d' ' -f1)"
    echo "driver_zeroing_sha256=$(sha256sum "$RH/replay_driver_zeroing.zag" | cut -d' ' -f1)"
} | tee -a "$LOG"
echo "BUILD_OK" | tee -a "$LOG"
