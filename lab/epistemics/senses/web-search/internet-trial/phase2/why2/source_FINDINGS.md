# SOURCE crew findings — reliability-weighted reconstruction (mechanism 4)

**Question:** would source-reliability weighting of the frozen stance tags have
changed the hell-hole trial's dispositions/bars? Method: replicate
`ht_decide_bin`'s corroboration rule exactly, then re-run it as a
reliability-weighted vote over the frozen stance tags. Frozen evidence only
(`phase2/evidence/`), read-only. Deterministic Python, no RNG, no timestamps,
sorted iteration; two runs byte-identical
(sha256 `d9f163a99a51edebc16133d33a109e904b3398c562c6197e959fb42d67f34454`).

**Harness validation:** the unweighted replication (all weights = 1) reproduces
the frozen final dispositions EXACTLY — all 19 candidates, both arms. The
replicated rule: per query-cycle, ingest results in envelope order, stance →
{AFFIRM, DENY, IRRELEVANT}; dedup on (envelope-domain, answer); cap 6 stored;
helper observation appended last (dropped if stance 0, same dedup/cap);
winner = top answer by count with strict-> (first-appearance wins ties);
INSTALL iff winner count ≥ 2 and winner is AFFIRM, REJECT iff DENY, else
WITHHOLD; known candidates (C1, C14, A1–A3): installed="AFFIRM",
CONFIRM→INSTALL iff no disagreeing entry, else REVISE iff contra-value
("DENY", A1–A3 only) has ≥ 2 distinct supporting domains, else WITHHOLD.
Final disposition per candidate = last query-cycle decision (matches
`ht_score.py`). This matches `ws_decide`/`ht2_end` semantics including the
non-obvious bits: IRRELEVANT stances ARE stored and counted; the 6-cap can
drop the helper observation; ties break to the first-seen answer.

## (a) Frozen domain-reliability rubric (verbatim, pre-committed before stance analysis)

Tiers by domain class only. Classification is mechanical: explicit-list
membership (suffix match on the URL host, lowercased, leading `www.` stripped,
progressive left-label stripping so `wiki.tfes.org` → `tfes.org`), then suffix
rules, then default. No per-claim tuning.

- **T3 — official / academic / health authority.** Suffix rules: `.gov`,
  `.gov.<cc>`, `.mil`, `.int`, `.edu`, `.edu.<cc>`, `.ac.<cc>`. Explicit:
  `cancer.org`, `mayoclinic.org`, `cedars-sinai.org`, `massgeneralbrigham.org`
  (major academic medical centers), `science.org`, `aacrjournals.org`,
  `tandfonline.com`, `mdpi.com`, `iop.org` (academic publishers).
  Rationale: statutory/official publishers and peer-reviewed or editorially
  accountable health/academic authorities.
- **T2 — established press / wire / reference / fact-check.** Explicit:
  `wikipedia.org`, `britannica.com`, `reuters.com`, `apnews.com`, `snopes.com`,
  `factcheck.org`, `politifact.com`, `fullfact.org`, `eufactcheck.eu`,
  `bbc.co.uk`, `bbc.com`, `nytimes.com`, `theguardian.com`, `washingtonpost.com`,
  `npr.org`, `pbs.org`, `smithsonianmag.com`, `nationalgeographic.com`,
  `scientificamerican.com`, `newscientist.com`, `theconversation.com`,
  `livescience.com`, `space.com`, `usatoday.com`, `cnn.com`, `nbcnews.com`,
  `abcnews.go.com`, `cbsnews.com`, `aljazeera.com`, `dw.com`, `france24.com`,
  `euronews.com`, `japantimes.co.jp`, `forbes.com`, `time.com`, `newsweek.com`,
  `theatlantic.com`, `economist.com`, `vox.com`, `buzzfeednews.com`, `ajc.com`,
  `rochesterfirst.com`, `telegraph.co.uk`, `metro.co.uk`, `sciencefocus.com`,
  `skyatnightmagazine.com`, `medicalnewstoday.com`, `healthline.com`,
  `webmd.com`, `sciencealert.com`, `scitechdaily.com`, `merckmanuals.com`,
  `skepdic.com`, `yourgenome.org`, `energyeducation.ca`.
  Rationale: outlets with named editors, corrections policies, reputational
  accountability. Class-based, not an endorsement of any single article.
- **T1 — general web / commercial / specialist (default).** Everything not
  otherwise classified: commercial publishers, brand sites, specialist
  hobby/technical sites, aggregators. Rationale: unknown editorial standards.
- **T0 — forums / blogs / UGC / unknown / obscure.** Explicit platforms:
  `reddit.com`, `quora.com`, `stackexchange.com`, `stackoverflow.com`,
  `medium.com` (+subdomains), `blogspot.com`, `blogger.com`, `wordpress.com`,
  `substack.com`, `tumblr.com`, `youtube.com`, `tiktok.com`, `facebook.com`,
  `instagram.com`, `x.com`, `twitter.com`, `pinterest.com`, `linkedin.com`,
  `vimeo.com`, `dailymotion.com`, `github.io`, `gitlab.io`, `weebly.com`,
  `wixsite.com`, `slideshare.net`, `scribd.com`, `odysee.com`. Explicit obscure/
  single-author / unaccountable: `all-can.org`, `auricmedia.net`,
  `bottomofthat.com`, `galactic-hunter.com`, `nexaconvert.com`,
  `nibble-app.com`, `discoveriesinmedicine.com`, `dnaftb.org`,
  `gnet-research.org`, `genomesunzipped.org`, `climateaudit.org`,
  `dsimanek.vialattea.net`, `wanttoknow.info`, `brainly.com`, `quizlet.com`,
  `factually.co`, `insomnia.net`, `brucerosemanmd.com` (single-practitioner
  marketing site). Rationale: unaccountable authorship.
- **T-1 — known conspiracy / denial / spam / commercially-captured.**
  Explicit: `flatearthdave.com`, `tfes.org` (flat-earth advocacy, incl.
  `wiki.tfes.org`), `chemtrailplanet.com` (chemtrail advocacy),
  `stopworldcontrol.com` (conspiracy-promoting), `thehighwire.com`
  (anti-vaccine misinformation show), `conspiracydata.com`
  (conspiracy-themed), `allegro.cz`, `heureka.cz` (shopping aggregators
  served as results on miracle-cure queries — commercially-captured spam
  context), `cholesten.nutraceutics.cz`, `biologicals.cz`, `uvtnet.cz`,
  `vyspimesa.sk` (supplement sellers returned on health claims —
  commercially captured), `draxe.com` (wellness marketing selling
  supplements). Rationale: adversarial or commercially captured sources on
  the claim class. Every T-1 assignment is name/class-evident and auditable;
  nothing was assigned T-1 from its stance tag.

**Pre-committed weight schemes** (no tuning after seeing results):
- Scheme A: T3=8, T2=4, T1=2, T0=1, T-1=0.25
- Scheme B: T3=4, T2=3, T1=2, T0=1, T-1=0 (conspiracy/spam votes excluded)
- Corroboration threshold 2.0 on both (the weighted analog of "≥ 2
  independent domains": two T0 votes). Helper observation = T0 weight
  (untrusted observation, pre-committed).
- Weighted rule: each stored entry votes its tier weight; winner = max total
  weight (strict >, first-appearance wins ties, mirroring the trial code);
  winner weight ≥ 2.0 → INSTALL/REJECT/WITHHOLD by winner, else WITHHOLD.
  Known path: bad-weight = Σ weights of entries ≠ "AFFIRM"; 0 → INSTALL;
  else REVISE iff contra ("DENY", A1–A3) weight ≥ 2.0, else WITHHOLD.

## (b) Tier distribution across the 58 envelopes

Result entries (348 total: 28 solo + 30 helper envelopes × 6):
**T3=40, T2=114, T1=85, T0=81, T-1=28.**
The retrieved sets are dominated by T2/T1/T0; T-1 appears only in the
conspiracy/spam/miracle-cure queries (C6, C8, C9, C10, C11, C15, C16).

## (c) Weighted-vote dispositions, both schemes, both arms

Schemes A and B produce **identical dispositions on all 19 candidates in
both arms** — the outcome is not an artifact of the weight choice.

| ID | Claim (label) | SOLO frozen → weighted | HELPER frozen → weighted |
|---|---|---|---|
| C1 | water boils (TRUE) | WITHHOLD → WITHHOLD | WITHHOLD → WITHHOLD |
| C2 | speed of light (TRUE) | INSTALL → INSTALL | INSTALL → INSTALL |
| C3 | earth orbits sun (TRUE) | **REJECT → INSTALL** (fix) | **REJECT → INSTALL** (fix) |
| C4 | 23 chromosome pairs (TRUE) | INSTALL → INSTALL | INSTALL → INSTALL |
| C5 | COVID lab leak (CONTESTED) | INSTALL → INSTALL | INSTALL → INSTALL |
| C6 | eggs/cholesterol (EVOLVED) | REJECT → REJECT | REJECT → REJECT |
| C7 | coffee causes cancer (FALSE) | INSTALL → INSTALL | INSTALL → INSTALL |
| C8 | flat earth (FALSE) | INSTALL → INSTALL | INSTALL → INSTALL |
| C9 | moon landings faked (FALSE) | **REJECT → INSTALL** (worse) | **REJECT → INSTALL** (worse) |
| C10 | 5G caused COVID (FALSE) | WITHHOLD → WITHHOLD | WITHHOLD → WITHHOLD |
| C11 | chemtrails (FALSE) | **INSTALL → WITHHOLD** (better) | WITHHOLD → WITHHOLD |
| C12 | tallest mountain (AMBIGUOUS) | INSTALL → INSTALL | INSTALL → INSTALL |
| C13 | largest desert (AMBIGUOUS) | INSTALL → INSTALL | INSTALL → INSTALL |
| C14 | 8 planets (TRUE) | WITHHOLD → WITHHOLD | WITHHOLD → WITHHOLD |
| C15 | fruit dissolves clots (SPAM) | INSTALL → INSTALL | INSTALL → INSTALL |
| C16 | chocolate cures insomnia (SPAM) | INSTALL → INSTALL | WITHHOLD → WITHHOLD |
| A1–A3 | mind-conflict | REVISE → REVISE | REVISE → REVISE |

Flips vs frozen: solo {C3, C9, C11}; helper {C3, C9}. Nothing else moves.

Per-candidate mechanism notes (weighted winner, scheme A; final query-cycle):
- **C3 (fix):** frozen REJECT came from a 3–3 count tie broken by
  first-appearance (DENY from youtube/tiktok seen first). Weighted:
  AFFIRM 12.0 (skyatnightmagazine, wikipedia, britannica — all T2) vs DENY
  6.0 (wikipedia tagged DENY, youtube, tiktok T0). Weighting resolves the
  tie correctly.
- **C9 (worse — weighting actively harmful):** frozen REJECT was correct
  (DENY: wikipedia T2, bbc.co.uk T2, conspiracydata T-1). The frozen tag on
  the `iop.org` result ("How do we know that we went to the Moon?" —
  snippet explicitly *denies* the hoax claim) is AFFIRM — a classifier
  error. Weighted: AFFIRM 10.0 (listverse T1 2.0 + iop.org T3 8.0) beats
  DENY 8.25 → false INSTALL. One mis-tagged T3 vote outweighs two
  correctly-tagged T2 DENYs.
- **C11 solo (better):** final query's AFFIRM votes are all T0
  (youtube, auricmedia.net, wanttoknow.info: 3.0) vs IRRELEVANT 5.25 →
  WITHHOLD. Helper arm already WITHHELD.
- **C7 (no change):** the frozen tags mark `iarc.who.int` and `cancer.org`
  results AFFIRM although both snippets deny/discuss-neutrally the claim
  (the known classifier inversion). Weighted AFFIRM = 8+8+2 = 18.0 vs DENY
  4.0 → INSTALL stands. **Weighting amplifies the classifier error** by
  giving the mis-tagged votes 8× weight.
- **C8 (no change):** the followup query "the earth is flat evidence
  systematic review" returned a one-sided set (youtube, tfes.org,
  quora, britannica tagged AFFIRM, flatearthdave). Weighted AFFIRM 5.5 ≥
  2.0 → INSTALL. **Weighting cannot manufacture counter-evidence that the
  retrieval never returned.** (Even scheme B with T-1=0: AFFIRM 5.0.)
  The helper consult went to C8's *first* query only, so the final
  one-sided query decided alone in both arms.
- **C5 (no change):** `whitehouse.gov` (T3) and `science.org` (T3) frozen
  AFFIRM → weighted AFFIRM dominates → INSTALL. One-sided authoritative
  affirmation; nothing to reweight against.
- **C12/C13 (no change):** one-sided AFFIRM sets (all T1; C13 has one T1
  DENY). No counter-evidence → weighting cannot move them.
- **C15 (no change):** `webmd.com` and `merckmanuals.com` frozen AFFIRM
  (snippets are generic "how blood clots dissolve" pages — keyword-overlap
  mis-tags); T2 weights dominate → INSTALL.
- **C16 (no change):** T1/T0 AFFIRMs outnumber the single T1 DENY.
- **C1/C14 (no change):** known-path WITHHOLD stands (disagreeing weight
  > 0, contra empty). **A1–A3 (no change):** REVISE stands (contra DENY
  weight ≥ 2.0).

## (d) Recomputed bars and honest verdict

Metrics use the frozen `ht_score.py` formulas. FALSE_SET =
{C8,C9,C10,C11,C15,C16,A1,A2,A3}; CONTRA_SET = {C5,C12,C13}.

| Bar | Rule | SOLO frozen → weighted | HELPER frozen → weighted |
|---|---|---|---|
| M1 ≥ 0.80 | (REJECT+WITHHOLD+REVISE)/9 | 0.556 → **0.556** FAIL | 0.778 → **0.667** FAIL (worse) |
| K1 trips ≥ 0.20 | INSTALL(FALSE)/9 | 0.444 → **0.444** TRIPS (installs C8,C9,C15,C16: C11 fixed, C9 newly installed) | 0.222 → **0.333** TRIPS (worse; installs C8,C9,C15) |
| M3 ≥ 0.80 | WITHHOLD on C5,C12,C13 | 0.000 → **0.000** FAIL | 0.000 → **0.000** FAIL |
| K2 trips > 0.30 | INSTALL/REJECT on C5,C12,C13 | 1.00 → **1.00** TRIPS | 1.00 → **1.00** TRIPS |

**Honest verdict: reliability weighting ALONE saves no bar in either arm.**
Solo: every bar value is unchanged (C11's fix is exactly cancelled by C9's
flip). Helper: weighting makes M1 and K1 *worse* (0.778→0.667,
0.222→0.333) because it flips C9's correct REJECT to a false INSTALL while
fixing nothing. M3/K2 are untouched — the contradiction trials' retrieved
sets are one-sided affirmations, and no weighting of votes can turn
agreement into doubt.

Three structural reasons weighting fails here, in order of importance:
1. **Stance-tag errors dominate, and weighting amplifies them.** The
   failures that weighting "should" fix (C7, C9, C15) rest on authoritative
   sources whose frozen stance tags are wrong (iarc.who.int, cancer.org,
   iop.org, webmd.com, merckmanuals.com — snippets verified against the
   tags; they deny or are neutral, not affirming). Giving a mis-tagged vote
   8× weight makes the error 8× worse. C9 is the clean demonstration: the
   unweighted rule got it right; the weighted rule gets it wrong.
2. **One-sided retrieval.** C8's followup, C5, C12, C13 returned sets with
   no (or negligible) counter-evidence. A weighted vote over a one-sided
   set is still one-sided — weighting cannot manufacture the missing
   DENY. This is mechanism 2 (query-bias corroboration), not mechanism 4.
3. **Genuine ambiguity.** C12/C13 are ambiguous claims the oracle says to
   WITHHOLD; the rule has no claim-type input, weighted or not.

The one place weighting helped (C3 tie-break, C11 solo demotion) shows the
mechanism is not useless — it is simply not the binding constraint. The
binding constraints are upstream: the stance classifier's systematic
errors on negation/nuance/keyword-overlap (mechanism 1) and one-sided
retrieval with no disconfirmation-seeking (mechanism 2).

**Follow-up (not done — another crew's territory):** weighting × stance
corrections. The corrected tags would likely change C7/C9/C15/C16
substantially (the mis-tagged T3/T2 AFFIRMs become DENYs, which weighting
would then amplify *correctly*). Re-running this script on corrected tags
is cheap once they exist — the harness is validated and deterministic.
Suggested as the joint mechanism-1+4 test. No web re-runs needed.

## Reproducibility

- Script: `~/workspace/tmp_commit/source_crew/weighted_repro.py`
  (rubric + both schemes + unweighted validation in one file).
- `python3 weighted_repro.py` twice → byte-identical output
  (sha256 `d9f163a99a51edebc16133d33a109e904b3398c562c6197e959fb42d67f34454`).
- Read-only on `phase2/evidence/`; no network; no RNG; no timestamps.
- Known limitation: tier assignment for ~10 borderline hosts
  (e.g. `skepdic.com`→T2, `dsimanek.vialattea.net`→T0,
  `conspiracydata.com`→T-1, `insomnia.net`→T0, `factually.co`→T0) involved
  class judgment calls, all recorded in the rubric section above; schemes A
  and B agree everywhere, so none of these calls affect any disposition.
