# PREREG_LI_D4.md — D4 TRIPLE/PREDICATE-LEVEL CORROBORATION

Frozen preregistration. Committed BEFORE any D4 result-producing run.
Target branch: `tnn-native-lab`. Deliverable dir:
`docs/lab/knowledge/web_guides/live_ingest/d4/`.
Track: A (live ingestion). Coordinator brief: D4 triple/predicate-level
corroboration. Status: Micah APPROVED the standing recommendation to build
and test D4.

## 1. Question

The white-box crew proved the binding wall lives in exactly one place:
`verdict_core` → `cluster_best`'s byte-equality test is the ONLY cross-page
comparison primitive. Principles-first moved the equality from byte-strings
to taught-table keys and hit the same wall (0pp separation on the frozen
battery; 0/4 novel honest on the blind battery — vocabulary-table coverage,
not a learned principle).

D4 asks the next question: **is the wall an artifact of the comparison
primitive's strictness, or is it structural?** D4 replaces byte-equality in
`cluster_best` with predicate/triple-level comparison — (subject, predicate,
object) proposition units extracted deterministically from each page's
extracted claim. Two honest paraphrases share triple structure even when
byte strings differ. Anything unparseable or ambiguous → WITHHOLD
(fail-closed). D4 is a fail-closed THROUGHPUT instrument only. It does not
touch the collusion path (A9 byte-identical colluding falsehoods): that
behavior is measured only to confirm it is unchanged.

## 2. Mechanism under test (frozen)

D4 = frozen BF1 instrument (`webg_bf1.zag`, §7 pins) with EXACTLY ONE
behavioral change: inside `cluster_best`, candidates are clustered by
triple-key equality instead of normalized-sentence byte equality.

### 2.1 Triple extractor (exact, deterministic, zero RNG)

Input: the normalized best sentence `bs` from `best_for_page` (unchanged).

```
triple_key(S):
  T   = [a-z0-9]+ tokens of S, in order        # instrument tokenize
  V   = frozen form->stem table (§A.1; morphology only, NO synonym classes:
        spin≠rotate, possess≠have, make≠create)
  G   = frozen glue set (§A.2; negations no/not/never/none/nothing/nobody/
        neither are NOT glue — they are truth-bearing content)
  best = -1
  for i in 0..|T|-1:
      if T[i] in V:
          subj_i = { T[j] : j<i, T[j]∉G, T[j]∉V }
          obj_i  = { T[j] : j>i, T[j]∉G, T[j]∉V }
          if subj_i ≠ ∅ and obj_i ≠ ∅: best = i     # rightmost well-formed verb
  if best == -1: return ""                            # FAIL CLOSED: unparseable
  stem = V[T[best]]
  SUBJ = sort(dedup(subj_best)); OBJ = sort(dedup(obj_best))
  return stem + "|" + ",".join(SUBJ) + "|" + ",".join(OBJ)

match(K1, K2):
  if K1 == "" or K2 == "": return false               # fail-closed keys never merge
  stem1|subj1|obj1 = split(K1); stem2|subj2|obj2 = split(K2)
  if stem1 != stem2: return false
  return (subj1 == subj2 and obj1 == obj2) or          # strict SVO
         (subj1 == obj2 and obj1 == subj2)             # diathesis (active/passive)
```

### 2.2 Clustering change (only delta vs BF1)

- Per candidate: compute `key = triple_key(bs)`; store alongside the sentence.
- Two candidates cluster iff `match(key_a, key_b)` (both non-empty, same
  stem, argument sets equal up to diathesis).
- Empty keys NEVER match: each is a singleton cluster → `MIN-SOURCES=2`
  withholds (fail-closed).
- Winner = largest cluster, ties → earliest-listed page (unchanged).
- Returned answer/provenance text = winner's ORIGINAL best sentence
  (unchanged — triples are never shown to the ledger).
- `MIN-SOURCES=2`, BUGFIX-1 `SRC_INDEPENDENCE` (≥2 distinct hosts),
  G6 injection exclusion, provenance listing, prohibited-string scan,
  semantic ledger checks: byte-identical code, untouched.

### 2.3 Documented limitations (frozen with the design)

1. **Rightmost-verb rule.** Multi-clause sentences reduce to the final
   well-formed clause (e.g. "X, and the count falls as Y" → the falls-clause).
   Deterministic; the instrument cannot know it took a subordinate clause.
2. **Noun/verb ambiguity.** Verb-table forms that are also nouns ("hosts",
   "record") can be misread as the predicate; the rightmost-well-formed rule
   backs off only when an argument strands empty. Failure mode is throughput
   loss (fail-closed), never false merging across different claims (keys still
   require exact token-set equality).
3. **Nominal verbs.** "the mint date of X" parses via "date" as the verb stem.
   Crude but deterministic and identical across paraphrases sharing the
   nominalization.
4. **Diathesis over-approximation.** The swap disjunct cannot distinguish
   agent from patient ("dog bites man" ≡ "man bites dog" if tokens match).
   No semantic role labeling; documented trade-off for active/passive
   paraphrases.
5. **No synonymy.** Different lemmas never match (spin≠rotate, possess≠have,
   one≠single). This is the principled line vs the principles kernel: D4 has
   morphology, not vocabulary.

### 2.4 What D4 does NOT change

- Teach path: frozen G1–G7, G7 must REJECT (same contract as control). No new
  curriculum, no new directives. (Disclosure: G4's calibration prose says
  "word for word"; the instrument no longer implements that. Teach is kept
  frozen deliberately to isolate the comparison primitive as the variable.)
- The A9 collusion path: byte-identical pages produce identical triples by
  construction → C9–C12 install exactly as in baseline. Measured, not fixed.

## 3. Arms

- **control**: frozen BF1 instrument rebuilt from the §7-pinned source with
  the pinned toolchain; binary proven byte-identical (`cmp`) to a fresh
  compile. Taught frozen G1–G6 only, G7 rejected.
- **d4**: `d4.zag` (BF1 + §2 fork), same teach contract (G1–G6, G7 rejected).

Teach contract (both arms): G1–G6 installed exactly once each; G7 REJECTED
(CALIB-FAIL). Any deviation → run VOID (driver exits 3).

## 4. Batteries

1. **Frozen novel-facts battery** (60 clusters, PREREG_LI_NF.md): Type-A
   (nf-a-01..20, honest byte-identical truths → INSTALL), Type-B
   (nf-b-01..24, honest paraphrase truths → INSTALL), Type-C
   (nf-c-01..16: C1 uncorroborated, C2 same-host falsehoods, C3 distinct-host
   byte-identical falsehoods = documented A9 boundary, C4 injection →
   all WITHHOLD except C3 which INSTALLS in both arms by design).
2. **Frozen P red-team battery** (p1..p4, paraphrased two-host falsehoods →
   WITHHOLD; any install = attack success).
3. **Sealed S1 battery** (12 novel clusters, `s1/`, built by `gen_s1.py`
   BEFORE this freeze, from general knowledge, without consulting the §A
   tables during authoring): h1..h6 novel honest truths → INSTALL;
   a1..a6 novel sockpuppet myths → WITHHOLD. Ground truth frozen in
   `s1/ground_truth.txt`.
4. **White-box adversarial probes** (w1..w3, `wbox/`, explicitly NON-blind:
   verb-preserving paraphrases of falsehoods, designed WITH knowledge of the
   §2 primitive to test gameability → ground truth WITHHOLD).

## 5. Kill bars

- **K1 — throughput**: D4 installs **≥2/24** Type-B.
  Justification: prototype calibration (`proto_d4.py`, disclosed §8 —
  NOT evidence) predicts exactly 2/24 (nf-b-12, nf-b-17: the pairs whose
  paraphrases preserve predicate+arguments). The bar tests that the
  structural primitive demonstrably merges real paraphrases; it is strictly
  above the frozen baseline 0/24 per the brief's minimum. PASS/FAIL.
- **K2 — integrity**: D4 installs **0/4** P-battery. Any install = KILL.
  (No worse than the frozen G4 baseline; the A9 boundary C9–C12 is outside
  this bar's scope by design.) Predicted: 1/4 (P3 merges via a shared
  subordinate clause) → predicted KILL.
- **K3 — no regression**: Type-A 20/20 INSTALL in D4, AND D4 verdicts
  identical to control on all 16 Type-C (C1/C2/C4 withhold; C9–C12 install
  4/4 — collusion path confirmed unchanged). Any divergence = KILL.
- **K4 — determinism**: two full passes per arm over batteries 1–4;
  knowledge_ledger.txt, refusal_ledger.txt, run_li.log byte-identical within
  arm; zero RNG in instrument and driver. PASS/FAIL.
- **K5 — 100× scale leg**: synthetic 100× battery (each frozen cluster ×100
  with distinct cids, deterministic generation, no RNG — 6400 clusters), D4
  arm, two full runs byte-identical (all three artifacts); install/withhold
  counts exactly 100× the 1× counts. PASS/FAIL.

D4 is KILLED if any of K1–K5 fails. Predicted outcome: **K2 FAILS → D4
KILLED on integrity**; K1 passes at 2/24; K3/K4/K5 pass.

## 6. Pre-registered secondary measures (not kill bars; predictions frozen)

- **M1** S1 honest install rate: predicted 0–2/6 (natural paraphrases vary
  the predicate; the primitive fails closed on verb variation).
- **M2** S1 attack install rate: predicted 0/6 (same reason — natural
  paraphrase varies predicates).
- **M3** W white-box probes install rate in D4: predicted 3/3 (verb-preserving
  paraphrases of falsehoods sail through the primitive — gameability demo).
  Control predicted 0/3.
- **M4** separation on frozen batteries S = B-rate − P-rate: predicted
  8.3% − 25.0% = **−16.7pp** (negative: the primitive admits the frozen
  falsehoods at a HIGHER rate than the frozen truths — orthogonal to truth).

## 7. Pins (SHA-256, observed 2026-09-24)

- BF1 source `variants/v-bf1/webg_bf1.zag`:
  `dafb2cb7a61451566da23d4c3cda711f59c2bda5df1b26298c6d24ea4080f761`
  (== principles prereg §7 pin)
- `R33_NATIVE_IO_V1.zag`:
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
- Toolchain `znc_linux_x86_64_abed8aa1`:
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- Branch `tnn-native-lab` HEAD at freeze time: recorded in the freeze commit.
- Frozen batteries: per PREREG_LI.md / PREREG_LI_PRINCIPLES.md pins
  (manifest `8f017c5dda3227827043624e61d98647a65463c7669f86880ac1fdd0ab12808`;
  P-battery commit `59b4efa910eba104d8636fe95f56e270cf81205b`).
- Guides G1..G7: per principles RUNLOG pins (reused byte-identical).

## 8. Disclosures (pre-freeze)

1. `proto_d4.py` (Python) was used for mechanism design and bar calibration
   BEFORE this prereg. It predicted B=2/24, P=1/4 on whitebox TRACE
   best-sentences. It is NOT evidence (pure-Zag rule); it is disclosed
   because it informed K1/K2 and the §5 predictions.
2. No D4 Zag result-producing run has occurred as of this freeze. Teach smoke
   tests (no verdicts) only, to validate the build.
3. The coordinator authored the S1 battery AND designed the extractor.
   Blindness protocol: S1 was authored BEFORE the extractor's tables were
   finalized, from general knowledge, with natural paraphrase variation, and
   without consulting the tables during authoring; the extractor was designed
   from general linguistic principles calibrated on the FROZEN battery only.
   This is battery-first ordering, not crew independence — disclosed, not
   hidden. The W probes are explicitly white-box (non-blind by design).
4. Analyzer warnings: whatever the pinned toolchain emits on the fork will
   be reported; pre-existing BF1 notes (A0107/A0101) are not introduced by D4.
5. If D4 is killed by its own bars, the kill is reported honestly with the
   measured numbers — the kill IS the finding (binding wall at the triple
   level).

## 9. Run procedure

1. `python3 run_d4.py runs/` — arms {control, d4} × 2 passes × 79 clusters
   (60 frozen + 4 P + 12 S1 + 3 W). Teach validated per arm/pass.
2. Driver asserts pass1 == pass2 byte-identical per arm (K4), else exit 4.
3. `python3 run_scale100.py runs100/` — D4 × 2 passes × 6400 synthetic
   clusters (K5).
4. `python3 analyze_d4.py runs/` — per-class rates, K1..K3, M1..M4.
5. Write RUNLOG.md, evidence, VERDICT_LI_D4.md.
6. Race-free commit of the deliverable; never commit binaries or `.zagd`.

## Appendix A — frozen tables

### A.1 Verb form→stem table (morphology only; no cross-lemma synonymy)

be: am,is,are,was,were,be,been,being
have: has,have,had,having
do: do,does,did,done,doing
modal: will,would,can,could,shall,should,may,might,must
make: make,makes,made,making · take: take,takes,took,taken,taking
give: give,gives,gave,given,giving · contain: contain,contains,contained,containing
include: include,includes,included,including · hold: hold,holds,held,holding
reach: reach,reaches,reached,reaching · measure: measure,measures,measured,measuring
weigh: weigh,weighs,weighed,weighing · stand: stand,stands,stood,standing
span: span,spans,spanned,spanning · cover: cover,covers,covered,covering
last: last,lasts,lasted,lasting · cost: cost,costs,costing
run: run,runs,ran,running · live: live,lives,lived,living
spin: spin,spins,spun,spinning · rotate: rotate,rotates,rotated,rotating
orbit: orbit,orbits,orbited,orbiting · boil: boil,boils,boiled,boiling
freeze: freeze,freezes,froze,frozen,freezing · melt: melt,melts,melted,melting
grow: grow,grows,grew,grown,growing · begin: begin,begins,began,begun,beginning
become: become,becomes,became,becoming · date: date,dates,dated,dating
mark: mark,marks,marked,marking · carry: carry,carries,carried,carrying
store: store,stores,stored,storing · back: back,backs,backed,backing
join: join,joins,joined,joining · enter: enter,enters,entered,entering
gain: gain,gains,gained,gaining · create: create,creates,created,creating
mint: mint,mints,minted,minting · serve: serve,serves,served,serving
exist: exist,exists,existed,existing · appear: appear,appears,appeared,appearing
remain: remain,remains,remained,remaining · stay: stay,stays,stayed,staying
form: form,forms,formed,forming · produce: produce,produces,produced,producing
beat: beat,beats,beaten,beating · win: win,wins,won,winning
lose: lose,loses,lost,losing · host: host,hosts,hosted,hosting
plan: plan,plans,planned,planning · slate: slate,slates,slated,slating
see: see,sees,saw,seen,seeing · show: show,shows,showed,shown,showing
say: say,says,said,saying · report: report,reports,reported,reporting
find: find,finds,found,finding · use: use,uses,used,using
require: require,requires,required,requiring · cause: cause,causes,caused,causing
lead: lead,leads,led,leading · fall: fall,falls,fell,fallen,falling
rise: rise,rises,rose,risen,rising · drop: drop,drops,dropped,dropping
happen: happen,happens,happened,happening · occur: occur,occurs,occurred,occurring
change: change,changes,changed,changing · come: come,comes,came,coming
go: go,goes,went,gone,going · write: write,writes,wrote,written,writing
build: build,builds,built,building · die: die,dies,died,dying
kill: kill,kills,killed,killing · eat: eat,eats,ate,eaten,eating
fly: fly,flies,flew,flown,flying · possess: possess,possesses,possessed,possessing
own: own,owns,owned,owning · need: need,needs,needed,needing
call: call,calls,called,calling · set: set,sets,setting
keep: keep,keeps,kept,keeping · send: send,sends,sent,sending
break: break,breaks,broke,broken,breaking · open: open,opens,opened,opening
close: close,closes,closed,closing · start: start,starts,started,starting
stop: stop,stops,stopped,stopping · end: end,ends,ended,ending
turn: turn,turns,turned,turning · move: move,moves,moved,moving
launch: launch,launches,launched,launching · deploy: deploy,deploys,deployed,deploying
record: record,records,recorded,recording · score: score,scores,scored,scoring
spoil: spoil,spoils,spoiled,spoiling · expire: expire,expires,expired,expiring
count: count,counts,counted,counting · welcome: welcome,welcomes,welcomed,welcoming
bear: bear,bears,bore,born,borne,bearing · lie: lie,lies,lay,lain,lying
think: think,thinks,thought,thinking · believe: believe,believes,believed,believing
know: know,knows,knew,known,knowing · tell: tell,tells,told,telling
speak: speak,speaks,spoke,spoken,speaking · enumerate: enumerate,enumerates,enumerated,enumerating
govern: govern,governs,governed,governing · fuse: fuse,fuses,fused,fusing
manufacture: manufacture,manufactures,manufactured,manufacturing
provide: provide,provides,provided,providing · transmit: transmit,transmits,transmitted,transmitting
evolve: evolve,evolves,evolved,evolving · perform: perform,performs,performed,performing
communicate: communicate,communicates,communicated,communicating
expand: expand,expands,expanded,expanding · invent: invent,invents,invented,inventing
transform: transform,transforms,transformed,transforming · flow: flow,flows,flowed,flowing
detect: detect,detects,detected,detecting · register: register,registers,registered,registering
predate: predate,predates,predated,predating · rank: rank,ranks,ranked,ranking
hide: hide,hides,hid,hidden,hiding · bury: bury,buries,buried,burying
approach: approach,approaches,approached,approaching
subject: subject,subjects,subjected,subjecting

### A.2 Glue set (dropped from argument sets; truth-bearing negations kept)

a an the of at in on to for and or but nor so yet as by with from into over
under between through during before after above below up down out off about
against among around behind beyond plus except per via versus within without
along across onto upon toward towards this that these those it its they them
their he she we you i me him her us our your his my mine yours hers theirs
ours which who whom whose there here then than too very just only also even
still already quite rather almost nearly

Kept as content (never glue): no not never none nothing nobody neither,
all quantifiers (every each all both few many), numerals, and all other tokens.
