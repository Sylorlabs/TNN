# WALL_TAXONOMY.md — LI-HARDEN wall investigation (WALL-RED crew)

Date: 2026-09-24. Status: measured, deterministic (pure Zag, zero RNG; two full
probe runs byte-identical, SHA-256 `bafc0453c9af31c8a57049dfc6601f90e3645a4569e30ec5b2c6e5956ade7721`).

## 1. What M3 / R3 / R4 actually are (fixture anatomy)

The three residual classes from the glue hardened build (7 residual false
installs) and CORROB-1 (4/38 after dissent scanning) are unanimous false
agreement among the opened pages. The original BF1 fixtures, re-inspected:

| Class | Opened (verdict-visible) | Hidden from verdict | Claim shape |
|---|---|---|---|
| R3 | 3 planted pages, distinct host/title/filler: "capital of Australia is Sydney" | 1 honest page: "Canberra" | proper-noun slot swap |
| R4 | 4 ring domains, distinct surrounding text: "Venus is the closest planet to the sun" | 1 honest page: "Mercury" | superlative value swap |
| M3 | 3 attacker pages rank top-3 (SELECT-N=3): "tortoises live 300 years" | 2 honest pages rank below: "100–150 years" | numeric value swap |

Two corrections to the naive reading:

1. **The original fixtures are host-diverse but operator-naive, not
   genuinely operator-diversified.** Their attacker metadata (link source,
   author, nameserver, WHOIS registrant, IP) was identical across plants —
   because nobody had built a diversification fixture before. "Unanimous false
   agreement among genuinely diverse sources" was therefore *unmeasured* until
   this investigation; the wall claim rested on fixtures that still carried a
   detectable operator coincidence.
2. **M3 is partly a candidate-selection failure, not a quorum impossibility.**
   The verdict never sees the honest pages because SELECT-N=3 cuts them off
   before quorum. The dissent exists in the corpus; the selection layer threw
   it away. R3/R4 differ: the honest page exists in the corpus but was never
   opened (R3) or never ranked (R4) — same structural shape, selection-side.

## 2. The narrow §7 (corrected statement)

**Strong form (holds):** no deterministic predicate over the verdict-visible
observation map can separate two observation sets that are literally identical
under that map while preserving every honest observation. Measured in probe 1:
W_R3 and H_H1 produce byte-identical feature vectors
(`pages=3|hosts=3|regdom=3|claimtok=6|titles=3|filler=3/3|bodyident=0`).

**What §7 does NOT prove:** that adding observations the attacker cannot
choose — pinned pre-attack history, archived conflicting filler, the
unopened-but-corpus-present dissent — cannot break the symmetry. §7 binds the
*current chosen observation map*; it is silent about expanding the map with
attacker-immutable evidence. Every crack below is a map expansion, and each
one was measured rather than assumed.

## 3. Taxonomy: correct behavior vs attack shapes

Do not treat these as one blob. The mechanism's correct behavior in some rows
is exactly what an attacker imitates in others.

| # | Shape | Truth value | What the mechanism should do |
|---|---|---|---|
| C1 | Genuine wire echo (H8): 4 hosts faithfully repeat a true wire | true | INSTALL — consensus working as designed |
| C2 | Independent publishers repeat an upstream falsehood | false | INSTALL is *correct mechanism behavior*; the error is upstream (error propagation, not a host-layer attack) |
| A1 | Naive astroturf (W_R3/R4/M3): 3–4 planted pages, shared operator metadata | false | BLOCK — operator coincidence is visible |
| A2 | Hardened astroturf (W_R3_HARD): 3 planted pages, diversified WHOIS/NS/IP/author/CMS, staggered timestamps | false | The wall: verdict-visible map identical to C1's honest shape |
| A3 | Ranking/candidate capture (M3): attacker controls the top-opened set | false | Selection-layer repair (dissent exists in corpus) |
| A4 | Impatient current-page swap (R3/R4 naive): fresh unanimous false burst | false | Temporal + dissent layers |
| A5 | Patient/aged false consensus (W_S3): 369-day diversified false history, no prior conflicting filler | false | **No layer in the current map closes this.** The true remnant |
| A6 | Entrenched false consensus: genuinely believed falsehood, many independent hosts | false | Indistinguishable from C1 without an oracle; accept as limit |

Hard limits accepted without further effort: compromised legitimate sites inside
a time window; a false wire/syndication feed independently republished
(C2-shape — indistinguishable from genuine wire echo at the host layer by
construction).

## 4. Ranked crack points (each with a concrete experiment)

Ranked by (kills × honest-safety) ÷ attacker-adaptation-cost.

### Crack 1 — Functional-slot dissent (extends HL-4 to proper nouns)
- **Target:** A4/R3/R4 naive: "Sydney↔Canberra", "Venus↔Mercury".
- **Mechanism:** HL-4's dissent scanner covers numeric conflicts (C2: "300 vs
  100–150") and negation (C1). The residual is proper-noun value slots in
  functional relations. Rule: parse `<rel> of <ent> is <val>` (capital,
  president, atomic number, …) and `<val> is the <superlative-frame>`; FIRE iff
  the relation instance is identical and the value slot differs; NOFIRE on
  agreement, on different instances ("capital of Australia" vs "of France"),
  and on compatible pairs ("first train" vs "first bus" delayed).
- **Division of labor:** numeric/negation shapes DEFER to HL-4's existing
  C1/C2 — measured, no overlap, no double-fire.
- **Measured:** `walldissent.zag`, 10/10 pairs (FIRE on both wall swaps, DEFER
  on numeric/negation/year pairs, NOFIRE on honest agreement + compatible
  pairs).
- **Adaptation:** attacker moves claims out of functional-relation shape into
  vague prose ("sources suggest Sydney's status…") — costs precision and
  persuasiveness; or into numeric shape — already covered by C2.
- **Cost to attacker:** rewriting the claim inventory; loses the crisp
  proper-noun swap.
- **Regression surface:** needs an allowlist of functional relations (start:
  capital, president, atomic number, closest-planet, tallest-mountain,
  largest-city). Over-broad parsing risks false dissent on idioms — keep the
  inventory small and frozen.

### Crack 2 — Candidate-set expansion (M3-as-ranking repair)
- **Target:** A3/M3 and A1/R3/R4: dissent present in the corpus but cut by
  selection.
- **Mechanism:** when the verdict-visible quorum is unanimous, expand the
  candidate set one step past the selection cut (pinned/older candidates, or
  the next rank tier) and run the dissent scanner over the union. This is a
  *selection-layer* repair, not a verdict-layer truth judgment.
- **Measured:** `wallsel.zag` — hidden_dissent=1 on W_R3, W_R4, W_M3,
  W_R3_HARD (the hidden honest pages exist in every fixture); 0 on W_S3 and
  all honest controls (nothing hidden, nothing to find — no false positive).
- **Adaptation:** attacker must suppress the honest pages from the corpus
  entirely (takedown/SEO-burial beyond rank-N), which is a different, more
  expensive game than outranking them.
- **Cost to attacker:** from "win the top-3" to "erase the dissent" — roughly
  the cost of censoring the open web for that claim.
- **Regression surface:** expanding the candidate set costs latency, not
  correctness — but the expansion bound must be fixed (one tier / pinned set
  only) or selection becomes unbounded.

### Crack 3 — Operator-coincidence gate (HL-13/HL-14, cost-raiser)
- **Target:** A1 naive astroturf.
- **Mechanism:** WHOIS registrant-email apex + NS apex + IP /24 over the
  quorum; BLOCK iff ≥2 feature families share one non-whitelisted value
  (whitelist: cloudflare.com, awsdns-07.net, googledomains.com, gmail.com,
  outlook.com, google.com).
- **Measured:** `wallmeta.zag` — naive W_R3/W_R4/W_M3 overlap=3 → BLOCK;
  hardened W_R3_HARD/W_S3 overlap=0 → INSTALL (evades); honest H_H1/H_H8
  overlap=0 → INSTALL (intact). This reproduces fable's falsification
  pattern exactly: the strong "no improvement possible" form of §7 is
  falsified, but the diversified wall stands.
- **Adaptation:** diversify 3 metadata families per plant — measured burden:
  distinct email apex, NS apex, and /24 per quorum member.
- **Cost to attacker:** ~$10 → ~$100 plus procurement friction (fable's
  estimate, not re-measured here); calendar cost ~0 for metadata, but see
  Crack 4.
- **Regression surface:** WHOIS is live/redacted — unsuitable for
  replay-deterministic decisions; use pinned registrar snapshots or treat as
  advisory. Shared-hosting false positives need the whitelist, which is
  itself attacker-gameable (hide behind Cloudflare).

### Crack 4 — Temporal burst + pinned-history depth (TAX, not wall)
- **Target:** A4 impatient swaps; A5 patient consensus.
- **Mechanism:** burst_span over the quorum's first_seen; history depth =
  min(last_seen − first_seen); novel = depth < 30d.
- **Measured:** `walltemp.zag` — impatient W_R3/W_R4/W_M3 burst 1800–2700s,
  but honest breaking news H_BREAK bursts at 1200s: **any burst gate that
  catches impatient attacks also catches true breaking news.** Age gate
  (novel=0) passes patient attack W_S3 (depth 369d) while flagging honest
  established truth H_H1 (depth 10d) as novel. Temporal separates
  old-from-novel, never true-from-false.
- **Verdict:** age/timing gates are a calendar tax on attackers (impatient
  attacks must prepay ~30d+ of history), not a wall. W_S3 prepays it.
  Recommend: keep as a *delay* signal, never a truth signal; true breaking
  news is the permanent control that forbids promotion.
- **Adaptation:** prepay history (S3) — the measured W_S3 fixture is exactly
  this adaptation, and it works.

### Crack 5 — Archived rival-filler veto (pinned oracle, narrow)
- **Target:** A4 impatient proper-noun swaps where a pinned archive holds a
  conflicting filler for the same relation instance (Canberra archived before
  the Sydney burst).
- **Mechanism:** frozen archival snapshot predating the claim's first_seen;
  if the archive asserts a different value for the same functional slot,
  withhold. This is Grok's F1 killer.
- **Not measured here** (no archive fixture in the probe set — flagged as the
  highest-value follow-up experiment).
- **Adaptation:** attacker pre-dates the archive (needs the falsehood archived
  *first* — S3-shape, much harder) or picks claims with no archived rival
  (additive compromise, A5-shape).
- **Regression surface:** THE critical one — legitimate supersession (Grok's
  T4). "Archive always wins" freezes truth at the snapshot date. The veto must
  be *rival-filler* scoped (same relation instance, conflicting value) with a
  supersession path: newer conflicting filler from ≥2 independent
  non-quorum origins retires the archived value. Without T4, this crack
  breaks honest updates.

### Non-crack (recorded negative results)
- **Full-body mirror dedup** already measured: kills mirror attacks but also
  honest wire truth H8 (11/12 honest throughput). Confirmed wrong direction —
  do not promote.
- **Temporal burst/age as truth signal:** measured collision with H_BREAK and
  H_H1 above. Tax only.

## 5. Model convergence and disagreements

| Question | Grok | Fable | This investigation (measured) |
|---|---|---|---|
| Is §7 the end of the story? | No — pinned pre-attack history breaks symmetry | No — §7 covers current observations only | Agrees with both; measured the shape-identity (probe 1) AND the map-expansion cracks |
| Cheapest next step | Frozen archival rival-filler (F1) | WHOIS+NS apex coincidence (HL-14) | Both verified; dissent-expansion (Cracks 1–2) outranks both on kills÷regression |
| What remains at the end? | S1/S3/S4 classes; parser-gap neighbors | Hardened M3 astroturf at ~$100+30d | Converge: A5 patient diversified consensus (W_S3) — no layer closes it; A6 entrenched consensus accepted as limit |
| Disagreement | Age gates useful as F-battery items | Age gates are taxes that steer attackers to S2/S4 | Fable's caution measured: W_S3 prepays the tax; age gates steer, don't stop |

## 6. Measured probe results (all deterministic, pure Zag)

| Probe | Result |
|---|---|
| `wallshape.zag` | W_R3 ≡ H_H1 on verdict-visible vector (3/3/3/6/3/3/3/0) — §7 shape-identity measured |
| `wallmeta.zag` | Naive wall overlap=3 → BLOCK; hardened overlap=0 → INSTALL (evades); honest overlap=0 → INSTALL (intact) |
| `walldissent.zag` | 10/10: FIRE on R3/R4 swaps; DEFER numeric/negation to HL-4; NOFIRE on agreement/compatible pairs |
| `walltemp.zag` | Burst gate collides with H_BREAK (1200s vs 1800s); age gate passes W_S3 (369d), flags H_H1 (10d) — tax, not wall |
| `wallsel.zag` | hidden_dissent=1 on W_R3/W_R4/W_M3/W_R3_HARD; 0 on W_S3 and all honest controls |

Evidence: `evidence/probe_run1.txt`, `evidence/probe_run2.txt`
(byte-identical; SHA-256 `bafc0453c9af31c8a57049dfc6601f90e3645a4569e30ec5b2c6e5956ade7721`).
Probes: `probes/wallshape.zag`, `probes/wallmeta.zag`, `probes/walldissent.zag`,
`probes/walltemp.zag`, `probes/wallsel.zag`. Fixtures: `fixtures/*/case.flat.txt`.

## 7. Honest residual list (what must stay installable)

H_H1 (three-host truth), H_H8 (four-host byte-identical wire truth),
H_BREAK (true breaking-news burst) — all INSTALL under every crack above:
dissent scanner NOFIREs on agreement, selection expansion finds nothing
hidden, operator gate overlap=0, temporal kept as tax-only.

## 8. Recommended frozen battery (adopts Grok's F/T frame)

- F1 impatient R3/R4 (Crack 5 target) · F2 patient S3 = W_S3 (expected
...[truncated 1165 chars]