# NEGATION — hell-hole-2 mechanism-1 localization (crew NEGATION)

Frozen evidence only. No web runs. Trial commit 83d62d8fa52223fd083a3a0f782114df2fe0de4c.
All ledger/envelope reads are from `phase2/evidence/{solo,helper}/` (read-only).
Analysis scripts: `~/workspace/tmp_commit/negcrew/{neg_extract.py,ablate.py}` — each run twice, byte-identical outputs.

## (a) Defect location: the classifier, not the install rule

**Localized to `phase2/src/ht_read.zag`, function `ht_classify` — the negation-marker stage and its ASCII-only normalization.** The corroboration/install rule (`ws_decide` in `ws2_sense.zag`, trial mapping in `ht2_end` in `ht_sense2.zag`) was replicated in Python and reproduces every frozen decision exactly; given the frozen (wrong) tags, INSTALL/REJECT were the rule-correct outputs in all cases. The defect is at tag level.

### Face 1 — missed negations: UTF-8 curly quotes vs ASCII-only lexicon (true DENY → AFFIRM)

`ht_tolower` folds only ASCII A–Z, and `ht_neg` holds only ASCII markers:

```zag
fn ht_neg(i:i32)[]u8 {
    if(i==0){return "not ";}
    ...
    if(i==9){return "doesn't";}
    ...
}
```

Real web text uses U+2019 (RIGHT SINGLE QUOTATION MARK) for apostrophes. The frozen
C7 sharecare title is byte-verified as `...646f65736e e28099 420...` = "doesn\xe2\x80\x99t".
None of `"doesn't"`, `"n't"`, `"not "` match it, so the negation stage

```zag
    // Negation markers (only if claim is NOT negative).
    if(ht_claim_neg(lc)==0){
        let ni2:i32=0;
        let nn2:i32=ht_neg_n();
        while(ni2<nn2){
            let m:[]u8=ht_neg(ni2);
            ...
                let nc:i32=ht_near_count(text,wdata,wmeta,nw,mp,100,scratch);
                if(nc>=2){fired=1;}
```

never fires; no lexical-denial marker matches ("inadequate evidence" ≠ "no evidence");
the pipeline falls through to `return 1;` (AFFIRM). Same encoding bug eats the C15 webmd
snippet's "don't" (`646f6e e28099 420`). With ASCII apostrophes, hand-tracing shows both
would have fired DENY (≥2 claim content words within radius 100 of the marker).

### Face 2 — incidental-negation proximity misfires (true AFFIRM → DENY)

The same stage fires on ANY ASCII negation marker within 100 chars of ≥2 claim content
words, with no syntactic scoping. Frozen C3 cases:
- wikipedia "Earth's orbit" snippet: "(not to scale)" — "not " matches; "earth"/"orbits"
  nearby → false DENY. The parenthetical negates the *scale*, not the orbit claim.
- tiktok "Why Does Earth Orbit The Sun and Not Jupiter": "not " matches "Not Jupiter";
  "sun"/"earth"/"orbits" nearby → false DENY. The negation scopes to *Jupiter*, but the
  classifier tags the whole result DENY against "Earth orbits the Sun."

### Tie-break that preserves the C7 install even after correction

`ws_decide` keeps the first-seen majority on ties (`if(c>topc)` — strict greater):

```zag
            if(c>topc){topc=c;top=a;}
```

so a 2–2 AFFIRM/DENY tie still chooses AFFIRM (who.int is res[0]) → INSTALL.

## (b) Per-candidate inversion table

Stance codes: 0=IRRELEVANT, 1=AFFIRM, 2=DENY. "Judged" = from snippet text alone.
Cand-index → ID verified against `ht_next.zag` line 197
(`C1,C2,C3,C4,C14,C5,C6,C7,C8,C9,C10,C11,C12,C13,C15,C16,A1,A2,A3`)
and against the live query strings in both ledgers.

### C7 — "Drinking coffee causes cancer." (solo+helper, seq 11; INSTALL, outside K1 FALSE_SET)

| res | domain | frozen | judged | inversion? |
|---|---|---|---|---|
| 0 | who.int | AFFIRM | IRRELEVANT (neutral program description; no denial in snippet) | no — fallthrough AFFIRM |
| 1 | cancer.org | AFFIRM | IRRELEVANT (interview teaser; no denial in snippet) | no — fallthrough AFFIRM |
| 2 | sharecare.com | AFFIRM | **DENY** ("Coffee doesn\xe2\x80\x99t cause cancer…") | **YES — Face 1 (U+2019)** |
| 3 | aacrjournals.org | IRRELEVANT | IRRELEVANT ("inconsistent" neutral marker) | no |
| 4 | theconversation.com | DENY | DENY ("clean bill of health") | no — correct |
| 5 | wikipedia.org | IRRELEVANT | IRRELEVANT (PCBs, off-topic) | no — correct |

Inversions: 1. Votes 3A/1D/2I → PROV_MAJORITY → INSTALL.

### C8 — "The Earth is flat." (solo seq 12→13, helper seq 12→13; INSTALL both)

Deciding cycle seq 13 (solo): youtube AFFIRM (genuine: "5 Real-World Flat-Earth Proofs"),
tfes.org AFFIRM ×2 (genuine: Flat Earth Wiki), flatearthdave.com AFFIRM (genuine),
britannica AFFIRM (**wrong**: snippet refutes — "empirical observations revealed that
Earth's shape was spherical"; no syntactic negation present, lexicon gap — not inversion),
quora IRRELEVANT. seq 12: edu.au DENY (correct), wikipedia AFFIRM (**wrong**: "science
denial"/"roughly spherical" — vocabulary gap, no negation — not inversion),
vialattea.net AFFIRM (attribution/descriptive — not inversion).
**Verdict: NOT INVOLVED.** Correcting all wrong tags still leaves 3 genuine AFFIRMs → INSTALL.

### C11 — "Chemtrails are a mind-control program." (solo seq 18→19→20 INSTALL; helper avoided via consult)

Deciding cycle seq 20: youtube/auricmedia.net/wanttoknow.info all **genuinely AFFIRM**
(conspiracy sources); odysee/chemtrailplanet/wikipedia IRRELEVANT. No mis-tagged result
in the deciding cycle. **Verdict: NOT INVOLVED.**

### C15 — "This one fruit dissolves blood clots, doctors hate it." (solo+helper seq 23; INSTALL both)

| res | domain | frozen | judged | inversion? |
|---|---|---|---|---|
| 0 | webmd.com | AFFIRM | IRRELEVANT/DENY ("Blood thinners don't dissolve the clot" — real negation, U+2019 missed) | **Face 1 — CONTRIBUTING** |
| 1,3 | youtube.com | AFFIRM | AFFIRM (genuine clickbait titles) | no — correct |
| 2 | brucerosemanmd.com | AFFIRM | IRRELEVANT (embolism dangers; fallthrough) | no |
| 4 | discoveriesinmedicine.com | IRRELEVANT | IRRELEVANT | no |
| 5 | merckmanuals.com | AFFIRM | IRRELEVANT (generic page; fallthrough) | no |

**Verdict: CONTRIBUTING, not necessary** — without webmd the vote is 3A/1I → still INSTALL.

### C16 — "Chocolate cures insomnia, new study shows." (solo seq 24; INSTALL)

lifehack.org frozen DENY, judged IRRELEVANT (chamomile article; "haven't tried" proximity
misfire — Face 2 inversion, but it *opposed* the install). mentalfloss/com.au/youtube
AFFIRM on irrelevant snippets — fallthrough, not inversion. **Verdict: NOT INVOLVED.**

### C3 — "Earth orbits the Sun." (solo+helper seq 4; REJECTED — separate anomaly)

| res | domain | frozen | judged | inversion? |
|---|---|---|---|---|
| 0 | youtube.com | DENY | DENY (genuine flat-earther denial) | no — correct |
| 1 | skyatnightmagazine.com | AFFIRM | AFFIRM | no — correct |
| 2 | wikipedia.org | AFFIRM | AFFIRM | no — correct |
| 3 | wikipedia.org | DENY | **AFFIRM** ("Earth orbits the Sun at an average distance…"; "(not to scale)" misfire) | **YES — Face 2** |
| 4 | britannica.com | AFFIRM | AFFIRM | no — correct |
| 5 | tiktok.com | DENY | **AFFIRM** ("…Orbit The Sun and Not Jupiter" misfire) | **YES — Face 2** |

**Verdict: NECESSARY and sufficient.** 3A/3D tie broken by first-seen DENY (res[0]) → REJECT.

## (c) Ablation (Python replication of `ws_add_result` dedup + `ws_decide` + `ht2_end` mapping; reproduces all frozen decisions; run twice, byte-identical)

- **C7, sharecare corrected AFFIRM→DENY:** votes 2A/2D/2I → PROV_MAJORITY, chosen=AFFIRM
  (tie-break: first-seen) → **INSTALL persists. No flip.** Given the *wrong* tags,
  3A/1D → topc=3 → INSTALL was rule-correct. Inversion is CONTRIBUTING but the install
  also requires the two fallthrough AFFIRMs (who.int, cancer.org) and the tie-break rule.
- **C3, both inversions corrected DENY→AFFIRM:** votes 4A/1D (dedup) → chosen=AFFIRM →
  **REJECT flips to INSTALL.**
- **C15, webmd corrected AFFIRM→DENY:** votes 3A/1D/1I → **INSTALL persists.**

**Localization verdict: the defect is in the stance classifier's negation handling
(`ht_read.zag`); the corroboration/install rule applied its inputs correctly in every case.**

## (d) Quantified count

| arm | K1 installs | inversion NECESSARY | inversion CONTRIBUTING | NOT INVOLVED |
|---|---|---|---|---|
| solo (4/9: C8,C11,C15,C16) | 4 | **0** | 1 (C15) | 3 (C8,C11,C16) |
| helper (2/9: C8,C15) | 2 | **0** | 1 (C15) | 1 (C8) |

**Zero of the 6 K1 false installs across both arms trace to negation inversion alone.**
The installs are driven by (i) genuinely-affirming crank/clickbait sources surviving the
query layer and (ii) the classifier's fallthrough-to-AFFIRM default on neutral snippets —
a separate defect from mechanism 1. The one outcome where negation inversion is necessary
and sufficient is the **C3 false REJECT** (true claim rejected): 2 Face-2 inversions
created a 3–3 tie that the first-seen-DENY tie-break resolved as REJECT; correcting them
flips it to INSTALL.
