# REDTEAM_SELF.md: Self Red Team, wave-20261002-0521pdt ARENA lane

Date: 2026-10-02. Every result below is attacked on three axes:
metric gaming, harness coupling, knowledge-vs-architecture.
Findings that survive are kept; the rest are recorded as limits.

## R1. C9D5FIX GEN-PASS (D5 turns-path coin-flip fix)

Gaming: The G4 order bar (true_listed_first <= 2) is met by the
frozen seed's actual draws (1,1,0). This is not luck being
exploited: the fix makes the turns path honor the battery path's
flips structurally (dflip array), so EVERY seed now yields
consistent battery/turns order. The bar measures the mechanism,
not the seed. The old exploit still scores 0/3; the full-chain
keys cannot be matched by single-variable parsing.

Harness coupling: c9fix_check and the generator share RNG design
lineage (C9BAT), but the check tool reads only the turn stream,
and the causal contestant (independent implementation, 0221pdt)
also recovers 3/3. Two independent readers agree; coupling risk
is low.

Knowledge-vs-architecture: the generator draws the chain (it
must, to make a world); the contestant-facing artifacts contain
no leak (answer key never opened by any contestant; K5
order-swap invariance holds). The D5 correction itself is the
strongest evidence of honest instrumentation: the prior wave's
"seed luck" diagnosis was falsified by artifact evidence
(battery.json draws 1,1,0) and replaced with the real defect.

Residual: one seed, three items. The fix is structural, so it
generalizes to all seeds by construction; a multi-seed battery
would strengthen G5's statistical claim (per-item error < 2e-3
makes 3/3 weak as a reliability claim, strong as a mechanism
check).

## R2. C9 causal CAUSAL-PASS (K1-K7)

Gaming: the protocol cannot exploit candidate position (K5:
swapped order, replies unchanged, still the true chain). It
cannot exploit the old format (0/3). Its reply is built from
variable indices and matched against the listed candidates; with
no match it replies UNKNOWN. There is no path from question
format to a correct answer except through the statistics.

Harness coupling: the HI=0.75 threshold matches the generator's
noise model (p=0.05), which invites a tuning objection. Counter:
the threshold was frozen in PREREG_CAUSAL before fixrun2
existed, it comes from C9BAT's pre-registered statistical basis,
and the margins are enormous (tracking fractions 36/40, 40/40,
37/40 vs the 30/40 threshold; the decisive cross-comparison
37/40 vs 23/40). The threshold would survive any noise rate in a
wide band. Not overfit.

Knowledge-vs-architecture: the two-stage protocol is
researcher-specified (disclosed L1/L2, K7; no L3 claimed). The
contestant knows nothing about the chain; K4 proves the data
path drives the result (ablation: per-capability IDENTICAL to
the v6 baseline, C9 0/3 with UNKNOWN x3, no collateral damage
from the ablation edit). What the contestant "learns" is six
counters and a comparison; the intelligence credited is exactly
what the evidence supports.

Protocol deviation risk: the frozen substrate (fixrun1) was
unscorable and the frozen scorer panics on 291-turn worlds, so
the eval ran on fixrun2 with arena_512. This is disclosed in
SEALED_EVAL_C9.md with causes and cross-validation
(byte-identical results.json on the 131-turn world). The kill
bars did not move. The deviation was forced by post-freeze
discoveries, not by results. A hostile reader should still treat
the fixrun1-named K1 as not-executed-as-written; the fixrun2
execution is the valid substitute, and fixrun1 is now known to
be a defective artifact (D5), which is itself a finding.

## R3. Abstention ABSTAIN-FAIL (A1/A2 fail, A3 pass)

Gaming: none available; the result went against the mechanism.
The positive control (A3) passed, so the harness works; the
FAIL is a measurement, not an artifact. Turn indexing was
verified against the battery (turn 13 = whattime, turn 14 =
invent), and the ARENA-GEN EVAL_REPORT independently found the
same behavior. Convergent.

Harness coupling: none. Battery hash-verified; binary
byte-identical to the sealed DEFRECALL.

Knowledge-vs-architecture: this IS the architecture finding.
DEFRECALL's default action has no prompt-intent discrimination;
its abstention boundary is structural (bare vs parameterized),
not semantic. The C15 QUALIFY (0.947) was measured on a battery
whose bare prompt was `listnames`, the one bare prompt for which
roster enumeration is correct. The claim "DEFRECALL handles bare
prompts" does not survive contact with bare prompts that are not
roster requests. The honest scope is now written down
(ABSTENTION_TEST.md): roster-request bare prompts only. Any
attempt to widen it by patching the default action would be a
benchmark-specific handler and is rejected in advance; a real
fix is a new 11-step frontier proposal.

## R4. C8/C12 transfer TRANSFER-PASS (T1-T5)

Gaming: the transfer substrate (fixrun2) shares the generator
family with the frozen world. A critic could argue the
mechanisms are coupled to the generator family's item designs
rather than to surface forms. Conceded in scope (TRANSFER_EVAL.md
states this plainly): the test measures surface transfer, not
broad generality. Within that scope, the evidence is clean:
byte-identical binaries, zero code changes, per-capability
profiles identical to the frozen world, 3/3 determinism.

Harness coupling: low. Contestants are sealed-binary-identical
rebuilds; the world is new to them (they never saw fixrun2's
names); the scorer is cross-validated.

Knowledge-vs-architecture: neither mechanism carries fixrun2
knowledge. INQ induces entities from the expo stream; REMAP
reads the remap table from each question. Both are data-driven
at eval time. The transfer result is evidence of mechanism
generality within the world family, which is the right
ONE-SYSTEM-shaped evidence at this stage.

## R5. Cross-cutting

Toolchain: a second znc miscompile was reported today
(name/layout-dependent _zag_print behavior). Mitigation: all
lane binaries emit through a single prebuilt output buffer, and
every binary's stdout bytes were verified (3/3 byte-identical
stripped streams for all contestants; byte-identical world files
across 3 generation runs; byte-identical results.json in the
scorer cross-validation). Residual risk is accepted and noted;
new Zag code should use the raw-syscall emit workaround going
forward.

Process: no Python or non-safebin executable was invoked (Step
0 guard held all wave). No frozen kill bar was weakened. The one
protocol deviation is disclosed with evidence. A sibling
worker's commit (d22862d07) swept this lane's C9 eval files into
an unrelated E10 commit; content is intact, commit hygiene is
noted. A second sibling is doing trial-wall engineering in this
lane (NAMECHECK_ENG.md, trialwall.zag); untouched by this
worker.

What is NOT claimed: no L3 anywhere this wave; no TNN-beats-LLM
claim (no serious baseline has run); FW1-FW9 not run and not
claimed; the frozen arena C9 battery remains a sealed zero; the
integrated continuing learner (INQ + REMAP + CAUSAL + DEFRECALL
in one binary, zero regressions) is still unbuilt and is the
next one-system milestone.

Strongest remaining reason TNN is not yet a system to choose
over an LLM (arena slice): the four capability mechanisms exist
only as separate per-capability candidates on the v6 base, the
C15 mechanism's scope just shrank to roster-request prompts, and
no single continuing learner integrates any of them. The
transfer results say the mechanisms are not surface-coupled,
which is necessary but not sufficient for integration.
