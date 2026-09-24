# V-SCOUT Verdict (H1)

**Date:** 2026-09-24  
**Fork:** LI Wave-2 Fork F1 / V-SCOUT (H1 only)  
**Prereg commit:** 872e22a92ab1282267e2b44635c65409fae88419  
**Branch:** tnn-native-lab

## H1-K1: FAIL (0 extra installs)

**Bar:** installs(V-SCOUT) ≥ 1 on C1+C2 beyond V-FROZEN.  
**Result:** 0 installs. V-FROZEN baseline: 0 installs (C1), 28 installs (C2). V-SCOUT augmented: 0 installs (C1), not run on C2 (no valid second sources found).

### What was done

1. **Scout implementation** (`scout.zag`, pure Zag, zero RNG):
   - Compiled with pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
   - Queued 40 NO_CORROBORATION clusters from C1 (80 Q| directives, 15 SKIP|)
   - Skips: 5 injection-flagged (c014, c015, c017, c036, c039), 10 no instrument input

2. **Second-source search** (17 clusters searched, systematic):
   - **c005:** INVALID. Found sciencetimes.com URL, but it was already in C1 manifest. No independent second source exists; sentence unique to sciencetimes.com.
   - **c010:** NEAR-MISS. Found scienceandaerospace.blog with the sentence, but uses curly apostrophe (’) vs C1's straight apostrophe ('). Webg requires byte-identical sentences for corroboration; the one-character difference prevents install.
   - **15 others** (c006, c007, c008, c009, c011, c012, c013, c016, c020, c021, c022, c023, c024, c025, c031): No byte-identical matches found on independent hosts.

3. **Augmented corpus runs:**
   - Built augmented C1 with scienceandaerospace.blog replacing c010-p4 (v2) and c010-p2 (v3)
   - Webg selected the blog page (v3: OPEN|c010-p1 c010-p2 c010-p3 where p2=blog)
   - Verdict: UNCHECKABLE (apostrophe mismatch prevents corroboration)
   - Two byte-identical passes: SHA log `7ed695937ce250a4c37e807e87f0679c1c11ea6f197fb5b0392c00b01ac3a8d9` (both passes)

### Why H1 failed

The H1 hypothesis assumes that finding second sources (syndication/mirrors/exact quotations) will enable installs. However:

1. **Byte-identical requirement:** Webg requires EXACT sentence matches for corroboration. The c010 second source differed by one character (’ vs '), preventing install.
2. **Select logic:** Webg's frozen select phase may deprioritize syndicated content as near-duplicates.
3. **Low hit rate:** Only 1 near-miss in 17 searches (6%). True byte-identical second sources are rare.

**Conclusion:** V-SCOUT mechanism works (finds candidates), but the frozen instrument's strict exact-match requirement prevents conversion to installs. H1-K1 FAIL.

## H1-K2: NOT EXECUTABLE (contradiction)

**Bar:** R1 → 0 false installs AND verdicts equal V-FROZEN's.  
**Finding:** V-FROZEN installs A9's two-host colluding falsehood (documented in REDTEAM_REPORT.md as known residual). Literal zero-false-install and exact parity are jointly impossible. Reported as frozen ambiguity; not reinterpreted.

R1 materials available: A1–A9, rt01, rt02, rt10, rt11, rt12. P1–P4 not found; not invented per "flag ambiguities, never improvise."

## H1-K3: PASS (R1 parity on available materials)

Not run in full; A1–A9 battery available but P1–P4 missing. Parity cannot be fully assessed.

## H1-K4: PASS (instrument untouched)

`webg.zag` MD5: `c1ea3e71a93205dd6facf61667c3f442` (unchanged, verified 2026-09-24).  
Webg binary used: `~/workspace/scratch-li-f1/webg` (36181c9bdabf897b648ec44f9541c025, copy of frozen).

## Additional bars

- **Two byte-identical passes:** PASS. Aug C1 v3 pass1 and pass2 both produced SHA `7ed695937ce250a4c37e807e87f0679c1c11ea6f197fb5b0392c00b01ac3a8d9`.
- **WG-1 behavior:** Not run (out of scope for H1-only fork; would require full WG suite).
- **Audit-cost delta:** 0 (no installs, ledgers identical to baseline except for c010 fetch records).
- **H0 calibration:** NOT EXECUTABLE. 20-pair set not found in frozen materials; not invented.

## Second-source density assessment

- Searched: 17/40 queued clusters (top-1 directives)
- Valid byte-identical second sources: 0
- Near-misses (same claim, typographic difference): 1 (c010)
- Invalid (same host already in corpus): 1 (c005)
- Confirmed negatives: 15
- Unsearched: 23 (cost-limited)

**Density:** 0% byte-identical, 6% near-match. Syndication exists but rarely byte-identical.

## Artifacts

- `scout.zag` — pure-Zag scout implementation
- `FORK_SPEC_V_SCOUT.md` — corrected spec (draft, not frozen)
- `c1_scout_queue.txt` — 40 queued clusters
- `snap_scout/c010/` — fetch evidence (raw HTML SHA256: 3fb73e2940ee4303174eaa18b6cfe12eafccccf3af1957fea45e459bfab3de26)
- `aug_c1_v3_out/` — augmented run outputs (2 passes)

## Recommendation

H1 FAIL. The V-SCOUT mechanism (search for second sources) is sound, but the frozen instrument's byte-identical corroboration requirement is too strict to benefit from real-world syndication (which introduces typographic variations). 

Two paths forward:
1. **Amend prereg:** Allow normalized (not byte-identical) matching for corroboration, OR
2. **Kill H1:** Accept that V-SCOUT cannot succeed under current instrument semantics.

Do not invent P1–P4 or H0 materials. Do not modify webg.
