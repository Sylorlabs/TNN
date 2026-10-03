# X-FU7 adversary result: H-FDCR-UNIFIED7

Date: 2026-09-29 (executed 2026-09-30 UTC).
Red team: H-FDCR-UNIFIED7 independent red team (H-FDCR-UNIFIED7-RED).
Target: H-FDCR-UNIFIED7 builder result `18dd712a3` (prereg
`855322a77`, transparent Amendment 1 `42cbe6396`).

## Verdict

**H-FDCR-UNIFIED7 is DOWNGRADED, not killed.**

Two independent DOWNGRADE findings fired (X-FU7-2/B2b and
X-FU7-3/C3b). No KILL criterion fired (X-FU7-3/C4 held: the
uncertainty NOTE fired honestly and the definite lost-vote NOTE
did not fire for the sole-overflow2 subject h1; X-FU7-4
reproduced the original 47/47 battery byte-identically).

The downgraded claim is the exact frozen R1 sentence from the
builder's prereg Amendment 1:

> "NOADD_DROP_OVERFLOW now genuinely counts distinct subjects
> dropped beyond the 64-name capacity"

That sentence is overstated. `NOADD_DROP_OVERFLOW` is an
overflow-name admission-event counter, not a lifetime
per-distinct-subject counter: a subject cleared from the
overflow-name list by R3 membership can be re-admitted and
re-counted, and a subject dropped once past all naming capacity
can be counted in both tiers at once.

## What survives the attack

- Plain re-drop deduplication (X-FU7-1): re-dropping a
  main-named or overflow-named subject does not re-increment any
  tier. The dedup functions work while names remain present.
- The 128 vs 129 boundary (X-FU7-3/C1, C2): 128 distinct drops
  name all 64 overflow subjects (ov=64, ov2=0); the 129th
  distinct drop increments only the event tier (ov2=1).
- NOTE honesty for the sole-overflow2 subject (X-FU7-3/C4): h1
  was `vote_lost=0` (unknown), g128 stayed `vote_lost=1`
  (definitely-known), and the emitted NOTE was the uncertainty
  NOTE, not the definite lost-vote NOTE.
- The full original battery (X-FU7-4): 47/47 reproduces.

## Lineage

- Builder prereg: `855322a77`
- Builder Amendment 1 (transparent, post-first-run): `42cbe6396`
- Builder result: `18dd712a3`
- Adversary prereg (frozen before attack code): `e4c6f5103`
- Adversary Amendment 1 (fixtures only): `fe0b21052`
- Adversary Amendment 2 (fixtures only): `68d41853a`
- This evidence commit: (recorded at commit time)

## Frozen bars (from PREREG_FU7_ADV.md)

X-FU7-1 (overflow-list dedup under re-record):
- A1: re-drop main-named f1 -> no tier may increment.
- A2: re-drop overflow-named g1 -> no tier may increment.
- KILL: none. DOWNGRADE: any re-drop of an already-named
  subject re-increments any tier.

X-FU7-2 (drop -> member -> merge-overflow re-record):
- Setup: 128 distinct drops (64 main-named, 64 overflow-named);
  require total=128, overflow=64, overflow2=0.
- B1: `T e1 | is_a | animal` members e1 and R3-clears it;
  require vote_lost(e1)=0, total=128, overflow=64.
- B2a (Amendment 2): `T e1 | is_a | pet` extends animal to
  {"is_a=animal","is_a=pet"}; require animal nfeat=2, no drop.
- B2b (Amendment 2): `T s1 | is_a | animal` extends pet to
  {"is_a=pet","is_a=animal"}; set-identity fires
  `con_merge_into(pet, animal)` ("CONCEPT-MERGE 1 into 0"); pet
  is full so e1 is merge-overflow re-recorded into its freed
  overflow slot. Require total=129, vote_lost(e1)=1,
  vote_lost(s8)=0, and the raw to contain "CONCEPT-MERGE 1 into
  0" (direction confirmation).
- DOWNGRADE: overflow==65 after B2b (only 64 distinct subjects
  were ever overflow-named; e1 counted twice). VOID if the
  merge does not fire in the required direction.

X-FU7-3 (128 vs 129 boundary, cross-tier, NOTE honesty):
- C1: 128 distinct drops -> total=128, ov=64, ov2=0, all named.
- C2: 129th distinct drop (h1) -> total=129, ov=64, ov2=1;
  h1 honestly unknown (vote_lost=0); g128 still
  definitely-known (vote_lost=1).
- C3: member+clear g65, then re-drop h1 -> DOWNGRADE if h1 is
  counted in BOTH tiers (ov=65 AND ov2=1).
- C4: direct-discovery probe -> KILL if the definite lost-vote
  NOTE fires for the sole-overflow2 subject (it must be the
  uncertainty NOTE).
- DOWNGRADE: C3 cross-tier double count.

X-FU7-4 (regression):
- Rebuild committed `unified_fdcr7.zag` from
  `git show 18dd712a3:...`, run 3x. KILL: any FAIL line, any
  nonzero exit, or any byte difference between runs.

Verdict rule: any KILL -> KILLED; else any DOWNGRADE ->
DOWNGRADED; else SURVIVES.

## Raw results (final run)

Harness: `fu7adv.zag` = committed `unified_fdcr7.zag` lines
1..2135 (byte-verified against commit `18dd712a3`) + attack-only
`main()`. Pure Zag. Toolchain
`/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`
(`znc 2026.07.0-dev (edition 2026)`). Final build: 23 analyzer
warnings (non-fatal), native binary written.

Raw: `FU7_ADV_RAW_R1.txt`, md5
`d760300faf81c9a1b5fc6ce882a6e018`, 3/3 byte-identical, exit 0
x3.

```
X-FU7-1 setup: total=74 ov=10 ov2=0 PASS
X-FU7-1/A1 re-drop main-named f1: no tier increment PASS
X-FU7-1/A2 re-drop overflow-named g1: no tier increment PASS
X-FU7-2 setup: total=128 ov=64 ov2=0 PASS
X-FU7-2/B1 e1 membered+cleared: lost=0 vote>=0 total=128 ov=64 PASS
X-FU7-2/B2a animal extended to 2 features, no drop PASS
X-FU7-2/B2b MERGE-PATH-ARMED
X-FU7-2/B2b CONFIRMED: merge-overflow re-record re-named e1 (lost=1) and re-incremented overflow to 65; same distinct subject counted twice. R1 per-distinct-subject claim FALSIFIED. DOWNGRADE-FINDING
X-FU7-3/C1 128 distinct: total=128 ov=64 ov2=0, all named PASS
X-FU7-3/C2(a) 129th distinct: total=129 ov=64 ov2=1 PASS
X-FU7-3/C2(b) h1 honestly unknown (lost=0) PASS
X-FU7-3/C2(c) g128 still definitely-known PASS
X-FU7-3/C3a g65 membered+cleared PASS
X-FU7-3/C3b CONFIRMED: h1 counted in BOTH tiers (ov=65 names 2nd drop as distinct; ov2=1 keeps 1st drop as event). DOWNGRADE-FINDING
X-FU7-3/C4 BEGIN
X-FU7-3/C4 END rc=0
X-FU7-ADV VERDICT: DOWNGRADED
```

Merge direction confirmation (raw):
`ULEARN concept: CONCEPT-MERGE 1 into 0`

X-FU7-3/C4 block (between BEGIN and END):
```
ULEARN: NOTE vote status uncertain for some train input(s) (NOADD drop name capacity exceeded; 129 total drops, 64 distinct subject(s) beyond name capacity; 1 further drop events beyond overflow naming capacity); train_con may exclude lost votes
ULEARN: direct discovery -> proc slot 0 (intent seq recorded, train_len=2, concept=-1)
```
The uncertainty NOTE fired; the definite NOTE
("train input(s) lost concept votes") did not. No KILL.

## Causal interpretation

DOWNGRADE finding 1 (X-FU7-2/B2b, same-tier double count).
`noadd_drop_clear` (R3) removes a subject's name from both
name lists when it becomes a concept member, but lifetime
counters are deliberately kept. The merge path
(`con_merge_into` -> `noadd_record` -> NOADD table full ->
`noadd_drop_record`) then re-admits the same subject string
into the freed overflow-name slot and increments
`NOADD_DROP_OVERFLOW` again. Sequence for e1: overflow-named
(drop 63 of 64, ov=64) -> membered into animal (cleared, ov
stays 64) -> animal merged into pet ("CONCEPT-MERGE 1 into
0"), pet full -> e1 re-recorded (total 129, ov=65,
vote_lost(e1)=1, vote_lost(s8)=0 so no bystander victim). 65
overflow increments for 64 distinct subjects. The R1 sentence
"genuinely counts distinct subjects" is false under this
lifecycle; the counter counts overflow-name admissions.

DOWNGRADE finding 2 (X-FU7-3/C3b, cross-tier double count).
h1's first drop (129th distinct) found both name lists full and
incremented only the event tier (ov2=1). After g65 was
membered+cleared, h1's second drop found a free overflow slot
and was named (ov=65). h1 is now counted in both tiers: once
as an event and once as a named distinct subject. The two
tiers are not mutually exclusive across clear+re-drop cycles.

What did NOT break. The dedup itself is sound while names
persist (X-FU7-1). The boundary is exact (C1/C2). The NOTE
wording for the sole-overflow2 subject is honest (C4): the
system says "uncertain", never "definitely lost", and keeps
g128's definite status intact. The original 47/47 battery is
unaffected (X-FU7-4).

## Mechanism properties disclosed (not findings)

- Membership is sticky under the teach API. Re-teaching an
  existing member takes the cross-batch extension path in
  `handle_concept_learn` (extends the concept's feature set),
  never `con_form`. The drop -> member -> drop cycle therefore
  cannot re-drop through `con_form`; the merge path is the only
  member re-record route. (Found via the pilot VOID, Amendment
  1.)
- Merge survivor = last-extended concept
  (`con_merge_check(W,ci)` -> `con_merge_into(W, ci, c2)`).
  Fixture order determines which concept absorbs which; the
  Amendment 1 run merged pet into animal ("CONCEPT-MERGE 0
  into 1") and its overflow victim was s8, a legitimate new
  distinct subject, so that run is VOID for the DOWNGRADE
  criterion. (Amendment 2.)
- Stored concept strings are append-only; no stale
  string-pointer issue was found in the clear path.

## Iteration history (all preserved)

- Pilot (prereg as frozen): B2 drove the extension path, not
  the re-drop path (total stayed 128). VOID per the prereg's
  VOID rule. Raw: `FU7_ADV_RAW_PILOT.txt`, md5
  `eb2da0bb722cd157030f2a3f4fe57f58` (3/3 byte-identical).
- Amendment 1 run: merge fired in the wrong direction
  ("CONCEPT-MERGE 0 into 1"); overflow victim was s8
  (legitimate). The in-Zag "CONFIRMED" line in that run was a
  misinterpretation (counter checked, subject identity not).
  VOID for the DOWNGRADE criterion. Raw:
  `FU7_ADV_RAW_AMEND1.txt`, md5
  `a38a8b087febfd2cecd722e0a2cf3c1e` (3/3 byte-identical).
- Final run (Amendment 2 fixtures): md5
  `d760300faf81c9a1b5fc6ce882a6e018` (3/3 byte-identical).

## X-FU7-4 regression detail

Rebuilt `unified_fdcr7.zag` from
`git show 18dd712a3:docs/lab/research-lead/overnight-20260928/unified_fdcr7.zag`
(3232 lines), compiled and ran 3x. Exit 0 x3, 3/3
byte-identical, md5 `a28b0dca016472b1daad625e0b3d56b4`
(matches the builder's reported MD5 exactly), zero FAIL
lines. Raw: `FU7_REG_RAW_R1.txt`. The original 47/47 result
reproduces exactly; the DOWNGRADE concerns the R1 claim
wording, not the battery outcome.

## Build and governance disclosures

- Pure Zag throughout: harness built by extracting committed
  source lines and appending an attack-only `main()`; no
  Python used for editing, building, running, or analysis.
  One accidental `python3` heredoc invocation occurred during
  scratch reconstruction; it printed a literal string and was
  aborted before doing anything. It touched no evidence.
- First compiler invocation was piped through `head`; the
  closed pipe prevented binary production. A clean rerun
  completed (22 analyzer warnings). Final build: 23 analyzer
  warnings, all non-fatal.
- Binaries and `.zag-cache` exist only under `/tmp/fu7adv`
  and `/tmp/fu7reg`; none are committed.
- Em-dash byte scan: `PREREG_FU7_ADV.md` and `FU7_ADV_RESULT.md`
  are clean. `fu7adv.zag` contains exactly one U+2014 byte, on
  line 1, inside the inherited builder source header comment
  (`// unified_learn.zag — End-to-end ...`); it is pre-existing
  in the builder's committed source (commit `18dd712a3`) and
  was preserved to keep the harness top byte-identical to the
  committed source (cmp-verified). The attack-only `main()`
  appended after line 2135 contains no em dashes.
- Suggested R1 claim repair (for the builder, not adopted
  here): "NOADD_DROP_OVERFLOW counts overflow-name admissions
  (distinct while names persist; a cleared subject may be
  re-admitted and re-counted)". Adoption is the builder's
  decision under a new prereg.
