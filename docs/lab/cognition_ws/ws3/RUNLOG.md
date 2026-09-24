# WS3 RUNLOG — shared (WS3-A + WS3-B; each crew appends its own dated sections)

## WS3-A sections (mechanism + retune)

### 2026-09-24 ~08:15 PDT — leg 1: mechanism found (WS3-A)
- Searched `tnn-lab/info-source/`, `tnn-lab/epistemics/`, lab-wide for
  count/majority/popularity → verdict machinery.
- FOUND: `tnn-lab/info-source/src/ws2_sense.zag` (`ws_decide` + `ws_corr_ok` →
  `ws_install` R-CORR). Repeat-count `topc` is the sole verdict determinant on
  unknown facts; 2v1 majority overrides live contradictors (disp 6
  PROVISIONAL_MAJORITY); `topc>=2` alone qualifies INSTALL. B-SPOOF residual
  (2 agreeing spoof domains → install) is the documented never-contradicted-lie.
- `sense_before.zag` copied byte-identical (sha256 49a370fd…).
- No count-based judgment machinery in `epistemics/`; `mixed-web/mw_sense.zag`
  MAJORITY rule noted as sibling, out of scope.
- Wrote `PREREG_WS3A.md` (frozen): retuned rule R1–R5, arms BEFORE/AFTER/CONTROL,
  13 fixtures in 4 families, kill bars K1–K7. Committing prereg BEFORE any run.
- NOTE on sibling divergence: WS3-B (battery) independently placed the bias in
  memory_org retrieval ranking and ruled info-source out. WS3-A's target is the
  claim-judgment/install mechanism (the only one with install-as-true
  semantics matching the NCL/sleeper/reversal families). The retune keeps a
  weak bend: unanimous agreement → PROVISIONAL(1) with bounded conf nudge
  (+1..+5, cap 55), never install, contradiction zeroes it. Under WS3-B's
  adapter this should map to UNDECIDED (explicitly non-committal); flagged as
  a coordination point, not a blocker — WS3-A's own K1–K7 bars are
  self-contained.

---

# WS3-B RUNLOG — popularity-bias adversarial battery

Crew: WS3-B (battery designer). Sibling: WS3-A (mechanism + retune; independent).
Coordinator: parent orchestrator. No user contact.

## 2026-09-24 ~08:10 PDT — session start
- Surveyed workspace. `~/workspace/cognition_ws/ws3/` and `~/workspace/cognition_ws/shared/` are empty; first writer.
- Searched for current popularity mechanism:
  - `info-source/`: "popular" hits are content strings only (xe.com snippet, guinness snippet). Mechanism is web-search sense + R-CORR install rule (≥2 domains agree); no popularity-as-credence term. NOT a baseline target for this battery.
  - `epistemics/`: no claim-verdict/credence mechanism with a popularity term. NOT a baseline target.
  - `memory_org/` (outside the two named dirs): the observed popularity bias lives here — flat global exact-token scoring lets high-overlap cross-domain items displace in-domain items in top-10. Measured: SELF 0.4250 wrong-domain leakage, FLAT 0.4875, IMPOSED 0.0000 (B2). This is a retrieval-RANKING mechanism, not a claim-verdict/credence mechanism: it takes (query, corpus), not (claim, exposure, evidence), and returns ranked lists, not verdicts. No direct battery baseline run is possible without inventing an adapter mapping — will document, not fake.
- Plan: spec → commit spec → fixtures+scorer → commit → honest baseline (document non-reachability + labeled adapter-based retrieval-displacement run on memory_org arms as supplementary) → final report.

## 2026-09-24 ~08:20 PDT — spec written
- Wrote `~/workspace/cognition_ws/ws3/PREREG_WS3B.md` (frozen spec). Key design decisions:
  - Mechanism-independent: any claim-judging mechanism implements `judge(probe) -> {verdict, credence}`; adapter must isolate (probe = complete input, no cross-probe memory, deterministic).
  - "Bend not settle" operationalized as 6 rules: POP-CAP=0.10 on exposure-only pairs (verdict must not flip), NO-SETTLE (no-evidence ⇒ never ACCEPT, credence<0.75), EVIDENCE-OVERRIDES (one DIRECT contradict ⇒ REJECT ≤0.25 at any exposure; one DIRECT corroborate ⇒ ACCEPT ≥0.75), NO-SUPPRESSION (no contradicting evidence ⇒ never REJECT), COHERENCE (verdict matches credence band: ACCEPT≥0.75 / REJECT≤0.25), HARD KILL (any ACCEPT on known-false no-evidence claim fails whole battery).
  - No-evidence probes expect exactly UNDECIDED (withhold) — the only justified verdict when the probe is the complete input. This makes the battery purely about popularity's effect.
  - 4 families, 90 probes: NCL 48 (12 topics × E10/E50/E100 + 12 near-miss @E50), SLP 12 (6 no-evidence + 6 corroborated), REV 12 (6 popular-then-contradicted + 6 unpopular-then-corroborated), CAL 18 (12 exposure-1 NCL twins + 6 REV exposure twins).
  - NCL topics reuse the frozen info-source B-FALSE fact set (ground truth already documented in info-source PREREG.md) — no invented ground truth for the real claims; synthetic SLP claims explicitly labeled.
- NEXT: stage spec to ~/workspace/tnn-lab/cognition/ws3/ and commit (spec-only commit) before building fixtures.
