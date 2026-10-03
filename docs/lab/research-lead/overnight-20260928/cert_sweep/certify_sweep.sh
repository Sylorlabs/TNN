#!/bin/sh
# certify_sweep.sh <base.zag> -- H-BASECERT-SWEEP-1 sweep wrapper.
# Same four checks as base_cert/certify_base (CERT-A leak, CERT-B arena,
# CERT-C determinism 3/3, CERT-D correctness), adapted for bases that
# diverged from the original ma_base.zag assumptions:
#   1. The base defines its own ev_query (richer than the driver's glue,
#      with ctx/decay/rebind machinery): the driver glue is dropped and
#      the base's own ev_query is the entry point under test.
#   2. The base defines fn main: the scratch copy (only) is trimmed from
#      the `fn main(` line to EOF so the cert driver's main links.
# The base file on disk is never modified. Uses safebin tools only.
# New code is pure shell; the compiled payload is base + pure-Zag driver.
set -u
export PATH="$HOME/safebin"

if [ "$#" -ne 1 ]; then
  echo "usage: certify_sweep.sh <base.zag>" >&2
  exit 2
fi
BASE="$1"
if [ ! -f "$BASE" ]; then
  echo "CERT-VERDICT FAIL (base file not found: $BASE)" >&2
  exit 2
fi
case "$BASE" in
  *.zag) ;;
  *) echo "CERT-VERDICT FAIL (not a .zag file: $BASE)" >&2; exit 2 ;;
esac

HERE="$(dirname "$0")"
DRIVER="$HERE/cert_driver_noevq.zag"
if [ ! -f "$DRIVER" ]; then
  echo "CERT-VERDICT FAIL (sweep driver missing: $DRIVER)" >&2
  exit 2
fi

SCRATCH="$(mktemp -d /tmp/cert_sweep_XXXXXX)" || {
  echo "CERT-VERDICT FAIL (could not create scratch dir)" >&2
  exit 2
}
[ -d "$SCRATCH" ] || { echo "CERT-VERDICT FAIL (scratch dir missing)" >&2; exit 2; }
trap 'rm -rf "$SCRATCH"' EXIT INT TERM

BASE_SHA="$(sha256sum "$BASE" | cut -d' ' -f1)"
cp "$BASE" "$SCRATCH/base.zag"
MAINLINE="$(grep -n '^fn main(' "$SCRATCH/base.zag" | head -1 | cut -d: -f1)"
if [ -n "$MAINLINE" ]; then
  # Trim the base's own main from the SCRATCH COPY ONLY.
  head -n $((MAINLINE - 1)) "$SCRATCH/base.zag" > "$SCRATCH/base_nomain.zag"
  mv "$SCRATCH/base_nomain.zag" "$SCRATCH/base.zag"
  echo "CERT note: base defines fn main (line $MAINLINE); scratch copy trimmed, on-disk base untouched"
fi
EVQ="$(grep -c '^fn ev_query(' "$SCRATCH/base.zag")"
echo "CERT note: base ev_query definitions: $EVQ (driver glue dropped, base entry point under test)"
cat "$SCRATCH/base.zag" "$DRIVER" > "$SCRATCH/cert_full.zag"
echo "CERT base=$BASE sha256=$BASE_SHA"

if ! znc "$SCRATCH/cert_full.zag" -o "$SCRATCH/cert_bin" > "$SCRATCH/compile.log" 2>&1; then
  echo "CERT-VERDICT FAIL (compile error; log below)"
  cat "$SCRATCH/compile.log"
  exit 1
fi
grep -q "wrote native" "$SCRATCH/compile.log" || {
  echo "CERT-VERDICT FAIL (no binary written; log below)"
  cat "$SCRATCH/compile.log"
  exit 1
}

i=1
PREV=""
DETOK=1
while [ "$i" -le 3 ]; do
  if ! timeout 300 "$SCRATCH/cert_bin" > "$SCRATCH/run$i.txt" 2>"$SCRATCH/run$i.err"; then
    echo "CERT-C DETERMINISM run$i TIMEOUT/CRASH FAIL"
    DETOK=0
    break
  fi
  H="$(sha256sum "$SCRATCH/run$i.txt" | cut -d' ' -f1)"
  echo "CERT-C run$i sha256=$H"
  if [ -n "$PREV" ] && [ "$H" != "$PREV" ]; then
    DETOK=0
  fi
  PREV="$H"
  i=$((i+1))
done
if [ "$DETOK" -eq 1 ]; then
  echo "CERT-C DETERMINISM 3/3 byte-identical PASS"
else
  echo "CERT-C DETERMINISM FAIL"
fi

A="FAIL"; B="FAIL"; D="FAIL"
grep -q "^CERT-A LEAK .* PASS$" "$SCRATCH/run1.txt" 2>/dev/null && A="PASS"
grep -q "^CERT-B ARENA .* PASS$" "$SCRATCH/run1.txt" 2>/dev/null && B="PASS"
grep -q "^CERT-D CORRECT PASS$" "$SCRATCH/run1.txt" 2>/dev/null && D="PASS"
echo "CERT-A LEAK $A"
echo "CERT-B ARENA $B"
echo "CERT-D CORRECT $D"

echo "--- run1 output ---"
cat "$SCRATCH/run1.txt"

if [ "$A" = "PASS" ] && [ "$B" = "PASS" ] && [ "$D" = "PASS" ] && [ "$DETOK" -eq 1 ]; then
  echo "CERT-VERDICT PASS (A=$A B=$B C=PASS D=$D)"
  exit 0
fi
echo "CERT-VERDICT FAIL (A=$A B=$B C=$([ "$DETOK" -eq 1 ] && echo PASS || echo FAIL) D=$D)"
exit 1
