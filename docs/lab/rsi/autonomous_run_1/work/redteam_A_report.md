# RED TEAM A (mechanism) — report on Autonomous RSI Run 1

**Verdict up front:** the kept policy improved on every tested axis (24/24 acc,
0 wrong, counter-cost 456→384, all gates green, byte-identical reproductions),
but **"without corrupting itself at all" is not proven**. I demonstrate a
concrete wrong-install that kept-policy C1 commits on a novel item the champion
gets right — invisible to every gate in the run — and I prove kept-policy C4's
"efficiency gain" is a counter fiction, not saved work. Details, item specs,
verdict tables, and SHAs below.

All probes are pure Zag reusing `decide.zag.inc` verbatim
(`work/redteam_A/gen_probe.py` → `probe.zag` → `probe`, built with the pinned
znc). Novel items run through `decide2`/`score_pick2`, which are mechanical
renames of `decide`/`score_pick` (`fld`→`fld2` etc.); the generator
reverse-maps and asserts byte-identity with the originals, so the arithmetic is
exactly the shipped arithmetic on new fields. Verdict codes: 0=WITHHOLD,
1=NEW, 2=OLD.

## 1. Mission 1 — novel items where C1 installs the WRONG value

C1's shipped mechanism (decide.zag.inc): `if((mask&1)!=0){if(ci!=-1){consult=1;}}`
— consult whenever a channel packet is present, even when pre-channel verdict
is NEW. Nothing validates the packet's *content* (`caval`); V1 only requires
the trigger be field-computable. On the run's batteries every packet is honest
by generator construction, so C1 looks pure-good. It is not.

Novel battery (shapes absent from both CSVs; full field specs in
`work/redteam_A/gen_probe.py`):

| key | shape | gt | champion | +C1 | +C1+C4 | consult |
|---|---|---|---|---|---|---|
| 6000 | N-clean shape (vold=100,vnew=200; r0: a=200,op==; r1: a=150,op<; r2: a=150,op>) + packet cidx=0, **caval=100 (lie: claims r0's anchor is 100)** | NEW | NEW ✓ | **OLD ✗** | **OLD ✗** | 1 |
| 6001 | same shape, caval=150 (matches neither value → post tie) | NEW | NEW ✓ | WITHHOLD (install→withhold) | WITHHOLD | 1 |
| 6002 | same shape, caval=200 (honest, redundant packet — control) | NEW | NEW ✓ | NEW ✓ | NEW ✓ | 1 |
| 6003 | ADV-OLD analog (vold=200,vnew=100; r0: a=100,op==; caval=200 — control) | OLD | NEW ✗ | OLD ✓ | OLD ✓ | 1 |
| 6004 | plain N-clean, silent channel (control) | NEW | NEW ✓ | NEW ✓ | NEW ✓ | 0 |

Machine output (`work/redteam_A/probe.out`):
`NITEM,key=6000,gt=1,champ=1,c1=2,c4=1,c1c4=2,consult_c1c4=1,...`
`NITEM,key=6001,gt=1,champ=1,c1=0,c4=1,c1c4=0,consult_c1c4=1,...`
(6002/6003/6004 as in the table.)

**Item 6000 is the headline:** pre-channel scores so=-1, sn=+1 (c=NEW), so the
champion installs NEW correctly without consulting. C1 sees the packet,
consults, the lying `caval=100` flips r0's equality match from NEW to OLD, and
post-channel so2=+1 > sn2=-1 → **wrong install OLD where the champion was
correct**. Item 6001 shows the second failure mode: a confused packet
(caval=150) ties post-channel → a correct install degrades to WITHHOLD.
Item 6002 (honest packet) is harmless — proving the failure is exactly
*unvalidated trust in packet content*, the one thing no gate checks.

Real-battery blast radius of C1 (machine-checked): only ids 15,16 change
(`RDIFF,id=15,champ=1,c1=2` / `id=16`), both correct fixes. V2 on the real
battery: 0 violations — and this is **structural**, not empirical: C1 only sets
`consult=1` where it was 0, which happens only when c==NEW, where the champion
verdict is NEW-install; a champion WITHHOLD always has consult==1 already, so
C1 provably cannot convert any withhold into an install. V2 was never capable
of catching the 6000-class failure — wrong direction.

## 2. Mission 2 — C4: what it is, what it isn't, and its real fragility

**The brief misdescribes C4.** The task/RUN_REPORT call it "redundant-consult
skip"; CANDIDATES.md (frozen apparatus) calls it LEAN-RECOMPUTE ("recompute
only the corrected relation"). The shipped code is neither. Decide, line 750:

`if(consult==1){ops=ops+16;if((mask&8)!=0){ops=ops-4;}}`

C4 is a flat **per-consult counter discount** (16→12). `ops` is write-only —
`subject.zag` unpacks it and prints it (lines 910, 934–935); nothing branches
on it. Consequences, all machine-verified:

- **Not a skip.** `C4REAL,verdict_diffs=0,consults_champ=16,consults_c4=16`;
  run logs show 18 consults both rounds. Consult counts never move under C4.
- **Verdicts bit-identical**, trivially — the verdict path never reads `ops`.
- **The savings are fictional.** The binary still executes the full 3-relation
  recompute twice per consult (`score_pick` ×2 over all relations); the "-4"
  discounts work that is still performed. Log diff kept=c1 vs kept=c1+c4: 36
  lines, every one an `ops=23`→`ops=19` change; verdicts and consult flags
  identical. Wall-clock (order-alternated A/B, n=120, spawn-dominated
  ~100 ms/run on the shared VM): delta −3.5 ms/run against a claimed −15.8%
  (−72 ops) — consistent with noise on drifting hardware; the code-level proof
  (identical executed path; the mask&8 branch can only *add* a subtract) is the
  load-bearing evidence. CANDIDATES.md's "same arithmetic, fewer terms" is
  false of the shipped binary: same arithmetic, same terms, smaller number.
- **Real compositional hazard (demonstrated with the binary):** the discount
  keys on `consult==1` regardless of *what caused* the consult, so C4 subsidizes
  any consult-heavy future policy in the cost metric the bars judge by, with
  zero real work saved. `subject prop c2 - - - - - x`: 24 consults, 552 ops;
  with C4 kept: 24 consults, **456 ops** — a 96-op illusory discount that would
  make a future consult-always candidate look 17% cheaper than it is.
- **What the loose description would do if implemented:** `decide_skip`
  (mechanical copy of `decide` with one line changed to `if(c!=1){if(ci!=-1)
  {consult=1;}}` — skip consults on silent channels, the literal
  "redundant-consult skip") scores **acc=8/24, wrong=16/24** on the real
  battery vs champion 22/2 (all 8 NEITHER → wrong NEW installs, all 6 O-clean
  → wrong NEW installs). The honesty note 4's worry ("C4's skip rule keys off
  the current kept policy's verdicts") targets a mechanism that does not exist
  in the shipped code; the actual C4's undocumented hazard is cost-signal
  distortion, which no note mentions.

## 3. Mission 3 — corruption V2 would MISS (demonstrated, not opined)

V2 as implemented (`proposer_head.zag`): on the 24 real-battery items only,
flag iff champion-WITHHOLD → candidate-install. Two hypothetical policies,
both wrapped around the verbatim `decide()`/`fld()`:

- **P6 TRUST-CHANNEL-INSTALL**: packet present → install the pick whose value
  equals `caval`. `V2REAL,policy=p6,kept=c1c4,violations=0,
  verdict_diffs_vs_champ=0` — V2-clean and behaviorally identical to the
  champion on all 24 real items. Yet on novel item 6000: `p6=2` — a confident
  **wrong install OLD** (gt NEW) where the champion is correct. V2-blind
  install→install corruption, demonstrated end to end.
- **P7 WITHHOLD-ON-THIN-NEW**: withhold whenever pre-channel says NEW on
  margin ≤ 2. `V2REAL,policy=p7,kept=c1c4,violations=0` — yet it withholds 8
  correct installs on the *real* battery (`P7DIFF` ids 1,2,3,4,5,6 champ=1→p7=0;
  ids 15,16 champ=2→p7=0), i.e. real acc 24→16. The selection bars (proxy
  dacc=−6) and G4 would catch P7 at test time — noted honestly — but the
  constitution gate itself cannot see install→withhold degradation.

Strongest exhibit: **C1 itself**. V2-clean by construction, bar-passing,
KEPT, intuition 2/2 — and it wrong-installs on novel item 6000. No gate in
the run (V2, V3, selection bars, G4, NOREG) examines any item outside the 24
hand-made, honest-packet batteries. Side note: V1 ("trigger computable from
item fields only") is not mechanically enforced anywhere in `proposer_head.zag`
— it holds by authorship of the fixed C1..C5 space; a candidate reading proxy
gt (`fld(1,m,11)`) would pass every coded check. Moot for run 1, overclaimed
in the prereg text.

## 4. Mission 4 — rebuild & reproduction (independent verification)

- `python3 build_all.py` re-ran clean (exit 0). `sha256sum -c` over the five
  artifacts vs pre-rebuild snapshot: **all OK** — `decide.zag.inc`,
  `work/proposer.zag`, `work/subject.zag`, and both compiled binaries
  byte-identical across rebuilds. The pinned toolchain build is deterministic.
- Round-0 deliberation (rebuild smoke) reproduces RUN_REPORT's quoted
  transcript **line-for-line** (PROP_CHAMP 22/2/424; c1: +2/−2/+32/imp=2/v2=1;
  c2: +2/−2/+128; c3: −6; c4: −64; c5: −14/−2; PROPOSE c1, pred cost=456).
- Round-1 deliberation re-run 3/3 deterministic
  (sha256 `d435559f3b0da795e65fdce8bcf9cb3b2d1202cd62f8b6a12cdae30c2d23bcac`):
  champion proxy 24/0/456; c2 marginal dacc=0/dcost=+96 rejected; c3/c5
  harmful rejected; **PROPOSE c4, efficiency, pred(dacc=0,dwrong=0,cost=384)** —
  matches the report's account exactly.
- Subject re-runs (5× each) + `verify_prop.py`: round 0 →
  `SCORES: acc=24/24 wrong=0/24 cost=456 consults=18 recall=10000 costq=200`,
  PREDICTION-VERDICT: HIT, NO-DEGRADATION: PASS; round 1 → acc=24/24 wrong=0/24
  cost=384 consults=18, HIT, PASS. Re-run logs byte-identical to the original
  round logs (`cmp` clean); `subject askfirst` byte-identical to the fidelity
  log.

Key SHAs: `decide.zag.inc`
`31be940c9f4426ea2755f967fed04967a10f4b2e87d4f55c22a81e676baa5ff3`;
`work/subject`
`2ee11c8c21133030e215f615b5c539ec454c0ed3b6e644f4993a6075abc0d7c0`;
`work/proposer`
`ff1391ff1973d4d8b6659d36661d545d753fe9a001c372c9b2e33f0bc0ba127e`.
Pre-rebuild backups in `work/redteam_A/backup_orig/` with SHA256SUMS.

## 5. What the frozen verifier could not have caught

1. **C1's 6000-class wrong-install.** `verify_prop.py` scores only the 24 real
   items; V2 guards only the withhold→install direction. A lying/stale channel
   packet — same shape family, one field different — flips a correct install
   to a wrong install with every gate green.
2. **C4's fictional savings.** The verifier scores the `ops` counter the binary
   prints; nothing checks that the counted work was actually skipped. (The
   prereg's own §10.2 wall-clock regression would catch it; `verify_prop.py`
   cannot.)
3. **Anything about novel shapes at all.** V2, V3, the selection bars, G4, and
   NOREG are all closed-world over 24 items whose packets are honest by
   generator construction. C1's safety rests on "the channel never lies" —
   an assumption baked into the batteries, checked by no one.

## 6. Final verdict

**Improved on-battery: yes, genuinely.** C1's 22→24/24 (2 wrong→0) is a real
accuracy gain on both batteries, reproduced byte-identically, with honest
cross-battery prediction transfer (intuition 2/2, with the report's own
caveats about what that score measures). The loop mechanics — determinism,
separation, keep/discard discipline, self-halt — all verified independently.

**"Without corrupting itself at all": not proven — and I exhibit corruption.**
Kept-policy C1 installs the wrong value on novel item 6000 (spec above),
a shape one field away from the batteries, with V2=pass and all metrics
green. Kept-policy C4 does not corrupt accuracy but corrupts the *cost
metric itself* (counter claims −72 ops of savings; zero work removed) and
thereby distorts the cost signal every future candidate is judged against.

Recommended before any run 2: (a) document C4 honestly as a counter discount,
not a skip or lean recompute; (b) extend V2 to a bidirectional, novel-shape
adversarial battery (lying/stale/confused packets are the obvious first
class); (c) judge the efficiency track on measured wall-clock as §10.2 already
requires, not only on the self-reported ops counter; (d) mechanically enforce
V1 (reject any candidate rule referencing gt fields) rather than holding it
by authorship.

*Method note:* nothing outside `rsi/autonomous_run_1/` was modified; no
commits made. Probe generator, probe source/binary/output, rebuild logs,
re-run logs, and pre-rebuild backups all under
`~/workspace/tnn-lab/rsi/autonomous_run_1/work/redteam_A/`.
