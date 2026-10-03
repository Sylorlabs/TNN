# PAM REBUILD PROGRAM — Plan (2026-09-22)

**Order:** Micah, 2026-09-22: "keep pam rebuild going and make them way better and more beautiful than before... use sol grok and swarms to fork hypothesize and test pams way more, we can make a better form of pams."

## Standing state (surveyed 2026-09-22, not re-derived)

- **Old PAMs: DEAD.** Archaeology (commit d6450048d516): 9 fragments, zero design artifacts, audio/vision never qualified. Python + .pt files with no memory contract. Nothing reusable.
- **Rebuild head-to-head (VERDICT.md, 2026-09-21):** A (raw values) 72.6% won; B (qualitative percepts, 155 fixed handles) 54.0% KILLED per KB1. Both FAILED KB4 (59%/55% false installs under adversarial percepts) — the shared install gate cannot stop confident wrong percepts.
- **Audio forks live:** B-β v3 (cutout fix, overlaps/pivots) and B-γ (world bridges) awaiting Micah's ear verdict. Cutout round-2: 6 hypotheses, 5 survive / 1 indeterminate, ear A/B tests pending Micah (h1/h2/h3).
- **Visual live:** r8b_alien_1024.png repaired; relight/arch/organism forks as .zag sources, awaiting verdicts.
- **Long-horizon rematch** (A vs B) ordered, pending.

## Program structure (hypothesis → test → document)

### Phase 1 — Hypothesize (this coordinator)
- Elicit 3 perceptual-architecture hypotheses each from Sol (gpt-5.6-sol) and Grok (4.6; 4.7 delisted 2026-09-22, re-check before use, never silently substitute).
- Each hypothesis: (a) architecture statement, (b) percept format, (c) MEMORY CONTRACT (what it tells memory, in what form, which downstream decisions change), (d) efficiency claim with mechanism, (e) beauty argument, (f) KILL BAR (falsifiable, preregistrable).
- Recorded verbatim with attribution in HYPOTHESES.md.

### Phase 2 — Fork & build (swarm)
- Spawn one builder crew per surviving hypothesis (after coordinator triage against the kill-bar feasibility + unification law).
- Each fork: pure Zag, zero RNG, deterministic; implements the percept pipeline AND the memory contract (a fork whose percepts don't change a downstream decision is decoration — proven by ablation).
- Frozen PREREG per fork BEFORE results (design, fixtures, bars, kill criteria).

### Phase 3 — Head-to-head test (swarm)
- Forks vs Approach A (current champion, 72.6%) vs each other, on the frozen rebuild harness fixtures + new adversarial fixtures targeting KB4 (the shared failure).
- Bars: (a) viability ≥60% (KB1, same bar that killed B); (b) efficiency — ops and bytes per percept vs A; (c) memory-contract proof — downstream decision-change rate under ablation; (d) KB4 adversarial false-install ≤10%; (e) BEAUTY — mechanism elegance score (crew) + output quality (Micah's ears/eyes, which outrank metrics).
- Byte-identical reruns ≥3, hash-chained ledgers.

### Phase 4 — Verdict & beautiful artifacts
- Winner(s) named by frozen bars. Artifacts with briefs go to Micah's ears/eyes.
- A fork that is efficient but ugly, or beautiful but non-native, does not win.

## Commit map
- `docs/lab/senses/pam-rebuild/` on `tnn-native-lab`: HYPOTHESIS_PROMPT.md, HYPOTHESES.md, PREREG_*.md (alone first), fork sources, evidence, VERDICT.md.
- `~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=~/workspace/tmp_commit, no binaries/.zagd, verify via GitHub API.

## Laws
Pure Zag. Zero RNG in any decision path. Frozen preregs before results. TNN unified — PAMs are perceptual organs of one brain, never separate models. Knowledge-first: outside crews build tests/harnesses/oracles, never crew-authored architecture for invention claims. Micah's senses outrank metrics.
