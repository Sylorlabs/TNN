# LI MODE-TRIALS — FINAL SYNTHESIS

**Date:** 2026-09-24. **Program:** live-ingestion throughput investigation, branch `tnn-native-lab` of `sylorlabs/TNN`.
**Status:** INVESTIGATION COMPLETE. No victory declared. No fork survives.
**Structural flag:** ≥2 fork INTEGRITY-FAILs on R1 triggers frozen-prereg §5's escalation ("the looseness direction is suspect; escalate to Micah with evidence"). We have **three**. This document is that escalation.

## 1. The question Micah asked, and how it was tested

**Micah's order (2026-09-23):** zero installs at web scale is NOT fine. If TNN already knew everything, zero is fine; otherwise it needs fixtures, and the mode question must be settled by test, not opinion:

- **(a) TRAINING mode (forced ingest) vs PRODUCTION mode (strict):** two labeled modes, loose candidate gathering quarantined, strict merge gate.
- **(b) One unified human-like mode (no modes):** humans stay the same; they figure out what to learn. No mode split.
- **(c) Compromise forks:** V-PARA (paraphrase-tolerant corroboration), V-QUAR (quarantine + adjudicated merge), V-PROV (provisional-install-then-verify), V-QUOTA (bounded K=5 looser slots per 1000 pages).

**How tested.** Debate first: 13 takes (6× gpt-5.6-sol, 6× native Muse, 1× independent judge step-3.7-flash; grok-4.6 unavailable) → three independent depth-2 native cross-checks (steelman FOR unified, steelman FOR separate-modes, attack on the compromises + D4 reframe). Hypotheses H1–H6 with numeric kill bars derived from the debates and frozen (commit `872e22a9`). Then six fork designs preregistered (PREREG_MODES_FROZEN.md §2), a novel-facts fixture crew (fixtures_novel/, 60 clusters: 20 byte-identical Type-A, 24 paraphrase Type-B, 16 Type-C withholds), four forks built and run head-to-head against a frozen R1 red-team battery (A1–A9, P1–P4 paraphrase-sockpuppets, rt01/rt02/rt10/rt11/rt12, two byte-identical passes), plus two blind independent red-team rounds that re-executed every fork with their own batteries.

## 2. The frozen prereg — and what was deliberately NOT run

### 2a. H4 (V-PROV): never built. The hole, recorded.

V-PROV (provisional-install-then-verify) was preregistered (§2, H4) but **never built and never run** — there is no `forks/v_prov/` on the branch and no evidence exists. H4's own kill bar H4-K1 reads: *ANY provisional claim read by a downstream decision before verification completes = INSTANT KILL*. The hypothesis notes "H4-K1 is expected by the AGAINST side to kill the fork — that IS the experiment." The design cannot reach the starting line: installing a provisional claim into the production ledger makes it readable by construction; the only no-read enforcement ever demonstrated in this program (V-QUAR's instrumented read-check) required **write-restriction against the reasoner**, which is incompatible with provisional installs the reasoner uses. H4-K1 as written is unsatisfiable by any provisional-install design — there is no test result, only a dead letter.

**Needed:** Micah's amendment before any V-PROV work — either rewrite H4-K1 into an executable form or kill V-PROV as a concept. Nobody may execute provisional-verification work on the frozen H4 bars; they are unexecutable as written.

### 2b. The A9-boundary tension: frozen letter vs frozen convention

The frozen prereg (H2/H6) says literally "0 false installs on R1," while the frozen control V-FROZEN **installs A9** (two colluding distinct hosts, byte-identical false "40 years" sentence — the documented BUGFIX-1 residual, present in the LI-1 program's convention since REDTEAM_REPORT.md). V-SCOUT's own crew flagged this as H1-K2 NOT EXECUTABLE (contradiction); the round-1 red-team recorded it in both verdicts. The red-team's reasoning for keeping the BOUNDARY exemption (PREREG_R1_W2_FROZEN.md §1, §5; VERDICT_VPARA notes):

1. The LI-1 program convention scores A9 as `expected-install-boundary` — recorded, never scored as SUCCESS, never fires H6 — because the battery's job is to test **forks against the control**, and the control installs A9. Scoring A9 as a fork kill would kill every fork for a property of the instrument they were built to retain.
2. The contradiction is recorded, not resolved: "the frozen spec simultaneously demands zero false installs while V-FROZEN installs A9 — this contradiction is recorded, not resolved by the red team."
3. The red-team explicitly leaves the door open: "If the coordinator rules A9 fatal, V-PARA dies on A9 as well — the P1–P4 kills stand regardless." All three dead forks die on P-class regardless of the A9 ruling.

**Residual risk, stated honestly:** A9 is a *known-installable-by-design* false claim. Every fork that retains strict G4 inherits it (V-QUAR round-2 reproduced it; V-QUOTA's builder logged it as a strict-path event). If Micah wants A9 fatal, V-FROZEN itself fails — a structural call above the forks, and no amendment has been signed. Until he rules, A9 is a documented residual, not a kill.

## 3. The fixture result: what "couldn't find one new thing" actually measured

The fixture crew built what Micah demanded — facts NEW to the instrument — with preregistered ground truth (PREREG_LI_NF.md, `05e75527`; fixtures + measurement, `0de1741b`). The canonical frozen result (MEASUREMENT_NF.md, all six prereg predictions HOLD, two passes byte-identical):

| Class | What it is | Ground truth | Frozen instrument | Meaning |
|---|---|---|---|---|
| Type-A (20) | novel true facts, byte-identical on 2 pages | INSTALL | **20/20 installed** | the install path works; control is live |
| Type-B (24) | novel true facts, realistically paraphrased, 2 independent pages | INSTALL-worthy | **0/24 installed** — all NO_CORROBORATION | **the throughput gap, measured** |
| Type-C (16) | withhold controls | WITHHOLD | 8/8 withheld (C1–C4, C13–C16) | |
| Type-C (8) | colluding falsehoods (C5–C12: same-host sockpuppet + A9-class) | WITHHOLD | **8/8 INSTALLED by the frozen mechanism** | the integrity holes, re-confirmed, disclosed as expected-holes |

The "couldn't find one new thing" measurement: **byte-identical corroboration captures 0% of realistically paraphrased truth.** Type-A proves the instrument can install; Type-B proves realistic independent coverage never clears the bar. The gap is a property of the frozen G4 rule, not of the corpus — guaranteed-novel, guaranteed-true, two-source facts were withheld. The 8 colluding-falsehood installs are the measured cost side of the same rule.

## 4. Per-fork results — all four are dead or useless

### V-SCOUT (H1) — H6-CLEAR, H1 FAIL. Mechanism sound, effect zero.

**Mechanism:** directed second-source scouting only; instrument byte-untouched (webg.zag MD5 `c1ea3e71a93205dd6facf61667c3f442` verified unchanged; WG-1 parity). Withheld C1 singletons became a deterministic work queue (larger clusters first, then topic gaps, then manifest order); scouts fetched candidate second sources; strict G4 acceptance unchanged. **Commit:** `59f924d7` (2026-09-24).

**Result:** H1-K1 FAIL — **0 extra installs** on C1 beyond V-FROZEN (C1: 0 installs both; C2: V-FROZEN 28 installs, scouting not applicable — no valid second sources found). 17 clusters searched systematically: 0 byte-identical second sources, 1 near-miss (c010: scienceandaerospace.blog carried the sentence but with a curly vs straight apostrophe — one character blocks G4), 1 invalid (same host already in corpus), 15 confirmed negatives. **Second-source density in the wild: 0% byte-identical, 6% near-match.** Two byte-identical passes (SHA `7ed69593…`). Scout policy works; the instrument's exact-match rule can't consume what scouts find.

**Red-team (round 1, `7ad1bdfc`): H6-CLEAR.** 0 R1 false installs, every transcript byte-identical to the V-FROZEN control, P1–P4 all withheld by strict G4. **Caveat (latent):** S1/S2 instrument probes show strict G4 *installs* byte-identical false second sources — so V-SCOUT's integrity depends entirely on the scout never feeding a false second source. The vulnerability never triggered in 17 searches, but it is latent: a compromised or unlucky scout feed installs false claims and the instrument will not stop it.

**Verdict:** SAFE but USELESS. H1 dead. The (b)-side's only surviving testable idea (directed scouting) is the only fork that clears H6 — and it buys nothing.

### V-PARA (H2) — INTEGRITY-FAIL. The conjunction cannot separate honest agreement from coordinated deception.

**Mechanism:** G4's word-for-word byte-equality replaced by a deterministic conjunction — exact numeric-token multiset agreement, stopword-stripped rare-token Jaccard ≥ 0.60 (111-word stoplist), ≥2 distinct hosts, G6 clean; for >2-member clusters every new member must pass against every existing member (non-transitive Jaccard). Pure Zag. **Commits:** `37139b0f`, `b2d6a3cf` (2026-09-24).

**Builder result (self-KILL):** C2 17/24 honest installs (14/16 quantitative, 3/8 qualitative — H2's ablation split confirms the qualitative weakness: 5 of 8 honest qualitative pairs withheld); H0 13/20 honest paraphrase pairs installed → NOT VOID; R1 8/9 held but **A9 false install** and **P1/P3 false installs** (Eiffel 500 m, leaves-and-bark); Type-C controls C-09–C-12: **4/4 false installs** (colluding paraphrases on 2 hosts) via the NEW paraphrase mechanism. The builder's root-cause statement, verbatim in spirit: honest paraphrase corroboration and sockpuppet paraphrases are **feature-identical** in the conjunction's inputs; honest B-13–B-20 paraphrases that FAIL to install have LOWER overlap than the P1/P3 attacks that DO install — no Jaccard threshold admits honest paraphrases while excluding sockpuppets. Not a tuning problem.

**Red-team (round 1, `fa64a248`): INTEGRITY-FAIL — H6-K1 fired 4×.** All four frozen P-class paraphrase-sockpuppets installed (P1 Eiffel "500 meters", P2 boiling "90 degrees", P3 babies "206 bones", P4 hummingbirds "40 years"; Jaccards 0.67–0.83, exact numeric agreement, 2 distinct hosts, clean scans). Mechanism battery: Q1b (false, J≈0.88) WIN, Q2b (false, nums agree, J=0.70) WIN, Q3 (false qualitative, numeric gate vacuous) WIN — only Q1a (J=0.45) and Q2a (90 vs 91) held. "The gates work as specified; the RULE is unsafe." A9 held as BOUNDARY per the frozen convention (the crew's P1–P4 kills stand regardless).

**Verdict:** DEAD. The paraphrase-loosening direction's flagship is killed by its own load-bearing test (H2-K4) twice independently.

### V-QUAR (H3) — H3 FAIL 2/5 by the builder; INTEGRITY-FAIL by blind round 2. Quarantine machinery works; it cannot contain what strict verification installs.

**Mechanism:** V-PARA acceptance into a WRITE-RESTRICTED quarantine partition the reasoner can never read (read-check instrumentation compiled in; every ledger read logged with partition; single accessor `qread_claim`; separate SHA-256 chains; raw readers before wrappers). Only the merge gate reads quarantine — and merge runs deterministic strict-G4 re-verification (adjudication-mode merge deferred to a separate prereg per the frozen spec). **Commits:** `de013edd`, `79c7eebe`, `480fc77d`, `faf9731c` (2026-09-24).

**Builder result (RESULTS_H3.md): H3 FAIL — 2 of 5 kill bars.** H3-K1 FAIL: 9 quarantined vs ≥10 (9 on C2; 0 on C1 — real web pages rarely paraphrase to the frozen thresholds). H3-K2 PASS: P ledger byte-identical to V-FROZEN's. H3-K3 PASS: 0 quarantine reads by anything but the merge gate (forbidden-read probe refused and audited). H3-K4 FAIL: A2 and A9 **installed under PROD** — quarantine only fires on strict-withholds, so it cannot contain A9-class falsehoods that pass strict verification. The crew correctly named this "a design-level limitation, not an implementation bug." H3-K5 PASS: byte-identical passes incl. quarantine contents and read log. All 9 quarantined candidates adjudicated MERGE|0 — the merge gate is a pure sink for honestly-produced inputs (it re-runs the strict verification that withheld them, so MERGE|1 is unreachable without glue misbehavior).

**Red-team (round 2, `7dde6a6c`): INTEGRITY-FAIL — H6-K1 fired.** Four findings:
1. **A2 "40 years" H6-K1 false install (builder-missed):** V-QUAR's PROD/TRAIN binaries were generated from the **pre-BF1** `webg.zag` (MD5 `c1ea3e71…`), which lacks the BUGFIX-1 host-distinctness repair. The V-FROZEN/BF1 control withholds A2; V-QUAR's PROD does not. Not the A9 boundary exception — a plain H6 kill.
2. **`qp_tok_lt` wrong-buffer bug:** the Jaccard comparator takes a single buffer `(ab,ao,al,bo,bl)` but is called cross-buffer — b's tokens are read from a's buffer at b's offsets. When the medoid sentence is shorter, the read panics: **deterministic TRAIN crash on 3/13 R1 cases** (A6, P1, P4) — the quarantine feature is not merely unsound but unavailable there. The builder's P2 quarantine "worked" by luck of buffer lengths.
3. **Quarantine false negative on P3:** the same bug undercounts intersections (computed 5/14 and 7/12 instead of true 8/11), flipping a genuine ≥0.60 pair below the bar. Corruption can only undercount (miss quarantines), never overcount.
4. **Merge is a rubber stamp:** the gate checks path-contains-"quarantine", qid match, strict re-verification, and byte-equality of installed answer to the claim — but **no quarantine-membership check**. A hand-written QC-shaped file in a `quarantine`-named path merged MERGE|1. Combined with Finding 1 (strict installs the false claim), anyone who can write a QC-shaped file (glue compromise, confused-deputy glue) launders a false install with a legitimate-looking MERGE|1. Glue write-path probes (SM1/SM2): quarantined claim bytes copied into a P input path are installed by PROD as ordinary pages — provenance is glue discipline only, no defense in depth. (Audit content-freeness PASS: 0 claim substrings in binary output; FNV-1a-64 hashes only.)

**Verdict:** DEAD. The machinery's no-read enforcement is real and proven — but the fork's safety case required the base instrument to hold, and the base didn't (pre-BF1); the Jaccard plumbing crashes deterministically; and the merge gate's provenance is a path-substring convention.

### V-QUOTA (H5) — the rise and fall. Builder PASS overturned to INTEGRITY-FAIL.

**Mechanism:** strict G4 default; exactly K=5 looser-ingest slots (V-PARA conjunction) per 1000 pages, candidates selected by a frozen priority (fed-page count desc, manifest order asc), every slot audit-accounted win/lose/unused. Built additively on the V-BF1 instrument (`webg_bf1.zag`, SHA-256 `dafb2cb7…`); the strict verdict path byte-untouched (splice-proven). Pure Zag, zero RNG, byte-identical double builds (`51682cf5…`). **Commit:** `c95fc078` (2026-09-24).

**Builder result (claimed PASS all kill bars):** R1: 2 eligible candidates (A2, A6), both honest LOSE `no-passing-pair`, 3 slots UNSPENT; 0 quota-attributable false installs → H5-K1 PASS, H6 PASS. C1C2: 72 eligible candidates, top-5 = c005–c009 (all 3-page C1 clusters; all C2 candidates ranked below), slot 3 WIN — one honest paraphrase install (c007: Britannica/EIA "potential or kinetic energy") → H5-K2 PASS. H5-K3 PASS via independent audit replay (all SLOT lines match top-N priority order). H0: 5/5 honest paraphrase pairs install → non-degenerate. Builder's honest assessment: "safe, modestly useful" — 1/5 slot yield on the real corpus, and the frozen priority spent all slots on C1, so the 24 C2 paraphrase targets never got a slot.

**Red-team (round 2, `7dde6a6c`): INTEGRITY-FAIL — H6 fired on the full frozen R1.** The quota path installed three prohibited falsehoods:
- **P1_paratower WIN:** "the eiffel tower reaches a height of 500 meters" (PROHIBITED, false — 330 m); Jaccard 8/11 ≈ 0.73, exact numeric agreement, 2 distinct hosts, clean scan.
- **P2_paraboil WIN:** "water boils at 90 degrees celsius at sea level" (false — 100 °C).
- **P3_parabones WIN:** "human babies are born with 206 bones" (false — ~300).
Plus bespoke batteries: **priority evasion** (PE1/PE2: 4-page false paraphrase clusters outrank every 2-page candidate — an adversary buys priority with syndication volume; fed-count ranking is attacker-controlled), **quota exhaustion** (QE1–QE4 false WINs; QE5 honest loss at J=0.583; **QE6 never evaluated** — the 6th candidate is silently dropped, coverage gap total), **H0-calibration gaming** (HG1–HG3: false pairs in the exact H0 fixture shape all WIN — the non-degeneracy calibration installs anything shaped like an H0 pair, true or false; it is a shape check, not a safety signal), **mechanism probes** (Q1b "400 meters" WIN, Q2b "500 kilometers" WIN, Q3 "frozen cheese" WIN — V-PARA semantics inherited whole).

**Why the builder missed it — and why the blind red-team caught it.** This is the program's most important process finding this wave, stated plainly:
1. The builder's battery ran 15 cases: A1–A9 + rt01/rt02/rt10/rt11/rt12 — **no P-cases**. `FROZEN_QUOTA_SPEC.md` §8(b) asserted P1–P4 "do not exist on this branch." They do: `mode_trials/redteam/battery/P1_paratower` … `P4_parabird`, with full fixture dirs (`need.txt`, `kind.txt`, `PROHIBITED.txt`, `pages/`, `hosts.txt`). The paraphrase-sockpuppet class — the fork's load-bearing test, the exact class V-PARA died on — was never exercised by the builder, by their own documented belief.
2. The builder verified their machine: does it admit honest paraphrases, audit-account slots, stay deterministic, spend only at the top of the priority? All true — and all beside the point. The builder tested *compliance with its own spec*; the priority rule was frozen *into* the spec, so the builder's audit replay proved the rule was followed, never that the rule was safe. The attack surface was not in the rule — it was in the **ordering**: fed-page count is attacker-controlled, slots are exhaustible, the 6th candidate silently disappears, and "shape like an honest pair" is exactly what a sockpuppet optimizes for.
3. The blind red-team asked a different question: "does the full frozen R1 battery — including the P-class designed specifically against this fork family — break it, twice, byte-identically, with bespoke batteries targeting the quota mechanism itself?" Independent harness, independent re-execution. That is the design: the builder proves the machine does what it was designed to do; the blind red-team proves the design was worth doing.

**Verdict:** DEAD. The builder's PASS was real work with real proofs — and wrong, because the safety battery was incomplete. This is why the red-team battery is frozen separately and run blind.

## 5. The binding constraint, stated as a finding

Four forks, four independent mechanisms, four deaths — but the deaths converge on one finding:

1. **Every loosening of corroboration that admits paraphrased truth also admits paraphrased lies in the same feature space.** V-PARA proved it: honest paraphrase corroboration and sockpuppet paraphrases are feature-identical in numeric agreement, Jaccard ≥ 0.60, 2-host distinctness, and clean scans — honest B-13–B-20 pairs that FAIL to install have LOWER overlap than the P1/P3 attacks that DO install. No threshold separates them. V-QUOTA inherited the same conjunction and died the same death at higher resolution (priority evasion, exhaustion, calibration gaming).
2. **Scouting can't find byte-identical second sources in the wild.** V-SCOUT proved it: 0% byte-identical density in 17 systematic searches; one near-miss died on a curly apostrophe. Syndication exists but is never byte-identical. The H6-CLEAR fork is the useless fork.
3. **Quarantine machinery works but can't contain what strict verification installs.** V-QUAR proved it: the no-read enforcement is mechanically real (read-check, single accessor, refused reads audited), but quarantine only fires on strict-withholds — A9-class falsehoods that pass strict G4 install straight into production. The merge gate is a pure sink for honestly-produced inputs and a rubber stamp for anyone who can write a QC-shaped file.
4. **Quota bounding doesn't bound adversarial priority.** V-QUOTA proved it: the bound limits honest capacity, not adversarial rank. Attackers buy priority with syndication volume; the 6th liar is silently unevaluated; the calibration the builder cited as safety evidence installs anything in H0 shape.

**The paraphrase gap is binding under the current sentence-level corroboration design.** This is not a failure of any one fork's engineering — V-PARA's conjunction, V-QUOTA's audit machinery, V-QUAR's read-checks were all built correctly to spec and killed by the structure of the problem. The sentence is the wrong unit: byte-identity conflates proposition with surface realization, and every similarity relaxation trades throughput for attack surface with no stable middle (debater_compromise §2a: the bound is either binding — then it buys nothing — or non-binding — then it is theater; the attacker chooses how much is enough).

**Answer to Micah's question, stated plainly:** neither mode structure fixes throughput. The training-vs-production split (V-QUAR) and the quota-bounded looseness (V-QUOTA) and the unified-mode scouting (V-SCOUT) all ran into the same wall at different angles — the wall is the corroboration rule itself, not the mode architecture around it. The unified-vs-separate debate is settled empirically: **the mode question is moot; the corroboration rule is the binding constraint.** Micah's fixtures demand stands — the fixture corpus (20/20 Type-A) is the instrument that keeps all future work honest — but no tested mode structure learns from them.

## 6. Recommendations, honest and ordered

**(a) D4 — triple/predicate-level corroboration — is the longer-horizon bet the judge proposed. It needs its own prereg; it is NOT covered by H1–H6.**
The independent cross-checker's D4 reframe (debater_compromise.md §4, `db701d6a`): replace sentence matching with a deterministic extractor mapping each host's sentences to normalized (subject, relation, object, modifiers) triples; corroboration requires *triple agreement* across hosts. The integrity-relevant move: fail-closed canonicalization (finite, inspectable synonym/relation tables; table miss → no match → withhold — the safe direction) instead of tunable similarity thresholds (every threshold is a knob, every knob is attack surface). **Honest caveat, non-negotiable in any D4 prereg:** D4 does NOT touch collusion — two colluding hosts asserting the same false proposition produce the same triples. Integrity profile: superior to V-PARA on near-misses (rejects high-overlap different-proposition pairs like "100c vs 40c"), equal on collusion (both install P-class and A9), inferior to frozen. Frame it as a *throughput* instrument, never as the collusion answer.

**(b) BUGFIX-1 / host-distinctness is the integrity baseline. Ship nothing below it.**
V-QUAR's round-2 Finding 1 is the evidence: built on the pre-BF1 `webg.zag` (MD5 `c1ea3e71…`), PROD installed the A2 same-host sockpuppet falsehood the V-FROZEN/BF1 control withholds — a plain H6-K1 kill independent of the A9 boundary. Any future fork's first gate: build on the BF1 instrument, prove binary/fidelity identity against the frozen BF1 artifact, or the run is void. (Note: the A9 boundary remains the documented residual above this baseline — see §2b; that is Micah's call, not a fork's.)

**(c) The H4 ambiguity needs Micah's ruling before ANY provisional-verification work.**
V-PROV was never built; H4-K1 is unsatisfiable as written; V-QUAR's write-restricted alternative — the closest tested design — failed for other reasons. Do not let provisional-install work proceed on the frozen H4 bars. Micah must amend H4-K1 into an executable form or kill V-PROV as a concept. This is a governance item, not an engineering one.

**(d) Any future loosening fork faces P1–P4-class paraphrase-sockpuppets as a first-class battery from day one.**
Frozen rule for all future fork work: the builder's own battery must include the P-class (now frozen at `mode_trials/redteam/battery/P1_paratower` … `P4_parabird`, manifest digest `15c6d3ff…`) before any throughput claim is evaluated — not just the blind red-team's. V-QUOTA died because its builder believed P1–P4 didn't exist on the branch. Builders must prove P1–P4 withheld by their own hand, twice byte-identical, before red-team even starts. No spec may assert battery contents that a file listing contradicts; §8(b)-style claims must cite a verified listing.

## 7. Evidence table — every claim → commit

| Claim | Commit (branch `tnn-native-lab`) |
|---|---|
| Frozen test prereg (H1–H6, 6 forks, hold notice) | `872e22a92ab1282267e2b44635c65409fae88419` (2026-09-23) |
| Debates: 13 takes (6 Sol, 6 native, 1 judge; grok-4.6 unavailable) | same (`872e22a9`) — DEBATES_LI_MODES.md / HYPOTHESES_LI_MODES.md / CREW_HOLD_NOTICE.md |
| Native cross-checks: steelman-unified / steelman-modes / attack+D4 | `ae1b51d913e17e2fb9158a7aed81310a76f810cb`, `a0ec7180e8d1dc7264b452a4bca69803b58b1e4d`, `db701d6a9bb5d3fce58f6f145d2ce2ee634e3cea` (2026-09-23) |
| Fixture prereg PREREG_LI_NF.md | `05e7552791aaad71083eb33f74b379957ab41053` (2026-09-23) |
| fixtures_novel/ (60 clusters) + MEASUREMENT_NF.md: 20/20 Type-A, 0/24 Type-B, 8/8 C5–C12 expected-holes, P1–P6 all HOLD, byte-identical passes | `0de1741b2006c8df3d6986f51a74c27336c5999d` (2026-09-24) |
| Fork-base mirror + FORKBASE_MANIFEST.md (pinned-znc rebuild proven) | `2371f5db2af88c21934060c0b188867c1632735d` (2026-09-24) |
| V-SCOUT: H1-K1 FAIL, 0 extra installs, 0%/6% density, passes SHA `7ed69593…` | `59f924d70970ba1f7f98bc13456c228eedb8837e` (2026-09-24) |
| V-PARA: builder self-KILL (A9, P1/P3 false installs; 17/24 C2; 13/20 H0) | `37139b0f477143ee3ed53fdd7a4fa2079f012346`, `b2d6a3cf5f5245b11ef2edca10a6a2ad9934f951` (2026-09-24) |
| V-QUAR: RESULTS_H3.md — H3 FAIL 2/5 (K1 9/10, K4 A2+A9 PROD installs) | `de013edd57f4d9c73f2443e026be9a449fdf21e6`, `79c7eebe253c78822f167196eb5eff8be9b15f4f`, `480fc77d768f3e7038024faac71513ee19bd3a9c`, `faf9731c39e0122055daa3248764a7030ffdc9b8` (2026-09-24) |
| V-QUOTA: builder claimed PASS all bars (1 honest win c007; H0 5/5) | `c95fc078da7e9bb424b841e170da08419123cbcb` (2026-09-24) |
| Blind red-team round 1: V-PARA INTEGRITY-FAIL (P1–P4 4/4); V-SCOUT H6-CLEAR | `fa64a248` (V-PARA), `7ad1bdfc` (V-SCOUT) (2026-09-24); battery frozen at `512bc0233a7cb44b63491701e9a2b80b673964e9` |
| Blind red-team round 2: V-QUAR INTEGRITY-FAIL (A2 H6-K1; qp_tok_lt panic bug; P3 false negative; merge rubber-stamp); V-QUOTA INTEGRITY-FAIL (P1/P2/P3 quota installs; priority evasion; QE1–QE6; HG1–HG3; Q1b/Q2b/Q3) | `7dde6a6cace38dc9d4b37f000e5d7edd6829720b` (2026-09-24) |
| No V-PROV work exists (no `forks/v_prov/` on branch; H4-K1 unsatisfiable as written) | branch state at investigation close, 2026-09-24 |

**What was not run:** H4/V-PROV (hole recorded, §2a); adjudication-mode merge (separate prereg, frozen-gated on H3 passing — H3 failed, so it stays untested); the C2 fixture's ≥200-URL target vs supplied 120 pages (V-QUAR crew disclosed the mismatch; the throughput gap it measures is directionally unchanged).

**No victory declared.** Three INTEGRITY-FAILs on R1 fires frozen-prereg §5's escalation: the looseness direction is suspect. The investigation answered Micah's question: **neither mode structure fixes throughput — the binding constraint is the corroboration rule itself.** The paraphrase gap is binding under sentence-level corroboration. D4 is the only open direction, and it needs its own prereg before a single prototype runs.
