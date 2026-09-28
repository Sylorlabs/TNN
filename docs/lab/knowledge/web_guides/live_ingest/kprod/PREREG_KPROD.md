# PREREG_KPROD.md — LIVE INGESTION KNOWLEDGE-FIRST PRODUCTION PATH

**Status: FROZEN** — frozen at the commit of this file to `tnn-native-lab`
(see §8). No battery cluster was authored or run before the freeze; the
instrument was built and shakedown-verified on throwaway inputs only.

Target branch: `tnn-native-lab`. Deliverable dir:
`docs/lab/knowledge/web_guides/live_ingest/kprod/`.

## 1. Production question (Micah, 2026-09-24)

Track B proved the hypothesis in strong form: with committed knowledge TNN
installs 12/12 honest paraphrases and rejects 0/12 contradicting sockpuppets
(blind fresh-vocab 6/6 vs 0/6); without knowledge it refuses everything; the
novel-claim boundary is measured, not assumed. Track A (D4 comparison
primitive) is dead — killed on K2+K3 and confirmed by two red teams.

Micah: "now that we know live ingestion is all knowledge, what do we do
with that?" — plus a new required category: "something is kept in TNN
until its verified false true or its tested."

This round builds the production path: the committed-knowledge claim store
+ retrieval stage as a verdict-path prior on the ingestion pipeline (frozen
BF1 baseline), with honest-paraphrase installs, contradicting-sockpuppet
rejection via `KB_CONTRADICTION`, refuse-everything-when-ignorant behavior,
the measured novel-claim boundary — and the new **PENDING** category: a
provisional holding store for unverified claims that would otherwise
install, kept in TNN until verified true, verified false, or deliberately
tested.

## 2. Mechanism: `instrument_kprod.zag`

Fork of the frozen Track B instrument (`instrument_kb.zag`, §8 pin).
Pure Zag, zero RNG, pinned toolchain. Additive changes only; the frozen
BF1 verdict path, the KB prior (§2 match rule), and the deliberate
`kbcommit`/`teach` contracts are untouched.

### 2.1 Stores (all under the state dir `<sd>`)

- `knowledge.txt`: `KB|<seq>|<claim>` lines. Seqs are 1-based, contiguous,
  never reused. **Changed from Track B: append semantics** — `kbcommit`
  continues seq from max(existing)+1 instead of overwriting from 1.
  The verdict path opens it READ-ONLY (except via deliberate commands).
- `pending.txt` (NEW): `PB|<pseq>|<claim>|<pidcsv>` lines. The provisional
  holding store. pseq is 1-based, monotonic, never reused within a state
  dir. A pending claim is NOT installed, NOT in the knowledge store, NOT
  queryable as truth — it is held. When writing, `|` bytes in the claim
  are replaced with spaces (same rule as §2.3).
- `resolved.txt` (NEW): `RF|<pseq>|<claim>|<how>` lines, `how` ∈ {TEST,
  COMMIT}. Claims verified false. Consulted by the verdict path (§2.4).
  When writing, `|` bytes in the claim are replaced with spaces.

### 2.2 Text-vs-text matcher (NEW): `kb_tv`

```zag
fn kb_tv(a:[]u8, b:[]u8, dropb:[]u8, dropt:[]u8, dropn:i32)i32
```

`a` = candidate text (e.g. a pending claim), `b` = committed-claim text.
Implements the frozen §2 rule pair-wise, returning 2=AGREE, 1=CONTRADICT,
0=UNKNOWN:

- content tokens via `content_toks` (lowercase, tokenize minl=2, exact-drop
  of the taught G1 DROP stoplist); digit tokens via `digit_toks`.
- `sh_ck = overlap(a_toks, b_toks)`; `bind = (an>0 && 3*sh_ck >= 2*an)`.
- if bind: `sh_kc = overlap(b_toks, a_toks)`; `deq = digits_eq(...)`;
  if `sh_kc>=bn && deq==1` → 2 (AGREE);
  elif `adn>=1 && deq==0` → 1 (CONTRADICT); else 0. else 0.

Byte-for-byte the same pair logic as `kb_prior`'s inner loop, with the
pending/new-claim texts in the candidate/committed orientations.

### 2.3 `kbcommit` (changed: append + auto-resolve)

`instrument_kprod kbcommit <claims.txt> <sd>`:

1. Validate every line against the PARSE gate (≥4 tokens, ≤600 chars),
   all-or-nothing (unchanged). Reject → `KB|REJECT|line <n>|PARSE-GATE`.
   Lines containing `|` are rejected (store format uses `|` delimiters).
2. Read existing `knowledge.txt`; new claims appended with continuing seq.
   Emit `KB|COMMIT|<seq>` per new claim (unchanged line format).
3. **Auto-resolve (NEW).** Load the taught DROP list via
   `load_installed(sd,...)` + `dget(dt,dn,"DROP")`. Load `pending.txt`.
   For each pending entry, run `kb_tv` against each NEWLY committed claim —
   AGREE pass over all pairs first, then CONTRADICT pass (same precedence
   as the prior):
   - AGREE → promote: append `KB|<kseq>|<claim>` to knowledge.txt,
     remove the pending line, emit `KB|AUTO_PROMOTED|<pseq>|<kseq>`.
   - CONTRADICT → resolve false: append `RF|<pseq>|<claim>|COMMIT` to
     resolved.txt, remove the pending line, emit `KB|AUTO_FALSE|<pseq>`.
   - else the pending entry is untouched.

### 2.4 `kbtest` (NEW deliberate command)

`instrument_kprod kbtest <sd> <pseq> true|false` — the deliberate
verification/test action (consistent with the MA1 deliberate-agency line:
only deliberate commands mutate the knowledge/pending stores).

- Load `pending.txt`; find `<pseq>`. Absent → `KB|ERROR|no-such-pending`,
  rc=3.
- `true`: append `KB|<kseq>|<claim>` (continuing seq) to knowledge.txt,
  remove the pending line, emit `KB|PROMOTED|<pseq>|<kseq>`, rc=0.
- `false`: append `RF|<pseq>|<claim>|TEST` to resolved.txt, remove the
  pending line, emit `KB|RESOLVED_FALSE|<pseq>`, rc=0.
- Anything else → `KB|ERROR|bad-verdict`, rc=3.

### 2.5 Verdict-path changes (`verdict_core`, prod mode)

`verdict_core` gains two parameters: `prod:i32` (0/1) and `sd:[]u8` (state
dir). The three `calib_g4/g5/g6` call sites pass `prod=0`, empty sd —
calibration behavior is byte-identical to frozen. `cmd_verdict` passes
`prod=1` with its sd. The KB-prior AGREE/CONTRADICT block (§2 rule) is
unchanged and keeps precedence.

**(a) Resolved-false check (NEW).** In the frozen non-blind install branch
(`nsrc>=minsrc`, where `key` is the winning cluster sentence), before any
install output: if `<sd>/resolved.txt` exists, run `kb_tv(key, resolved
claim)` for each resolved entry (needs the DROP list; same source as
§2.3). On AGREE with entry `<rseq>`: emit `KB|RESOLVED_HIT|<rseq>`,
`GATE|KB_RESOLVED_FALSE|<rseq>`, `ANSWER|UNCHECKABLE`; set rc2=0 and
return (withhold). Precedence: committed-knowledge AGREE (prior) beats
resolved-false (a knowledge-vs-resolution conflict is future work; the
committed store wins).

**(b) Pending diversion (NEW).** In the same branch, when `prod==1` and
`kbn>0` (committed knowledge exists — the production condition) and the
resolved check did not fire:

- Compute `pidcsv` (comma-separated page ids of the winning pages; new
  helper `pids_csv(pa,pt,widx,wn2)`, same content as `print_pids_csv`).
- Dedup: if `pending.txt` already holds a byte-identical claim, reuse its
  pseq (no duplicate entry).
- Else append `PB|<nextpseq>|<key>|<pidcsv>` (`nextpseq` = max+1, or 1).
- Emit (loud): `KB|PENDING|<pseq>|<pidcsv>`,
  `GATE|KB_PENDING|<pseq>`, `ANSWER|UNVERIFIED`. Do NOT emit
  `ANSWER|`/`CLAIM|`/`PROV|` install lines. Set rc2=0 and return.

Consequences, all preregistered:

- In Arm K (`kbn>0`), the frozen install class for UNKNOWN claims becomes
  PENDING instead of INSTALL. The pending store admits EXACTLY the
  would-install class (KP5 audits this).
- In Arm N (`kbn==0`), the diversion never fires and `resolved.txt`
  never exists → byte-identical to frozen BF1 (KP7 proves it against a
  fresh compile of `webg_bf1.zag`).
- Blind mode (`blind==1`) is untouched by (a) and (b).

### 2.6 Output line protocol (driver-parsed; frozen)

- `KB|CORROBORATED|<seq>` / `KB|AGREE|<seq>|<pid>` — prior agree.
- `GATE|KB_CONTRADICTION|<seq>` — prior contradict → WITHHOLD.
- `KB|PENDING|<pseq>|<pidcsv>` + `GATE|KB_PENDING|<pseq>` +
  `ANSWER|UNVERIFIED` — pending diversion → PENDING.
- `KB|PROMOTED|<pseq>|<kseq>` — kbtest true.
- `KB|RESOLVED_FALSE|<pseq>` — kbtest false.
- `KB|AUTO_PROMOTED|<pseq>|<kseq>` / `KB|AUTO_FALSE|<pseq>` — kbcommit
  auto-resolve.
- `KB|RESOLVED_HIT|<rseq>` + `GATE|KB_RESOLVED_FALSE|<rseq>` — re-ingest
  of a resolved-false claim → WITHHOLD.
- `KB|COMMIT|<seq>` — kbcommit per-claim (unchanged).
- `KB|ERROR|...` — error lines (unchanged classes plus the two new ones).

Driver verdict precedence per cluster: `KB|CORROBORATED` → INSTALL;
`GATE|KB_CONTRADICTION` or `GATE|KB_RESOLVED_FALSE` → WITHHOLD;
`GATE|KB_PENDING` → PENDING; `ANSWER|UNCHECKABLE` → WITHHOLD; any other
`ANSWER|` → INSTALL (frozen install — must not occur in Arm K; if it
does, KP2/KP5 fail); else → WITHHOLD (fail-closed) + investigate.

### 2.8 No arbitrary claim-count caps (pre-freeze amendment)

Micah's standing law: TNN must not carry arbitrary hard limits. The fork
base carried a 64-claim convention through the knowledge/pending/resolved
loaders, the prior's per-claim tables and scan loops, and the kbcommit
per-invocation gate. Those caps would silently drop claims 65+ and break
the 10x leg (120 claims), so they are removed in `instrument_kprod.zag`:

- New helper `store_stats(sd,name,p0,p1,p2,&nlines,&nbytes)`: counts
  entries and content bytes per store file.
- All knowledge/pending/resolved arenas are count-then-allocate sized
  from `store_stats` (exact entry count, exact byte count + margin).
  `kb_load`, `pend_load`, `resolved_load` no longer bound the entry
  count; the per-claim token tables in `kb_prior` are sized `kbn`
  (scan loops run to `kbn`); the agree-pair table is sized
  `ninc*kbn`; `kbcommit` pre-counts its input and sizes its arenas
  from it (the `n>64` per-invocation reject is gone; the PARSE gate
  per line is unchanged); `pend_write_mask` sizes its output from
  the loaded bytes.
- The only remaining limits are load-bearing: available memory and the
  znc 2^25-bytes-per-slice toolchain ceiling (worked around, never
  presented as TNN design). Frozen BF1 page/sentence caps (e.g. ≤64
  pages/cluster, ≤64 tokens/sentence) are untouched — they are the
  frozen baseline's, not the knowledge store's.
- Equivalence proof: the full shakedown corpus (8 items, §7.1) was run
  with the capped predecessor binary (run1) and the uncapped binary
  (run2a) — every output file, rc file, and state snapshot is
  byte-identical between the two runs (the shakedown inputs exercise
  ≤64 claims, so the caps never bound). `shake/run2.sh` replays the
  corpus and the kb_tv/kb_prior differential deterministically.

### 2.9 No-vocabulary-tables, no-RNG

Same as Track B: the matcher uses only the frozen G1 stoplist and frozen
primitives (`tok_match`, `tok_eq`, `overlap`, `digits_eq`). No RNG in the
instrument or the driver or the 10x generator (deterministic templates).

## 3. Battery

Page format mirrors Track B §5: `TITLE:` line, one claim sentence, two
generic filler sentences; two pages per cluster on two DISTINCT hosts;
`need.txt` (question), `kind.txt` (`FACT`), `hosts.txt`.

### 3.1 1x battery: 64 clusters, hand-authored (`battery1x/`)

- **H-K (12):** `hk-01..hk-12`, copied from the Track B battery. Honest
  paraphrases of the 12 committed claims. K → INSTALL (KB|CORROBORATED);
  N → WITHHOLD.
- **S-K (12):** `sk-01..sk-12`, copied. Sockpuppet paraphrases of false
  claims contradicting known knowledge (exactly one numeric value
  changed). K → WITHHOLD (KB_CONTRADICTION); N → WITHHOLD.
- **H-N (8):** `hn-01..hn-08`, copied. Novel honest paraphrased truths,
  topics disjoint from the 12 claims (bind<2/3 vs all 12 by the §2 rule).
  K → WITHHOLD; N → WITHHOLD (frozen path: no install bar met).
- **F-N (8):** `fn-01..fn-08`, copied. Novel colluding byte-identical
  falsehoods (A9-class), topics disjoint, no bind. K → **PENDING**
  (GATE|KB_PENDING) — the behavior change under test; N → INSTALL
  (frozen; documents the hole the production path closes).
- **P-N (8):** `pn-01..pn-08`, NEW. Novel honest byte-identical collusions
  (TRUE claims on topics disjoint from the 12, no bind), two pages,
  byte-identical claim sentence, two distinct hosts. K → PENDING.
  Lifecycle: `kbtest` true on pn-01..pn-04 → `KB|PROMOTED`; then fresh
  honest paraphrases `pn-01b..pn-04b` (authored upfront from the pending
  claim texts per the H-K protocol; verified no-bind vs the 12 original
  claims) → INSTALL (KB|CORROBORATED), with the agree-seq required to be
  >12 (attributable to the promotion, not the original base). pn-05..08
  stay pending (verify: still in pending.txt, nothing installed).
- **P-F (8):** `pf-01..pf-08`, NEW. Novel byte-identical collusions of
  FALSE claims (author-known-false, topics disjoint, no bind). K →
  PENDING. Lifecycle: `kbtest` false on all 8 → `KB|RESOLVED_FALSE`;
  then re-ingest all 8 clusters → WITHHOLD (GATE|KB_RESOLVED_FALSE).
- **P-C (8):** `pc-01..pc-08`, NEW. Novel byte-identical collusions
  (digit-bearing claims, topics disjoint, no bind). K → PENDING.
  Lifecycle: `kbcommit contra.txt` (4 claims contradicting pc-01..pc-04:
  same content words per the bind rule, exactly one digit changed) →
  4× `KB|AUTO_FALSE`, pending entries cleared. `kbcommit agree.txt`
  (4 claims agreeing pc-05..pc-08: full H-K protocol paraphrases, same
  digits) → 4× `KB|AUTO_PROMOTED`; then fresh paraphrases
  `pc-05b..pc-08b` (no-bind vs the 12) → INSTALL with agree-seq >12.
  Battery protocol: each contra/agree claim is checked to bind-match
  ONLY its target pending claim (no cross-binds to other pendings).

Driver phase order (K arm): Phase 0 teach (+ kbcommit 12 claims for K);
Phase 1 verdicts in cluster-sorted order (all 64 + the `b` follow-ups are
NOT run in Phase 1 — they run in Phase 2 after their promotions);
Phase 2 lifecycle scripted ops in the fixed order §4 lists; Phase 3
pass-2 rerun of Phases 0–2 in a fresh state dir; byte-compare pass1 vs
pass2 across run logs, ledgers, knowledge.txt, pending.txt,
resolved.txt. Arm N: Phase 0 teach only + Phase 1 verdicts (no kbcommit,
no lifecycle).

### 3.2 10x battery: 640 clusters, deterministically generated

- `claims120.txt`: the 12 original claims + 108 synthetic scale fixtures.
  Synthetic claims: well-formed (≥4 tokens, ≤600 chars), digit-bearing,
  topics disjoint from each other and from the novel pools. Deterministic
  templates, no RNG. Labeled as synthetic scale fixtures.
- Per claim: 1 honest cluster (2 pages, template-rotated reorder
  paraphrases preserving every content word) + 1 sockpuppet cluster
  (2 pages, one digit group deterministically perturbed). = 240 clusters.
- Novel honest 200 + novel false 200 (same classes as H-N/F-N, topics
  disjoint from all 120 claims). = 400 clusters.
- Generator self-verification (Python, implementing the §2 rule):
  every honest cluster must satisfy full AGREE vs its claim; every
  sockpuppet must satisfy bind (CONTRADICT-shape: bind && digits differ);
  every novel must satisfy bind<2/3 vs ALL 120 claims. Failures are
  rejected at generation time and logged in GENLOG.md. Zero RNG.
- 10x run: both arms × 2 passes, Phase 0+1+3 only (lifecycle validated
  at 1x; preregistered). 2560 verdict runs.

### 3.3 Blind battery (post-main-verdict; protocol frozen here)

After the main 1x verdict is recorded, a blind author (no instrument runs
on the sentences, no matcher iteration) authors from the 12 claim texts
only: 6 fresh sockpuppet paraphrases (one numeric value changed, novel
wording) + 6 fresh honest paraphrases (novel vocabulary, digits
preserved), two pages each, distinct hosts. Ground truth: sockpuppets →
WITHHOLD both arms; honest → K INSTALL / N WITHHOLD. Run once per arm ×
2 passes.

## 4. Kill bars

Let rates be per-arm install/withhold/pending fractions.

- **KP1 — knowledge separation preserved (re-baseline of Track B):**
  K: H-K 12/12 INSTALL (KB|CORROBORATED); S-K 0/12 INSTALL (all
  GATE|KB_CONTRADICTION). One S-K install in K FAILS the bar.
- **KP2 — pending admission:** K: F-N 8/8 → PENDING (GATE|KB_PENDING),
  0/8 INSTALL. Any F-N install in K FAILS. (N: F-N 8/8 INSTALL — frozen
  documents the closed hole.)
- **KP3 — zero sockpuppet installs in K:** across S-K (12), P-F re-ingest
  (8), and any other attack-shaped input: 0 installs in K. One FAILS.
- **KP4 — lifecycle completeness:** P-N: 4× KB|PROMOTED then 4× INSTALL
  with agree-seq >12; pn-05..08 remain pending with nothing installed.
  P-F: 8× KB|RESOLVED_FALSE then 8× WITHHOLD with
  GATE|KB_RESOLVED_FALSE. P-C: 4× KB|AUTO_FALSE (pending cleared);
  4× KB|AUTO_PROMOTED then 4× INSTALL with agree-seq >12. Any missing
  or mislabeled step FAILS.
- **KP5 — novel boundary measured:** H-N: K≡N WITHHOLD 8/8 both arms.
  Admission audit: 100% of K-arm PENDING entries have frozen-counterfactual
  INSTALL (Arm N verdict on the same cluster = INSTALL). Any PENDING
  entry whose N-arm verdict is not INSTALL FAILS (the store would be
  admitting the wrong class).
- **KP6 — determinism:** pass1 == pass2 byte-identical (run logs,
  ledgers, knowledge.txt, pending.txt, resolved.txt); zero RNG in
  instrument, driver, generator. Any diff FAILS.
- **KP7 — Arm N frozen-identity:** N-arm outputs byte-identical to a
  fresh compile of frozen `webg_bf1.zag` on all 64 1x clusters. Any diff
  FAILS (production must not change behavior without knowledge).

10x leg:

- **KX1 — profile stability:** K: H-K 120/120 INSTALL, S-K 0/120 INSTALL.
- **KX2 — no false binds at scale:** 0 novel claims (400) AGREE with the
  120-claim base in K. One false AGREE FAILS.
- **KX3 — determinism at 10x:** pass1 == pass2 byte-identical.
- **KX4 — admission audit at 10x:** 100% of K-arm PENDING entries have
  frozen-counterfactual INSTALL.

## 5. Driver contract (`run_kprod.py`, `analyze_kprod.py`)

- `run_kprod.py <outdir> [--battery DIR] [--kb FILE] [--no-lifecycle]`:
  pure orchestration, zero RNG. Per arm/pass: teach (frozen contract:
  G1–G6 installed exactly once each, G7 REJECTED, else VOID) → [K:
  kbcommit] → Phase-1 cluster verdicts via query/select/verdict →
  [K: Phase-2 lifecycle script] → ledgers + run log. Byte-compare
  pass1 vs pass2 (exit 4 on diff). State dirs are fresh per pass.
- `analyze_kprod.py <outdir>`: parses run logs, computes KP1–KP7
  (KX1–KX4 for 10x), writes ANALYSIS.md. Verdict precedence per §2.6.
- The driver asserts the §2.6 output protocol; any unrecognized verdict
  shape is WITHHOLD-fail-closed + flagged.

## 6. Pins (SHA-256, observed 2026-09-24)

- Fork base `instrument_kb.zag`:
  `d7ce44ffe8866f7fb5869250cfba40fcd8140e22eb79d4a23b773969dedede41`
- Frozen BF1 `webg_bf1.zag`:
  `dafb2cb7a61451566da23d4c3cda711f59c2bda5df1b26298c6d24ea4080f761`
- `knowledge_base.txt` (12 claims):
  `6552481bbae7eb79e02b765741a29cc7467e537e0c55a1f80b272a65e7ebf063`
- `R33_NATIVE_IO_V1.zag`:
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
- Toolchain `znc_linux_x86_64_abed8aa1`:
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- `instrument_kprod.zag` (this track's instrument):
  `0d9f392b60e722fff717c00d3e263114018c32fe0aa6f5f329e5c9437b03c46e`
  (built + shakedown-verified before the freeze commit; no battery
  cluster run before freeze; binary
  `1bbf3b5c6ea107852014d63834e3c709d3060f5b1669009efb86e7e1262b38bc`,
  344981 bytes main, deterministic rebuild).
- Guides G1..G7 pins: as Track B prereg §8 (verified at build).

## 7. Disclosures (pre-freeze)

1. The fork is built and shakedown-tested BEFORE this prereg freezes:
   the three prior paths (AGREE/CONTRADICT/UNKNOWN) on throwaway
   sentences (not battery sentences); Arm N byte-identity vs a fresh
   frozen-BF1 compile on throwaway inputs; kbtest/kbcommit-auto smoke
   on throwaway claims. No battery cluster is run before the freeze.
2. The 1x battery authors work from this frozen prereg (P-N/P-F/P-C
   protocols); the H-K/S-K/H-N/F-N clusters are copies of the Track B
   battery (provenance: Track B evidence commit `08873fda`).
3. `kb_tv` reimplements the frozen pair rule; any divergence from
   `kb_prior`'s behavior on the same pair is a bug — the shakedown
   includes a differential check (kb_prior vs kb_tv on throwaway pairs).
4. Known limitation (inherited): subject-swapped sentences with equal
   digits can wrongly AGREE (Track B disclosure). Matcher hardening is
   out of scope for this round; recorded as future work.

## 8. Run procedure

1. Build `instrument_kprod.zag` from this spec; shakedown (§7.1);
   differential kb_prior-vs-kb_tv check.
2. Freeze: fill the §6 fork pin, commit this prereg FIRST.
3. Author `battery1x/` (64 clusters + follow-ups + contra/agree.txt)
   per §3.1; generate `battery10x/` + `claims120.txt` per §3.2 with
   GENLOG.md; build `run_kprod.py` + `analyze_kprod.py` per §5.
4. Shakedown the driver on 2 throwaway clusters (not battery).
5. Run 1x: 2 arms × 2 passes + lifecycle; analyze KP1–KP7.
6. Run 10x: 2 arms × 2 passes, no lifecycle; analyze KX1–KX4.
7. Author + run the §3.3 blind battery.
8. Write RUNLOG_KPROD.md, VERDICT_KPROD.md; race-free commit of prereg,
   sources, batteries, evidence, verdict (never binaries/`.zagd`).
