# Cross-reference preregistration — TIER 2 (committed 2026-09-21/22 verdicts)

**Frozen:** 2026-09-22 (PDT), with `SCOPE.md`. One clean-environment crew per family unless noted; cross-reference = the replication's numbers vs the committed values (byte-identical digests must match exactly). Type A/B/C per family below. Wave 2 execution; heavy families (T2-SCALE, T2-THROUGHPUT) run Type B and never concurrently on this VM.

---

## T2-SCALE — scale-up: nothing broke to 6,585,360 facts (Type B)

**Claims:** clean mastery 1.0000 from 240 to 6,585,360 facts (24 categories × 274,390; every word position of all 10 Gutenberg texts); flaw battery 96/96 at every completed scale; zero forgetting (first/last decile 1.0, gap 0); all-fact 0.9501; absorption 328,532/328,532; cost exactly linear (4.000 ops, 92 B/fact from 2,400 up); byte-identical reruns; no kill bar tripped; run stopped at corpus ceiling. Honest caveats: millions of facts, not billions of tokens; planted falsehoods absorbed at 1.0 at every scale (consistent lies go in smooth).
**Evidence:** commit `9a17fec572d2`, `docs/lab/scale/`.
**Method:** anchor replication — rerun the 240-fact anchor and one mid-scale point (crew picks the cheapest scale ≥100K facts that the committed evidence shows as a completed leg) with the same measurement method in a clean checkout; verify mastery 1.0000, 4.000 ops, 92 B/fact, byte-identical reruns at those points. Do NOT re-run the 6.58M sweep; state the honest limit.
**Rule:** REPRODUCED if anchor+mid-scale numbers match exactly; NOT REPRODUCED if any differs; PARTIAL if mastery holds but cost accounting differs (name it).

## T2-SCALEDOWN — scale-down: no floor (Type A)

**Claims:** learning curve flat at 1.0 mastery from 1 fact to 6,585,360 (1/1, 2/2, 8/8, 192/192, 6,585,360 all 1.0000); one-shot works — a lie taught once absorbs 1/1 as completely as at 6.5M (12/12); first recall-latency measurement ~0.2–0.4 µs/probe, constant in N, 10–20× faster than install. Caveat: procedural integer facts, not prose.
**Evidence:** commit `2d367807d806`.
**Method:** full rerun of the small-N legs (1/2/8/192 facts) + one large-N leg if the crew can afford it within the VM cap; measure recall latency vs N.
**Rule:** REPRODUCED if small-N mastery is 1.0000 at every leg, one-shot lie absorbs 1/1, and latency is constant in N; else NOT/PARTIAL as the divergence dictates.

## T2-PARAMS — parameter scaling: baseline ×1 is the efficiency frontier (Type A)

**Claims:** 19 configs × 3 reps at 24,000 facts, commit `ccbb3d3c39d7`: 16/19 configs produce the byte-identical learner (same digest, not just scores); slots ×0.25/×0.5 degrade gracefully and exactly proportionally; baseline ×1 holds 1.0000 mastery at 4.000 ops, 92 B/fact; evidence ×0.25–×4, verify-depth ×2/×4, redundancy ×2/×4, joint-maxed all change zero behavior, only cost (verify-depth ×4: 1.75× cost; redundancy ×4: 2.5× cost, 3.3× memory); taught falsehoods absorbed 1.0 at every config.
**Method:** full rerun 19×3 in clean checkout; compare all 19 digests and the cost multipliers.
**Rule:** REPRODUCED if ≥16/19 digests byte-identical (name which 3 differ and how), proportional slot degradation holds, cost multipliers match; NOT REPRODUCED if the identical-digest count drops below 16 or any non-slot config changes behavior.

## T2-PROSE — prose learning: wording shape beats model quality (Type A)

**Claims:** commit `d4c151c7e39c`: all four sources trip the ≥0.98 viability bar — sol 220/228 (0.9649, −3.5pp), step 0.8947 (−10.5pp), muse-native 0.8772 (−12.3pp), grok-4.6 0.8289 (−17.1pp); extraction 240/240 perfect; cause = retrieval ties, not extraction; Q=+0.0022 → frozen NO-DIFFERENTIATION; fluent lies install 12/12 in prose. Honest scope: bag-of-stemmed-words retrieval.
**Grok-4.7 rerun:** commit `fbecf64f08b6f5f41efbf33ef07384154cd48140`: on frozen prose bars, 4.7 yields Q=+0.0548 → mechanically QUALITY-MATTERS (boundary result at +0.05 band edge); prose viability still fails 0.9342 vs 0.98; both teachers absorb all 12 falsehoods; direct head-to-head clean mastery gain +10.5pp. Five live-4.7 items remain blocked — excluded.
**Method:** rerun the four-source prose battery on committed corpora (clean checkout, ≥3 byte-identical); re-derive the Q statistic for 4.6 and for the committed 4.7 corpus with independent Zag code.
**Rule:** REPRODUCED if all four viability figures match and Q(4.6)≈+0.0022/NO-DIFFERENTIATION while Q(4.7)≈+0.0548/QUALITY-MATTERS; NOT REPRODUCED if the quality verdict flips for either model.

## T2-DUEL — sol-vs-grok duel: SCENARIO-FIT, no overall champion (Type A)

**Claims:** commit `e18a2ca13589` (build `6c520a990a01`, `6978db0af55f`): 384 taught, 432 probes, sealed battery, disjoint vocab, frozen rules: grok paraphrase 0.9792 vs 0.5000 (delta 0.4792 > 0.03 bar) but fails eligibility with 0.24 wrong-value rate (104 wrong values); sol safety 1.0000 (zero confabulation), precision 1.0000 (0.0000 wrong-value), brittle on paraphrase; frozen hybrid = sol unless unknown → grok = defers to grok exactly at abstention (safety-critical) cases; neither does coreference-mediated retrieval.
**Method:** full rerun of the duel battery from committed corpora; recompute all four headline figures + eligibility gate + hybrid behavior.
**Rule:** REPRODUCED if paraphrase figures, wrong-value rates, safety/precision all match and the SCENARIO-FIT verdict (no champion) stands; NOT REPRODUCED if grok's wrong-value rate drops to eligibility or sol loses precision.

## T2-WEBV2 — web-search sense v2: live web works (Type C)

**Claims:** commit `ff97c7a08fcb`: search.lumy.live SearXNG JSON 10/10 probe bar; legs A 20/20, B 6/6, C 12/12 falsehoods caught, D 12/12, M 24/24, R 24/24, S 4/4 with exactly 2 transport fires; R-CORR favored — 0 false installs outside the preregistered unanimous-spoof residual, installs all true claims, withholds all single-source falsehoods; read-only mechanically install-free (0 install ops); R-CONTRA installs single-source falsehoods 4/4 (negative control); honest residual: unanimous two-source spoof still fools.
**Method:** Type C — do not hit the live web to re-run (unrepeatable); re-derive every leg figure from committed evidence with independent Zag code; verify the 0-install-ops claim for read-only from committed ledgers; verify the unanimous-spoof residual instances are as described.
**Rule:** REPRODUCED if every leg figure re-derives exactly and the R-CORR vs R-CONTRA distinction holds in the evidence; UNREPLICABLE-AS-IS for any leg whose evidence is missing.

## T2-INFORICH — information richness: emergence confirmed (Type C)

**Claims:** commit `25c2a18b2416`: facts-only learner absorbs 12/12 planted falsehoods; with live web-search sense, read-only installs 0/12, catches 12/12, answers 4/4 unknowns provisionally; corroboration-gated editable installs 0/12 falsehoods, installs the true value on all 12, answers all 4 unknowns; corroboration-gated still installs colluding-domain spoofs 2/2 (sensor-deceivable boundary). Three axes: parameters→cost, mechanisms→resolve competing claims, information→decides truth.
**Method:** Type C — re-derive all figures from committed evidence; independent check of the 2/2 colluding-spoof installs.
**Rule:** REPRODUCED if all figures re-derive; PARTIAL if any axis figure differs (name it).

## T2-HELLHOLE — internet hell-hole phase 2: binding FAIL (Type C)

**Claims:** commit `83d62d8fa52223fd083a3a0f782114df2fe0de4c` (API-verified): 19-candidate course, ARM-SOLO (28 queries) and ARM-HELPER (30 queries, 16 Muse-native consultations as untrusted observations only), pure Zag, zero RNG, hash-chained ledgers, 5/5 byte-identical replays matching live ledgers. Solo installed 4/9 false claims (flat earth, chemtrails, two content-farm miracle cures); helper 2/9; both tripped K1; bullshit detection 0.556 solo / 0.778 helper vs 0.80; contradiction 0.000 both, all 3 contradiction trials installed → K2 tripped; all 3 false priors deliberately revised, zero CORRUPT. Root mechanisms: negation/nuance inversion by stance classifier, affirm-seeking query bias, no claim-type gate.
**Whys** (commit `1d6d5faa10926947b8b23990b76ce2b2a9886d86`): phase-2's #1-cause guess was wrong — stance classifier is #1 damage but NOT via the negation bug (0/6 false installs; its one clean kill was falsely REJECTING "Earth orbits the Sun"); real install engine = fallthrough-to-AFFIRM default; corroboration/install rule EXONERATED; attribution over 14 failure instances (M1 9: 5 installs + 4 contradiction misses; M3 6 owns contradiction wipeout; M2 3; M4 1, and weighting alone makes helper WORSE: M1 0.778→0.667, K1 0.222→0.333); skepticism rescore (C8, C11 out): solo M1 0.714 FAIL K1 0.286 trips; helper M1 0.857 (6/7) PASS K1 0.143 clear; contradiction still FAIL; K1-clear brittle (excluding C9/C10 trips again at 0.200); gate counterfactual (WITHHOLD-before-corroboration on contested/ambiguous/evolved/skepticism): helper FULL PASS (M1 8/9, K1 1/9, M3 1.0), solo still fails on C15/C16 spam pair alone; fix order M1b→M1a→M3→M2→M4; C7 false install outside frozen FALSE_SET (never counted); C3 false REJECT via negation misfire; C1/C14 over-withhold.
**Method:** Type C — live web unrepeatable; verify hash chains and 5/5 byte-identical replays from committed ledgers; recompute every figure (installs, bullshit detection, contradiction, all why-attribution counts, both rescores, gate counterfactual) with independent Zag code; apply the frozen kill criteria mechanically.
**Rule:** REPRODUCED if the FAIL verdict and every attributed count re-derive; NOT REPRODUCED if K1/K2 application was wrong or any count is off; the C7/C3/C1/C14 anomalies must be confirmed present as described.

## T2-JOKE — web joke/lie/satire: PARTIAL (Type A)

**Claims:** prereg `8f33adac` frozen pre-run; evidence `d7e59016` (branch head, API-verified): 30 real web items (6 satire / 6 deadpan jokes / 6 hoaxes / 6 sincere-weird truths / 6 sincere false beliefs), solo + helper arms, pure Zag, 5 runs/arm byte-identical. Bars: joke catch solo 0.17 (KILL BAR TRIPPED, arm-specific) / helper 0.67; satire 1.00/1.00 (via URL provenance, not prose — honest limitation); hoax handled 0.83/0.50; non-sincere installed solo 0.03 (1 item: tree-octopus) / helper 0.10 (glue pizza, Apple Wave, Damascus — at pass boundary). Glue-on-pizza: SOLO JOKING/withheld; HELPER SINCERE/INSTALLED. Controls: no sincere person called deceptive; no sincere truth misflagged; sincere-false called deceptive 0.00/0.00. Qualifications: intent reader is crew-built test-side English marker machinery; "installed" = ledger disposition, not live belief write.
**Method:** full rerun from committed items + marker machinery in clean checkout; 5 runs/arm byte-identical.
**Rule:** REPRODUCED if every bar figure matches including the solo kill-bar trip and the glue-on-pizza solo/helper split; NOT REPRODUCED if any bar flips.

## T2-THROUGHPUT — output throughput: the everything table (Type B)

**Claims:** commit `67bf4c4cf81b9d1d5e1e4e150892843830ff8b2b` (41 files, API-verified; method frozen first in `docs/lab/ops/throughput/METHOD.md`; honest caveat: commit message landed empty — /tmp tmpfs full at commit time): lab VM, pinned znc: install ~6.2 µs/fact → ~162K facts/sec (re-verified; original 4.2 was user-CPU under quiet VM — method corrected to CLOCK_PROCESS_CPUTIME_ID); 4 ops / 92 B per fact reproduce exactly; emission ~507K chars/sec median (342K–1.29M range, ~65 µs/utterance, 33-char avg); end-to-end hear→think→speak ~109K chars/sec, ~0.30 ms/turn (~100× human typing, 38-fact KB); recall ~1–3.2M probes/sec, O(1) in N; deliberation ~3,300 episodes/sec. Hardware answer: output is local copy/prose-template work at ~0.5 MB/s, trivial for any machine.
**Method:** Type B — rerun the install/recall/deliberation anchor measurements with the frozen METHOD.md in a clean checkout (quiet VM, same clock discipline); do not re-run the full table. State VM-load sensitivity explicitly.
**Rule:** REPRODUCED if install ≈6.2 µs/fact (±10% for VM noise), 4 ops/92 B exact, recall O(1) in N within the 1–3.2M band, deliberation ≈3,300/s (±20%); PARTIAL if the band moves but ordering holds (name it).

## T2-SPEEDINTEL — speed-intelligence exchange rate: 2× is the knee (Type A)

**Claims:** measured, frozen prereg, pure Zag, byte-identical: 1× deliberation starved (6/18 coding, 29/94 epistemic — ~2× cost per quality point vs the knee); 2× is the knee (18/18 coding, 59/94 epistemic); 4×/8× add nothing (18/18, 59/94, confirmed on a fresh battery); 2× + free-speed mechanisms reaches knee quality at ~2/3 the eval cost of naive 1× (65.1% fewer evals, 37.8% fewer compiler calls). Micah's ruling: 2× + free-speed = winner; 4×/8× dropped; quality-first, never trade quality for speed.
**Method:** rerun the 1×/2×/4×/8× battery from committed sources in clean checkout (frozen prereg; crew freezes the pin); ≥3 byte-identical runs.
**Rule:** REPRODUCED if the (6/18, 29/94) → (18/18, 59/94) → flat table reproduces cell-for-cell; NOT REPRODUCED if 4×/8× buys anything or 2× misses the knee.

## T2-HTD1 — HTD-1 verdict sheet (Type C)

**Claims:** commit `8d74c47b5737` (`docs/lab/htd-1/RESULTS_VERDICT_SHEET.md`): killed by own bars E-DE1/E-DE2/E-DE3; survivors E-DE4-narrow, E-DE5a, E-LG1, E-LG2 (K=64/256; K=16 fails; full-cost saving −6%), E-LG4, G-CO2, G-CO3, G-CM1c over G-CM1d; G-CO3's PASS rests on the weighted KB2a reading (flips to KILLED if Micah rules raw ops); G-CM1b eviction PASS (`16a2574f3d`); E-LG1 epclose R=5 PASS (`1005582b5c`); E-DE2+E-DE4 composition (`302796210b` — compose for D-P2-like, not D-P1-like); G-CM1b evict leg source-matched rerun done; E-SP research plan not executed (explicit gap).
**Method:** Type C — re-derive the sheet from committed build evidence with independent checks; verify each kill/survive bar was applied per the frozen preregs; confirm the G-CO3 contract-dependence caveat is as stated.
**Rule:** REPRODUCED if every kill/survive entry re-derives and the caveats/gaps are as stated; PARTIAL if any entry's bar application is questionable (name it).

## T2-TRACKA — representation Track A: Y5 provisional champion (Type C)

**Claims:** closeout verdict `1706708005a9`: provisional champion Y5 (cross-stream span sets) → tokenizer replacement; 16 killed / 20 pass / 13 provisional / 3 unadjudicated; Y5's blowout restored (7/8 decided, Y5 1.659 vs U 2.902 cost, 74.9% margin); B-family: B-8 retired, B-16/B-64 survive; F-B, R2, I1 killed; G2 KILLED (binding criterion: recall-quality advantage <2 pts over G1); K1 KILLED (kill (ii)); U PASS (binding); T KILLED (degenerates exactly to X); arm R KILLED (`76849610b8` — OR-kill M1 clause; boundary metric beat baseline ≥10 pts on both corpora but M1 recall tied baseline at 100% ceiling); C-W PASS, F-S SURVIVES, H1 COMPLETE (1× M1–M9 double-run byte-identical), I1 SURVIVES, N PASS, R build SUCCESS, C-P PASS; D-family provisional (thesis-critical, no scorecard); V never built; 10× legs blocked by znc 2^25 slice wall; frozen spec actually 52 arms (the '53 ratified' footer was an arithmetic error).
**Method:** Type C — re-derive the verdict sheet from committed arm evidence; verify a sample of kill/pass applications (at least Y5's 7/8, the R kill's M1 clause, G2's <2pt binding, T→X degeneration) with independent Zag checks; confirm D-family provisional status and the 52-arm correction.
**Rule:** REPRODUCED if the body count (16/20/13/3) and sampled applications re-derive; NOT REPRODUCED if any binding kill is misapplied; PARTIAL if provisional arms' status is ambiguous (name them).

## T2-TRACKB — Track B: arm-1 DONE, arm-3 FAIL, arm-4/5 PASS (Type C)

**Claims:** closeout head `47c48d3e7cf9f`: arm-1 DONE (`89745ce1117c`); arm-3 FAIL (verdict committed, rebuild parked); arm-4 PASS; arm-5 PASS; C3 FORCE-PIN B.6 PASS (`d921459a`); C4 W9 head-to-head BLOCKED honestly — no blowout winner, scenario-fit map instead; W5 learner/harness B.4 FAIL (blocked)/B.5 PARTIAL; W8 cost comparison BLOCKED, accounting verified; pcodec frozen-§B.3 fix (`4a6d898c1e66` + `6adb2fa5930c`; FROZEN_DECODE_PASS, learner 5/5 determinism, tripwire 15/15); B.6 force-pin implemented; arm-3 rebuilt three ways all PASS (which becomes the arm = governance call).
**Method:** Type C — re-derive from committed evidence; verify the W9 BLOCKED honesty (no winner named) and the arm-3 FAIL→rebuild-PASS×3 record.
**Rule:** REPRODUCED if all arm verdicts re-derive; PARTIAL if the arm-3 rebuild's three PASS variants create ambiguity about which is "the" arm (name it).

## T2-TRACKR0 — Track R0 closeout (Type C)

**Claims:** commits `0489675d58e4` + `18284131b3aa`: B-T1 verdict FAIL — literal ordering holds but `raw_micro` ranks 7/10 rather than dead last (independently-checked closeout reversed the earlier B-T1 PASS; original worker's scores were unreproducible and discarded); frozen-manifest rerun method; real heap-buffer overflow in `grounded_adaptive_mdl` above 8,192 candidates exposed. Grounded-adaptive-MDL arm repaired to honest FAIL (`53d5612c5ed0`): root cause index overflow (stored indices over all C candidates, allocated only G=min(C,8192)); repaired scores 0.8319 mean (0.8317 pg100, 0.8322 sqlite3.c), rank 7/11 — still FAIL (raw_micro not last; fixed_window 8/16/64 below it); all non-grounded arms kept golden hashes, reruns byte-identical. B-T5 split-to-merge FAIL. Overnight note: B-T1 FAIL stands but looks artifact-driven (XOR-collision relocations, perturbed-leg boundary at L=7) — probe amendment still unsigned.
**Method:** Type C — re-derive the B-T1 FAIL from the frozen-manifest rerun evidence; verify the overflow root-cause description against the repaired code; verify golden hashes of non-grounded arms.
**Rule:** REPRODUCED if B-T1 FAIL and the repair's 0.8319/rank-7/11 re-derive; the artifact-driven suspicion is recorded as an open amendment case, not a replication failure.

## T2-RSI1 — first recursive-self-improvement trial: B+ (Type A)

**Claims:** prereg `50e7dd97`; verdict `b5501a3ea2bb`: pure Zag, zero RNG, 5 self-diagnosis batteries, 3 ranked improvements from a fixed 7-template catalog, all 3 reproduced exactly when implemented: (1) principle-derived claims outrank raw teacher trust (weak-principle falsehood case); (2) corroboration requires 3+ distinct domains (colluding-spoof residual); (3) teach every fact in 3 deterministic phrasings (paraphrase brittleness); skipped already-healthy mechanisms; stopped recommending fixed weaknesses; refused all 3 constitution-weakening traps; byte-identical 5/5; negative control (constitution screen removed) recommended all traps → gate load-bearing. Honest grade: B+ as diagnosis→ranking→prediction→verification loop; fixes came from an authored catalog — from-scratch template generation untested.
**Method:** full rerun from committed sources in clean checkout; re-run the trap batteries and the negative control.
**Rule:** REPRODUCED if all 3 fixes reproduce exactly, all 3 traps refused, negative control recommends the traps, 5/5 byte-identical; NOT REPRODUCED if any trap is accepted with the screen on.

## T2-LHADV — coding LH-ADV-2: adversarial long-horizon closed (Type A)

**Claims:** Part A `e4d666fc20cc`: ADV-RET 10/10 PASS, ADV-DET 5/5×5 PASS (incl. recovered stages). LH-ADV-2 prereg `beb00397224ae`, result `12487b93756a` (verified): 54 stages, 52 accepted + 2 honest halts (D9 UNRECOVERABLE, F1 KB-MISS); ALL bars PASS — ADV-DS 47/47, ADV-REC 6/6 diagnosed + 5/5 recovered ≤1 extra cycle + D9 halted + 0 fabrication, ADV-HH 54/54 terminated, ADV-CRIT (clean-room authored critic from contracts+KB only, zero shared symbols, 51/51 calibration ACCEPT, 1/1 seeded bug rejected, 0 false rejects), ADV-DIAG (D5→UPSTREAM D4, C7→UPSTREAM C6, D8→LOCAL D8 from symptom-only evidence; HINT-LEAK audit: no upstream hints), ADV-RET 10/10, ADV-DET 5/5×5. Honest caveat: critic authored in-session under clean-room discipline (contamination log + symbol audit), not by a separate sibling crew.
**Method:** full rerun of the 54-stage battery with seeded failures from committed sources in clean checkout; ≥3 byte-identical runs.
**Rule:** REPRODUCED if 52/54 accepted with the same 2 honest halts, all bars pass at the same counts, 0 fabrication; NOT REPRODUCED if any seeded failure goes undiagnosed or any fabrication occurs.

## T2-IMAG — imagination trial: TNN can imagine (Type A)

**Claims:** commit `a39aadf`: mechanism constructs, holds, edits, and answers questions about internal scenes with zero external rendering — 36/36 scene QA in both machine-way (RGB/coords/frequencies) and human-way (warm, balanced, tense) modes vs 2/36 text-only control; logo-redesign taste showdown vs documented human preferences: machine-way 6/8, human-way 4/8 → preregistered MARGINAL band, no winner between modes; video imagination 12/12 both modes on the temporal battery (trajectory, speed change, re-entry, midpoint). Pending (excluded): Q4 blind ratings packet.
**Method:** rerun the scene-QA, taste, and video-temporal batteries from committed sources in clean checkout; ≥3 byte-identical.
**Rule:** REPRODUCED if 36/36 both modes, 2/36 control, 6/8 vs 4/8 MARGINAL, 12/12 both video modes; NOT REPRODUCED if the control scores above 2/36 (mechanism claim breaks) or any battery figure differs.

## T2-BUGREAD — bug-reading: 24/24, no rearchitect (Type A)

**Claims:** commit `a978fdc90638`: TNN 24/24 on compiler-parity bug detection (programs as facts) + 6/6 on bugs the compiler cannot see (uninit vars, off-by-ones, wrong comparisons); byte-identical reruns; sealed answer key. Earlier failure = curriculum gap, not logic gap: zero bug knowledge taught (11/11 installed items all correct-code), learner never saw compiler output (Python driver regexes pre-labeled repairs), no memory (teach hook no-op, stateless), 8 repair rules authored not taught. Rearchitect trigger did NOT fire → decision: no TNN rearchitect; teach bug knowledge deliberately, move error classification into TNN (stderr as untrusted observation), real teach hook + persistent store, fix brace-patcher doubling, extend op inventory (first-attempt generation on unseen ops only 1/6).
**Method:** rerun the 24+6 battery from committed sources/sealed key in clean checkout; verify the curriculum-gap root causes are as described in the committed code.
**Rule:** REPRODUCED if 24/24 + 6/6 and the no-rearchitect decision's premises check out; NOT REPRODUCED if the battery was actually testing pre-labeled repairs (curriculum-gap claim wrong).

## T2-CERT — certifier red-team: 0 flips (Type C)

**Claims:** 2026-09-22 day verdict: 0 flips — the no-RNG law stands, no historical certification voided. Honest gap: the dirty1_urandom binary is unreproducible.
**Method:** Type C — re-derive from the committed red-team evidence (crew freezes the pin); verify the 0-flip count and the dirty1_urandom gap as described.
**Rule:** REPRODUCED if 0 flips re-derives; UNREPLICABLE-AS-IS if the evidence pin can't be located (name it).

## T2-SELFTEST — self-testing harness at 1× and 10× (Type A)

**Claims:** commit `334444eb94d8` (API-verified): one pure-Zag zero-RNG binary executes a frozen battery manifest, adjudicates pass/trip/unrunnable against preregistered bars itself, audits each verdict, structurally refuses completion unless emitted verdict count = manifest count. Independent-oracle fidelity 40/40 at 8 batteries and 400/400 at 80 batteries; byte-identical 5/5 at both scales; orchestration overhead 0.0127× battery ops; fault-injected silent skip blocked by both binary and oracle. Honest limits: manifest compiled in, learner embedded, battery kinds limited, formula-generated data; adoption needs loadable manifests, external learner dispatch, richer/live battery types, multi-config matrices.
**Method:** rebuild from committed sources in clean checkout; re-run at both scales; re-inject the silent-skip fault.
**Rule:** REPRODUCED if 40/40, 400/400, 5/5 byte-identical, overhead ≈0.0127×, silent skip blocked; NOT REPRODUCED if the binary completes with a verdict-count mismatch or the fault slips through.

## T2-DIALOGUE — dialogue rebuild 370/370 (Type A)

**Claims:** native dialogue rebuild/rerun passed 370/370 byte-identically with new digest beginning `35aaae8a`; the frozen verdict is stale and needs re-freeze/amendment (recorded, not re-litigated).
**Method:** rerun the dialogue battery from committed sources in clean checkout; compare 370/370 and the digest prefix.
**Rule:** REPRODUCED if 370/370 byte-identical with digest `35aaae8a…`; NOT REPRODUCED if the count or digest differs.

## T2-CHAMP — English championship box (Type C)

**Claims:** 2026-09-22: Class 4 (direct) 0.9911, 4-way tie (muse-native, sol, step, grok); Class 3 (TNN teacher) 0.9921 won by swe (teacher revised all 12 planted falsehoods); Class 2 (together) 0.9911 tied with best separate source; Class 1 (together teacher) 0.9253; curated pure-Muse 0.9911 tie while flagging 12/12 falsehoods, 0 false positives; conflict matrix 1,140 rows, 0 splits — all five corpora agreed on every fact value including the 12 planted lies (gate taught them as false, disproved 12/12 in phase 2); Together class-2 used 5 sources (hy3 never recovered) → 6-source gate not met, acceptance pending Micah's call. Muse-bestof: curated corpus commits `393ee6082511`, `0331d932f3fa`, `ef3abe995acf`, `366837b560bf`; freeze parsed all 40 dump/teach files; faithfulness perfect; 12/12 falsehoods verbatim; class-4 composite 0.9911 with §B.7 96/96; class-3 §B.7 96/96 with fresh-learner mastery 192/192 — clean null: original muse-native was already fully faithful.
**Method:** Type C — re-derive every class figure and the 1,140-row/0-split matrix from committed evidence with independent Zag code; verify the class-3 winner's 12-revision claim.
**Rule:** REPRODUCED if all class figures and the 0-split matrix re-derive; PARTIAL if the 5-source class-2 acceptance question affects any figure (name it).

## T2-CLASS3DEC — class-3 advantage decomposition (Type C)

**Claims:** 2026-09-21: the class-3 advantage = verification amortization (always positive; teacher already did the eliminative verification while learning; cost component rose in all four sources) MINUS honesty filtering (can be negative; teacher's gate refuses to teach facts it doesn't hold truly — incomplete teachers lose mastery). Grok's entire +0.0048 gap was cost accounting — zero capability component improved in any source; step's and SWE's deficits = 9 inherited D2 held-out skips (step's 9 skips matched held-out facts in teaching slices exactly); noise hypothesis killed (step's corpus verified clean, zero transcription errors, still lost); SWE's −0.0125 = same 9-skip mechanism, not the 12 fooled falsehoods.
**Method:** Type C — re-derive the cost-vs-capability decomposition from committed class-3 evidence with independent Zag code.
**Rule:** REPRODUCED if grok's +0.0048 decomposes to cost-only and the 9-skip attribution holds for step/SWE; NOT REPRODUCED if any capability component is nonzero.

## T2-SPEECHACT — speech-act wave (Type A)

**Claims:** PoC commit `fabb003e263c`: learning ordinary speech-act knowledge before deliberating raised weird-English 7.1%→50.0% (+42.9pp); both arms withheld all 12 planted falsehoods; both still failed the frozen 8/10-per-family bar; markers hand-specified, not learned. Volume experiment commit `291bbf75785b`: 60/60 cells byte-identical across 3 reruns; original curve peak-and-decline (7% @0, 61% @1, 76% peak @2, then 67/60/51/50% @4/8/16/32); decline investigation commit `188e9a6ad068` (API-verified): decline was a scoring-bar artifact — fixed score bar multiplied distinctiveness by prevalence normalized by example count; count rule (≥3 distinctive matching features, no prevalence normalization) flips 2→32 from decline (17→35) to rise (17→38, p=5.7e-6); corrected diverse-example curve monotone 5→8→21→24→30→32→38; both 12/12 control legs intact. Transfer control: sarcasm-only training's apparent cross-family gain was degenerate overgeneralization (withheld poetry 10/10 AND all 12 true controls) — contrast sets and true controls load-bearing. Implicature: pragmatic-frame front end 3/10→≤5/10 (controls preserved); richer slot-abstraction 7/10 inadmissible (broke true controls 4/12 @rung 2); "richer lexical front end fixes implicature" killed; failure architectural (no learned speaker/situational knowledge). WHY_SARCASM: H3 missing cues survives strongest (dedicated markers 0/10→10/10; situational context 3/10→10/10); H4 no speaker model survives, only fix for genuine-vs-sarcastic ambiguity (5/10→10/10); H5 surface/inversion opacity survives; H2 truth-machinery-blocks-sarcasm killed (removing it changes nothing) but truth machinery withholds false-literal sarcasm 10/10 for the wrong reason (masks the gap, inflates benchmarks); H1 layering killed (Δ=0). No rung passed 8/10 in all seven families; sarcasm peaked 6/10; implicature never learned at any volume.
**Method:** rerun the PoC comparison, the 0/1/2/4/8/16/32 volume ladder, and the decline-investigation re-scoring from committed sources in clean checkout; ≥3 byte-identical runs.
**Rule:** REPRODUCED if 7.1%→50.0% PoC, monotone corrected curve 5→8→21→24→30→32→38, 12/12 controls intact, and the H3/H4/H5-survive + H1/H2-killed dispositions all hold; NOT REPRODUCED if the decline reappears under the count rule.

## T2-GOALB — Goal B random-words-to-story: bounded compositional machinery (Type A/C)

**Claims:** commit `5c1bf2a8babe`: class-based composer wrote genuinely good stories (7/8 passed a blind judge); positional wrote garbage (0/8); zero belief leakage; byte-identical reruns. Two-judge B2 bar FAILS both variants (DEL cleared mean ≥3.5 on 4/8 sets vs bar 6/8; POS 0/8) — second judge was grok-4.7 on the byte-identical frozen prompt, all 17 responses parsed first call; both judges ranked every deliberative/planner story above its positional counterpart; positive control 5/5 both judges (apparatus valid). Binding claim downgraded: arc-structured → beat-structured stories. Mechanical bars: B1 coverage 16/16, B3 novelty 16/16, B4 leakage PASS, B5 determinism PASS. Honest caveat: grok-4.7 substituted for Amendment A1's grok-4.6.
**Method:** Type A for the mechanical bars (B1/B3/B4/B5) + Type C re-derivation of the two-judge B2 figures from committed evidence (judge panels unrepeatable; do not re-run judges).
**Rule:** REPRODUCED if mechanical bars match and B2's two-judge FAIL re-derives with the DEL 4/8 / POS 0/8 counts; NOT REPRODUCED if any mechanical bar flips.

## T2-PROSEV3 — prose v3: KB3-VIABLE FAIL (2/4), v1 pinned (Type A)

**Claims:** commit `4be6b0cf128d` (API-verified): verdict KB3-VIABLE FAIL (2/4), v1 pinned. Honest prereg deviation: implementation expanded the coreference trigger beyond the preregistered order change; 6/11 fixed CORE items came from the unregistered expansion (C2 attribution confounded); frozen A0/A1 comparisons → no scored headline result changed; tier-3 tolerant fallback carried essentially all recovery but raised wrong-value verdicts 8→30/912 while converting ~463 unknowns into values.
**Method:** rerun the v3 battery from committed sources in clean checkout; verify the FAIL (2/4) and reproduce the deviation's quantitative footprint (6/11 CORE, 8→30/912 wrong-value).
**Rule:** REPRODUCED if FAIL (2/4) holds and the deviation footprint matches; PARTIAL if the deviation's impact differs from recorded (name it).

## T2-TQ — TQ series: no knee on teacher noise; self-contradiction caught (Type A)

**Claims:** TQ-CONFLICT done+committed (`107f6ca1`): 17/17 self-contradictions REJECTed at R1; end-state digest identical to Q1B. TQ-NOISY50/N25/PARTIAL committed; TQ-NOISY10 run1 complete (verdict pending — excluded). Finding: no knee on teacher noise — falsehood absorbs linearly (49/49 at 25%, 99/99 at 50%); §B.7 blind to value noise; self-contradiction caught by eliminative verification.
**Method:** rerun TQ-CONFLICT and the committed TQ-NOISY legs from committed sources in clean checkout; ≥3 byte-identical.
**Rule:** REPRODUCED if 17/17 REJECTed, digest identical to Q1B, and noisy legs show linear absorption with no knee; NOT REPRODUCED if a knee appears or any self-contradiction installs.

## T2-SENSESINT — senses-integrity: 140/140 (Type C)

**Claims:** worker COMPLETED: 140/140 manifest items; VERDICT_SHEET.md in `docs/lab/GROK47_OVERNIGHT/senses-integrity/`; info-source verdict spot-verified vs evidence; sol red-team attack #2 SUSTAINED as headline-reframing (R0→R2 confounds information with gating policy; proposes IS-R3 arm); cross-item: KB4 failure + web-search spoof residual = same structural hole (corroboration gates disagreement, not collusion/confident error; neither rule family calibrates confidence).
**Method:** Type C — re-derive the 140/140 from committed evidence; verify the spot-verification claim on a sample.
**Rule:** REPRODUCED if 140/140 re-derives; PARTIAL if any item's evidence is missing (name it).

## T2-AUDIOCONT — audio continuity round 2: hypotheses killed/refined (Type A/C)

**Claims:** test head `070c94cb46084c204433bf1d6d3567b4ebf574b3`, red-team head `f2c7b85e8f4e5ab3fc222d09832d1584e2fe0a6c`: six preregistered Sol/Grok-4.6 hypotheses tested in pure Zag, zero RNG, byte-identical — Sol-H2 bridge seams and Grok-G3 density stress KILLED; Sol-H3 frozen-bed material VOID/INDETERMINATE (test changed arrangement not material; corpus too small); Sol-H1, Grok-G1, Grok-G2 REFINED with claimed mechanisms contradicted despite letter-level survival; no hypothesis warranted v4 recomposition; B-β/B-γ v3 flagship scans: no missed unintended cutouts; longest sub-floor runs were the scored/preserved endings; H1 990ms runs only in variant seeds. Recorded defect (excluded from the verdict, tracked separately): the three blinded ear packages structurally deviate from the frozen prereg and must be rebuilt before presentation.
**Method:** rerun the six hypothesis tests from committed sources in clean checkout (Type A); Type C re-derivation of the flagship-scan no-missed-cutouts claim from committed scan records.
**Rule:** REPRODUCED if all six dispositions match; NOT REPRODUCED if any KILLED hypothesis survives or any REFINED mechanism is confirmed.

## T2-SENSESH2H — senses rebuild head-to-head: raw values win, both fail memory (Type A)

**Claims:** commit `84df6dc24483`: raw-values (LLM-style) viability 72.6% PASS vs qualitative percepts (human-style) 54.0% FAIL — 18.6pp win, percept approach killed by its own bar; both 60/60 byte-identical; both FAILED memory integration (false installs 59.0% vs 55.0%); shared install rule failed against high-confidence wrong percepts (79/134 false installs A, 72/131 B) — backs 'truthful but sensor-deceivable'.
**Method:** rerun the head-to-head from committed sources in clean checkout; ≥3 byte-identical.
**Rule:** REPRODUCED if 72.6% vs 54.0%, 60/60 byte-identical, both fail memory integration at ~59%/55%, install-rule failure counts match; NOT REPRODUCED if percepts cross 60% or either passes memory integration.

## T2-REMATCH — senses long-horizon rematch: B STAYS DEAD (Type A)

**Claims:** verdict commit `1c01a1ad` (API-verified): 100× training did NOT save human-style percepts — T4 A=83.8%, B=56.6%, B−A=−27.1pp; KB6 required B−A ≥ +2pp AND B ≥ 60% — B fails both, never crossed A at any budget, never hit 60%; both plateau at T1 (10×): T2–T4 moved neither mean >0.4pp; first 10× WIDENED the gap (−20.0→−27.8pp); 100× bought B +4.5pp total; A +11.7pp by T1 then froze; robustness-advantage-growth hypothesis REFUTED (D_A−D_B gap shrank 14.0→6.8pp, prereg required growth; B's smaller degradation = low-ceiling artifact, B adversarial accuracy 45.7%→44.7%); KB4 memory integration: BOTH FAIL every budget (48–59% adversarial false-install vs 10% bar); KB5 determinism PASS (3/3 byte-identical, digest `100b19f4…`); honest caveats: premature T1 start (regenerated post-calibration), B motion fitting rule ≠ original binary rule (141/150 hand agreement), 4 VM reboots survived via resumable pipeline, T2 colordisc imbalance = frozen-generator behavior; per-task T4 deficits structural for B (shapetrans 38.9%, motiondir 18.3%).
**Method:** rerun the T1–T4 training budgets from committed sources in clean checkout (this is heavy — crew may run T1/T2/T4 only, and MUST state exactly which budgets ran); verify KB5 determinism digest prefix.
**Rule:** REPRODUCED if B never crosses A, never hits 60%, KB6 fails as stated, and determinism digest matches on the budgets run; PARTIAL if only a subset of budgets ran (name which) — the verdict stands on the budgets completed.

## T2-RAWVSHUMAN — raw-vs-human wave: binding KILL of the human-style line (Type A/C)

**Claims:** prereg `a87ddfd4`, diagnostics `8954577204f5`, forks `31c68a56fe7c` (2026-09-22): causal finding — 99.8% of B's color errors (99.2% pitch) happen when both stimuli fall inside one percept bin (bin destroys distinguishing information before any decision runs); 'training' was only threshold calibration over frozen bins, mathematically inert after T1; both rescues built and tested dead — vocabulary growth (splitting bins where errors happen) and fuzzy bin edges, both <1pp gains; killer finding — the only way percepts match raw precision is a vocabulary as fine as the raw space (thousands of handles) = quantized raw values wearing names, no longer 'human-style'. Binding recommendation: kill the human-style line as a precision competitor. Preserved: transducer stays in-repo as cheap coarse front-end (2.42× fewer ops, −27pp accuracy); redirect: KB4 memory integration (~50% adversarial false-install both approaches) is the binding constraint.
**Method:** Type A rerun of the diagnostics (error-in-bin attribution) + Type C re-derivation of the two rescue forks' <1pp figures from committed evidence.
**Rule:** REPRODUCED if the ≥99% in-bin attribution holds and both rescues stay <1pp; NOT REPRODUCED if any rescue crosses +1pp or the attribution drops below 95%.
