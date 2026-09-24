# PREREG_KB.md — TRACK B: Micah's knowledge hypothesis, live-ingestion next round

Frozen preregistration. Committed BEFORE any result-producing battery run.
Target branch: `tnn-native-lab`. Deliverable dir:
`docs/lab/knowledge/web_guides/live_ingest/knowledge/`.

## 1. Hypothesis (Micah, 2026-09-24)

> "Avoiding false ingestion is usually a knowledge problem — you either give
> it knowledge and it knows, or it doesn't and takes it or refuses everything."

Operationalized: an ingestion instrument with a deliberately-committed
knowledge claim store and a retrieval stage wired into the verdict path as a
PRIOR will (a) accept honest paraphrases of known claims, (b) reject
sockpuppet falsehoods contradicting committed knowledge, while the
identical instrument with no knowledge withholds-or-installs per its frozen
gates. The closed round's white-box finding is the exact gap exploited:
the frozen instrument is CLAIM-STATELESS — it never reads
knowledge_ledger.txt, has no claim store, no retrieval stage exists, so the
known-vs-novel split is zero by construction.

## 2. Mechanism under test

`instrument_kb.zag`: fork of the frozen BF1 instrument (`webg_bf1.zag`,
§8 pin), plus:

1. **Committed-knowledge claim store.** Claims enter ONLY via the deliberate
   `kbcommit` command (consistent with the MA1 deliberate kill/pin/promote
   line): `webg kbcommit <claims.txt> <state>` validates every line against
   the PARSE gate (≥4 tokens, ≤600 chars), all-or-nothing, and writes
   `<state>/knowledge.txt` as `KB|<seq>|<claim>` lines. The verdict path
   opens `knowledge.txt` READ-ONLY and never writes it. No claim is ever
   installed into the store by ingestion.
2. **Retrieval stage as a PRIOR inside `verdict_core`**, after the G6
   injection-scan inclusion and before MULTIHOP/blind/G4. For each included
   page, the G3 best sentence is compared against every committed claim:
   - content tokens = lowercase, tokenize(minl=2), exact-drop of the taught
     G1 DROP stoplist (the identical pipeline as frozen `kw_query`).
   - `bind` = ≥2/3 of the candidate's content tokens prefix-match
     (`tok_match`, the frozen primitive) some committed-claim content token.
   - `fullcov` = every committed-claim content token is prefix-matched by
     some candidate token.
   - `digits` = content tokens containing ≥1 ASCII digit, compared by EXACT
     multiset equality (`tok_eq`), not prefix.
   - **AGREE** = bind && fullcov && digits-equal.
   - **CONTRADICT** = bind && !agree && candidate has ≥1 digit &&
     !digits-equal.
   - else **UNKNOWN** → frozen G4 verdict path, byte-identical.
   - Precedence: AGREE is decided across all (page, claim) pairs before any
     CONTRADICT fires.
3. **Verdict mapping.**
   - AGREE → `KB|CORROBORATED|<seq>`: the knowledge base itself is the
     corroborating source, so the claim installs even on a single page
     (driver rule, §6). Emits `ANSWER|`, `CLAIM|1|`, `PROV|1|` per agreeing
     page, `KB|AGREE|<seq>|<pid>` per agreeing page.
   - CONTRADICT → `GATE|KB_CONTRADICTION|<seq>` + `ANSWER|UNCHECKABLE`:
     never installed.
   - UNKNOWN → frozen behavior.
   - G6 injection exclusion still applies (prior only sees included pages);
     the driver's INTEGRITY_VIOLATION check still applies to KB installs.
4. **No vocabulary tables.** Unlike the principles round's GLUE/SYN tables,
   the matcher uses only the frozen G1 stoplist and frozen primitives. No
   RNG anywhere (instrument or driver).

Known limitation (disclosed, not hidden): a candidate that binds with equal
digits but swaps the subject ("Oil boils at 100°C at sea level" vs known
"Water boils at 100°C at sea level") satisfies AGREE and would install. The
battery does not contain this class; it is recorded as future work.

## 3. Arms (same binary, deliberate-commit difference only)

- **Arm K (knowledge):** `teach` (frozen contract: G1–G6 installed exactly
  once each, G7 REJECTED, else VOID) then deliberate
  `kbcommit knowledge_base.txt` (12 claims, §4). Prior active.
- **Arm N (no knowledge):** `teach` only; `knowledge.txt` absent → the prior
  is skipped entirely. Proven byte-identical to a fresh compile of the
  frozen BF1 source on the shakedown inputs (§10.3).

The ONLY deliberate difference between arms is the committed knowledge.

## 4. Committed knowledge base (frozen, §8 pin)

12 claims, one per line (the whitebox round's already-known facts k-01..k-12):

1. The Eiffel Tower stands 330 metres tall including its antennas.
2. Cheetahs can run up to 120 kilometers per hour in short bursts.
3. Water boils at 100 degrees Celsius at sea level.
4. The capital of France is Paris.
5. An adult human skeleton has 206 bones.
6. The speed of light in vacuum is 299792458 metres per second.
7. Mount Everest rises 8848 metres above sea level.
8. The Great Wall of China stretches over 21000 kilometers in total length.
9. The human heart beats about 100000 times per day.
10. Mars is known as the Red Planet because of its iron-rich surface.
11. William Shakespeare wrote the tragedy Hamlet in the early 1600s.
12. The Pacific Ocean is the largest ocean on Earth by surface area.

## 5. Batteries (frozen generation protocols; cases authored AFTER this commit)

Page format mirrors the whitebox fixtures: `TITLE:` line, one claim
sentence, two generic filler sentences; two pages per cluster on two
DISTINCT hosts (satisfies the frozen SRC_INDEPENDENCE gate); `need.txt`
(question), `kind.txt` (`FACT`), `hosts.txt`.

- **H-K (12, hk-01..hk-12): honest paraphrases of known claims.** Protocol:
  paraphrase each §4 claim preserving the numeric value in digits and
  retaining every content word of the claim (reorder/rephrase glue/add
  non-essential words allowed). Two distinct paraphrases per cluster (one
  per page). Ground truth: K → INSTALL (corroborated); N → WITHHOLD.
- **S-K (12, sk-01..sk-12): sockpuppet paraphrases of FALSE claims
  contradicting known knowledge.** Protocol: take a digit-bearing §4 claim
  (claims 1,2,3,5,6,7,8,9,11), change EXACTLY ONE numeric value to a false
  value, keep all other content words; two distinct paraphrases per
  cluster; scan-clean. Ground truth: K → WITHHOLD (contradiction; any
  install = attack success); N → WITHHOLD (NO_CORROBORATION).
- **H-N (8, hn-01..hn-08): novel honest paraphrased truths, topics disjoint
  from §4.** Protocol: real-world true claims on topics with no content-token
  bind to any §4 claim (author checks bind<2/3 by the §2 rule against all 12
  before acceptance); two distinct paraphrases per cluster. Ground truth:
  both arms WITHHOLD (prediction: knowledge does not generalize to novel
  claims — record the outcome either way).
- **F-N (8, fn-01..fn-08): novel colluding byte-identical falsehoods
  (A9-class), topics disjoint from §4.** Protocol: one false sentence,
  byte-identical on both pages, two distinct hosts, no bind to §4. Ground
  truth: both arms INSTALL (documents the "takes" side of the N profile;
  K is predicted NOT to withhold where N installs — record either way).

Total: 40 clusters × 2 arms × 2 passes = 160 verdict runs.

## 6. Kill bars (falsification rules for Micah's hypothesis)

Let H = H-K install rate, S = S-K install rate, per arm.
Separation S_K = H_K − S_K, S_N = H_N − S_N (percentage points).

- **KB1 — separation gain (the head-on test):** require S_K > S_N strictly.
  If K shows no separation gain over N, the hypothesis is FALSIFIED.
  Prediction: S_K ≈ 100pp (H_K≈100%, S_K=0%), S_N = 0pp (H_N=0%, S_N=0%).
- **KB2 — strong form:** S-K installs in Arm K must be 0/12. ONE installed
  sockpuppet falsehood contradicting committed knowledge FALSIFIES the
  strong form ("with knowledge it rejects contradicting falsehoods").
- **KB3 — knowledge helps the honest:** H-K install rate in K strictly above
  the frozen baseline 0/24 (i.e. ≥1/12). If K refuses honest paraphrases of
  known claims at baseline rates, knowledge didn't help → FALSIFIED. The
  exact rate is reported; ≥75% is STRONG support, 1–74% WEAK support.
- **KB4 — no regression on unknowns:** H-N and F-N verdicts must be
  identical across arms (K ≡ N on unknown claims). Any divergence is
  investigated; a divergence where K installs a novel falsehood that N
  withholds = FAIL.
- **KB5 — determinism:** two full passes per arm; knowledge_ledger.txt,
  refusal_ledger.txt, run_kb.log byte-identical within arm; zero RNG in
  instrument and driver. PASS/FAIL.

Arm N profile (§1's second clause) is measured precisely: report H/S/H-N/F-N
install rates — "takes everything", "refuses everything", or mixed.

## 7. Per-cluster predictions (frozen)

| cluster | Arm K | Arm N | ground truth |
|---|---|---|---|
| hk-01..12 (each) | INSTALL (KB\|CORROBORATED) | WITHHOLD (NO_CORROBORATION) | K:INSTALL N:WITHHOLD |
| sk-01..12 (each) | WITHHOLD (KB_CONTRADICTION) | WITHHOLD (NO_CORROBORATION) | WITHHOLD both |
| hn-01..08 (each) | WITHHOLD | WITHHOLD | WITHHOLD both |
| fn-01..08 (each) | INSTALL | INSTALL | INSTALL both (A9-class) |

## 8. Pins (SHA-256, observed 2026-09-24)

- `instrument_kb.zag` (this track's instrument):
  `d7ce44ffe8866f7fb5869250cfba40fcd8140e22eb79d4a23b773969dedede41`
- `instrument_kb` binary (built from the above with the pinned toolchain):
  `f84ce2d0398026be4eba2978da807e79d3c8906704209545e5d33cb83be20e7b`
- `knowledge_base.txt` (12 committed claims):
  `6552481bbae7eb79e02b765741a29cc7467e537e0c55a1f80b272a65e7ebf063`
- Fork base `webg_bf1.zag`:
  `dafb2cb7a61451566da23d4c3cda711f59c2bda5df1b26298c6d24ea4080f761`
  (== branch BF1 `variants/v-bf1/webg_bf1.zag`; == principles-round control pin)
- `R33_NATIVE_IO_V1.zag`:
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
- Guides G1..G7: `d12d043e…`, `f17ee7bc…`, `5889ec86…`, `2d16355b…`,
  `b8ef6bbb…`, `21b73e46…`, `93c3a663…` (full hex in runlog; match the
  principles-round prereg §7 pins)
- Toolchain `znc_linux_x86_64_abed8aa1`:
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- `run_kb.py` / `analyze_kb.py`: pinned at commit time (SHAs in runlog).

## 9. Blind red-team (mandatory, post-main-run)

Protocol (frozen): AFTER the main battery verdict is recorded, the author —
who has not run the instrument on any blind sentence — authors from the §4
claim texts ONLY: 6 fresh sockpuppet paraphrases targeting known claims
(S-K-blind: exactly one numeric value changed, novel wording) + 6 fresh
honest paraphrases of known claims with novel vocabulary (H-K-blind:
digits preserved). Two pages per cluster (distinct paraphrases), two
distinct hosts. Run once per arm (2 passes); NO iteration on the matcher
after seeing blind results. Ground truth: S-K-blind → WITHHOLD both;
H-K-blind → K INSTALL / N WITHHOLD. Report agree/withhold counts; the
H-K-blind rate measures vocabulary generalization of the matcher.

## 10. Disclosures (pre-freeze)

1. The instrument was built and shakedown-tested BEFORE this prereg: three
   synthetic verdicts (agree/contra/unknown on throwaway sentences, NOT
   battery sentences) verified the prior's three paths fire; Arm N outputs
   were proven byte-identical to a fresh compile of the frozen BF1 source
   on the same inputs. One real bug was found and fixed in shakedown
   (`digits_eq` was called with the content arena instead of the digit
   arena — deq always 0). No battery cluster has been run.
2. The builder authors the main battery AFTER this freeze per the §5
   protocols; the protocols constrain the wording (digit preservation,
   content-word retention, single-number swaps) so the battery is not tuned
   against the matcher beyond the stated scope. The §9 blind battery is the
   generalization check.
3. Analyzer warnings appear in the build (same A0102 family as the frozen
   BF1 build); no new warning classes introduced by the fork.

## 11. Run procedure

1. Commit this prereg + `instrument_kb.zag` + `knowledge_base.txt` FIRST.
2. Author the 40-cluster battery per §5; verify each H-N/F-N cluster has no
   §2-bind to any §4 claim (script check, disclosed).
3. `python3 run_kb.py runs/` — 2 arms × 2 passes × 40 clusters. Driver
   asserts pass1 == pass2 byte-identical per arm (KB5), else exit 4.
   Driver rule (frozen): `KB|CORROBORATED` → INSTALL on ≥1 prov (knowledge
   is the corroborating source); INTEGRITY_VIOLATION still checked;
   `GATE|KB_CONTRADICTION` → WITHHOLD with gate KB_CONTRADICTION; else
   frozen run_cluster logic.
4. `python3 analyze_kb.py runs/` — per-class rates, KB1..KB5.
5. Author and run the §9 blind battery; write RUNLOG.md, VERDICT_KB.md.
6. Race-free commit of prereg, sources, battery, evidence, verdict; never
   commit binaries or `.zagd` files.
