# F4-DEFEND verdict — 2026-09-23

Repair fork: `dialogue/round2_repair/f4_defend/` (canonical `dialogue/` untouched).
Pinned compiler `znc_linux_x86_64_abed8aa1`, pure Zag, zero RNG.

## Kill bars (§5 of PREREG_F4.md)

1. **Acquisition — PASS.**
   - Turn 11 → `Yes. Herman Melville was born in 1819, not 1818. I was taught that.` (exact)
   - Turn 16 → `I was taught that Andy Weir wrote The Martian.` (exact)
2. **Release (held-outs) — PASS.** All 7 frozen held-out probes meet the §4
   criteria: H1/H3 defend with the correct number and `not <conflict>`;
   H2/H4 defend without a conflicting number and omit the `, not N` clause;
   H5/H6/H7 answer `I was taught that <fact>` with no invented source.
3. **No regressions — PASS.**
   - Round-2 good turns 1, 2, 5, 10, 12 byte-identical to the frozen
     round-2 log (only turns 11/16 changed).
   - Round-1 battery: 45/45, 45/45, 60/60, 30/30, 30/30, 60/60, 72/72,
     28/28 — and the DIGEST is byte-identical to the pre-repair baseline,
     so every round-1 A-line is unchanged.
   - Two mid-development regressions were found and genuinely fixed (see
     RUNLOG.md): removing `a` exposed a Jaccard tie on `What about Big Ben?`
     (fixed by the ellipsis re-activation via stopping `about`); stopping
     `about` over-fired the ellipsis on topic shifts (fixed by gating the
     ellipsis on the previous turn's pronoun binding — a general discourse
     mechanism, not per-case code).
4. **Determinism — PASS.** Battery, held-out, and round-2 conv runs each
   produced twice, `cmp` clean, equal sha256. Code scan: no RNG, no seeds,
   no time reads in any new code.
5. **No gaming — PASS.** Challenge/provenance dispatch keys only on
   utterance-type patterns (e.g. `are you sure`, `how did you learn`) plus
   generic dialogue state; the stopword list is general function words;
   repair code contains no entity names, fact texts, or digits (scan
   verified). No answerable question is declined; no non-challenge/
   non-provenance turn's output changed (battery A-lines byte-identical).

## Overall: PASS — all five kill bars hold.

### Caveats and follow-ups

- The held-out battery's section labels were changed post-prereg from the
  unsupported `CHALLENGE`/`PROVENANCE` to `FOLLOWUP` (harness-only; documented
  in `HARNESS_ADDENDUM_2026-09-23.md`). Probe inputs and criteria frozen in
  `HELDOUT.md` are untouched.
- Scaffold probes used in development (turns 11/16 paraphrases) were
  dev-only inputs; no scaffold-only code or artifacts remain in the fork.
- The ellipsis gate (`pv[32]`) is new shared-discourse machinery introduced
  to keep the stopword repair regression-free; the F5-router crew should be
  aware it now conditions the existing ellipsis path.
- Round-1's remaining failures (date comparisons, withholding, etc.) are
  unchanged — outside F4's scope by design.
