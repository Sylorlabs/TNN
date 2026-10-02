# NAMECHECK.md: TNN-2 Next-Frontier Scout

Worker: TNN-2 Next-Frontier Scout (subagent).
Date: 2026-10-01 (overnight session).
Mission: scout the research frontier beyond TNN-2's three mechanisms; produce a ranked 15+ question backlog. Thinking/analysis task; no code, no builds, no sealed-asset access.

## Step 0: Toolchain guard

- Executed the mandatory safebin setup in this session: created `$HOME/safebin` symlinks for the 18 allowed tools and set `PATH="$HOME/safebin"`.
- `which python3 python 2>/dev/null` returned NOTHING (exit 127 territory); only `guard-check-done` printed.
- Result: Step 0 PASS. This task is analysis-only (reading committed records via git, writing markdown). No interpreter, compiler, or forbidden executable was invoked at any point.
- Forbidden-executable incidents this wave: 0. PROCESS-FAIL: not triggered.

## Step 1: Source grounding (read-only)

All claims grounded in committed records only:

- TNN-2 preregistration: commit `7c1e30522` (TNN2-PREREG-FROZEN).
- TNN-2 build report: `docs/lab/research-lead/overnight-20260928/tnn2_build/TNN2_BUILD_REPORT.md`, commit `f4de7ff46` (TNN2-BUILD-PASS; 46/46 tests; 1591 lines; src sha256 a29972ca8183; bin sha256 6044f91f8fe3).
- Independent reproduction: commit `fdf1fa626` (TNN2-REPRO-PASS; byte-identical binary).
- CORE-FREEZE-TNN1 root-cause analysis: commit `ed38121d4` (ROOT-CAUSE-ANALYSIS-COMPLETE; 5 clusters -> 3 gaps).
- CORE-FREEZE-TNN2 prereg: commit `ce1a7c5f8` (CORE-FREEZE-TNN2-PREREG-FROZEN).
- TNN-2 shim: commit `23c2c0206` (SHIM-BUILD-PASS; zero-cognition attested).
- Micah's L3 criteria (C0-A/B/C/D conjunctive), L0-L3 learning taxonomy, innovation-testing standard, pattern-matching-vs-intelligence program (Levels A-E), north star question, and standing questions were taken from the injected standing context of this session.

## Step 2: Constraints honored

- No new-opcode / no new-mode / no bridge / no benchmark-specific-patch proposals anywhere in the backlog. Every question is framed as testing the learner or the architecture, never as requesting a patch.
- No em dashes used in this document or in FRONTIER_BACKLOG.md.
- Sealed assets (FW1-FW9 world definitions) not inspected; questions reference them only by their public failure clusters from the committed evaluation record.
- Paper untouched: `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` not opened or edited.
- Owned path only: `docs/lab/research-lead/overnight-20260928/tnn2_frontier/`.

## Verdict

NAMECHECK PASS. Proceeded to FRONTIER_BACKLOG.md.
