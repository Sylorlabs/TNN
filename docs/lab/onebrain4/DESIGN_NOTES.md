# DESIGN_NOTES — v7 problem set (Round 4)

How the 44 fresh items were built, what each category is for, and the structural checks performed in `single` mode before freeze. No `.zag` source was opened; all mechanism claims rest on frozen Round-3 traces and single-mode structural probes.

---

## 1. Category budget

| Category | IDs | n | Purpose |
|---|---|---|---|
| V4-binding (forget-hurt, H2) | q01–q05 | 5 | V4 (by=6) denies the forget-target fact → `onebrain`/`nov4` pick 19 (wrong, expected 15); `nov4` keeps 15. Supports claim 2 (V4 harmful). |
| V4-binding (correction-hurt, H1) | q06–q08 | 3 | V4 (by=0) denies the correction-target fact → `onebrain` picks 19 (wrong, expected 16); `nov4` keeps 16. Supports claim 2. |
| Reintegration-room R1 (joke vs memory) | q09–q14 | 6 | Readings 4/5, expected 14. `single` picks 13 (score order); reintegration should prefer the grounded 14. Feeds K1‴. |
| Reintegration-room R2 (joke vs resume) | q15–q20 | 6 | Readings 1/4, expected 17. `single` picks 13; reintegration should prefer the grounded 17. Feeds K1‴. |
| Reintegration-room R3 (resume vs compose) | q21–q24 | 4 | Readings 1/8, expected 18. `single` picks 17; reintegration should prefer the grounded 18. Feeds K1‴. |
| Reintegration-room R4 (challenge vs provenance) | q25–q28 | 4 | Readings 2/3, expected 20. `single` picks 19; reintegration should prefer the grounded 20. Feeds K1‴. |
| Support-quality (Cat-D-like) | q29–q36 | 8 | Same mechanics as R1–R4 but the wrong reading's trigger is more prominent while fact support favors the expected bid. Tests support-quality reasoning that score order misses. |
| Anchors | q37–q40 | 4 | Stable items; all modes expected to agree. Catch implementation breakage. |
| Withhold-by-absence | q41–q44 | 4 | KB-absent entities (wug, quux, fnord, glorp); expected 23. Documents the known generator limitation (machinery answers 19/20). |

Total: 44. The 20 reintegration-room + 8 support-quality items (28) all meet reintegration-room mechanics (≥2 evidence readings, margin ≤12).

---

## 2. Design rules (from frozen R3 traces + probes)

- **Readings 0 and 6 avoided** in reintegration-room/Cat-D items: frozen R3 traces showed correction/forget audit paths drive V4 denial.
- **`?` used** in clean reintegration-room queries so assertion-by-absence (rd7) does not interfere.
- **Keyword→fact map** (single-token probes, 2026-09-27): `eiffel`→fid5+fid11, `tower`→fid5, `everest`/`taller`→fid11, `moby`/`dick`→fid0, `herman`/`melville`/`born`→fid1, `pride`/`prejudice`→fid4, `louvre`→fid3, `france`/`capital`→fid2, `joke`→fid10. Safe (no fact): `novel`, `better`, `greater`, `funny`, `story`, `tale`, `whaling`, `museum`, `austen's`, `famous`, `gallery`.
- **"eiffel" drags fid11**: any "eiffel tower" query creates a third fid11 candidate. Avoided in V4-binding items (kept to exactly 2 candidates); tolerated as inert in some R1/R2/R4 items (V4 does not fire without readings 0/6).
- **Joke-bid grounding**: a bare "joke" grounds bid13 in fid10 (inter=1); "funny"/"hilarious" carry no fact, so bid13 falls back only when its operative content has no fact keywords (else it grounds in the strong entity and kills discrimination).

---

## 3. V4-binding structural checks (manual simulation, single-mode evidence)

**H2 (q01–q05), V4 by=6 (forget).** Each item has exactly 2 candidates, both inter=2 (rel=2). The forget-target fact carries 1 fired dependent bid (bid15); the challenged fact carries 2 (bid19+22). V4 denies the least-relevant; on the rel tie it denies fewer dependent bids → denies the forget-target fact → bid15 cleaned → survivors bid19/bid22 → `nov4`/`onebrain` pick 19 (wrong, expected 15); `single` picks 15.

| Item | Forget target (denied) | Challenged (survives) |
|---|---|---|
| q01 | fid0 moby dick (dep=[15]) | fid4 pride (dep=[19,22]) |
| q02 | fid1 melville (dep=[15]) | fid0 moby (dep=[19,22]) |
| q03 | fid2 france-capital (dep=[15]) | fid4 pride (dep=[19,22]) |
| q04 | fid4 pride (dep=[15]) | fid1 melville (dep=[19,22]) |
| q05 | fid1 melville (dep=[15]) | fid2 france-capital (dep=[19,22]) |

**H1 (q06–q08), V4 by=0 (correction).** Each item has exactly 2 candidates: A-fact inter=2 (rel=2), B-fact (correction target) inter=1 (rel=1). The target entity appears once, via "i meant X", while the initial clause uses a no-keyword paraphrase ("austen's novel", "the whaling tale", "the paris museum"). V4 denies the least-relevant → denies the B-fact → bid16 and bid22 cleaned → `onebrain` picks 19 (wrong, expected 16). Without V4, bid16 (232, grounded) outscores bid19 (224) → `nov4` picks 16.

| Item | A (survives, i2) | B target (denied, i1) | Paraphrase used |
|---|---|---|---|
| q06 | fid0 moby dick | fid4 prejudice | "austen's novel" |
| q07 | fid1 melville | fid0 dick | "the whaling tale" |
| q08 | fid2 france-capital | fid3 louvre | "the paris museum" |

**Design correction during drafting.** The first H1 draft gave the B-fact inter=2 (target word repeated), which would have produced a rel tie → V4 denying the A-fact (fewer deps) → a help, not a hurt. The inter=1 redesign was validated in single mode before freeze.

---

## 4. Reintegration-room checks (single-mode, pre-freeze)

- `readings` column exactly matches single-mode ev1 readings on all 44 items.
- All 36 fork-target items (q01–q36) have top-two fired-bid margin ≤12 (observed 1–12).
- `single` winners are the lower-bid (score-order) choice on all 28 reint-room items (13 over 14, 13 over 17, 17 over 18, 19 over 20) — i.e., the headroom reintegration is meant to close.
- Anchors q39 (margin 18) and q40 (margin 21) are wide-margin; q37 (margin 3) may fork but v6 precedent (q33/q34) shows the fork preserves winner 21.
- Withhold items q41–q44: bid23 fires in single mode; winners are 19/20 (the documented generator limitation).

---

## 5. Known risks / caveats

- **Duel kills (2/17 base rate on `?`-items in v6).** If the fork duel kills the lower reading in an R1/R2/R3 item, `nov4nG` would pick the human-correct bid and the item would anti-contribute to K1‴. v6 precedent shows no duel kills on the (4,5)+?, (1,4)+?, (1,8)+?, (2,3)+? shapes used here, but the risk is structural and disclosed.
- **q26-shape precedent.** v6 q26 ("prove the moby dick claim and cite the source too?") duel-killed rd3. R4 items avoid "too?" and "claim" phrasings; they mimic the q27 (no-kill) shape instead.
- **q43 rephrase.** The first draft ("cite a source for the fnord's origin story?") fired only rd3; rephrased to "prove the fnord's origin and cite a source?" for readings 2/3.
- **Expected bids are human judgment.** Rationales were authored without reference to machine winners; single-mode winners (which follow score order) were used only to confirm structural headroom, never to revise expectations.
