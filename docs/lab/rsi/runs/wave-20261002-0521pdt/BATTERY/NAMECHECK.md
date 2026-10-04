# NAMECHECK.md: battery E10, wave wave-20261002-0521pdt

Lane: BATTERY-E9 (fresh sealed adversarial battery on TNN-2's three new
mechanisms). Battery generation: E10 (tenth). Rationale for the
generation name: battery E9 was completed by the wave-20261002-0221pdt
lane BATTERY (PREREG_BATTERY_E9.md frozen in commit 495d30fce, all nine
worlds run 3x byte-identical, verdicts M1/M2/M3 MECHANISM-WEAK,
SEALED_RESULTS.md committed). The task premise ("E9 in flight") was
stale; re-running E9's identical worlds would not be a fresh battery.
E10 is a NEW sealed battery: nine new worlds on the same three
mechanisms, materially different from FW1-FW9, the 1421pdt battery, and
E9, applying all six triviality-review corrections plus the lessons
queued by E9 (orphan-poisoning follow-up family, retrieval-based E-K15
rewording, pre-freeze barspec index machine check).

## Step 0 (toolchain guard, mandatory first)

- Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`:
  SAFEBIN-READY, 36 tools, `python3` and `python` absent from safebin PATH.
- Exported `PATH="$HOME/safebin"` for all subsequent work in this lane.
- Verified: `which python3` returns nothing (exit 1) under the safebin PATH.
- Pinned znc: `/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`,
  matches the sealed freeze evaluation record).
- PURE ZAG ONLY for all research logic (worldgen, scoring, state
  inspection, degenerate-walk generation). Shell (safebin bash/awk/grep)
  only for byte checks, file transport, hash manifests, and the
  deterministic interactive driver loop.
- Pinned-compiler rule observed in all new Zag code: no `as *i32` +
  `q[0..n]` slice construction inside functions; u8-cell loop idiom
  with little-endian pack/unpack helpers.
- Forbidden executable invoked: none. (Any invocation would be an
  automatic PROCESS-FAIL of this wave.)
