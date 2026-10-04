#!/bin/sh
# cert_hostadapter.sh <adapter.zag> <hostbase.zag> -- host+adapter cert.
# Usage: cert_hostadapter.sh /path/to/adapter.zag /path/to/hostbase.zag
#
# Certifies a host-dependent adapter layer (e.g. xio_core2.zag) against a
# trial-family host base (e.g. composition_collapse/cl_full.zag). The
# adapter must classify as ADAPTER under the certify_base_v2 rules
# (host-dependent layer, no trial substrate); the host must classify as
# BASE (defines tnn2_init). Anything else is NOT APPLICABLE, not FAIL.
#
# The host's own main is trimmed from the SCRATCH COPY ONLY so the
# adapter driver's main links; the adapter must not define main or
# ev_query (both would collide with the host). On-disk files are never
# modified.
#
# Checks (pure-Zag driver, 3 deterministic runs, 300s timeout each):
#   AC2 REGISTRY    empty registry; xio_build field layout; find/count
#   AC3 FAILCLOSED  garbage exec -> -999999; no-adapter -> -2; bad
#                   expected -> -2; sclass/oty/dep_rel/stage on
#                   graphless nodes fail closed
#   AC4 CLASS2      hand-built class-2 MAP roundtrip through the host:
#                   oty/sclass/dep_rel/stage_exec re-derivation
#   AC5 ADAPT       two-MAP value-level handoff via xio_build/exec/adapt
#   AC6 GATE        sclass mismatch gate: same-class pairs never
#                   attempted, cross-class attempts fail closed
# Verdicts: XIO-CERT-VERDICT PASS | FAIL | NOT APPLICABLE.
# Exit codes: 0 PASS, 1 FAIL, 3 NOT APPLICABLE, 2 usage error.
set -u
export PATH="$HOME/safebin"

if [ "$#" -ne 2 ]; then
  echo "usage: cert_hostadapter.sh <adapter.zag> <hostbase.zag>" >&2
  exit 2
fi
ADAPTER="$1"
HOST="$2"
for f in "$ADAPTER" "$HOST"; do
  case "$f" in
    *.zag) ;;
    *) echo "XIO-CERT-VERDICT NOT APPLICABLE (UNKNOWN: not a .zag file: $f)" >&2; exit 3 ;;
  esac
  if [ ! -f "$f" ]; then
    echo "XIO-CERT-VERDICT NOT APPLICABLE (UNKNOWN: file not found: $f)" >&2
    exit 3
  fi
done

HERE="$(dirname "$0")"
DRIVER="$HERE/cert_adapter_driver.zag"
if [ ! -f "$DRIVER" ]; then
  echo "XIO-CERT-VERDICT FAIL (adapter driver missing: $DRIVER)" >&2
  exit 1
fi

AD_SHA="$(sha256sum "$ADAPTER" | cut -d' ' -f1)"
HO_SHA="$(sha256sum "$HOST" | cut -d' ' -f1)"
echo "XIO-CERT adapter=$ADAPTER sha256=$AD_SHA"
echo "XIO-CERT host=$HOST sha256=$HO_SHA"

# ---- classify the adapter (same rules as certify_base_v2) ----
if [ "$(grep -c '^fn tnn2_init(' "$ADAPTER" || true)" -gt 0 ]; then
  echo "XIO-CERT-VERDICT NOT APPLICABLE (BASE: adapter file defines trial substrate; use certify_base_v2)"
  exit 3
fi
if [ "$(grep -c '^fn main(' "$ADAPTER" || true)" -gt 0 ]; then
  echo "XIO-CERT-VERDICT FAIL (adapter defines fn main; an adapter layer must not)"
  exit 1
fi
PROBE="$(mktemp -d /tmp/certv2_haprobe_XXXXXX)" || {
  echo "XIO-CERT-VERDICT NOT APPLICABLE (UNKNOWN: could not create probe dir)" >&2
  exit 3
}
cp "$ADAPTER" "$PROBE/cand.zag"
printf 'fn main()void { return; }\n' >> "$PROBE/cand.zag"
if znc "$PROBE/cand.zag" -o "$PROBE/probe_bin" >"$PROBE/probe.log" 2>&1; then
  echo "XIO-CERT-VERDICT NOT APPLICABLE (MECHANISM-EXPERIMENT: adapter file compiles standalone; not a host-dependent layer)"
  rm -rf "$PROBE"
  exit 3
fi
if ! grep -q 'call to unknown function' "$PROBE/probe.log"; then
  ERR="$(grep -m1 -i 'error' "$PROBE/probe.log" | head -c 160 || true)"
  echo "XIO-CERT-VERDICT NOT APPLICABLE (UNKNOWN: adapter probe compile failed otherwise: $ERR)"
  rm -rf "$PROBE"
  exit 3
fi
rm -rf "$PROBE"
echo "XIO-CERT-CLASS adapter=ADAPTER host=BASE"

# ---- classify the host ----
if [ "$(grep -c '^fn tnn2_init(' "$HOST" || true)" -eq 0 ]; then
  echo "XIO-CERT-VERDICT FAIL (host is not a trial base: no tnn2_init)"
  exit 1
fi

SCRATCH="$(mktemp -d /tmp/certv2_hostadapt_XXXXXX)" || {
  echo "XIO-CERT-VERDICT FAIL (could not create scratch dir)" >&2
  exit 1
}
[ -d "$SCRATCH" ] || { echo "XIO-CERT-VERDICT FAIL (scratch dir missing)" >&2; exit 1; }
trap 'rm -rf "$SCRATCH"' EXIT INT TERM

cp "$HOST" "$SCRATCH/host.zag"
MAINLINE="$(grep -n '^fn main(' "$SCRATCH/host.zag" | head -1 | cut -d: -f1 || true)"
if [ -n "$MAINLINE" ]; then
  head -n $((MAINLINE - 1)) "$SCRATCH/host.zag" > "$SCRATCH/host_nomain.zag"
  mv "$SCRATCH/host_nomain.zag" "$SCRATCH/host.zag"
  echo "XIO-CERT note: host defines fn main (line $MAINLINE); scratch copy trimmed, on-disk host untouched"
fi
cp "$ADAPTER" "$SCRATCH/adapter.zag"
cat "$SCRATCH/host.zag" "$SCRATCH/adapter.zag" "$DRIVER" > "$SCRATCH/xio_full.zag"

if ! znc "$SCRATCH/xio_full.zag" -o "$SCRATCH/xio_bin" > "$SCRATCH/compile.log" 2>&1; then
  echo "XIO-CERT-VERDICT FAIL (compile error: adapter surface not satisfied by host; log below)"
  cat "$SCRATCH/compile.log"
  exit 1
fi
grep -q "wrote native" "$SCRATCH/compile.log" || {
  echo "XIO-CERT-VERDICT FAIL (no binary written; log below)"
  cat "$SCRATCH/compile.log"
  exit 1
}
echo "XIO-CERT note: host+adapter+driver compiled; adapter host-function surface satisfied"

i=1
PREV=""
DETOK=1
while [ "$i" -le 3 ]; do
  if ! timeout 300 "$SCRATCH/xio_bin" > "$SCRATCH/run$i.txt" 2>"$SCRATCH/run$i.err"; then
    echo "XIO-CERT determinism run$i TIMEOUT/CRASH FAIL"
    DETOK=0
    break
  fi
  H="$(sha256sum "$SCRATCH/run$i.txt" | cut -d' ' -f1)"
  echo "XIO-CERT run$i sha256=$H"
  if [ -n "$PREV" ] && [ "$H" != "$PREV" ]; then
    DETOK=0
  fi
  PREV="$H"
  i=$((i+1))
done
if [ "$DETOK" -eq 1 ]; then
  echo "XIO-CERT DETERMINISM 3/3 byte-identical PASS"
else
  echo "XIO-CERT DETERMINISM FAIL"
fi

AC2="FAIL"; AC3="FAIL"; AC4="FAIL"; AC5="FAIL"; AC6="FAIL"
grep -q "^XIO-AC2 REGISTRY .* PASS$" "$SCRATCH/run1.txt" 2>/dev/null && AC2="PASS"
grep -q "^XIO-AC3 FAILCLOSED .* PASS$" "$SCRATCH/run1.txt" 2>/dev/null && AC3="PASS"
grep -q "^XIO-AC4 CLASS2 .* PASS$" "$SCRATCH/run1.txt" 2>/dev/null && AC4="PASS"
grep -q "^XIO-AC5 ADAPT .* PASS$" "$SCRATCH/run1.txt" 2>/dev/null && AC5="PASS"
grep -q "^XIO-AC6 GATE PASS$" "$SCRATCH/run1.txt" 2>/dev/null && AC6="PASS"
echo "XIO-AC2 REGISTRY $AC2"
echo "XIO-AC3 FAILCLOSED $AC3"
echo "XIO-AC4 CLASS2 $AC4"
echo "XIO-AC5 ADAPT $AC5"
echo "XIO-AC6 GATE $AC6"

echo "--- run1 output ---"
cat "$SCRATCH/run1.txt"

if [ "$AC2" = "PASS" ] && [ "$AC3" = "PASS" ] && [ "$AC4" = "PASS" ] && [ "$AC5" = "PASS" ] && [ "$AC6" = "PASS" ] && [ "$DETOK" -eq 1 ]; then
  echo "XIO-CERT-VERDICT PASS (AC2=$AC2 AC3=$AC3 AC4=$AC4 AC5=$AC5 AC6=$AC6 C=PASS)"
  exit 0
fi
echo "XIO-CERT-VERDICT FAIL (AC2=$AC2 AC3=$AC3 AC4=$AC4 AC5=$AC5 AC6=$AC6 C=$([ "$DETOK" -eq 1 ] && echo PASS || echo FAIL))"
exit 1
