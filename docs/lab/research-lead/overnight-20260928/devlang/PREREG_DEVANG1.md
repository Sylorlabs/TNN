# PREREG_DEVANG1: Developmental Semantic Language from Raw Stream

**Status:** FROZEN. Committed before any implementation.
**Date:** 2026-09-30.
**Worker:** F3 (Developmental Semantic Language Builder).
**Owned path:** `docs/lab/research-lead/overnight-20260928/devlang/`

## 1. Mission

Build a world where language arrives as raw unsegmented character sequences.
The learner must acquire, strictly online, the pipeline:

raw stream -> learned segmentation -> recurring units -> grounded concepts
-> relations -> composition -> answers/actions.

Meaning is grounded in world consequences (object selection + reward),
not researcher dictionaries.

**Do NOT create SEG10.** SEG is mature infrastructure. This wave uses
segmentation as a component, not a research target.

## 2. Addressing DEVINT1 A1 (feed-schedule sensitivity)

DEVINT1 attack A1 found the reported numbers were feed-schedule sensitive
because the lexicon was built from all 12 observations before segmentation
(future-data leakage). This wave requires TRUE ONLINE processing:

- Episode t is processed using ONLY state derived from episodes 0..t-1.
- Bigram counts, lexicon, grounding, negator/comparative statistics
  are updated AFTER episode t is segmented and interpreted,
  using only episode t's data.
- The segmentation of episode t MUST NOT use bigram counts that
  include episode t or any later episode.
- Kill bar K10/K12 enforce this by code audit.

## 3. World design

### 3.1 Objects

Each episode shows 3 objects. Each object has:
- color: 0=red, 1=blu, 2=grn (grn appears only in phase 2 and test)
- shape: 0=ball, 1=cube, 2=tri (tri appears only in phase 2 and test)
- size: 0=smal, 1=big

### 3.2 Vocabulary (surface forms, no spaces in utterances)

- tak (take, 3 chars)
- not (negation, 3)
- red (3), blu (3), grn (3, phase 2+)
- bal (3), sph (3, synonym for ball), cub (3), tri (3, phase 2+)
- big (3), biger (5), smal (4)

Variable word lengths: 3, 4, 5. Morphology: big/biger share the
form "big". Synonyms: bal/sph both denote ball.

### 3.3 Episode templates

- DIRECT: "tak"+COLOR+SHAPE. Target = unique object with that color
  and shape. Scene ensures exactly one match.
- NEG: "tak"+"not"+COLOR. Target = unique object whose color != COLOR.
  Scene has two objects of COLOR, one of a different color.
- REL: "tak"+"biger"+SHAPE. Target = bigger of two SHAPE objects.
  Scene has two SHAPE objects of different sizes, one distractor.
- SIZE: "tak"+"big"+SHAPE or "tak"+"smal"+SHAPE. Target = unique
  object with that size and shape.

### 3.4 Phases

**Phase 1 (60 episodes):** colors {red,blu}, shapes {ball,cube}.
- DIRECT (24): tak+red+bal (4), tak+red+sph (4), tak+red+cub (4),
  tak+blu+bal (4), tak+blu+sph (4), tak+blu+cub (4)
- NEG (12): tak+not+red (6), tak+not+blu (6)
- REL (12): tak+biger+bal (6), tak+biger+cub (6)
- SIZE (12): tak+big+bal (3), tak+big+cub (3),
  tak+smal+bal (3), tak+smal+cub (3)

**Phase 2 (40 episodes):** add grn, tri.
- DIRECT new (20): tak+grn+bal (7), tak+grn+tri (7), tak+red+tri (6)
- DIRECT old (8): tak+red+bal (2), tak+blu+cub (2),
  tak+red+cub (2), tak+blu+bal (2)
- NEG old (4): tak+not+red (2), tak+not+blu (2)
- REL old (4): tak+biger+bal (2), tak+biger+cub (2)
- SIZE new (4): tak+big+tri (4)

**Test (20 episodes):** novel compositions, NEVER observed verbatim
in training. Learner state frozen after phase 2; no updates on test.
- DIRECT novel (6): tak+grn+cub (3 scenes), tak+blu+tri (3 scenes)
- SYN novel (3): tak+grn+sph (3 scenes)
- NEG novel (3): tak+not+grn (3 scenes)
- REL novel (3): tak+biger+tri (3 scenes)
- SIZE novel (3): tak+smal+tri (3 scenes)
- 3-WAY novel (2): tak+big+grn+bal (2 scenes)

**Explicit hold-outs (must NOT appear in training):**
grn+cub, blu+tri, grn+sph, not+grn, biger+tri, smal+tri, big+grn+bal.

### 3.5 Scene generation

Deterministic seeded LCG. For each episode, generate 3 objects via
rejection sampling to satisfy the template's uniqueness constraint.
Seed fixed in implementation. Same scenes for learner and controls.

## 4. Learner (all online, t-only)

### 4.1 State
- bigram[26][26]: character bigram counts (a-z).
- lexicon: up to 64 entries (bytes, len, count).
- ground[64][8]: co-occurrence of lexicon entry with target's
  8 feature-values (colorRx3, shapex3, sizex2).
- neg_viol[64], neg_tot[64]: negator statistics.
- cmp_ok[64], cmp_tot[64]: comparative statistics.

### 4.2 Online protocol (episode t)
1. Observe objects and utterance bytes.
2. Segment utterance using bigram counts from episodes 0..t-1 ONLY.
   (At t=0, counts are zero; DP falls back to minimal segments.)
3. Look up/add segments in lexicon.
4. If training (t<100): observe target.
   a. Predict via interpret (for accuracy tracking).
   b. Update bigram counts with utterance t.
   c. Update lexicon counts.
   d. Update grounding from target's features.
   e. Update negator/comparative stats from adjacent pairs.
5. If test: predict only. No state updates.

### 4.3 Segmentation
Bigram DP. dp[i] = max score for prefix of length i.
seg_score(j,i) = sum_{k=j}^{i-2} log2(bigram[b[k]][b[k+1]]+1)
                 - BOUNDARY_COST, with BOUNDARY_COST = 4 (frozen).
Backtrack for segments. Log via integer ilog.

### 4.4 Grounding
primary(s) = argmax over 8 feature-values of ground[s][fv],
valid only if lexicon count[s] >= 2.

### 4.5 Negator detection (generic, not hardcoded to "not")
For adjacent pair (m, x) in a training segmentation:
if primary(x) is valid, neg_tot[m]++.
If target violates primary(x), neg_viol[m]++.
is_negator(m): neg_tot[m] >= 3 AND neg_viol[m]*10 >= neg_tot[m]*7.

### 4.6 Comparative detection (generic, not hardcoded to "biger")
For segment s followed by x with valid shape primary:
cmp_tot[s]++.
If target == argmax(size) among objects with that shape, cmp_ok[s]++.
is_comparative(s): cmp_tot[s] >= 3 AND cmp_ok[s]*10 >= cmp_tot[s]*8.

### 4.7 Interpretation
Pass 1: build tokens. Skip "tak" (action marker, identified as the
lexicon entry that appears utterance-initially in >90% of episodes;
fallback: first segment).
- If is_negator(s) and next exists: token(next, polarity=-1), skip 2.
- Elif is_comparative(s) and next has shape: token(COMPARATIVE, shape),
  skip 2.
- Else: token(s, polarity=+1), skip 1.
Pass 2: score objects 0..2.
- token(s,+1): (f,v)=primary(s); +1 if object has it else -1.
- token(s,-1): (f,v)=primary(s); +2 if object lacks it else -2.
- token(COMPARATIVE, sh): +3 if object is max-size among shape sh.
Select max score; tie -> lowest index.

### 4.8 Controls (same scenes, same online protocol where applicable)
- C1 (no segmentation): whole utterance = one lexicon entry.
  Memorize utterance->target. On novel utterance, predict most
  frequent training target (tie -> smallest index).
- C2 (fixed-width-3): segment into 3-char chunks (last may be short).
  Then identical grounding/interpretation as learner.
- C3 (literal substring memory): memorize training pairs. On test,
  predict target of training utterance with longest common substring
  (tie -> earliest). No grounding.

## 5. Kill bars (numbered, frozen)

- K1 (lexicon discovery): >= 8 of the 10 phase-1 true words
  (tak, not, red, blu, bal, sph, cub, big, biger, smal) present as
  exact lexicon entries by end of phase 1.
- K2 (DIRECT novel): >= 5/6 correct on tak+grn+cub and tak+blu+tri.
- K3 (NEG novel): >= 2/3 correct on tak+not+grn.
- K4 (REL novel): >= 2/3 correct on tak+biger+tri.
- K5 (SYN novel): >= 2/3 correct on tak+grn+sph.
- K6 (SIZE novel): >= 2/3 correct on tak+smal+tri.
- K7 (3-WAY novel): >= 1/2 correct on tak+big+grn+bal.
- K8 (beats controls): learner test accuracy (20 items) exceeds the
  best control by >= 15 percentage points.
- K9 (new vocab acquisition): >= 7/10 correct on last 10 phase-2
  training episodes.
- K10 (true online, governance): code audit confirms strictly
  sequential processing; no structure is built from future data.
  Bigram/lexicon/grounding updates for episode t occur after
  episode t is segmented/interpreted.
- K11 (no future leakage in segmentation, governance): the bigram
  counts used to segment episode t exclude episode t (verified
  by update ordering in code).
- K12 (determinism): 3/3 byte-identical outputs.

**Verdict rule:** BUILD-PASS requires K1, K8, K10, K11, K12 plus
at least 4 of {K2..K7, K9}. Otherwise BUILD-FAIL.

## 6. Expected classification

This wave tests developmental integration (the pipeline), not
representational invention. The composition skeleton (interpret)
is researcher-designed; the segment meanings, negator flag, and
comparative flag are learned. Honest classification target:
strong L2 developmental integration. NOT claiming L3.

## 7. Determinism and purity

- Seeded LCG for scene generation; no wall-clock, no ASLR-dependent
  behavior in output.
- Pure Zag only. No Python at any stage.
- No em dashes in documentation.
- 3/3 byte-identical runs required (K12).

## 8. Commits

- This prereg committed ALONE before any .zag implementation.
- Implementation + raw + result committed separately.
- Owned paths only. Local commits only.
