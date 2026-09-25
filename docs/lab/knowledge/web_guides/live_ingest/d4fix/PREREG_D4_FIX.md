# PREREG D4-FIX — keep D4's K1 throughput, add role/modality/reference logic + UNDETERMINED outcome

Status: **FROZEN** — 2026-09-25. This document is the contract. Any change to the
mechanism, batteries, or kill bars below requires a new prereg version.

## 1. Background

D4 (live-ingestion corroboration instrument, PREREG_LI_D4.md) was KILLED:
- K1 throughput PASS: 2/24 Type-B installs (nf-b-12, nf-b-17) vs control 0/24.
- K2 integrity FAIL: installed 1/4 known falsehoods (p3, via subordinate-clause
  triple reduction).
- K3 no-regression FAIL: Type-A 17/20 (lost 4 exact duplicates whose verbs were
  outside the frozen verb table: "lists", "defeated", "drew", "strikes");
  Type-C agreement 15/16.
- Blind red team (VERDICT_REDTEAM.md): honest paraphrases 6/6 install; attacks
  installed 3/6 — argument reversal ("Wolves beat Hawks" / "Hawks beat Wolves"),
  modality collapse ("would beat" / "beat"), pronoun/reference collapse
  ("She wrote…" vs "He wrote…" with different antecedents).

Root causes (white-box):
- `triple_key` sorts/dedupes subject and object token sets and `d4_keys_mergeable`
  allows unconditional subject/object swap as "diathesis" → role reversal merges.
- Modal verbs are verb forms; the rightmost well-formed verb can erase the
  modal distinction → modality collapse.
- Pronouns (he/she/…) are in the glue set → reference collapse.
- Empty/unparseable keys never merge → exact-byte regression on unknown verbs.

Micah's governing example: "Hawks beat Wolves" and "Wolves beat Hawks" must not
merge. The system must recognize the contradiction, attempt resolution via
committed knowledge + logic, and retain both as UNDETERMINED/PENDING if logic
cannot decide.

## 2. Frozen mechanism (D4-FIX = D4 + M1..M6, pure Zag, zero RNG)

### M1 — Proposition frame v2 (d4fix_triple.zag, fork of d4_triple.zag)

Triple key format (all sections `|`-separated, tokens lowercased, sorted, deduped
within subj/obj):

```
stem|modals|vseq|voice|subj|obj
```

- `stem`: stem of the rightmost well-formed verb (unchanged D4 rule).
- `modals`: comma-joined sorted RAW modal forms present anywhere in the
  sentence, from {will, would, can, could, shall, should, may, might, must}.
  Empty when none. Raw forms (not stems): "would beat" ≠ "will beat" ≠ "beat".
- `vseq`: comma-joined surface verb forms in sentence order (every verb-table
  hit). E.g. "marks,mint,date".
- `voice`: "P" if a be-form surface token (am/is/are/was/were/be/been/being)
  appears before the extraction verb, else "A".
- `subj`/`obj`: ordered-role content token sets (sorted, deduped) — same
  extraction as D4, except personal pronouns **he, she, him, her, his, hers**
  are REMOVED from the glue set and are content. All other glue is unchanged.

Primary-clause key (for contradiction detection), format
`pstem|pmodals|psubj|pobj|pvoice`:
- `pstem`: stem of the LEFTMOST verb form that is lexical — i.e. its stem is
  not in {will, can, shall, may, must, be} (excludes modals and be-forms) — and
  has non-empty content subject and object. Falls back to the extraction verb
  if no such verb exists.
- `pmodals`: modal forms appearing before the primary verb.
- `pvoice`: "P" if a be-form appears before the primary verb, else "A".

### M2 — Merge rule (replaces the unconditional diathesis swap)

`d4_keys_mergeable(ka, kb)`:
1. If either key is empty → 0 (unchanged; byte-fallback in M4 covers this).
2. stem must be equal; `modals` must be equal (modality is part of identity).
3. Strict: subj_a == subj_b AND obj_a == obj_b → 1.
4. Swap: subj_a == obj_b AND obj_a == subj_b AND subj_a != subj_b →
   merge (1) ONLY IF the verb-form sequences differ (vseq_a != vseq_b) OR
   voice is "P" in either key. If vseq is identical and both voices are "A",
   the swap is FORBIDDEN (returns 0): two active clauses using the identical
   verb construction with swapped arguments are contradictory claims, not
   paraphrases.
5. Else → 0.

Rationale: honest active/passive pairs ("back"/"is backed", "beat"/"were
beaten") always differ in vseq or voice, so they still merge (K1 preserved:
nf-b-12 merges via differing vseq marks/mint/date vs carries/mint/date;
nf-b-17 merges via differing vseq back vs is,backed and passive voice).
Identical active constructions with swapped roles ("beat"/"beat", both A)
never merge.

### M3 — Contradiction relation (checked BEFORE merge, per candidate pair)

`d4_keys_contradict(ka, kb, pa, pb)` returns:
- 0 = no contradiction detected
- 1 = ROLE-SWAP
- 2 = MODAL
- 3 = REFERENCE

Using primary-clause keys (pa, pb):
- ROLE-SWAP (1): pstem_a == pstem_b AND pmodals_a == pmodals_b AND
  multiset-union(psubj_a, pobj_a) == multiset-union(psubj_b, pobj_b) AND
  psubj_a != psubj_b AND pvoice_a == "A" AND pvoice_b == "A".
  (Union-equality — not exact swap — because shared adjuncts like "winter"
  in "last winter" otherwise mask the swap.)
- MODAL (2): pstem_a == pstem_b AND psubj_a == psubj_b AND pobj_a == pobj_b
  AND pmodals_a != pmodals_b.
- REFERENCE (3): pstem_a == pstem_b AND pmodals_a == pmodals_b AND
  psubj_a == psubj_b AND pobj_a == pobj_b is false ONLY in pronoun tokens:
  after removing {he,she,him,her,his,hers} from all four role sets the sets
  are equal, but the full sets differ.
- Else 0.

Contradicting pairs NEVER merge and NEVER join the same cluster. Each detected
pair is recorded with both normalized sentences and the reason code.

### M4 — Exact-byte fallback (repairs K3)

In `cluster_best`: if both candidates have EMPTY triple keys and their
normalized best sentences are byte-identical → merge. (Covers verbs outside
the frozen table: "lists", "defeated", "drew", "strikes".)

### M5 — UNDETERMINED outcome (verdict + runner)

- The instrument's `verdict` command prints, in loud mode,
  `CONTRADICT|<sentA>|<sentB>|<reason>` for every detected pair, where reason
  is one of ROLE-SWAP / MODAL / REFERENCE. (Backward compatible: the driver
  ignores unknown line prefixes; ANSWER|/PROV|/GATE| semantics unchanged.)
- The runner (`run_d4fix.py`) writes `undetermined_ledger.txt`:
  - `U|<seq>|<cid>|<sentA>|<sentB>|<reason>` per pair.
  - Resolution attempt per pair against committed knowledge: if exactly one
    of sentA/sentB byte-equals an installed `K|` claim in the knowledge
    ledger accumulated so far → `RESOLVE|<seq>|KB-<A|B>|<winning sentence>`;
    otherwise → `RESOLVE|<seq>|UNRESOLVED|BOTH-PENDING`.
  - Resolved pairs do NOT auto-install: installation still requires ≥2
    independent in-cluster sources (deliberate-agency law). The KB-backed
    side is recorded for deliberate promotion.
- The runner also writes `pending_import.txt`: one normalized claim per line
  (both sides of every UNRESOLVED pair), directly consumable by the PENDING
  track's `kbpend` (`claims.txt` format). Pending claims are structurally
  separate from installed knowledge: `knowledge_ledger.txt` format unchanged
  (`K|`/`P|` lines), `refusal_ledger.txt` unchanged (`R|` lines).

### M6 — Determinism

Pure Zag, zero RNG anywhere in the instrument. No Python-side set iteration
in output paths (sorted lists only). Two full runs must be byte-identical
across `knowledge_ledger.txt`, `refusal_ledger.txt`, `undetermined_ledger.txt`,
`pending_import.txt`, `run_li.log`.

## 3. Batteries (all frozen inputs, reused byte-identical)

- B1: 60 novel-facts clusters (`fixtures_novel/snap`, Type-A 20 / Type-B 24 /
  Type-C 16) — K1/K3 bars.
- B2: P battery p1..p4 (paraphrased falsehoods) — integrity probe.
- B3: S1 battery h1..h6 / a1..a6 — honest vs sockpuppet probe.
- B4: W probes w1..w3 — white-box mechanism probes.
- B5: blind red-team battery h1..h6 / a1..a6 (12 clusters,
  `d4_rt_blind1_work/battery/`) — honest active/passive vs attacks.
- B6: 100× scale leg — 6400 synthetic clusters, counts must be exactly 100×
  the 64-cluster pilot.

## 4. Kill bars (F1..F8)

| Bar | Requirement | Predicted |
|-----|-------------|-----------|
| F1 K1 throughput | Type-B installs ≥ 2/24 (the D4 pair: nf-b-12, nf-b-17), control 0/24 | 2/24 |
| F2 role preservation | Zero identical-active-verb role-swap merges. Blind a1, W w2 → WITHHOLD | withhold |
| F3 modality preservation | Zero factual/conditional merges. Blind a2, W w3 → WITHHOLD | withhold |
| F4 reference preservation | Zero different-antecedent merges. Blind a6 → WITHHOLD | withhold |
| F5 K3 no regression | Type-A 20/20; Type-C verdicts identical to control arm | 20/20 |
| F6 undetermined behavior | Every contradicting pair (a1, a2, a6, w2, w3) appears in undetermined_ledger.txt with correct reason; neither side installed from those clusters | 5 pairs |
| F7 honest paraphrases | Blind h1..h6 install 6/6 | 6/6 |
| F8 determinism | Two full passes byte-identical on all five artifacts; zero RNG (grep) | identical |

Secondary measures (reported, not kill bars):
- S-a: P battery installs (D4: 1/4 via p3's subordinate-clause reduction; the
  nominal-verb blind spot is NOT addressed by M1..M6 — predicted 1/4).
- S-b: S1 honest installs (D4: 0/6 — predicted 0/6, mechanism unchanged there).
- S-c: W w1 (predicate shadowing via nominal "date") — predicted still
  INSTALLS (same nominal-verb blind spot as p3). Known residual.
- S-d: blind a3/a4/a5 → WITHHOLD (unchanged).
- S-e: 100× scale leg counts exactly 100× pilot.

FAIL = any F-bar missed. PARTIAL never ends the track (Micah's law).

## 5. Known residuals (not addressed by this prereg)

- Nominal-verb blind spot: when the rightmost "verb" is a nominalization
  ("date", "last", "mint"), the main clause's predicate is invisible to the
  key. p3 and w1 still install. A future prereg may add clause-structure
  roles; this one is scoped to role/modality/reference + UNDETERMINED.
- Negation ("not" is glue) and quantifier subtleties beyond content tokens.

## 6. Commit plan (sylorlabs/TNN, branch tnn-native-lab)

1. This prereg (now).
2. `src/d4fix.zag` + `src/d4fix_triple.zag` (forks; pure Zag).
3. `run_d4fix.py` + evidence (ledgers, verdict analysis).
Never commit binaries or `.zagd` cache files.
