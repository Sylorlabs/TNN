# RESULTS — Step 1c: sealed verdict record + two coincident firewalls + ledger canonicalization

**Verdict: GO.** Zero kill bars fired.

**Prereg:** `PREREG_FIREWALLS.md`, committed frozen before implementation at
`57773c3ada3556ffb960d527ba382bbee5cecca9` (2026-09-20). No prereg amendment
was created; every fix below was implementation-to-prereg, not prereg-to-code.

**Builds (pure Zag, zero RNG, znc `abed8aa1`):**
- `fw_bin`: `73b51ac99f54e21c75aceecee9ab5ebb880bbb18760b7e252d900654161990d5`
  (two invocations, byte-identical rebuild verified by `cmp`)
- `fwgate_bin`: `bd649a9eb956c1df55a4cc2f87f1011bd72da31aabd11c5db6021fb1b1592809`

**Step 1d integration: PENDING** (sibling builder owns phrasing variation;
Step 1c passes every bar independently).

## Kill-bar scorecard

| Bar | Requirement | Result |
|---|---|---|
| S12-K1 | 200 pairs × 4 modes, byte-identical record/digest/ledger | 200/200 cells (`run_verdictinv.txt`) |
| S12-K2 | 5/5 tamper probes detected | 5/5 (`run_tamper.txt`) |
| S12-K3 | static no-backchannel audit clean | 0 violations, 7 files (`run_gate_clean.txt`) |
| S13-a | 1,600 replays, zero MemOp divergence | 200/200 cells, 0 divergences |
| S13-b | zero ledger divergence | 0 divergences (`run_meminv.txt`) |
| S13-c | read-watch silent across judge calls | 0 deltas; negative control `WATCH_LIVE,1` (planted read trips it) |
| S13-d | no mem_judge→vary edge | gate clean (import + token) |
| S14-K1 | 8×32 cells, identical (refuse, code, cited-set) | 8/8 (`run_refuseinv.txt`) |
| S14-K2 | no EXPR/RNG/clock path into REFUSE_DECIDE | gate clean on `fw_refuse.zag` |
| S14-K3 | no rendered refusal contradicts its triple | 0 contradictions (full-depth cite-set check) |
| S14-K4 | ≥2 distinct renderings per family | 0 vacuous cells (retry path never needed) |
| S15 | 200 forced-variant pairs; replay; byte-scan; recompute | 200/200 pairs, 0 failures (`run_ledginv.txt`) |
| S20-K1 | 20/20 planted violations detected | 20/20, 0 missed (`run_gate_probes.txt`) |
| S20-K2 | 0 false positives on clean build | 0 violations |
| S20-K3 | 100×10 wiring probes change nothing | 100/100 (`run_wiring.txt`) |
| S20-K4 | logged-state replay byte-identical | 200/200 (`run_replay.txt`) |
| S20-K5 | MUST-NOT fields stable at identical state | covered by wiring + replay |

Determinism: `verdictinv` rerun byte-identical (`cmp` clean). No RNG,
wall-clock, or float token in any firewall module (static grep).

## Implementation notes (no prereg change)

1. **VARIANT_EQ semantics.** The prereg freezes both the chain formula
   (`entry_hash` commits to the payload, which carries `variant_id`) and the
   kill condition ("byte-identical except `variant_id`"). A literal byte
   comparison is unsatisfiable under a hash chain: the forced `variant_id`
   mechanically changes the entry's `entry_hash` and every downstream
   `prev_hash`/`entry_hash`. `fw_led_cmp` therefore implements the coherent
   reading the prereg's §3 states explicitly ("identical ledger **payload**
   bytes across modes"): both chains verify individually, then header fields
   and payload bytes are compared with only the 2 `variant_id` bytes masked.
   Chain-mechanical fields are excluded from the cross-mode comparison because
   they are fully determined by the payloads + the frozen chain formula.
2. **STATE_HASH preimage.** It commits only to judgment-side state
   (clock, ctx, focus, store, strengths), never to `led.prev`; committing to
   the chain would have made the payload a function of `variant_id` and
   broken VARIANT_EQ. The chain itself is anchored by `prev_hash`/`entry_hash`.
3. **Zag string-literal cast.** `"d" as u8` does not yield 100 — it yields an
   address-derived byte that differs per occurrence. All such uses were
   replaced with numeric ASCII codes (found via an isolated compiler probe;
   the tamper battery caught it: 0/5 before the fix, 5/5 after).
4. **Gate bug, caught by its own trial.** `g_probe_kind` returned the judge
   token list for `vary`-kind probes; the 20-probe trial caught it (16/20
   before, 20/20 after). The gate is thus tested by the same adversarial
   method it applies.

## What this proves

Expression variation is structurally incapable of changing verdicts, memory
decisions, integrity refusals, or ledger contents: the verdict is sealed
(write capability consumed) and ledger-appended before the phase seam flips;
the expression side receives only a sealed copy, a state digest, and a mode;
the read-watch, call-site rule, import allowlist, and wire-token audit are
each covered by a live negative control (planted violation or planted read)
that the harness demonstrably catches.

## Files

Sources: `fw_ledger.zag fw_judge.zag fw_refuse.zag fw_vary.zag fw_verdict.zag
fw_run.zag fwmain.zag fwgate.zag`, `substrate/`, `probes/` (20).
Evidence: `run_*.txt`, `build_hashes.txt`, `sha256sums.txt`.
Runner: `run_step1c.sh` (exit 0 = all green; build gate fails before trials).
