# worker_06 log — chunk_06 sweep (50 rows, all md)
Date: 2026-09-22. Worker: cb4ba97b label. All rows are design/prereg documents (no trial results yet anywhere in this chunk) — verdicts are reviews against standing known outcomes; no kill bar fires because no results exist to evaluate. No zag/jsonl/py rows in this chunk, so no compile checks or parses were needed. No grok-4.7 calls made (native review sufficed).

## Ground-truth anchors verified by the worker
- `wave10/rc3/RESULTS_RC3.md` exists: "Verdict: PASS — 40/40 preregistered checks, byte-identical reruns, zero RNG" at 100x, dated 2026-09-20. Citations of "RC3 at 100x" across the chunk are grounded.
- Audit entry layout per committed convention (AGENTS.md): 16 words, byte offsets op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60 → 64 bytes (4-byte words).

## FINDINGS (cross-file, significant)

### F1. Audit entry size: 3-way inconsistency (touches P0 row t6/04)
- t4/20-cost-schedule §3: "Audit entry = 16 words = 64 bytes" — consistent with the byte-offset layout.
- t6/04-ledger-scaling §3: "**16 i64 words = 128 bytes/entry**" — self-inconsistent: it cites the same byte-offset layout (d2@60), which implies 4-byte words / 64 bytes. The 128-byte figure exists to make its chunk math exact (2^18 × 128 = 2^25 bytes per chunk).
- t6/09-failure-modes §3 F1: "~70 bytes/entry".
- Impact: t4/20's 10x budget math (1 KiB/ep nominal, 4 KiB cap) and t6/04's K8 ≤1.10x bar and chunk-capacity claims disagree by 2x on the base unit. One of the two P0-affected docs (t4/20 or t6/04) needs a dated amendment fixing entry size; the AGENTS.md-committed layout supports 64 bytes. Flagged for coordinator, not unilaterally fixed.

### F2. Track 5 arms have no shared domain spec (touches P0 row t5/15)
- t5/02 (learned-only): test domain = Zag code curriculum C1–C12.
- t5/03 (planted-only): test domain = fictional Zharovia, 240 facts.
- t5/05 (comparison protocol): D1–D4 domains (60-fact corpus, observational inference, deliberate judgment, traps).
- t5/15 §3 claims arms "fixed per slices 02/03/14: A = planted-only (learn-gate, Zharovia domain...); B = learned-only (identical domain spec...)". This is false across slices: 02 and 03 name different domains, so "identical domain spec" does not hold. The three-way comparison (slice 05) uses yet a third domain set. Track 5 cannot run its comparison until one domain spec is frozen for all arms — needs Micah-visible dated amendment (prereg change).

### F3. t5/03 Zharovia conflicts with standing no-toy-tests directive
- Micah's standing directive (2026-09-21): flagship evaluations use real data (real English like Gutenberg), not synthetic Zharovia facts.
- t5/03's entire planted-only arm is synthetic Zharovia facts; t5/15's framework inherits Zharovia. Undated docs — may predate the directive. Needs re-scoping to a real-data domain or an explicit Micah carve-out; otherwise the arm design is stale.

### F4. t7/01-pam-archaeology is STALE vs the 2026-09-20 verdict
- Standing memory: perceptual origins and trace-op semantics proven unrecoverable; pre-git session-file hunt CANCELLED; Micah will upload the TNN folder to Drive himself and the folder must not be touched until he gives the word.
- t7/01's falsifiable claim ("at least one complete, recoverable PAM vision or hearing design exists in the searchable locations") directly contradicts the unrecoverability verdict. L4 ("request Micah to locate and point us at the session files") conflicts with both the cancelled hunt and the hands-off-Drive order.
- Verdict: do not run L1–L5 as written; the doc needs re-scoping (or stands as historical record of the pre-verdict plan). At minimum the "recoverable design exists" claim must be struck.

### F5. Minor notes
- t4/07-code-debugging: cites "proven 40/40 at 1x/10x/100x" — grounded (RC1/RC2/RC3 chain, RC3 verified). But it references `docs/lab/waveN/` as a literal path — placeholder, sloppy.
- t6/09-failure-modes: "slice 17 replay protocol" cross-reference is unresolvable within t6 (slices 01–10); likely refers to another track's slice 17. Needs a qualified path.
- t6/10-trial-prereg L2 entry gate: "Micah signs this prereg" — pending; consistent with the known blocked status of the 1000x program. No conflict.
- t5/15-verdict-framework: weights 30/25/25/10/10 match the pending sign-off in standing memory; doc itself demands Micah's sign-off before any Track 5 trial — still blocked, consistent. Note F2/F3 apply to the framework's domain assumption.

## Per-file notes (condensed)
- t3/10: 20-plant blind red-team design vs slice-09 audit; prereg bars (kill on ≥1 escape, 0 false positives on 5 clean builds); honestly notes replay is blind to 11/20 plants and that plants are adversarial-by-construction. Design-only.
- t3/11: attack design A1–A5 vs slice-22 render gate; kill bars K-RT1..K-RT4; strongest claim is A1 (load/budget upstream of the gate). Design-only.
- t3/12: cross-arm attack surface Arm B (fenced RNG) vs Arm C (deterministic). Fenced RNG is consistent with AMENDMENT_2026-09-20_RNG_ARM_B (Arm B excluded from canonical legs, used as comparison). Flags K7 amendment question for Micah. Design-only.
- t3/13: trainer-manipulation experiment (Cohen's h≥0.30, p<0.01, n≥400 paired, 2 trainers incl. Micah surrogate); presentation firewall + force-pin floor rule. Design-only.
- t3/14: composition exploits A/B/C vs slice-23; scope firewall held in all constructions (only expression-choice degrades); strengthened bars K3'/K4'/KB proposed. Design-only.
- t3/15: S0–S3 taxonomy + aggregation + disagreement rules; calibration drill proposed. Design-only.
- t4/01: C1–C12 code curriculum, 3,950 eps; bars cite committed results only; next step is generator+instrument build. Design-only.
- t4/02: E1–E6 English curriculum; zero-drift bar (100/100 re-parse); "felt intensity is dead (law 9)" consistent. Design-only.
- t4/03: 5-class MRC; falsifiable via >15pt gap vs machinery-only control. Design-only.
- t4/04: phasing consistent with MA2 verdict (phases gate write-scope, never restraint). Design-only.
- t4/06: E0–E3 elimination teaching; cites MA4 18/18 (matches known); SPACE-WRONG gaming risk flagged. Design-only.
- t4/07: DBG-1..DBG-7; zero-repair-by-weakening tolerance; see F5. Design-only.
- t4/08: ASK/INSTRUCT/PLANT/DECEIVE/META + principal tags; resolves TRAP_UPGRADE §8 gap #4; K3 gate-invariance bar. Design-only.
- t4/09: CUR-R4 protocol; 120-episode battery (40/40/40); tiers budget, never decide. Design-only.
- t4/10: noise/incompleteness ladders; carries the 2026-09-20 LH-5 LCG contamination notice — remediation honored, cites quarantined numbers with the notice attached. Good practice.
- t4/11: seven controls C1–C7, each with its own positive control; battery-death rule (<6/7 firing controls kills the battery). Bars match sibling slices. Design-only.
- t4/12: GAP + TEACH organs; deliberate only, zero RNG; Track 5 planting-firewall link. Design-only.
- t4/13: 5-stage comprehension; self-application milestone (ma_kill/ma_pin/ma_unpin/ma_promote) on real committed substrate. Design-only.
- t4/14: composition teaching; Goodhart prevented by architecture; K1–K7; audience-model carryover kill bar K6. Design-only.
- t4/15: shift detection via violation register + quarantine/commit; cites 35/35 corroborated-elimination and 22/22 debate — both match known outcomes. Design-only.
- t4/16: interference via ledger kill-signatures; kill on silent erosion; honest "kill by neglect" gap admitted (RC3 100x path-level decay). Design-only.
- t4/17: integer-pair discipline, zero floats/RNG in decision paths (K1–K5); overflow risk honestly flagged. Design-only.
- t4/18: disconnect test + poison defense; sensor-hole honestly carried over. Design-only.
- t4/19: five-organ 10x integration trial; I1–I5 checkpoint gating; 1x pilot before 10x. Design-only.
- t4/20: cost/schedule; see F1. Next step (measured entries/ep histogram) is the right first move. Design-only.
- t5/01: prov=PLANTED header + OP_PLANT op; cites AGENTS.md layout correctly; kill-by-evidence path. Design-only.
- t5/02: learned-only baseline; see F2. Budget consistent with t4/01 (3,950). Design-only.
- t5/03: planted-only arm; see F2, F3. Design-only.
- t5/04: hybrid arm; Tier C/S division, corroborate/on_contradiction; anti-circularity. Design-only.
- t5/05: n=12, exact paired permutation tests (deterministic, no RNG); integrity gate 0.995; blinding audit. Design-only.
- t5/06: G1–G3 evidence ladder; concept-level kill bars K1–K5; suspend-abuse clause. Design-only.
- t5/07: sealed provenance + promotion rule; K1–K4; cache-verdict warning. Design-only.
- t5/08: L0/L1/L2 ladder, L3 force-pin separate human-only; 200/200 kill bar. Design-only.
- t5/09: indep_ratio monitor; vicious-cycle <5%; probe-cost bar (e). Design-only.
- t5/10: learned-only-extreme steelman; Munchausen concession on criterion; MA2 replayed as epistemic claim. Design-only.
- t5/11: planted-extreme steelman; bounded-domain home turf; 95% novelty-suspension bar. Design-only.
- t5/12: predicts L>=H>P; integrity as disqualifying gate; N/A-family exclusion honest. Design-only.
- t5/13: constitutional planting; RC1 line (TNN 0% of constitution); petition path social-engineering surface honestly flagged. Design-only.
- t5/14: kb_unplant + refusal guard; 50/50 decisiveness probes; chunked trace-search caveat. Design-only.
- t5/15: verdict framework; weights match pending sign-off; see F2, F3, F5.
- t6/01: scale ladder 1x→1000x; capacity/behavior distinguisher; one-amendment-per-leg guardrail; RC3 §§87/155 cites (dir verified). Design-only.
- t6/02: 12k-episode duration trial; OLS slope + floor kill bars; checkpoint-restart protocol. Design-only.
- t6/04: chunked ledger; see F1. Kill bars K1–K4; crash-during-seal honestly flagged. Design-only.
- t6/05: deliberation scaling; B=4|H|²; fallback as logged terminator; demand-ladder validity flagged as weakest point. Design-only.
- t6/06: integrity at scale; 2,595-temptation precedent matches known; S1000 99% bar justified; novelty-generation pass. Design-only.
- t6/07: variation at scale; H-entropy probe before judging D; salience-cap saturation as likeliest degeneracy. Dated 2026-09-20. Design-only.
- t6/08: curriculum at 1000x; control-saturation retirement rule (C6 thinness at 60k eps); 100x leg must pass first. Design-only.
- t6/09: F1–F6 pre-mortem; see F1 (entry size) and F5 (slice-17 ref). Completeness-falsifiable kill bar. Design-only.
- t6/10: binding 1000x prereg; program-kill vs leg-kill table; Micah sign-off block pending — consistent with blocked status. Design-only.
- t7/01: PAM archaeology; see F4 — STALE.

## Kill bars applied
None fire: every row in this chunk is a pre-trial design/prereg with no results recorded. All preregistered bars are intact and awaiting runs. No design in this chunk reports a fired kill condition.

## Rows not evaluable
None — all 50 rows read in full and reviewed. No exact duplicates of committed files detected (all are original wave11 design docs). No randomness concerns (no code rows). No znc miscompile patterns to check (no zag rows).
