# WAVE_RECORD.md

Wave: wave-20260930-0221pdt (scheduled 2026-09-30 02:21:54 PDT;
executed 2026-09-30 ~09:20-10:00 UTC).
Mode: INLINE, no subagents. Deliberate per the documented
runtime-failure precedent: three recent waves (20260928-1121pdt,
20260928-1421pdt, 20260929-1121pdt) died with "failed while waiting
for descendant subagents before resolution: follow-up has no durable
chat owner"; the 20260929-2321pdt inline wave completed cleanly. A
dead wave yields zero information; the owner's standing rule ranks
information gain above experiment count.

Run-start pin: 1f681e87b6a64fc65e4c01ead66b6db919c365b8 (recorded in
RUN_START_PIN.txt). Wave lock: absent at run start (no wave running);
timestamp written at start, removed at end. Origin: fetched at run
start; origin/tnn-native-lab (bedf8b4a) is an ancestor of local HEAD;
no merge needed, no reset (standing rule).

## 1. H-PI-REV2-F3 independent-adversary family [NEW]

Authority: debate wave-20260929-2321pdt, judge M5 (independent
adversary before reproduction). Prereg PREREG_PI_REV2_F3.md committed
alone at d80106155 (this wave's first act; no amendments). The
frozen implementation (847a8f10f) was NOT modified: working tree
verified byte-identical to the committed blob before building; binary
rebuilt with pinned znc 498abcb5 (one benign pre-existing analyzer
lint A0102; binary valid).

F3a (adversary byte 'w', last of sorted frozen allowed set, via the
frozen P8 argv interface): 3 executions, 3/3 byte-identical
(97dd4276), exit 0, fails=0.

Scorecard: K-F3-1 PASS (detection, DIAGNOSIS pos=0 byte=119
conflicts=0, PRIMITIVE-CONSTRUCTED (0,119), alt=C0 index 2, v3
ACTIVE parent v2, wab->www, priors unchanged, wqw->www reuse with no
new revision, R 8/8); K-F3-2 PASS (3/3 byte-identical); K-F3-3 PASS
(zero 'w'/'wab'/'www'/'wqw'/119 in committed machinery); K-F3-4 FAIL
('w' occurs in the frozen F1-reuse fixture "xqw").

Verdict: BUILD-FAIL per the frozen verdict rule, killing line
K-F3-4 cited. The kill is bar-design, not mechanism: the white-box
trace is clean and no mechanism failure is evidenced.

New audit finding: the parent prereg's allowed-set disjointness
rationale is inaccurate; only {i,k,m,r,v} are genuinely absent from
all frozen fixture inputs ('i' spent on F2; j,l,n,o,t,u in R inputs;
w in the F1-reuse fixture). Future adversary bytes must come from
{k,m,r,v}.

F3b (non-first-letter world ("abz"->"zzz"), S4 stress): design frozen
in the prereg; execution deferred (the frozen binary's committed P8
interface cannot express it; extending the interface needs its own
prereg plus implementation wave). Recorded FROZEN-DESIGNED, not a
verdict.

Evidence: f3a_evidence/EVIDENCE_F3A_run{1,2,3}.txt, RESULT_F3A.md.

## 2. Fork battery [NEW]: CONFIRM as a process confirmation

Fresh 77-entry run at run-start pin 1f681e87b, driver exit complete:
75 PASS, 0 FAIL, 2 UNTESTABLE (rh-pull-1-head, rh-pull-2-head; the
known non-TNN research-doc trees). LIVE entries (2):
arch-wave-20260929-2321pdt at a4314633 (newly enumerated archive),
local-tnn-native-lab at 1f681e87b (run-start tip). Uniform on all 75
tested: znc pin 498abcb5 (0 pin divergence); probe sha 3b29aa06 (0
divergence); b1/b2/b3 PASS; NEG1 E0002 75/75; NEG2 char-1
discrimination 75/75; harness_verdict_pass_count 1 on 75/75.
Duplicate-SHA group carried: {arch-wave-20260929-1721pdt,
local-1721pdt-tip} at 7c11ac5af. Remote: zero new refs
(origin/tnn-native-lab bedf8b4a unchanged). Scope stamp: toolchain
and extraction stability only.

Driver: batch_0221.sh derived from batch_2321.sh by mechanical edit
(sed/awk; zero Python); run_one.sh byte-identical to frozen
(4c2fadfc); harness re-verified byte-identical to frozen pin
(a2e6284c). Scratch: ~/workspace/fb0930_0221pdt/E/.

## 3. Interactive survey [NEW]: NONE new

158 new or modified .zag files in fed72668..HEAD (all from the
parallel research-lead process); zero chat/stdin/readline/interactive
pattern hits. Frozen probe instruments remain the only chat-capable
instruments. tnn_chat FIT staleness 4 of 8 (due at 8 of 8).

## 4. Commit-order self-check [NEW]: VALID

Prereg commit d80106155 contains exactly PREREG_PI_REV2_F3.md and
strictly precedes all F3 evidence commits. No implementation file
created or modified this wave. The check certifies order, which is
what the standing rule requires.

## 5. Python red-line touch [NEW]: NONE

Zero Python in wave work. Driver derivation used sed/awk only. Byte
checks used grep/sha256sum/cmp (shell only) per the 2026-09-30
standing rule.

## 6. Debate [NEW]: held, all motions ruled

Transcript: debate/ADVOCATE_0221.md, SKEPTIC_0221.md, JUDGE_0221.md.
M1: F3a BUILD-FAIL on K-F3-4 (skeptic's textual case dispositive;
mechanism exonerated on K-F3-1/2/3; re-freeze remedy queued). M2:
fork battery CONFIRM. M3: interactive survey NONE new CONFIRM. M4:
commit-order VALID CONFIRM. M5: queue amended (re-freeze F3a next
with byte from {k,m,r,v}; then independent reproduction; F3b
execution queued behind its interface-extension prereg).

## Provenance (verbatim probe answered in every debate motion)

Prereg text new this wave; implementation, binary lineage, fixtures,
F2 evidence inherited; F3a evidence, audits, fork battery evidence,
interactive survey, debate records new this wave. No recycled render
or re-certification presented as new; nothing in this wave touches
the image judge queue. All HELD statuses, rulings, banked questions,
governance items, sealed pairs, DP-1, salt dispositions, and
frontier dirs remain inherited and untouched.

## Queued next

Re-freeze F3a (corrected K-F3-4, byte from {k,m,r,v} by declared
rule) and re-run; then step 4 independent reproduction of H-PI-REV2;
F3b interface-extension prereg then execution; NQ4/NQ5 banked to
Micah; tnn_chat FIT due at 8 of 8 (staleness 4 of 8); his six pending
governance rulings (untouched); his blind verdicts on the sealed
pairs (unchanged, nothing added this wave); DP-1 presentation is a
parent-agent queue decision; Q1/Q2 banked; DDES t*=0 repair;
H-EXP2; H-ROUTER2; DEVANG2 retry; conditional-first builder lane.
Zero origin commits this window.
