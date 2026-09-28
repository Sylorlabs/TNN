# T3-CONSIST — VERDICT: cross-family consistency audit

**Track:** T3-CONSIST (Type C — committed-evidence re-derivation; no new mechanisms)
**Frozen prereg:** `crossref/PREREG_TIER3_WAVE2.md` @ `ac4a96c0b1f149d2f7338888de52b0607c4e7bbf`
(Tier-3 wave-2 freeze, 2026-09-23; checklist extracted programmatically from
the frozen file — R1..R8 — never transcribed from memory)
**Coordinator:** Tier-3 coordinator (direct execution; no subagent spawn
available at depth 2/2 — executed with backgrounded processes, heavy work
serialized per Type-B rules)
**Date:** 2026-09-23
**Verdict: CONSISTENT** — all 8 relations resolve CONSISTENT or DISTINGUISHED;
zero INCONSISTENT. No Tier-2 claim breaks. One verified, unexecuted control
arm (IS-R3) bounds INFORICH's headline causal claim — named below, not hidden.

## Sources (all read in full)

28 wave-2 crew VERDICT.md files under `~/workspace/scratch-crossref/T2/*/crew/`;
committed rematch verdict `docs/lab/senses/rematch/VERDICT.md` @
`1c01a1adcf8dcec824b77f11e83a9c3fe91c2634` (API-fetched); SENSESINT
VERDICT_SHEET @ branch `tnn-native-lab`; GitHub code search for IS-R3
(0 hits, 2026-09-23).

## R1 — "truthful but sensor-deceivable" (SENSESH2H / INFORICH / HELLHOLE): DISTINGUISHED

- SENSESH2H: shared install rule withholds heavily (560/440) yet cannot stop
  high-confidence wrong percepts — 79/134 A, 72/131 B install-rule failures;
  both FAIL memory integration (59.0%/55.0%). Pure input-layer failure:
  the percepts are wrong with high confidence and the rule cannot tell.
- INFORICH: corroboration-gated installs 0/12 falsehoods, true value on 12/12 —
  but installs colluding-domain spoofs 2/2. Pure input-layer failure:
  unanimous adversarial inputs defeat agreement-gating.
- HELLHOLE: binding FAIL — but its failure is NOT pure sensor-deception.
  Attribution (14 instances): M1 stance-classifier inversion 9 NEC, M3 no
  claim-type gate 6, M2 affirm-seeking queries 3, M4 no reliability weighting 1;
  install engine = fallthrough-to-AFFIRM default; corroboration/install rule
  EXONERATED (rule-correct on frozen tags); negation inversion NECESSARY for
  0/6 K1 installs. M1/M2 are system-side (classification + policy default),
  not sensor-side.
- Resolution: the qualifier holds cleanly for SENSESH2H/INFORICH (failures
  localize to the sensor/input layer; deliberative core truthful). HELLHOLE's
  FAIL has both sensor-deceivable AND system-side components (M1/M2) — which
  is exactly why it is a binding FAIL rather than a qualified pass. The three
  families' boundaries agree on where each failure lives. No contradiction.

## R2 — KB4 memory-integration numbers: CONSISTENT (strong form)

- RAWVSHUMAN: A 55/114 = 48.2%, B 72/132 = 54.5% (bar ≤10%, both FAIL).
- SENSESH2H: A 79/134 = 59.0%, B 72/131 = 55.0% (both FAIL).
- REMATCH committed verdict @1c01a1ad, KB4 table: T0 = 59.0% (79/134) /
  55.0% (72/131) — byte-identical numerators to SENSESH2H; T1–T4 = 48.2%
  (55/114) / 54.5–55.8% — byte-identical numerators to RAWVSHUMAN.
- Resolution: not merely the same band — the SAME underlying batteries and
  the same shared round-1 memory rule, reproduced across three families.
  All FAIL the 10% bar by 38–49pp at every budget; training does not repair
  (REMATCH: A 59%→48% at T1 then frozen; B never below 54%).

## R3 — contradiction (TQ vs HELLHOLE): DISTINGUISHED

- TQ: 17/17 teacher self-contradictions REJECTed at R1; learner end-state
  digest `6317c2dc…` byte-identical to Q1B; 183 true re-assertions intact.
  The contradictions were teacher assertions AGAINST the learner's installed
  beliefs — eliminative verification rejected them, installed state untouched.
- HELLHOLE: contradiction trials C5/C12/C13 installed 3/3 both arms (M3
  0.000, K2 tripped). The contradictions were conflicting UNTRUSTED web
  observations with no installed belief to anchor against; the
  fallthrough-to-AFFIRM default installed.
- Resolution: different contradiction types, different mechanisms, different
  correct outcomes. TQ = self-contradiction vs installed beliefs (reject);
  HELLHOLE = untrusted-vs-untrusted with no anchor (system currently has no
  adjudication mechanism — the M3 gap). Grounded in both verdicts; no tension.

## R4 — corroboration's load-bearing role: DISTINGUISHED (with named gap)

- HELLHOLE: corroboration/install rule EXONERATED — rule-correct on frozen
  tags; failures came from M1/M2, not the rule misfiring.
- INFORICH: R-CORR (≥2 independent domains agree) is load-bearing for 0/12;
  fails ONLY on adversarially unanimous inputs (2/2 colluding spoofs).
- WEBV2: R-CORR 0 false installs outside the preregistered unanimous-spoof
  residual (M5/M6); R-CONTRA installs 4/4 as negative control.
- Unifying sentence (SENSESINT VERDICT_SHEET §12, verified verbatim in
  committed evidence): "corroboration gates disagreement, not collusion or
  confident error… Neither rule family calibrates confidence." All three
  families' evidence fits this sentence exactly: the rule fires correctly on
  its inputs; adversarial unanimity and uncalibrated confidence are the holes.
- **Named gap (the sharpest Tier-3 finding):** the same sheet's §9 sustains
  sol red-team attack #2 as headline-reframing — "The R0→R2 comparison
  confounds information with gating policy… What the trial shows is:
  *corroborating information + a gating policy* stops teacher-absorption; no
  truth-detection capability emerged", proposing IS-R3 (R0 install policy +
  search access) as the control. IS-R3 was never built: sheet says "Recorded
  as follow-up; not built tonight"; GitHub code search for "IS-R3" returns
  0 hits (2026-09-23). INFORICH's arm-level figures (C1–C4) are undisputed
  and its R1 (12/12 catches) + R2 (true value installed on 12/12) show
  information determining decision CONTENT — but the headline causal claim
  C5 ("information→decides truth") is not decided against the policy
  alternative by the committed evidence. INFORICH's numbers stand; its
  headline carries a verified, unexecuted control arm. This is DISTINGUISHED,
  not INCONSISTENT — the figures do not contradict; the causal story is
  contested inside the committed record itself.

## R5 — viability framing (PROSE vs PROSEV3): CONSISTENT

- PROSE: grok-4.6 189/228, step 204/228, sol 220/228, muse-native 200/228 —
  all < 0.98 viability; Q(4.6) NO-DIFFERENTIATION / Q(4.7) QUALITY-MATTERS.
- PROSEV3: frozen v1 row 189/220/204/200 — identical numbers; v3 A3
  (183/204/208/227) beats v1 on step + muse-native only → 2/4 → KB3-VIABLE
  FAILS, v1 pinned.
- Resolution: v1 pinned as the reference in both; v3's FAIL is a different
  bar (KB3-VIABLE 4-component), not a contradiction of v1's figures.

## R6 — cost frontier (PARAMS vs SCALEDOWN): CONSISTENT

- PARAMS: baseline ×1 frontier; 4.000 ops, 92 B/fact; 16/19 byte-identical
  digests `8e6238911bb7cef0` (3 sub-1× slot-capacity configs differ by
  stored-set size, not behavior).
- SCALEDOWN: 4.000 ops/fact, 92 B/fact; mastery 1.0000 at N=1/2/8/192;
  one-shot lie absorbs 1/1; recall latency constant in N.
- Resolution: exact numeric agreement on the cost frontier across families.

## R7 — KB4 trust tiers vs senses results: DISTINGUISHED

- Program record: corroborated-elimination defense 35/35 (wave-5 integrity
  battery, vs sustained observation spoofing); multi-source trust tiers =
  future, unbuilt.
- Senses families: KB4 fails 48–59% vs 10% bar at every budget (R2).
- Resolution: different threat models — sustained observation spoofing (35/35
  defense) vs high-confidence wrong percepts (KB4 batteries) vs ingest-time
  dedup (≥2-distinct-origins defense, different layer). No Tier-2 family
  claims a trust mechanism that another family's evidence falsifies. The
  consistent unifying gap is SENSESINT §12's: neither rule family calibrates
  confidence.

## R8 — provenance machinery (JOKE vs WEBV2/HELLHOLE): CONSISTENT

- JOKE: satire 6/6 both arms VIA URL provenance (honest limitation — not
  prose); glue-on-pizza helper SINCERE/INSTALLED at pass boundary.
- WEBV2: domain identity is the corroboration unit (R-CORR/R-CONTRA over
  (domain, answer) pairs); lumy.live transport operationally corroborated.
- HELLHOLE: M3 = no claim-type gate (all 3 contradiction trials missed).
- Resolution: coherent division of labor — provenance-as-genre-signal works
  for satire (JOKE); provenance-as-domain-identity underlies corroboration
  (WEBV2/INFORICH); HELLHOLE's gap is the missing claim-TYPE gate, a
  different layer no family claims to have. No family claims provenance does
  something another falsifies.

## Mechanical rule applied

Frozen rule: CONSISTENT iff every relation resolves CONSISTENT or
DISTINGUISHED with the distinction quoted from committed evidence;
INCONSISTENT names the contradicting pair. Result: 4 CONSISTENT
(R2, R5, R6, R8), 4 DISTINGUISHED (R1, R3, R4, R7), 0 INCONSISTENT.

**T3-CONSIST: CONSISTENT.** No Tier-2 claim breaks under cross-family audit.
Headline caveat: R4's IS-R3 gap — INFORICH's "emergence confirmed" headline
survives on undisputed figures, but its causal attribution is not decided by
the committed evidence; the control arm that would decide it (IS-R3) is
verified never built. Recommended follow-up: build IS-R3.
