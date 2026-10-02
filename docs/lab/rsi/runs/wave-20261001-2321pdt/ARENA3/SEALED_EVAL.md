# SEALED EVALUATION: Arena TRX (wave-20261001-2321pdt, ARENA3 lane)

Frozen prereg: PREREG_ARENA_TRANSFER.md (committed alone at 829208f99,
strictly before the implementation commit 9191e71de; commit-order
self-check verified: prereg 2026-10-02 06:40:52 UTC, implementation
2026-10-02 06:43:17 UTC). No amendment was needed; the prereg ran unchanged.

## 1. Artifact identities

| Artifact | SHA-256 | Status |
|---|---|---|
| TRX base source (INQ candidate, committed) | 456589d6aa01247596fa69b84289b9e2c7739e1ec755cfb1946fbbab14cbecce | matches ARENA lane record |
| TRX source (committed 9191e71de) | 24b6609838c94951d46bc720e977d3c4da71d07981e1178d53144ca2b17af692 | 1399 lines; +80/-0 vs INQ base |
| TRX binary bin/trx | 46731d65c79d11ffcb41fee4c458e13b9e8f6cd403f6a10e02d5242aaae997ff | rebuild from committed source byte-identical |
| world_gen (rebuilt) | c4c8340c818e6848c88e34f1989bf382ff097c69a71d6621c6bf28b58dc85211 | matches refreeze record |
| arena (rebuilt) | 3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076 | matches refreeze record |
| turns.jsonl (regenerated) | 0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469 | matches sealed world, 131 turns, 68 items |
| PRE-RUN answer_key.json | a05ef916122ea9643fa69e4a4973b94ea1c603da642d9bd07788f61b89a07a51 | hash only, never opened; matches ARENA lane pre-run hash |
| K6a binary (prod off) | f4378427e17fcaa1c19eece7034181b3335d4e355123c16da415e3ea38f47a01 | one-line source delta (TRX_PROD_ON=0) |
| K6b binary (class off) | 4a86041fce50ce71c4e1e291564b9197b45f931cfd02274ecab62c0c02bc58f1 | one-line source delta (TRX_CLASS_ON=0) |

The TRX source is the INQ candidate plus the marked TRX section
(parse_remap with permutation validation, TRX_PROD_ON/TRX_CLASS_ON flags,
remap_prod and remap_class head handlers). Diff vs INQ base: 80 lines
added, 0 removed, all ASCII.

## 2. Sealed scores (3/3 runs identical)

| Cap | n | INQ baseline | TRX run1 | TRX run2 | TRX run3 |
|-----|---|--------------|----------|----------|----------|
| 1 | 6 | 1.000 | 1.000 | 1.000 | 1.000 |
| 2 | 4 | 1.000 | 1.000 | 1.000 | 1.000 |
| 3 | 6 | 1.000 | 1.000 | 1.000 | 1.000 |
| 4 | 4 | 1.000 | 1.000 | 1.000 | 1.000 |
| 5 | 6 | 1.000 | 1.000 | 1.000 | 1.000 |
| 6 | 3 | 1.000 | 1.000 | 1.000 | 1.000 |
| 7 | 3 | 1.000 | 1.000 | 1.000 | 1.000 |
| 8 | 4 | 1.000 | 1.000 | 1.000 | 1.000 |
| 9 | 3 | 0.000 | 0.000 | 0.000 | 0.000 |
| 10 | 2 | 1.000 | 1.000 | 1.000 | 1.000 |
| 11 | 2 | 1.000 | 1.000 | 1.000 | 1.000 |
| 12 | 6 | 0.000 | 1.000 | 1.000 | 1.000 |
| 13 | 6 | 1.000 | 1.000 | 1.000 | 1.000 |
| 14 | 6 | 1.000 | 1.000 | 1.000 | 1.000 |
| 15 | 1 | 0.000 | 0.000 | 0.000 | 0.000 |
| 16 | 6 | 1.000 | 1.000 | 1.000 | 1.000 |
| TOTAL | 68 | 0.853 | 0.941 | 0.941 | 0.941 |

64/68 = 0.941 (scorer displays truncated 0.941). Gain: +6 items, all C12.
tool_calls stays 7 (the INQ count); no new observe requests are emitted by
TRX, which parses the relabeling from the question instead of asking.

## 3. Kill bar verdicts

K1 (C12 = 6/6): PASS. Items 32..34 reply "2,3,0" (learned B template
(0,1,2) under the question-parsed remap [2,3,0,1]); items 35,37 reply
"yes" (candidate (0,3,2) equals the remapped learned A template);
item 36 replies "no" (candidate (1,3,2) differs). All six equal the
frozen scorer keys (plain streq rule for C12).

K2 (zero regressions): PASS. Per-capability scores on C1-C11 and C13-C16
byte-identical to the INQ BUILD-PASS record on all three runs; total
64/68. The stripped reply-stream diff vs the INQ run1 touches exactly 6
lines: turns 76..81 (items 32..37), UNKNOWN -> exact answers. The INQ
run1 stripped hash re-verified as
3b1911236a81c742204f0800da14933ac713ed1e23c9905cf05bc4693dcbb46d,
identical to the ARENA lane record.

K3 (determinism): PASS. 3/3 byte-identical stripped reply streams
(sha256 e692b5a47ebb4a0f1405e6c486c087a2358f5181853ca06290cf708d77fc69a5;
ms and rss_kb excluded, the v6 K6 exclusion class) and 3/3 byte-identical
stderr traces (sha256 d664b9eb600250e5fb5a8f7a1ee98b9f2710cc416305bfd5e59d7e6d8be76488,
identical to the INQ lane trace; TRX emits no new trace lines). Zero RNG
in decision paths.

K4 (pure Zag): PASS. `which python3` and `which python` print nothing at
lane start and lane end (safebin PATH throughout). Only znc-built binaries,
bash, safebin coreutils, and git read/commit ops were used. No
PROCESS-FAIL event.

K5 (sealed validity): PASS. world_gen and arena rebuilt from committed
sources with hashes matching the refreeze record; turns.jsonl regenerated
byte-identical to the sealed world; pre-run hashes recorded before the
contestant ran (turns.jsonl re-verified unchanged after the runs);
the key file was hashed but never opened; worlddir is
arg-presence-checked only. Grep audit of the TRX mechanism source for the
C12 literal answer string "2,3,0" and the remap literal "2,3,0,1": zero
hits. Disclosure (per prereg): the worker saw the C12 question strings
while verifying the turn protocol from the committed 1721pdt sealed
world; expected answers were derived mechanically from the generator
logic plus those question strings only; the keys were never opened; the
mechanism parses the remap and triples from the turn stream at runtime;
the grep audit is the evidence.

K6 (negative controls): PASS.
K6a (TRX_PROD_ON=0, one-line delta): remap_prod replies stay UNKNOWN;
C12 = 3/6 (class half intact: yes/no/yes), total 61/68 = 0.897.
K6b (TRX_CLASS_ON=0, one-line delta): remap_class replies stay UNKNOWN;
C12 = 3/6 (prod half intact: 3 x "2,3,0"), total 61/68 = 0.897.
Both halves are causal; neither ablation disturbs any other capability.

K7 (honesty preserved): PASS. All 3 C7 unknowable items reply exactly
"UNKNOWN" in all three sealed runs. Dev smoke test (in /tmp, never
sealed) verified: remap_prod on a non-template input replies UNKNOWN,
remap_prod with an invalid (duplicate) remap replies UNKNOWN,
remap_class with an invalid remap replies UNKNOWN, and remap_prod with
no learned templates replies UNKNOWN. No hallucination paths exist.

K8 (architecture): PASS. Delta: 80 lines added, 0 removed vs the INQ
base. 0 new modes, 0 bridges, 0 routers, 0 task-specific admission gates,
0 hardcoded semantic cases, 0 hardcoded entities/attrs/values/remaps/
templates/answers (keyword scan of added lines for
mode/bridge/router/admission/gate: 0 hits). The two insertion points
dispatch on question heads in the existing test handler, parallel to
zemprod/zemclass, with no capability-number gating. Learner-state
structures created: none new; TRX reuses the exposure-induced class-A/B
templates. Capability comes from learner state plus the question-parsed
relabeling, not from new source logic.

K9 (no L3 claim): PASS (disclaimer recorded). TRX does not meet
Criterion 0: the "apply the named relabeling to the learned template"
semantics is researcher-authored handler logic (fails C0-A); the
relabeling form is fixed and parsed, not incrementally constructed from
experience (fails C0-B); no unforeseen representational forms are
produced (fails C0-C); reusing the learned A/B templates across a
notation is structural reuse, not the invention of a new representation
(fails C0-D). Plainly: TRX is L1/L2 template-relabeling transfer
infrastructure, not L3 representational invention. No L3 claim is made.

## Verdict: BUILD-PASS

K1 through K9 all PASS. C12 moves 0.000 -> 1.000; total moves 58/68
(0.853) -> 64/68 (0.941) with zero regressions on the other 15
capabilities; 3/3 byte-identical reruns.

## Scope reminders (unchanged)

TRX is a CANDIDATE mechanism only. No L3 claim (K9), no TNN-2 substrate
claim, no TNN-beats-LLM claim. The canonical 0.573 is not moved by this
result (only a clean refreeze reproducing composition without
contamination can move it). The LLM baseline comparison remains pending
credentials and is out of scope. Remaining sealed zeros: C9 causal,
C15 goal. TRX was built on the INQ candidate; this lane's sealed run is
the integration test of the two candidates. ARENA2's lane directory was
empty at lane start, so no sibling capability collision was possible;
per the frozen prereg assumption, if ARENA2 later freezes a C12 prereg,
the two lanes are independent competing runs on the same capability.

## Toolchain

safebin PATH for the whole lane; `which python3` prints nothing
(re-verified at lane end); zero Python or other interpreter invocations;
shell only sequenced pinned znc, built binaries, git read/commit ops,
and file copies. No PROCESS-FAIL event. Zero em-dash bytes in lane docs
(verified by check_no_dash.sh before each commit).
