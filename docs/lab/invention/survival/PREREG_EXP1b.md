# PREREG EXP1b: Invent-to-Survive Retune (FROZEN 2026-09-27)

**Question:** Same as EXP1: can TNN genuinely INVENT under survival pressure,
producing novel working solutions not recalled from taught knowledge. EXP1b is
a retuned re-test, not a new question.

**Background (EXP1, wave-20260926-2321pdt, DISCARDed):** H1 killed on K1
(I-survive median 574 vs R median 600). Recorded defects that EXP1b repairs:
(1) Ceiling effect: one stationary mote sat at P's home in every variant, so
R camped it to 600 and no invention headroom existed. (2) The I arm used
schema-level plans (seek-crystal, seek-mote, COMBINE, DROP, ...), likely
violating the literal "six primitive actions" requirement. (3) Python was
used twice, breaking pure-Zag compliance. (4) K4 killed the invention claim
independently: the candidate scoring carried authored bonuses that encoded
productive compositions. (5) K5 incomplete: no independent blind auditor.

## The EXP1b mechanism (what changes; everything else inherits EXP1)

**M1. Ceiling removal (world retune).** Every mote has |velocity| >= 1: no
stationary motes anywhere. No mote's respawn cell is P's home cell or the
agent start cell. No mote's drift range [lo,hi] contains the home cell. R
cannot camp a fixed cell to 600. Strategic richness is retained: the retune
must still pass C3 (>= 3 distinct scripted strategies reaching >= 360 ticks).

**M2. Literal primitive-action I arm (no schemas anywhere).** A plan is a
sequence of at most 4 PRIMITIVE actions from {LEFT, RIGHT, EAT, TAKE, DROP,
COMBINE, WAIT} (4 satisfies the frozen "at most 6" bound; longer behavior
arises from chaining re-planned sequences). The candidate set is the full
enumeration of all 7^1 + 7^2 + 7^3 + 7^4 = 2800 sequences in length-ascending
lex order: pure combinatorics, zero authored productivity bias. The EXP1
i_prod_bonus is deleted and no replacement is allowed. COMBINE inside a plan
uses a fixed deterministic arg rule: the two most recently taken inventory
items (slots inv_n-2, inv_n-1); it is a safe no-op when fewer than 2 items
are held. Scoring: deterministic argmax over candidates of (mean experienced
delta-energy per plan-sketch + B0 novelty bonus for untried compositions);
ties go to the lowest candidate index; zero RNG. Execution is open-loop with
two preempting single-step taught reflexes that never advance the plan:
storm-active/in-zone/unsheltered flees (taught H3), energy below 25 runs the
survival reflex (taught H4). After a plan's actions are spent, its observed
delta-energy updates that sketch's mean credit and the arm replans.
I-survive uses B0 = 40; I-invent uses B0 = 80; the machinery is otherwise
identical (H2 test: explicit invention instruction vs implicit pressure, with
the novelty drive as the only parameter difference).

**M3. Pure Zag.** All implementation, runs, and analysis are in Zag. The
shell is used only to invoke the compiler, redirect stdout, and hash outputs
(hashing is not analysis). Pinned toolchain:
src/tools/toolchain/znc_linux_x86_64_abed8aa1, SHA-256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef, verified
before use. Any Python or shell text-processing of evidence voids
certification.

## World (frozen rules; parameters retunable within these rules until C1-C3 pass)

Same physics as src/world.zag (imported unchanged, recipe table still
hidden): 24 cells, 600 ticks, basal 1, E0 = 100, Emax = 200, 6 motes, 4
crystals, inventory cap 4, storm zone cells 6..17 with 3 windows at 4 damage
per tick unsheltered, 2 adjacent void cells, WARD/LAMP/BEACON/PLANK/SURGE
recipes, deep-region motes worth +40. 12 fixed variants, disjoint parameters
from EXP1, satisfying: every mote |v| in {1,2}; mote respawn cell is neither
the home cell nor the start cell; the home cell lies in no mote's [lo,hi]
range; exactly 2 motes flagged deep (+40) confined past the void; the home
cell is outside the storm zone on the starting side; void pairs, crystal
cells, storm windows, and mote geometry vary across variants.

## Arms

P: taught WARD strategy from kb/kb_p.txt (unchanged). Z: fixed-seed LCG
(documented control, unchanged). R: taught single-step heuristics from
kb/kb.txt (unchanged). I-survive / I-invent: M2 machinery. The only
architectural difference between R and I is the compositional planning
machinery plus novelty drive; KB, perception, and reflexes are identical.

## Training mass

kb/kb.txt and kb/kb_p.txt, committed verbatim (recipe table excluded as in
EXP1). No multi-step plans are taught to R, I-survive, or I-invent.

## Runs and metrics

12 variants x 5 arms = 60 runs. Primary metric: median survival ticks per arm
over the 12 variants. Secondary: plan logs of both I arms, mean energy at
death, cause-of-death distribution. Determinism: all 60 runs executed twice;
SHA-256 of the full stdout must be byte-identical across reruns.

## Calibration gates (validity; retune parameters within the frozen rules until met)

C1: median P >= 480/600, else the run is VOID (sim broken), not a kill.
C2: median Z < 150/600.
C3: >= 3 qualitatively distinct scripted strategies each reaching median
>= 360 ticks (candidates: forage, ward-turtle, lamp-farm, void-cross).

## Kill bars (frozen; weaken only with Micah's explicit approval)

K1: median(I-survive) <= median(R) kills H1.
K2: median(I-survive) <= median(Z) kills H1 and triggers a sim investigation.
K3: median(P) < 480 voids the run (sim broken), not a kill.
K4: novelty audit finds key strategy steps in the committed training mass, or
the winning strategy is a trivial recombination (per EXP1 PREREG section 2):
kills the invention claim.
K5: blind cuing audit derives I's key strategy from the training mass, world
rules, and goal statement alone: kills (cuing cannot be ruled out). The
auditor must not have authored the machinery; if no independent auditor is
available the implementer states the limitation honestly and K5 stays
incomplete (no self-certification).
K6: ablation (A2) shows removing novel-composition steps does not reduce
survival: kills the invention claim.

H2 has no kill bar; the I-survive vs I-invent comparison is reported either way.

## Required analyses

A1: for each variant where an I arm beats R by >= 60 ticks, extract the
winning trace and abstract it to a strategy sketch over primitive actions.
A2: deterministic replay with each novel-composition step replaced by the best
taught single-step alternative; measure the survival drop (feeds K6).
A3: qualitative comparison of compositional novelty rate vs Task 1's 8/58
(different metric; exploratory only).

## Audits

Novelty audit: text search of the committed training mass for each A1
sketch's composed steps (the composition, not just the words). Any key step
found fires K4. Cuing audit: a blind auditor (not the machinery's author)
receives only the training mass, world rules, and goal statement and derives
the best strategy it can; deriving I's compositional core fires K5.

## Standing laws

Pure Zag. Zero RNG in agent decision paths (Z's LCG is a documented control).
Byte-identical reruns (SHA-256 verified). Preregistered frozen kill bars: an
honest VOID or KILL is a successful experiment. Tests decide; nothing goes to
Micah except frozen-prereg amendments, governance, or irreversible/external
actions. No binaries, .zagd, caches, or derived files in the repo: code,
docs, committed training mass, world variants, results TSVs, and audit
reports only.

## Deliverables (new names; wave-2321 files stay intact)

PREREG_EXP1b.md (this file, frozen); src/exp1b_variants.zag,
src/exp1b_agent_i.zag, src/exp1b_runner.zag (world.zag, agent_p.zag,
agent_r.zag, agent_z.zag, lcg.zag reused unchanged); worlds_exp1b/v00.txt
through v11.txt; runs_exp1b/ (results TSVs for both reruns, SHA-256
manifest); evidence_exp1b/ (EVIDENCE_EXP1B.md, BAR_RESULTS_EXP1B.md, audit
reports, REDTEAM_EXP1B.md, WAVE_NOTES_EXP1B.md).

---

**FROZEN 2026-09-27.** Amendments require the coordinator's parent (main
agent) approval; weakening a kill bar requires Micah's explicit word.
