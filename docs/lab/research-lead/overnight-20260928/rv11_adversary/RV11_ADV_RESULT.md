# RV11-ADV RESULT: H-REVISE11 red team

**Date (UTC):** 2026-09-30
**Adversary prereg:** `cde064337` (committed alone before any attack
code, build, or run; pure Zag throughout)
**Target:** H-REVISE11 result `1a2fd99bd` (builder prereg `36b2fbc71`)
**Verdict: H-REVISE11 SURVIVES this red team (0/4 kill criteria fired)**

No em dashes in this document.

## Method

Attack harness `rv11_adv.zag` = lines 1-838 of the frozen
`revise11.zag` blob at `1a2fd99bd` (everything before `fn main`),
verified byte-identical against the frozen blob via `cmp`, plus an
attack-only `fn main`. Zero mechanism lines edited. The X-RV11-3 sweep
constructs stores by direct slot-byte writes using the mechanism's own
documented layout (so=56+(s-1)*64; set32 cpos/cval/nn; program bytes at
so+12; status at so+60), which is byte-identical to what `vs3_revise`
writes on a fresh store, and avoids EVIDENCE emit overhead. The X-RV11-1
P3b replication uses the real `vs3_revise` calls for full fidelity.
Built and run in /tmp/rv11adv only; no binaries committed.

Attack raw: `RV11_ADV_RAW.txt` (8,817,645 bytes), md5
`ea2637b940d8467c55d2272ff12c8764`, 3/3 byte-identical runs
(run1/run2/run3 all md5 `ea2637b940d8467c55d2272ff12c8764`).

## X-RV11-1: guard soundness (P3b replication + overreach attempt)

Exact P3b fixture replicated: P0=p0a ("zbq"->"qqq"); slot1 (0,122)
wprogP wrong PROVISIONAL; slot2 (1,98) p0aP correct most-recent;
input "zbq"; trusted label "qqq".

- `diagnose_rollback_check` returned exactly 0. PASS.
- Both slots remained PROVISIONAL (status 1) after the call. PASS.
- Exactly 1 GUARD line emitted between the P3B markers:
  `GUARD: no contradiction (store predicts trusted label); no state change`.
  PASS.
- Overreach attempt: the prereg defined overreach as a store where the
  guard fires yet the claim's own definition requires action. This is
  definitionally closed, not merely unobserved: the guard fires iff
  `vs3_apply(VS, inp)` predicts `true_out`; every action branch
  (Branch A, peeling, Branch B) requires the relevant store variant to
  mispredict `true_out`. A store cannot simultaneously predict and
  mispredict the label. The brute-force sweep below (320,868
  configurations) additionally confirms no configuration exhibits
  guard-fire plus state change, since all 122,952+74,964 non-guard
  configurations were classified and none reached the veto path.

X-RV11-1 HOLDS. No kill.

## X-RV11-2: exact counts (independent recount)

Pristine rebuild of `revise11.zag` from the frozen blob at
`1a2fd99bd`; compiled and run 3/3 byte-identical. Raw md5
`0fcb31f29db9d05a1c80809aa78619c3`, byte-identical to the frozen
`REVISE11_RAW.txt` blob at `1a2fd99bd` (verified via `cmp`).

- Source `ntest_total=ntest_total+1` increments: 145. Matches.
- Emitted `CHECK` lines: 129, all PASS, 0 FAIL. Matches.
- `GUARD` lines: exactly 2, at raw lines 276 and 295. Line 276 sits
  inside the `--- Phase P3b: veto (correct most-recent member, no
  action) ---` banner window (banner at line 273). Line 295 sits inside
  the `--- Phase Q1: guard closure (B-RV9-3 closed) ---` banner window
  (banner at line 292). Matches.
- Final line: `H-REVISE11 SURVIVES`. The `=== RESULT: 145/145 ===`
  line was confirmed in the earlier inspection.

X-RV11-2 HOLDS. No kill.

## X-RV11-3: Branch B veto reachability (brute-force sweep)

Configuration space: 1-3 revision slots; per slot cpos in {0,1,2},
cval in {98,113,122}, program in {p0aP correct, wprogP wrong, p0bP
identity}, status in {1 PROVISIONAL, 2 ACTIVE}; P0 in {p0a correct,
p0b wrong}; input "zbq"; trusted label "qqq". 54 + 2916 + 157464 =
160,434 configurations per P0 sweep; 320,868 total. Per
configuration: fresh store; skipped when the store predicts the label
(the guard's exact condition, verified with the guard's exact
predicate); otherwise firing set and `allmiss` computed with the
mechanism's own helpers; statuses snapshotted; `diagnose_rollback_check`
called; statuses re-checked. VETO-REACHED defined as allmiss==0 AND
rb==0 AND zero status change (the guard never fires in the tested
subset, so silent-0 with allmiss==0 uniquely identifies the Branch B
correct-member veto path).

P0-correct sweep: tested=74,964; skipped-guard=85,470; acted=74,964;
silent-allmiss1=0; veto=0; kill=0.
P0-wrong sweep: tested=122,952; skipped-guard=37,482; acted=10,008;
silent-allmiss1=112,944; veto=0; kill=0.

- `ADV-VETO-REACHED` lines in raw: 0. The veto is unreachable across
  the full swept space, confirming the disclosure. No DOWNGRADE.
- `ADV-VETO-KILL-SIGNAL` lines in raw: 0. No wrong PROVISIONAL firing
  member ever survived a veto-path call. No KILL.
- Sanity: per-sweep totals sum to 160,434 (tested + skipped-guard),
  confirming full coverage of the enumerated space.
- The 112,944 silent-allmiss1 P0-wrong configurations are the claimed
  no-action path: no correct firing member exists, the skip/peel tests
  find no restorable prefix, and the mechanism returns 0 with zero
  state change. All 10,008 acted P0-wrong configurations returned
  nonzero or changed state through Branch A, the peel, or Branch B.

X-RV11-3 HOLDS (veto unreached; no survivor violation). No kill, no
downgrade.

## X-RV11-4: regression diff audit (revise10 -> revise11)

Blob-to-blob diff of `aa422610f:revise10.zag` vs
`1a2fd99bd:revise11.zag`: 44 changed lines. Every changed line
classified after stripping diff prefixes and leading whitespace:

- 38 lines: `//` comments (header, P3b documentation correction,
  prereg references, expected-count comments, R10 disclosure text).
- 2 lines: the `=== H-REVISE10 ... ===` / `=== H-REVISE11 ... ===`
  banner emit pair.
- 4 lines: the `H-REVISE10 SURVIVES` / `H-REVISE11 SURVIVES` and
  `H-REVISE10 KILLED` / `H-REVISE11 KILLED` verdict emit pairs.
- 0 lines outside these categories.

Zero behavioral changes between H-REVISE10 and H-REVISE11, as the
builder claimed. X-RV11-4 HOLDS. No kill.

## Out-of-scope observation (no kill criterion, per prereg)

Robustness probe: one `diagnose_rollback_check` call with a 20-byte
input against the fixed 16-byte scratch buffers. Result: clean panic
`slice index out of bounds` (exit 1), in `vs3_apply` at
`pre[0..inp.len]`. This is a pre-existing design constraint of the
whole revise lineage (16-byte buffers sized for the len-3 test domain),
not an R11 regression. The panic is a bounds-checked abort, not silent
heap corruption. No verdict impact.

## Residual notes (not kill criteria)

1. The sweep space covers 1-3 slots, three programs, and the fixed
   ("zbq","qqq") pair. Larger slot counts, other inputs, and
   multi-node programs were not swept.
2. The overreach closure is definitional, resting on the code-reading
   that every action branch requires a mispredicting store variant.
3. The 16-byte scratch buffer bound above is untested territory for any
   input longer than 16 bytes; the mechanism panics cleanly rather than
   corrupting state.

## Verdict

H-REVISE11 SURVIVES this red team. All four frozen kill criteria held:
X-RV11-1 (guard sound, P3b replication exact, overreach definitionally
closed), X-RV11-2 (145/145, 129/129 CHECK PASS, 2 GUARD lines in the
correct phase windows, md5-identical raw), X-RV11-3 (Branch B veto
unreached across 320,868 configurations, zero survivor violations),
X-RV11-4 (zero non-comment, non-banner, non-verdict line changes
revise10 -> revise11).

## Governance and lineage disclosures

1. Adversary prereg `cde064337` was committed alone before any attack
   code, build, or run. Pure Zag throughout: implementation, builds,
   runs; analysis via shell grep/cmp/md5/diff/awk only. No Python at
   any step.
2. Mid-procedure incident: the VM wiped /tmp/rv11adv between two
   turns, destroying the first attack binary and its 3/3 raw outputs
   (md5 `ea2637b940d8467c55d2272ff12c8764`). The harness was rebuilt
   from the same frozen sources (mechanism region re-extracted and
   re-verified byte-identical; attack main rewritten identically) and
   rerun 3/3 byte-identical, reproducing the identical md5
   `ea2637b940d8467c55d2272ff12c8764` and identical sweep counters.
   The committed `RV11_ADV_RAW.txt` is the post-rebuild run1 output.
3. This red-team verdict concerns the R11 mechanism and its builder
   claims only. It does not adjudicate the standing H-REVISE7 through
   H-REVISE11 governance quarantine (the H-REVISE7 Python contamination
   and the unreproduced motivating finding), which remains open and is
   outside this adversary's scope.
4. Only owned paths staged:
   `docs/lab/research-lead/overnight-20260928/rv11_adversary/`.
