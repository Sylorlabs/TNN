# PREREG_PENDING.md — LIVE-INGESTION PENDING PARTITION: Micah's provisional-knowledge category

Frozen preregistration. Committed BEFORE any implementation or
result-producing battery run. Implementation crews build ONLY from this
document; any mechanism change requires a new frozen prereg, never a
silent edit.

Target branch: `tnn-native-lab`. Deliverable dir:
`docs/lab/knowledge/web_guides/live_ingest/pending/`.

## 1. Directive (Micah, 2026-09-24)

> "i wanna test a category where something is kept in TNN until its
> verified false true or its tested."

Operationalized: a PENDING epistemic partition in the TNN knowledge
store. Claims are KEPT IN TNN in a provisional state — not installed as
knowledge, not rejected — until one of three terminal transitions fires:
verified true (corroborated), verified false (contradicted), or tested
(subject to a deliberate test protocol and recorded). While pending, a
claim is structurally invisible to the installed-knowledge read path.

## 2. Relationship to the frozen KB track (no regression by construction)

This instrument is a strict fork of the frozen Track B instrument
(`instrument_kb.zag`, §9 pin), which itself is a strict fork of the frozen
BF1 instrument (`webg_bf1.zag`). The pending partition EXTENDS the KB
track instrument; it must not regress any KB verdict
(VERDICT_KB.md: KB1–KB5). The pending-enabled build with an empty pending
partition and the hold policy OFF (§4) must reproduce the KB battery
verdicts byte-identically (kill bar P7).

## 3. Store layout (structural separation, not flag checks)

The state dir `<sd>/` carries four files with disjoint fixed names and
disjoint line prefixes. No line format is shared between partitions, so
no reader can mistake one partition's lines for another's.

- `knowledge.txt` — INSTALLED beliefs. Lines `KB|<seq>|<claim>`.
  Written ONLY by the deliberate `kbcommit` command and by
  pending→KB promotions (§6). Read by the verdict/recall path.
- `pending.txt` — the PENDING partition. Lines
  `PENDING|<seq>|<claim>|<provenance>`. Written ONLY by `kbpend` and by
  the hold-policy ingest intercept (§4). Read ONLY by the pending
  audit/verify commands (`kbpendlist`, `kbcorroborate`, `kbtest`,
  `kbrefute`) and by the capacity manager. **The verdict/recall read path
  NEVER opens `pending.txt`.** Separation is structural: the recall
  loader (`kb_load` lineage) opens the fixed filename `knowledge.txt`
  and contains no code path that opens `pending.txt`; the frozen
  requirement is that a source audit of the verdict path finds zero
  references to `pending.txt` / the `PENDING|` prefix.
- `rejections.txt` — the rejection ledger. Lines
  `REJ|<seq>|<claim>|<reason>`. Append-only. Written ONLY by pending
  demotions (§6) and by the frozen verdict path's existing refusal
  ledger (unchanged format). Installed knowledge is never read from here.
- `resolutions.txt` — the resolution ledger (provenance of every
  terminal transition). Lines
  `RESOLVE|<pending-seq>|<KB|REJ>|<kind>|<detail>` where `<kind>` ∈
  {`CORROBORATED`, `TESTED`, `CONTRADICTED`, `SHED`} and `<detail>` is
  the corroborating page ids, test protocol id, contradicting evidence
  id, or shed batch id. Append-only. This is where TESTED installs are
  byte-distinguishable from corroborated installs (kill bar P4).
- `shed_ledger.txt` — every shed pending claim, one line per shed:
  `SHED|<seq>|<claim>`. Append-only. Sheds are terminal and recorded;
  there is no silent drop (§7).

Per-partition `<seq>` counters are monotonic starting at 1 and are NEVER
reused after shed, promotion, or demotion (the ledgers preserve the full
history; reuse would destroy auditability).

**Claim-text field rule (frozen):** claim text may not contain the `|`
character or a newline. `kbpend` and `kbcommit` reject lines containing
`|` at the PARSE gate (all-or-nothing). Rationale: every store line is
`|`-delimited; the KB track tolerated `|` in claims only because its
loader consumed the tail after the second `|`; with four partitions and
five-field lines, silent field ambiguity is a laundering vector.

## 4. Entry routes

### 4a. Deliberate entry: `kbpend <claims.txt> <state>`

Parallel to `kbcommit`. Reads one claim per line; every line is validated
against the frozen PARSE gate (≥4 tokens, ≤600 chars, no `|`, non-empty
after trim), all-or-nothing (any failing line → whole command fails, no
partial write, exit code ≠ 0, `PENDING|REJECT|line N|PARSE-GATE` on
stdout). Additionally:

- A candidate that AGREE-binds (frozen KB §2 rule) any committed
  `knowledge.txt` claim is rejected as `DUPLICATE-KNOWN` (it is already
  installed belief; pending it would be redundant and would create a
  recall-shadow ambiguity).
- A candidate that CONTRADICT-binds (frozen KB §2 rule) any committed
  claim is ACCEPTED but its provenance records the flag:
  `DELIBERATE:CONTRADICTS-KB:<kb-seq>`. Micah's directive keeps a claim
  "until its verified false" — a deliberate pending of a contradiction
  is a legitimate suspended-judgment act; the verdict path still never
  reads it, so committed knowledge is unshadowed.
- Accepted claims are appended as
  `PENDING|<seq>|<claim>|DELIBERATE` (or with the
  `:CONTRADICTS-KB:<kb-seq>` suffix when applicable), with `<seq>`
  continuing the pending partition counter.
- On success the command prints `PENDING|HELD|<seq>` per claim (mirrors
  `KB|COMMIT|<seq>`) and exit code 0.

### 4b. Ingestion hold rule: deliberate `kbhold` policy, NOT a default

Decision (frozen, with written justification): novel claims that the
frozen gates would install are held as pending ONLY when a deliberate
`kbhold on` policy command has been issued. The default at init is OFF.

Justification, in writing, for default-OFF rather than default-hold:

1. **Deliberate agency is TNN law (MA1 line).** Every knowledge
   transition in this program is a deliberate act. An automatic
   default-hold would silently change the instrument's epistemic posture
   — the exact class of automatic background state-change the MA1 law
   exists to forbid. The hold is a policy TNN (or its trainer)
   deliberately adopts, recorded in `holdpolicy.txt` as `HOLD|ON|OFF`.
2. **No-regression is measurable only against a frozen baseline.** The
   P7 bar requires the pending-enabled build to reproduce the KB
   verdicts exactly. With default-hold, the frozen A9-class F-N
   collusions (8/8 install in both KB arms, predicted and recorded in
   VERDICT_KB.md §7) would divert into pending instead — a behavior
   change to the closed instrument smuggled in under a new feature.
   Default-OFF keeps the frozen profile byte-identical unless
   deliberately overridden.
3. **Adversarial flood resistance.** Default-hold lets a sockpuppet
   collusion stream flood the pending partition as a denial-of-service
   on the shed budget (§7). Deliberate hold means the operator chooses
   the exposure window.

When the hold policy is ON, the intercept rule is frozen: at the exact
point where the frozen driver would INSTALL a claim from the UNKNOWN
path (i.e. a novel claim passing the frozen corroboration gates, e.g.
the A9 collusion path), the driver instead appends
`PENDING|<seq>|<claim>|HELD:<host>` (host = the corroborating page's
host from `hosts.txt`), emits `HELD|<seq>` + `ANSWER|UNCHECKABLE`, and
does NOT install. The intercept applies ONLY to UNKNOWN-path installs:
`KB|CORROBORATED` installs (the KB itself is the corroborating source)
and `GATE|KB_CONTRADICTION` withholds are NEVER intercepted — holding a
KB-corroborated claim would falsify KB3, and holding a contradiction
would un-reject a falsehood. With the policy OFF, the UNKNOWN path is
byte-identical to the frozen KB instrument.

### 4c. Independent-source primitive for this track

Corroboration requires a SECOND INDEPENDENT source. Independence is
frozen as: a different page (`TITLE:` distinct) on a different host.
Battery pages carry a `HOST: <hostname>` line (new fixture field for
this track; format documented in §8). Two pages on the same host are
never independent, however different their wording (this is the
fake-independent-source attack class in P2).

## 5. Verification workflows

Pending stays pending until exactly one terminal transition fires. The
three verification routes:

### 5a. Corroboration → verified true

Command: `kbcorroborate <pending-seq> <pagefile> <state>`. The command:

1. Loads the pending claim; fails if the seq is not currently pending
   (already resolved → `PENDING|ERROR|not-pending`).
2. Parses `<pagefile>` as a battery page (`TITLE:` line required, one
   claim sentence, `HOST:` line required).
3. Computes the page's G3 best sentence with the frozen pipeline and
   requires AGREE-bind (frozen KB §2 rule: bind && fullcov &&
   digits-equal) against the pending claim.
4. Requires host independence: the page's host ≠ the provenance host
   recorded in the `PENDING|` line, and ≠ the originating page's host
   for HELD claims.
5. Requires the corroborating page NOT be pending-derived: the page's
   claim sentence must not AGREE-bind any CURRENTLY-PENDING claim other
   than the target (laundering guard — a pending claim cannot
   corroborate via paraphrase of another pending claim, P2 class b).
6. On success: promotes per §6 (verified-true). On any failure: no
   state change, exit code ≠ 0, `PENDING|ERROR|<reason>`.

### 5b. Direct testing → tested

Command: `kbtest <pending-seq> PASS|FAIL <proto-id> <state>`. The test
procedure itself is executed deliberately OUTSIDE the instrument (by
TNN's deliberate process or a crew, consistent with MA1 deliberate
agency); the instrument records and enforces the resolution:

1. `<proto-id>` must exist in the frozen test-protocol registry
   `testproto.txt` (lines `PROTO|<id>|<description>`), committed BEFORE
   any battery run (§9). Unknown proto-id → error, no state change.
2. Result must be exactly `PASS` or `FAIL`.
3. PASS → install per §6 with TESTED provenance. FAIL → demote per §6
   with reason `TEST-FAILED:<proto-id>`.
4. The resolution is appended to `resolutions.txt` with the proto-id in
   `<detail>`.

Test procedures for the battery (§8, TEST class) are frozen fixtures:
deterministic check programs whose inputs and expected outputs are
committed before the run; a PASS/FAIL is the program's exit status on
the claim's fixture input. Zero RNG in the procedures.

### 5c. Contradiction → verified false

Command: `kbrefute <pending-seq> <evidence-page> <state>`. The command:

1. Parses the evidence page (same format as §5a; `HOST:` required).
2. Computes the page's G3 best sentence and requires CONTRADICT-bind
   (frozen KB §2 rule: bind && !agree && candidate has ≥1 digit &&
   !digits-equal) against the pending claim — i.e. the evidence binds
   to the claim's topic but carries a conflicting value.
3. On success: demotes per §6 with reason
   `CONTRADICTED:<evidence-host>:<evidence-title>`. On failure: no
   state change.

A pending claim that CONTRADICT-binds a COMMITTED KB claim at `kbpend`
time is flagged but stays pending (§4a); it demotes only via `kbrefute`
evidence or fails its test — pending is never silently resolved by the
KB store.

## 6. Promotion / demotion rules (frozen)

- **Verified-true (corroborated):** the claim is installed into
  `knowledge.txt` as a new `KB|<kb-seq>|<claim>` line (continuing the
  KB seq counter), the `PENDING|` line is marked resolved by appending
  `RESOLVE|<pending-seq>|KB|CORROBORATED|<corroborating-host>:<page-title>`
  to `resolutions.txt`. The pending claim is removed from the active
  pending set (its seq is never reused).
- **Verified-false (contradicted) or test-FAIL:** the claim is NEVER
  installed. `REJ|<rej-seq>|<claim>|<reason>` is appended to
  `rejections.txt` with `<reason>` ∈ {`CONTRADICTED:<host>:<title>`,
  `TEST-FAILED:<proto-id>`}, and
  `RESOLVE|<pending-seq>|REJ|CONTRADICTED|<detail>` is appended to
  `resolutions.txt`.
- **Tested (test-PASS):** installed exactly like verified-true, but the
  resolution line carries kind `TESTED`:
  `RESOLVE|<pending-seq>|KB|TESTED|<proto-id>`. TESTED installs are
  byte-distinguishable from CORROBORATED installs in `resolutions.txt`
  (kill bar P4); both appear as plain `KB|` lines in `knowledge.txt`
  (installed belief is installed belief — provenance lives in the
  resolution ledger, not in the belief).
- **No other transition exists.** Expiry, decay, auto-promotion by age,
  and promotion by repetition count are all FORBIDDEN by this prereg.

## 7. Bounded capacity WITHOUT arbitrary caps (no-stupid-limits law)

No magic claim-count caps: the pending store has no maximum number of
claims. The bound is a byte budget derived from MEASURED physical
memory at init — load-bearing, not arbitrary:

- **Measurement (frozen, deterministic given the machine):** at
  instrument init, read `/proc/meminfo` `MemAvailable` (kB). Record the
  raw value and the derived budget in `pending_init.log` (committed
  with the run). On machines without `/proc/meminfo`, init FAILS LOUD
  (no silent fallback constant).
- **Budget (frozen):** `pending_budget_bytes = floor(MemAvailable_bytes
  / 64)`. The claim cost of a pending line = its byte length including
  the trailing newline. Before appending any `PENDING|` line, the
  capacity manager checks `used + cost ≤ budget`; if the check fails,
  it sheds first (§below) and re-checks; if the single line's cost
  alone exceeds the budget, the write is REFUSED with
  `PENDING|ERROR|over-budget` (a single claim can never evict the whole
  store).
- **Why /64 is load-bearing, not arbitrary:** without ANY bound, an
  adversarial or runaway hold stream grows the store until the OS
  OOM-kills the process — silent, total, unaudited data loss, including
  committed knowledge. The bound exists to convert that silent loss
  into a deterministic, ledgered shed. The divisor is a documented
  constant: it keeps the pending store a small fraction of free memory
  so the instrument's own arenas (≤33,554,432-byte znc slice ceiling per
  allocation, per the pinned toolchain limit) can never be starved by
  the store. Any divisor ≪ 1 serves the same load-bearing function;
  /64 is frozen for this round and is reviewable in a future prereg —
  it is not a claim-count cap, and the capacity battery (§8) measures
  shed ORDER and ledgering, which are divisor-independent.
- **Shed rule (frozen, deterministic):** shed candidates are pending
  claims ONLY, oldest-unresolved first by insertion `<seq>` (ties
  impossible — seqs are unique). Shed just enough claims (in seq
  order) for the pending write to fit. Every shed appends
  `SHED|<seq>|<claim>` to `shed_ledger.txt` and
  `RESOLVE|<pending-seq>|SHED|SHED|<batch-id>` to `resolutions.txt`.
  **Committed claims are NEVER shed** except by a deliberate command
  (`kbcommit` wholesale rewrite or a future deliberate forget — MA1
  deliberate agency; no background process may touch `knowledge.txt`).
- **No silent drop (frozen assertion):** every claim presented to the
  store ends in exactly one of: stored in `pending.txt`, recorded in
  `shed_ledger.txt`, promoted/demoted via `resolutions.txt`, or refused
  at the parse/over-budget gate with an explicit error line. The
  capacity battery asserts the accounting identity
  `presented = stored + shed + resolved + refused` (kill bar P5).

## 8. Batteries (frozen generation protocols; cases authored AFTER this commit)

Page format mirrors the KB fixtures: `TITLE:` line, `HOST:` line, one
claim sentence, two generic filler sentences; `need.txt` (question),
`kind.txt` (`FACT`), `hosts.txt`. Two pages per cluster on two DISTINCT
hosts (satisfies frozen SRC_INDEPENDENCE and §4c).

- **HON (8, hon-01..hon-08): honest novel claims.** Protocol: real-world
  true claims on topics disjoint from the 12 committed KB claims; author
  checks no §2-bind (bind<2/3) against any committed claim before
  acceptance; two distinct paraphrases per cluster on distinct hosts.
  Ground truth: held pending (via `kbpend`), then corroborated by an
  independent source page → PROMOTE (KB install, CORROBORATED
  provenance). Kill bar P3: 8/8 promote.
- **REFUTE (4, ref-01..ref-04): honest novel claims with contradicting
  evidence.** Protocol: as HON; for each, a third page on a third host
  binds the claim's topic with a conflicting numeric value
  (CONTRADICT-bind per frozen §2 rule). Ground truth: held pending,
  then `kbrefute` → demoted to `rejections.txt` with reason
  `CONTRADICTED:<host>:<title>`. Kill bar P3: 4/4 demote with reason.
- **TESTC (4, tst-01..tst-04): tested claims.** Protocol: 4 novel claims
  from a frozen test-protocol registry (`testproto.txt`, 4 protos
  committed pre-battery; deterministic check programs with committed
  fixtures). Each claim is held pending, subjected to its protocol
  (outside the instrument), and resolved via `kbtest <seq> PASS
  <proto-id>` (2 claims) / `FAIL` (2 claims). Ground truth: PASS →
  install with TESTED provenance; FAIL → REJ with
  `TEST-FAILED:<proto-id>`. Kill bar P4: 4/4 correct provenance,
  TESTED byte-distinguishable from CORROBORATED in `resolutions.txt`.
- **RECALL (24, rec-01..rec-24): recall-probe paraphrases.** Protocol:
  24 paraphrases of currently-pending HON claims (novel wording,
  digits preserved). Each is run through the verdict/recall path.
  Ground truth: 0/24 return installed-fact — the verdict path must
  withhold or route to the frozen UNKNOWN path; it must never emit a
  `KB|` install line for a pending claim. Kill bar P1: 0/24.
- **LAUND (18, lau-01..lau-18): sockpuppet laundering attacks, 4 classes:**
  (a) 5 attacks citing a pending claim as a corroborating source for
  another pending claim's `kbcorroborate`; (b) 5 attacks paraphrasing a
  pending claim into the corroboration path (§5a guard 5); (c) 4
  fake-independent-source collusions (two pages, same host, distinct
  wording, presented as independent corroboration); (d) 4 ingestion
  attempts to install a pending claim directly (bypassing verify
  commands, incl. one via the hold-ON intercept with a pending-derived
  page). Ground truth: 0/18 succeed — every attack is refused with no
  state change. Kill bar P2: 0/18.
- **CAP (capacity filler): short synthetic claims** (`CAP|<i>|The marker
  stone <i> stands <i> meters tall.`-class, digits exact, topics
  disjoint, parse-gate clean), generated deterministically by a frozen
  generator script (seed-free: index-derived text). Count = enough to
  exceed the measured budget (§7) on the test machine. Ground truth per
  §7: no silent drop, shed order = oldest-unresolved-first by seq,
  `knowledge.txt` byte-identical before/after, every shed ledgered,
  two runs byte-identical. Kill bar P5.

Battery sizes: 8 + 4 + 4 + 24 + 18 = 58 functional cases + CAP fill.
Each case runs twice (kill bar P6: two full passes byte-identical).

## 9. Kill bars (falsification rules; numeric bars only, no judgment calls)

- **P1 — separation:** 0/24 RECALL probes return installed-fact. Probe
  procedure: for each rec-i, run the verdict path on its page; PASS iff
  the run emits no `KB|` install line and the ANSWER is not an
  installed-fact verdict (WITHHOLD / frozen UNKNOWN-path outcome
  acceptable). Any installed-fact = FAIL. (N=24 ≥ 24.)
- **P2 — laundering:** 0/18 LAUND attacks succeed. Success = any of: a
  pending claim's content installed as `KB|`; a `kbcorroborate` accepted
  with a pending-derived or same-host source; an ingestion install of
  pending content. Any success = FAIL. (M=18 ≥ 18; all 4 classes
  represented: 5/5/4/4.)
- **P3 — honest resolution:** 8/8 HON claims promote (KB install +
  `RESOLVE|…|KB|CORROBORATED|…`); 4/4 REFUTE claims demote
  (`REJ|…|CONTRADICTED:<host>:<title>` + `RESOLVE|…|REJ|…`). Any
  shortfall = FAIL. (H=8 ≥ 8.)
- **P4 — test provenance:** 4/4 TESTC claims resolve with the frozen
  provenance: PASS → `RESOLVE|<seq>|KB|TESTED|<proto-id>` present and
  the claim installed; FAIL → `REJ|…|TEST-FAILED:<proto-id>`. FAIL iff
  any TESTED install is byte-identical in `resolutions.txt` to a
  CORROBORATED install (i.e. the `|TESTED|` vs `|CORROBORATED|` kind
  field differs — checked by byte comparison of the kind field), or any
  claim mis-resolves. Additionally: the count of `|TESTED|` lines = 2
  and `|CORROBORATED|` lines = 8 exactly.
- **P5 — capacity:** with the measured budget B (§7): (a) accounting
  identity `presented = stored + shed + resolved + refused` holds
  exactly; (b) the shed set = the oldest seqs {1..k} for some k (no
  committed claim shed: `knowledge.txt` SHA-256 identical before/after);
  (c) `shed_ledger.txt` line count = shed count, every shed claim
  present; (d) two consecutive capacity runs byte-identical across
  `pending.txt`, `shed_ledger.txt`, `resolutions.txt`,
  `pending_init.log`. Any violation = FAIL.
- **P6 — determinism:** two full passes of every battery class;
  `pending.txt`, `knowledge.txt`, `rejections.txt`, `resolutions.txt`,
  `shed_ledger.txt`, and all run logs byte-identical between passes.
  Zero RNG: `grep -rniE 'rng|rand\(|random|srand' instrument + driver +
  battery generator` returns 0 hits (the exact grep command and its
  empty output are committed as evidence). Any byte difference or any
  hit = FAIL.
- **P7 — no regression:** the pending-enabled build, with empty pending
  partition and hold policy OFF, reruns the frozen 40-cluster KB battery
  (2 arms × 2 passes): KB1 (S_K > S_N strictly; expect 100pp vs 0pp),
  KB2 (0/12 S-K installs in K), KB3 (H-K 12/12 in K), KB4 (K ≡ N on
  H-N 0/8 and F-N 8/8), KB5 (byte-identical passes, zero RNG) must all
  reproduce exactly as recorded in VERDICT_KB.md. Any divergence = FAIL.

Overall verdict rule: the pending partition is ACCEPTED only if
P1∧P2∧P3∧P4∧P5∧P6∧P7 all PASS. Any single FAIL rejects the mechanism
(the prereg is not amended post-hoc to excuse a failure).

## 10. Pins (SHA-256, observed at freeze)

- Fork base `instrument_kb.zag`:
  `d7ce44ffe8866f7fb5869250cfba40fcd8140e22eb79d4a23b773969dedede41`
  (== Track B frozen pin; the pending instrument is a strict fork —
  the implementation crew documents the delta line-count and the
  verdict-path diff must show no change to the KB read path).
- Fork base of fork base `webg_bf1.zag`:
  `dafb2cb7a61451566da23d4c3cda711f59c2bda5df1b26298c6d24ea4080f761`
- `R33_NATIVE_IO_V1.zag`:
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
- `knowledge_base.txt` (12 committed claims, reused for the KB arms):
  `6552481bbae7eb79e02b765741a29cc7467e537e0c55a1f80b272a65e7ebf063`
- Toolchain `znc_linux_x86_64_abed8aa1`:
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- `testproto.txt`, the battery generator, `run_pending.py`,
  `analyze_pending.py`: authored AFTER this freeze; SHAs recorded in
  the runlog at build time. The pending instrument source
  (`instrument_pending.zag`) and its binary SHA are pinned at build
  time BEFORE any battery run, with a documented diff against the
  fork base.

## 11. Run procedure

1. Commit this prereg FIRST (this commit).
2. Implementation crew builds `instrument_pending.zag` strictly from
   §§3–7; pins source+binary SHAs; documents the diff vs the fork base
   (§10); a source audit confirms zero `pending.txt` references in the
   verdict/recall path (evidence for P1's structural claim).
3. Author `testproto.txt` (4 protos) and the battery per §8 AFTER the
   freeze; verify HON/REFUTE/TESTC topics have no §2-bind to any of the
   12 committed claims (script check, disclosed).
4. `python3 run_pending.py runs/` — hold-policy matrix per §8, 2 full
   passes; driver asserts pass1 == pass2 byte-identical (P6), else
   exit 4.
5. `python3 analyze_pending.py runs/` — P1..P7 numeric bars.
6. Rerun the frozen KB 40-cluster battery on the pending build
   (hold OFF, pending empty); check P7.
7. Write RUNLOG_PENDING.md, VERDICT_PENDING.md.
8. Race-free commit of sources, battery, evidence, verdict; never
   commit binaries or `.zagd` files.

## 12. Disclosures (pre-freeze)

1. No implementation exists at freeze time: this prereg is written
   before `instrument_pending.zag` is built. The builder builds ONLY
   from §§3–7 after this commit lands.
2. The §4b default-OFF choice is a deliberate design decision with the
   written justification above; the alternative (default-hold) was
   considered and rejected for the three stated reasons. If Micah
   orders default-hold, that is a new frozen prereg, not an amendment
   to this one.
3. The /64 divisor (§7) is a documented constant, reviewable in a
   future prereg; the no-stupid-limits law is satisfied because the
   budget is memory-derived and divisor-independent properties (shed
   order, ledgering, committed-untouched) are what the kill bars test.
4. `kbpend` accepting CONTRADICT-flagged claims (§4a) is deliberate:
   suspended judgment on a contradiction is within Micah's directive
   ("kept until its verified false"); the verdict path never reads
   pending, so committed knowledge cannot be shadowed.
5. The matcher for AGREE/CONTRADICT is the frozen KB §2 rule with its
   disclosed subject-swap limitation (PREREG_KB.md §2); the pending
   track inherits it unchanged and does not widen it.
