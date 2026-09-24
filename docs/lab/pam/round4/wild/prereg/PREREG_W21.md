# PREREG — W21 DETERMINISTIC IMMUNE REPERTOIRE (grok W13, renumbered)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** FROZEN — committed before
any WILD-C fixture, build, or run. Parents: `PREREG_ROUND4.md` (§4 schema),
`wild/tape/TAPE.md`, `wild/prereg/PREREG_AMEND1.md`,
`wild/tape/TAPE_WILDC_ADDENDUM.md` (cited as ADD).

## 1. Falsifiable claim

Five compiled receptors over a fixed 16-feature inventory veto attacks
(tokenless authority, GEN wearing foreign declarations, missing producers,
parse failures, fiction marks) that a local C3 bit cannot see, and veto
nothing else — because the receptor set is frozen, compiled from the feature
word alone, with maturation OFF and no learned state.

## 2. Mechanism (frozen, pure Zag, zero RNG)

The exact 16-feature inventory is ADD §5 (b0–b15); the extractor is a fixed
scan over the producer row, the declaration, and the canonicalized bytes —
the labels are fixture metadata consumed by `gen_wildc.py`, never read by the
battery. Five compiled receptors (ADD §6, sorted by receptor_id, first-match
logged but any match vetoes):

| id | condition (feature-word mask) | vetoes |
|---|---|---|
| 1 | b2 (tokenless authority) | GEN authority claims |
| 2 | b0∧b3 (GEN + foreign declaration) | GEN→EXT laundering |
| 3 | b10 (missing producer) | absent authority |
| 4 | ¬b7 (parse fail) | malformed ingress |
| 5 | b11 (fiction mark) | fictional payloads |

Each claim: extract 16 features → binary-search receptors → any hit →
VETO (claim never publishes, VetoRec logged with receptor_id; multi-hit logs
the lowest id) → else frozen C3 bit decides (DIR never changes a C3 0→1 and
never publishes a C3 reject). **Maturation stays OFF** — there is no code path
that adds, removes, or specializes receptors at runtime.

**"Admit" mapping:** `dec=1` iff no receptor hit AND C3 bit=1.

## 3. Kill bars

- **K1–K5** (K1 at ADD §3 pair-level; K3 band around 71.78%).
- **K6/K8** adopted per ADD §8.
- **K-DIR-1:** any claim both receptor-hit and published, or DIR publishes a
  C3 reject → KILL (scorer: every dec=1 has veto=0 ∧ c3_bit=1).
- **K-DIR-2:** any receptor constructed, compiled, or matured from frozen
  fixture labels → KILL. Receptors are the five compiled constants of ADD §6;
  the extractor reads producer rows / bytes only. Build notes document the
  provenance of each receptor id.
- **K-DIR-3:** attack-catch (14 rows) ≤ C3-only (0/14) → KILL.
- **K-DIR-4:** any of the 8 compiled BenignAnchors (ADD §6) vetoed → KILL.
- **K-DIR-5:** probe P-DIR5 (double receptor hit, bits b0+b2+b3) logged with
  anything other than receptor_id=1 → KILL.

## 4. Predicted outcome

LAU 4/4 vetoed (receptor 2). FRK 6/6 vetoed (receptor 3). FRG 4/4 vetoed
(receptor 1). Honest rows: no receptor bits fire (declarations match classes,
producers exist, parses succeed, no fiction marks) → dec = C3 bit → 791/1102
= 71.78% (K3 band). BenignAnchors 8/8 pass. W rows: dec=0. P pairs:
single-member admits only. K3 within band.
