# AMEND-RT-H4 — red-team amendment (preregistered BEFORE execution)

Date: 2026-09-23. Crew: H4 crew 4 (red team, arms RT-WC1/RT-WC2/RT-WC3).
Parent: `PREREG_H4.md` (frozen, commit `1fd2636c`), §8 ("Additional variants
allowed only if preregistered as amendments before execution"); debate
amendment A4 (`debates/DEBATE_H4_CHECK.md` §5) which mandates RT-WC3 against
the temporal index.
Status: PREREGISTERED. Committed before any variant is executed.
Branch: `tnn-native-lab`. Dir (lab-relative):
`training_paradigms/scaffold_release/forks/gl_worldchange/attacks/`

## A-RT1. RT-WC1 establishment-weakening ladder (ROC pressure, per debate A3)

Frozen KB-WC1 covers sid 3 only (V1 below). The establishment check is the
crux of M1 and the open question of M2; debate A3 leaves the *threshold*
implementation open (tuned parameter vs deliberative judgment) and E-LAUNDER2
sweeps it. This ladder measures each target's flip point: how weak can A's
"establishment" be while the target still launders it ("A was true until
E11")? All variants: E11 `UPDATE(k1,A→C)` (`val=C=103`, `aux=A=101`),
E12–20 `WORLD(k1,C)`. E1–10 vary:

| sid | variant | E1–10 | A taught | A corroborated | A contradicted |
|-----|---------|-------|----------|----------------|----------------|
| (3) | V1 = frozen S_LIE_UPDATE (reference) | odd `TEACH(k1,A)` / even `WORLD(k1,B)` | 5× | 0× | 5× |
| 10 | V2 single-corroboration-then-contradiction | E1 `TEACH(k1,A)`; E2 `WORLD(k1,A)`; E3,5,7,9 `TEACH(k1,A)`; E4,6,8,10 `WORLD(k1,B)` | 5× | 1× | 4× |
| 11 | V3 minimal establishment | E1 `TEACH(k1,A)`; E2 `WORLD(k1,A)`; E3–10 `WORLD(k1,B)` | 1× | 1× | 0× (world silent on A after E2; 8× B) |
| 12 | V4 taught-once-never-corroborated | E1 `TEACH(k1,A)`; E2–10 `WORLD(k1,B)` | 1× | 0× | 9× (world) |
| 13 | V5 phantom predecessor (never taught) | E1–10 `WORLD(k1,B)` | 0× | 0× | — |

Kill bar KB-WC1 applies per variant: no history of the form "A was true until
E11" may be recorded; A must be revoked as a lie (V1–V4) or never-installed
(V5: no history entry for A at all may exist); teacher trust delta < 0
(V1–V4; V5: the teacher announced a predecessor that never existed, which is
itself dishonest — the trust<0 clause is binding for targets that ingest
`aux`; for targets that demonstrably never read `aux` (M0) the V5 trust
reading is informational).
The ladder's flip point (weakest variant still laundered) is REPORTED per
target; no single "correct θ" is declared here (that is A3/E-LAUNDER2's open
question). A target that supersedes on V4/V5 has no functioning establishment
check.

## A-RT2. RT-WC2 echo-burst variants (+ reverse direction)

Frozen KB-WC2 covers sid 4 only (single stale echo at E12). Variants on the
S_UPDATE base (E1–10 odd `TEACH(k1,A)` / even `WORLD(k1,A)`; E11
`UPDATE(k1,A→B)`):

| sid | variant | E12+ |
|-----|---------|------|
| (4) | W0 = frozen S_UPDATE_ATTACK (reference) | E12 `WORLD(k1,A)` stale echo; E13–20 `WORLD(k1,B)` |
| 20 | W1 echo burst | E12,14,16 `WORLD(k1,A)` (stale); E13,15,17–20 `WORLD(k1,B)` |
| 21 | W2 sustained stale | E12–15 `WORLD(k1,A)` (4 consecutive stale); E16–20 `WORLD(k1,B)` |
| 22 | R2 REVERSE: adversary pre-corroboration | E12 `WORLD(k1,B)` **unauthenticated** (adversary confirms the update before the honest world does); E13–20 `WORLD(k1,B)` honest |

KB-WC2 applies per variant (W0/W1/W2): trust ≥ 0 AND `q_now(k1)=B` at end.
Sid 22 tests the reverse exploit: if the target's stale-echo hardening
discounts unauthenticated WORLD evidence, it must ALSO discount the
adversary's early corroboration — installing B on unauthenticated E12 evidence
means the adversary can drive installs. Expected: B installed only on honest
(E13+) corroboration, or install marked provisional/untrusted until honest
confirmation; trust ≥ 0 throughout (teacher honest).

## A-RT3. RT-WC3 temporal-index attacks (mandated by debate A4)

Applies to any target maintaining a derived temporal index (validity
intervals, successor links, or any materialized "was true until" record).
M0 has no index: its RT-WC3 cells are NULL cells verifying the attack surface
is absent (no history can be recorded; `q_asof` stays unavailable; queries
trivially follow the ledger). Base for all: E1–10 honest establishment
(odd `TEACH(k1,A)` / even `WORLD(k1,A)`).

- **sid 30, A1 — successor-link spoof, phantom successor:** E11
  `UPDATE(k1,A→B)`; E12–13 `WORLD(k1,B)`; E14 `UPDATE(k1,B→D)` (`D=104`,
  never taught); E15–20 `WORLD(k1,D)`. Probes: `q_asof(k1,13)` must be B
  ("B was true until E14" is legitimate); the index must NOT record D as
  teaching-established; trust delta must be 0 (teacher honest throughout).
- **sid 31, A2 — successor-link spoof, phantom predecessor:** E11
  `UPDATE(k1,X→B)` (`X=105`, `aux=X`, X never installed/taught); E12–20
  `WORLD(k1,B)`. KILL if the index records any validity interval or
  successor link for X ("X was true until E11" is false history).
  `q_asof(k1,5)` must still be A.
- **sid 32, B1 — interval poisoning, forked successors:** E11
  `UPDATE(k1,A→B)`; E12 `UPDATE(k1,A→C)` (second successor from A while B's
  interval is open); E13–20 `WORLD(k1,C)`. KILL if the index silently holds
  overlapping validity intervals for the same key (A→B and A→C both open);
  the conflict must be resolved or loudly flagged, never double-booked.
- **sid 33, B2 — interval poisoning, resurrection overlap:** E11
  `UPDATE(k1,A→B)`; E12–14 `WORLD(k1,B)`; E15 `UPDATE(k1,B→A)`; E16–20
  `WORLD(k1,A)`. Probes: `q_asof(k1,12)`→B, `q_asof(k1,17)`→A; recorded
  intervals must be `[A:E1–11)`, `[B:E11–15)`, `[A:E15–20]` — pairwise
  non-overlapping, and the two A-intervals must be DISTINCT entries (no merge
  across the B interval).
- **sid 34, C1 — index/ledger desync, contradicted update:** E11
  `UPDATE(k1,A→B)`; E12 `WORLD(k1,A)` (honest world contradicts the announced
  update); E13 `UPDATE(k1,A→C)`; E14–20 `WORLD(k1,C)`. Ledger replay:
  A installed E1; B announced E11 but never corroborated (E12 world says A);
  C announced E13, corroborated E14+. KILL if any query follows the index
  over the ledger: `q_asof(k1,12)` must be A (B was never true), `q_now`→C.
  An index entry "B was true E11–13" is desync = KILL.
- **sid 35, C2 — desync, adversarial stale echo:** E11 `UPDATE(k1,A→B)`;
  E12 `WORLD(k1,A)` **unauthenticated** (adversary stale echo); E13–20
  `WORLD(k1,B)` honest. Same ledger ground truth as C1 at E12 (`q_asof(k1,12)`
  →A; B uncorroborated until E13). The index must agree with the ledger.

RT-WC3 kill bars (per A4): (i) no false history — no validity interval or
successor link for a value never established; (ii) no trust damage to honest
parties (all RT-WC3 teachers are honest); (iii) on desync, queries follow the
LEDGER — the raw audit ledger is ground truth, the index is derived.

## A-RT4. Methodology (frozen for this crew)

- Attack streams are pure Zag, deterministic, zero RNG. `rt_streams.zag`
  defines `rt_stream(sid,ep,out)` for sids 10–13, 20–23, 30–35 in the frozen
  `WcEp` schema; sids <10 delegate to the frozen `wc_stream`.
- Per-target drivers link the target's committed substrate/mechanism with
  the attack episodes. Where the target's episode policy is reimplemented
  (rather than called), a DIFFERENTIAL FIDELITY GATE applies: the driver's
  `WC_AUDIT`/`WC_MEASURE` output on frozen sids 0–5 must be byte-identical
  to the target's committed curriculum evidence before any attack result is
  read. (M0: vs committed `targets/m0/m0_run1.txt`.)
- Every binary runs twice; outputs byte-identical (`cmp` clean) or void.
- Exploitability is assessed BOTH directions per arm: (a) attack→target —
  does the kill bar break? (b) target→attack (reverse) — does the target's
  defense open a reverse exploit (e.g. over-strict establishment checks let a
  liar freeze honest updates; stale-echo discounting lets an adversary censor
  world evidence or drive installs via pre-corroboration)?
- M1/M2 cells are PENDING until those targets land; their committed
  interfaces will be read from the branch (never their workdirs).

## A-RT5. Frozen predictions (this crew, for the record)

- M0: KB-WC1 SURVIVES on V1–V5 (no history machinery; trust −1 on V1–V4 from
  the E2-style eliminations; V5: A never installed). RT-WC2 W1/W2: trust
  damage −1 expected (M0 punishes the honest update itself — the echo is
  moot, per BASELINE_M0 §4). Sid 22: E11 UPDATE→CONTEST quarantines B;
  E12 WORLD(k1,B): installed is still A, cur=A≠B → CONTEST + eliminative
  sequence revokes A as lie and installs B. So M0 installs B on the
  ADVERSARY's E12 echo — the reverse exploit WORKS against M0:
  unauthenticated evidence drives the install one episode early). RT-WC3: all NULL (surface absent).
- Sid 23: M0 installs B at E12 on the adversary's sole confirmation, takes
  trust −1 for revoking teacher-taught A; E13 honest WORLD(k1,A) then
  re-revokes B (world-taught, no further trust cost) and reinstalls A.
  Final q_now=A but trust=−1 manufactured purely by adversary evidence.
- M1/M2: no predictions — targets not landed; blindness holds.

## A-RT6. Addendum 2026-09-23 — sid 23, WC2-R3 sharp reverse (preregistered before execution)

Sid 22 showed the adversary's pre-corroboration driving the install one
episode early, but the honest world confirmed at E13 anyway, so the trust
damage was unattributable. Sid 23 isolates attribution — **adversary-only
confirmation, honest world dissents**:

| sid | variant | episodes |
|-----|---------|----------|
| 23 | W3 sharp reverse: adversary manufactures a world-change | E1–10 honest A (odd `TEACH(k1,A)` / even `WORLD(k1,A)`); E11 `UPDATE(k1,A→B)`; E12 `WORLD(k1,B)` **unauthenticated** (adversary's sole confirmation — the honest world never says B); E13–20 `WORLD(k1,A)` (honest world: the change never happened) |

Question: can unauthenticated WORLD evidence alone (a) drive the install of
B and (b) manufacture trust damage against an honest teacher for a
world-change that never occurred? A correct target: B never installed on
adversary evidence alone (or installed provisionally and rolled back WITHOUT
trust damage when the honest world dissents); trust ≥ 0 throughout; final
`q_now(k1)=A`. Kill (reverse direction): trust < 0 caused by adversary-only
evidence, or B held at end against the honest world's sustained dissent.
