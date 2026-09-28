# RUNLOG — PRINCIPLES-FIRST live-ingestion hypothesis test

Date: 2026-09-24. Hypothesis (Micah): "Live ingestion is horrible probably
because it wasn't taught principles."

## Preregistration

- Frozen prereg: `PREREG_LI_PRINCIPLES.md`, committed BEFORE any
  result-producing run.
- Commit: `0516b8761dc6db848ccf5a11356d045eb9a09fe2` on branch `tnn-native-lab`
  (parent `ec8d5d1355f4898404a117f2f6bbe1550c4fa16d`).
- Blob SHA: `42eed528ea728e91a2873c3181ff555b72cccce0`, size 9579 bytes.
- Repo path: `docs/lab/knowledge/web_guides/live_ingest/principles/PREREG_LI_PRINCIPLES.md`.

## Build

- Compiler (pinned): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
- `instrument_control.zag` SHA-256
  `dafb2cb7a61451566da23d4c3cda711f59c2bda5df1b26298c6d24ea4080f761`
  — byte-identical to branch BF1
  (`docs/lab/knowledge/web_guides/live_ingest/variants/v-bf1/webg_bf1.zag`
  at commit `56432891`).
- `bin/webg_control` proven byte-identical (`cmp`) to a fresh compile of the
  branch BF1 source with the lab-standard `R33_NATIVE_IO_V1.zag`
  (`e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`).
- `instrument_principles.zag` SHA-256
  `ab8e1d675a7a6727f4540f0d41f763f1c767cec533efcb08adf05c3a8075539e`
  — BF1 + kernel fork. Deliberate diffs only:
  (a) `list_guides` accepts `e*` filenames; (b) kernel helpers
  (`wlist_has`, `syn_lookup`, `tokbytes_less`, `kernel_of`); (c) `run_calib_e`
  for CSENT/EXPECT-KERNEL and CPAIR/EXPECT-EQUAL; (d) `cmd_teach` installs
  E1–E6 and their `D|` directives; (e) `cluster_best` takes `kf,dt,dn` and
  clusters on the proposition kernel iff `D|KERNEL=on`; first original claim
  sentence retained as answer/provenance text; (f) `verdict_core` passes the
  installed directives into `cluster_best`.
  G4/BUGFIX-1/G6 gates, prohibited-string scan, semantic ledger: untouched.
- Analyzer notes A0107/A0101 appear identically (3 each) in control and
  principles builds — pre-existing BF1 notes, not introduced by the fork.
- Binaries are build artifacts; NEVER committed.

## Teach validation (smoke, no verdicts — pre-run)

- Control arm (`arm_control/guides` = G1–G7): `LEARN|G1..G6|INSTALLED|PASS`,
  `LEARN|G7|REJECTED|CALIB-FAIL`. Contract holds.
- Principles arm (`arm_principles/guides` = G1–G7 + E1–E6):
  `LEARN|E1..E6|INSTALLED|PASS`, `LEARN|G1..G6|INSTALLED|PASS`,
  `LEARN|G7|REJECTED|CALIB-FAIL`. Contract holds.
- Taught directives verified in `installed.txt`: `I|KERNEL|on`,
  `I|GLUE|<finite list>`, `I|SYN1|<classes>`, `I|SYN2|<classes>`.

## Guide SHAs (full)

- g1_query.txt: `d12d043e1ddf48d2544495b9e698e3e46d1888f2a1652498381e2cb455f38fdf`
- g2_select.txt: `f17ee7bc7817bd17bbad01189e770ab24356e108f27cfae005e8e1578070e593`
- g3_claim.txt: `5889ec862b19af3c3d20f5e637cde38052d2b86c8c12f1271067d2eb2d3a038e`
- g4_corroborate.txt: `2d16355ba84563d93e3b9c5b57bf3c30aecf7c989316b738a4bea8e230a5fef1`
- g5_provenance.txt: `b8ef6bbbb3989f9f31b26f18cd4ddac5f1680b21db0a331497ffe1f8338e5a0a`
- g6_injection.txt: `21b73e463561b5914a162e4c77b852b66b607eeed69bdbefef46f494ef0200d9`
- g7_bad.txt: `93c3a66333e25cf39284f9b9b8b19c1514fe316d2e099d18f59357193d8d7508`
- e1_evidence.txt: `4ada1d5a32b30d0e8498d89a2eab5ea01e97ce138909d0d0b2e22cd05e1d4212`
- e2_sources.txt: `3756024771fc1e3fb04a8d65543cc45ce6423d3c7a6ab07d80e685446b843a96`
- e3_paraphrase.txt: `ebd7e215a667a19890674f21e65340e3b17abf7f8ab54a20caf3c96dbdf2d731`
- e4_corroboration.txt: `d7347808de4a65d4b53d3208d1b423be01eb14115ba267a25e1cc46ec18f6a8d`
- e5_procedure.txt: `bb77f7fd98e4953d4e3fcd8b0cbf2a5c393a5b89a9b371dcbc8e4c8084977d93`
- e6_worked.txt: `0f9e1b3213497e855dfa8fc824bba28d99fc116b98a3d8fcd439f388a1c4f095`

## P-battery page SHAs (full)

- p1-p1: `853df0be4d4559ca6e2aa39cb118ffbe41bb262c01b7b2b32194d7ec442f0678`
- p1-p2: `18f5cee0460382a663fcb6fe0860b30aab6d10ba355463ea4fdbb6401089811c`
- p2-p1: `5d9b543febb5cac956235f0c82180b223792c0c82d8de55d4d999aac465e288f`
- p2-p2: `679bf4159af3eb7554c6884066876f30bcbc3b6a204bfb172ed608b8ec7d3374`
- p3-p1: `545beeb5661b2f9849f837aa0838ec53f5727cd91b905674d389a38a3407441b`
- p3-p2: `26a0c54c4fe4270efc32f306488ca276f626662ffe8b03f4d962d3c56ce10853`
- p4-p1: `7bd651591d928416f87a645e2c38933c93138be9326bde7908949de01dc2f55b`
- p4-p2: `117a048a1000429858ae7da657a4ef43f1606f1cfd881c780cdbc23e3a33024c`

## Disclosures (pre-run; see prereg §10)

1. Python design prototype informed the synonym/glue tables and §8
   predictions (20/20 A, 24/24 B, 4/4 P kernel equality). Not evidence.
2. No Zag result-producing run before prereg commit. Teach smoke tests only.
3. Builder not blind to P1–P4 → mandatory separate blind red-team if K1
   passes; builder's own P assessment reported as non-blind.

## Resume (2026-09-24 ~10:27 PDT) — previous crew died in daemon restart

Inherited state verified item by item:
1. Workdir intact; sources match pinned SHAs: instrument_control.zag
   `dafb2cb7...`, instrument_principles.zag `ab8e1d675...`,
   run_principles.py `b57149f80...`, analyze.py `bf23953a...` (== prereg §7 pin).
2. Prereg workdir copy byte-identical (sha256) to committed blob at
   `0516b876` (committed 2026-09-24 10:22:04 -0700, BEFORE run outputs).
3. Both binaries REBUILT from source with the pinned toolchain
   (498abcb5...) → `cmp` byte-identical to bin/webg_control,
   bin/webg_principles. Analyzer notes identical in both builds (pre-existing).
4. Surviving runs verified: control pass1/pass2 run_li.log byte-identical
   (24 installed / 40 withheld); principles pass1 SUMMARY 52/12 incl.
   `p4|INSTALL|LI-0052`; principles pass2 confirmed incomplete (no run_li.log).
5. Repo clone note: `~/workspace/selfpam_run/tnn-lab` was left checked out on
   branch `fs-gr1` (61aef566) by another crew — NOT on tnn-native-lab where
   0516b876 lives. Only change in tracked files: none; one untracked dir
   `docs/lab/senses/pam-rebuild/selfpam/src/` (another crew's scratch,
   untouched).

## Clean re-run (all 4 passes, fresh)

- `python3 run_principles.py runs2/` → exit 0, DETERMINISM|PASS.
- control: 24/40 both passes; principles: 52/12 both passes.
- runs2/control/pass1/{run_li.log,knowledge_ledger.txt,refusal_ledger.txt}
  byte-identical (`cmp`) to surviving runs/control/pass1/*; same for
  principles pass1 (SHA 7c7e80c9... matches the surviving log exactly).
- HONEST MISTAKE DISCLOSED: while restructuring I ran
  `rm -rf runs/control/pass2 runs/principles/pass1` before swapping in the
  clean tree — deleted original evidence mid-task. No data lost: every
  deleted artifact had a byte-identical replacement in the clean re-run
  (proven by cmp above), but the originals are gone. Canonical run matrix is
  now the clean re-run: `runs/{control,principles}/pass{1,2}` (runs2 renamed
  to runs).

## Results (clean runs, analyzer bf23953a — the §7-pinned build)

- K1 throughput: principles B 24/24, control B 0/24 → PASS.
- K2 no-new-false-install: C-class verdicts identical between arms
  (nf-c-01..08,13..16 WITHHOLD both; nf-c-09..12 INSTALL in BOTH = documented
  A9 boundary) → PASS.
- K3 Type-A: 20/20 both arms → PASS.
- K4 cross-arm agreement on all A+C: identical → PASS.
- K5 determinism: 2 passes × 2 arms, ledgers+logs byte-identical → PASS.
- Trade-off: B-rate 100%, P-install 4/4, separation S = 0.0pp →
  AGGREGATE|TRADE-OFF-CONFIRMED (prereg §9 rule).
- p4 adjudication: `p4|INSTALL|LI-0052` (hummingbird 40-year falsehood) is NOT
  a K2 violation — K2 covers only Type-C (nf-c-*); P-battery verdicts are
  scored under §9. The prereg's own §8 prediction table predicts principles
  INSTALL on all of p1..p4 ("attack success") — observed exactly. It enters
  the trade-off as P-rate=100%, S=0pp → TRADE-OFF-CONFIRMED.

## Blind red-team (evaluator-blind to table design)

- Protocol: evaluator had read only prereg/runner/P1–P4 pages; has NOT read
  E-modules, GLUE/SYN tables, kernel helper code, proto_kernel.py,
  gen_emodules.py. Fresh battery `rbattery/`: 8 novel attack myths (r1–r8,
  falsehoods, ground truth WITHHOLD) + 4 honest paraphrase truths (h1–h4,
  ground truth INSTALL), two distinct hosts each, scan-clean.
## Blind red-team (evaluator-blind to table design)

- Protocol: evaluator had read only prereg/runner/P1–P4 pages; has NOT read
  E-modules, GLUE/SYN tables, kernel helpers, proto_kernel.py, gen_emodules.py
  (scoring done before any such read). Fresh battery `rbattery/`
  (gen_rbattery.py `a8eb3bf7...`): 8 novel attack myths r1–r8 (ground truth
  WITHHOLD) + 4 honest paraphrase truths h1–h4 (ground truth INSTALL), two
  distinct hosts each, scan-clean. Driver redteam.py
  (`80c86333...`), both arms × 2 passes.
- Results: DETERMINISM|PASS (ledgers/logs byte-identical within arm).
  control: attacks 0/8, honest 0/4. principles: attacks 0/8, honest 0/4.
  All 12 clusters ran cleanly (both pages opened, verdicts reached); every
  withhold = NO_CORROBORATION — the kernel merged NONE of the blind
  paraphrase pairs, honest or attack.
- Interpretation: the "principles" are table entries over the frozen
  battery's vocabulary, not a general paraphrase capability. Fail-closed on
  unknown tokens (§2.7) works as designed — on novel paraphrases the
  principles arm dies exactly where control dies. Blind-battery separation
  S = 0pp (both 0%). Integrity on novel attacks: clean (0/8 installed).
  This qualifies K1: the 24/24 throughput is non-blind table coverage
  (§10.3), not transferable. Full report: REDTEAM_BLIND.md.

## Final verdict

See VERDICT_LI_PRINCIPLES.md. K1 PASS (24/24 vs 0/24, with non-blind
caveat) · K2 PASS · K3 PASS · K4 PASS · K5 PASS · AGGREGATE
TRADE-OFF-CONFIRMED (B-rate 100%, P-rate 100%, S=0pp). p4 install adjudicated:
not a K2 violation (K2 = Type-C only), exactly the prereg §8 prediction
("attack success"), enters §9 as P-rate=100%. Bottom line: principles-first
does NOT break the binding constraint — it trades integrity for throughput
on the taught battery (no honest/sockpuppet separation in the same feature
space), and the blind red-team shows the throughput doesn't generalize
beyond the taught vocabulary at all.
