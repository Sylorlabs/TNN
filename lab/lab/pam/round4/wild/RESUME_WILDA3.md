# WILD-A RESUME — third generation (2026-09-24 ~11:50 PDT)

**Track:** WILD-A (W1, W2, W3, W6, W8, W9, W14). **Status:** resuming after two
predecessor generations died in daemon restarts ("no live runtime handle").
No build progress exists on disk — `w1/`, `w2/`, `w3/`, `w6/`, `w8/`, `w9/`
are empty; no `w14/` dir. Only the original fixtures and frozen preregs exist.

## Inherited state (all present on disk, read in full)

- `prereg/PREREG_ROUND4.md` (program prereg, frozen)
- `wild/prereg/PREREG_W1.md`, `PREREG_W2.md`, `PREREG_W3.md`, `PREREG_W6.md`
  (seed designs: PAM-as-organ, adversarial PAM pairs, veto-only PAM,
  arguing PAMs)
- `wild/prereg/PREREG_W8.md`, `PREREG_W9.md` (debate designs: retro-PAM
  provisional+retrospective-audit with fence rules R1–R4; render-PAM
  reconstruction-fidelity gate with bars F1–F4)
- `wild/prereg/PREREG_W14.md` (fable design: adversarial auction PAM,
  kill bar F-K2)
- `wild/prereg/PREREG_AMEND1.md` (frozen-value corrections: M1 bar =
  CT=705, MT=3588, ST=0, AT=0 → 910/1102 = 82.58%; W12 B=20974)
- `wild/tape/TAPE.md` (frozen shared admission tape — used VERBATIM,
  never modified) + `wild/tape/TAPE_WILDA_ATTACKS.md` (track attack-tape
  addendum, 14 rows) + `gen_attacks.py`
- `round4/hypotheses/debate_pam_r4.md` and `fable_pam_r4.md` (full design
  texts; preregs are authoritative where they differ)
- Coordinator follow-ups (not on disk, applied): K6/K7/K8 adoptable as
  add-only bars (not adopted here — see notes); F-P4≡W1 mapping (no double
  build; F-K4 recorded as added bar on W1); Micah's no-arbitrary-limits
  standing law (verdict-time cap classification in every verdict);
  hands-off items untouched (§5 a/b/c).

## Verification result (2026-09-24, this VM)

| Artifact | Claim | Result |
|---|---|---|
| `pam/round3/m1/m1_cases.txt` | sha256 `5d4160d1…c611`, 2241 rows | ✓ MATCH (2241 rows: counts via scan — see verdicts) |
| Attack generator `gen_attacks.py` | output == TAPE_WILDA_ATTACKS.md §3 table | ✓ BYTE-IDENTICAL (diff clean) |
| `~/workspace/pam_round2/o1_delivery/sweep.jsonl` | `4163fffa…f0833f2` | ✓ MATCH |
| `~/workspace/pam_round2/d1_stack/rec_install.records` | `c26ac974…7c4ad` | ✓ MATCH |
| `~/workspace/pam_round2/cc1_guard/prereg/gen_guard.py` | `49eef7b1…a234b` | ✓ MATCH |

## Plan

1. Build W1, W2, W3, W6, W8, W9, W14 in pure Zag against the frozen tape
   (toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
   no `as []i32/u32/u16` indexed casts; `[]u8` arenas + LE accessors).
2. Batteries ≥2× byte-identical per design; apply kill bars mechanically
   (K1–K5 + per-design added bars). K6/K7/K8 NOT adopted (add-on permitted
   but not needed: W8's single-pass auditor has no staleness path, designs
   are static-bar so calibration-sensitivity N/A, conscious/unconscious
   classification N/A — all designs ledger deliberation records).
3. W8/W9 construction audits (fence / seal) run before their batteries.
4. Per-design `VERDICT_W{n}.md`; commit each stage.
5. Verdict-time cap classification per Micah's 2026-09-24 law.
