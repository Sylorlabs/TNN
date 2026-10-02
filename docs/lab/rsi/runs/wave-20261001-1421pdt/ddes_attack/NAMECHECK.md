# NAMECHECK: ddes_attack worker (wave-20261001-1421pdt, step 6 alternative-explanation attack on DDES V2 BUILD-PASS)

## Step 0: worker toolchain guard (MANDATORY FIRST STEP)

- Ran `bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`: SAFEBIN-READY, 36 tools linked, pinned znc OK (`znc_linux_x86_64_abed8aa1`), verify step printed "python3 absent from safebin PATH (OK)".
- Exported `PATH="$HOME/safebin"`.
- `which python3` prints nothing (exit 1). `which python` also prints nothing.
- Toolchain verification: pure Zag only. Every program written and run in this lane is compiled with the pinned znc. Zero Python at any stage (no glue, analysis, verifiers, harnesses). Shell used only to invoke znc, move/copy files, and run sha256sum/cmp/diff/grep from the safebin allowlist.
- No git commit, push, checkout, or branch change performed or planned; all files left uncommitted.

## Assignment

Step 6 of the 11-step pipeline: alternative-explanation attack on the
ddes_followup V2 BUILD-PASS (RESULT at
docs/lab/rsi/runs/wave-20261001-1121pdt/ddes/RESULT_DDES_FOLLOWUP_V2.md;
frozen prereg at
docs/lab/rsi/runs/wave-20261001-0821pdt/ddes/PREREG_DDES_FOLLOWUP_V2.md
plus AMENDMENT1). Claim under attack: K-G2..K-G9 pass on sealed
evaluation; World F FLAG line exact with correct convergence;
SCHEMA-RECORD byte-exact; SCAFFOLD-CALLS 0; World G CONVERGE-OK with
persisted predictions agreeing with EXEC; RECORD-LOAD byte-identical;
zero derivation markers in phase 2; static audit confirms
apply_persisted makes zero derivation-path calls. Bounded L2, no L3.

## Attack plan (all harnesses in Zag)

1. MEMORIZATION (mem_attack.zag): pure lookup table keyed on
   (world, config) reproducing the sealed trace byte-exact; cmp
   against run1.txt; 3/3 byte-identical reruns. Tests whether the
   evaluation protocol's output-level checks can distinguish the
   claimed mechanism from rote printing.
2. DERIVATION LEAK (leak_audit.zag): independent static audit. Embeds
   the ddesp2.zag source as a string literal (mechanically escaped,
   byte-faithful), strips comments and string literals, builds the
   call graph, BFS from apply_persisted over transitive callees,
   reports reachability of compute_arrivals, compute_frontier,
   synthesize_plan, predict, ddes_world. Does not trust the prior
   grep audit; independent scanner logic.
3. PHASE-2 CIRCULARITY (flow_slice.zag): data-flow slice. Mechanically
   extracts every set32(learner_state,...) site and checks whether the
   stored value is a numeric literal; lists ddes_world's return
   statements to check whether any derived value (best_v, best_t,
   p0, p1) flows out; checks the SCHEMA-RECORD emit site. Tests
   whether phase-2 predictions were produced by phase-1 computation
   or authored as constants.
4. SCHEMA BYTE-EXACTNESS (trivial_formatter.zag): prints the
   RECORD-LOAD line from a hardcoded literal with zero record reads
   and zero learner_state, then byte-compares the field substring
   against the SCHEMA-RECORD literal. Tests whether the
   byte-exactness check is load-bearing or formatter-agnostic.

## Verdict scale

Per attack: ATTACK-SUCCEEDS (claim weakened, exact evidence cited) or
ATTACK-FAILS (explanation excluded by evidence). Overall:
CLAIM-SURVIVES or CLAIM-WEAKENED.

## Results (20261001-1421pdt)

All four attacks executed in pure Zag (pinned znc, safebin PATH, zero
Python), each with 3/3 byte-identical deterministic reruns.

- Attack 1 MEMORIZATION: ATTACK-SUCCEEDS (scoped). mem_attack.zag, a
  pure (world, config) lookup table, reproduces the sealed run1.txt
  byte-exact (sha256 b8bc5fa9cd2feec8c239baad42eba88438c9dea4341b226189bcc81cca6fcde3,
  3/3, zero stderr). The mechanical output-level bars cannot
  distinguish it from the claimed mechanism.
- Attack 2 DERIVATION LEAK: ATTACK-FAILS. Independent Zag static audit
  (leak_audit.zag: comment/string stripping, call-graph BFS from
  apply_persisted over 24 parsed functions): all five derivation
  targets NOT-REACHED. Prior audit independently confirmed.
- Attack 3 PHASE-2 CIRCULARITY: ATTACK-SUCCEEDS (scoped, disclosed).
  flow_slice.zag proves all 6 learner_state writes in main() are
  numeric literals, ddes_world returns only control (0/ok), and all 6
  reads are in apply_persisted. Phase-2 predictions were authored, not
  computed; the surviving statement is "verified constants persist and
  are reused post-disconnect".
- Attack 4 SCHEMA BYTE-EXACTNESS: ATTACK-SUCCEEDS (narrow).
  trivial_formatter.zag passes the K-G7 field byte-exactness check
  with zero record reads; the check is formatter-agnostic.

Overall: CLAIM-WEAKENED (scoped). The bounded-L2 ceiling already
prices this in (C0-A..D fail); no hidden L3, no leak, no fraud.
Full evidence in ATTACK_DDES_V2_STEP6.md. Nothing committed.
