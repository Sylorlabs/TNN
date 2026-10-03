# RED-TEAM REVIEW: ARENA5 DEFRECALL BUILD-PASS (wave-20261001-2321pdt, lane RT-ARENA5)

Reviewer: independent red-team worker (RT-ARENA5). Every BUILD-PASS candidate gets a second opinion; this is that second opinion.

## Verdict: QUALIFY

The BUILD-PASS stands. All 8 frozen kill bars hold as frozen, and I independently reproduced the load-bearing evidence from the committed sources. The pass carries one named qualification: on the sealed battery the generic default action is extensionally equivalent to a listnames handler (the C15 probe is the only bare-prompt test item among the 68), so the generality claim rests on intensional audit plus dev-probe demonstration (both of which I reproduced), not on sealed-battery discrimination. The qualification does not overturn any bar; it bounds what the battery can discriminate.

## Attack axis 1: Weakened bars (prereg vs SEALED_EVAL, verbatim comparison)

Compared every bar in SEALED_EVAL.md against PREREG_DEFRECALL.md plus Amendment 1. No bar moved after freezing.

- K1 (C15 >= 0.900 on the fresh 68-item battery, all 3 runs): prereg bar verbatim; eval reports 0.947 on all three runs. No move. The honest 0.947 ceiling is independently confirmed: in the committed turns.jsonl, exactly 9 of 10 fresh entity names occur in expo turn events (2-4 occurrences each); Momado (index 9) occurs 0 times in expo events and only in C8 test questions. Set F1 with the 10-name key: 2000*9/(10+9) = 947.
- K2 (per-capability scores byte-identical to the v6 baseline on the SAME fresh battery): verbatim; eval table shows all 15 non-target capabilities identical. I verified the baseline actually ran on the fresh world: v6base/replies.jsonl answers item 0 ("fact|Nurada|color", a fresh-world entity name) with "amber". The stale "seed 71503461337030" label in results.txt headers is cosmetic (arena scorer label); the runs are on the fresh battery. Note carried below.
- K3 (3/3 byte-identical stripped reply streams, ms and rss_kb excluded; byte-identical defrecall traces): verbatim. I recomputed from the committed files: stripped.txt sha256 7dbf163ed6523ad0f22b7d00a14033843022933908a8ed6d8395fb3dceeb49b9 all three runs; roster_trace.txt sha256 a8b9f675dac241db8636b9f89108bacf470b23b427a2258ccfba272e78f6267a all three. Both match SEALED_EVAL exactly.
- K4 (pure Zag; which python3 prints nothing at lane start and end): verbatim. Lane NAMECHECK records both checks; my own builds in this review used only the pinned znc. No contrary evidence.
- K5 (sealed validity): verbatim, including the Amendment 1 seed-selection procedure. Independently verified: (a) my rebuild of arena.zag from the frozen source yields sha256 3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076, matching the refreeze record; (b) the world_gen variant differs from the frozen source by exactly one line (line 265, seed literal); (c) committed turns.jsonl and answer_key.json hashes match the pre-run recorded hashes (cfe8f5a13... and 12acb1e5...); (d) file-access audit by code inspection: read_file call sites are /proc/self/status, the turn file, own state.bin, own roster_trace.txt; worlddir is arg-presence-checked only (never opened); (e) grep audit: zero hits for all 10 fresh entity names in the mechanism source.
- K6 (ablation DEFRECALL_ROSTER_OFF: three roster_touch call sites disabled; C15 = 0.000; others unchanged): verbatim. The committed defrecall_abla.zag diff against the implementation is exactly the three call sites commented out (surgical 3-line delta). Committed runabla/results.txt: C15 = 0.000, total 54/68 = 0.794, every other capability byte-identical to the v6 fresh baseline. The C15 reply in runabla is UNKNOWN.
- K7 (architecture: diff v6 vs defrecall; 0 new modes/bridges/routers/gates/semantic cases; ZERO dedicated goal handlers; grep listnames = 0): verbatim. Independently verified: diff shows 174 lines added, 0 removed, 0 changed (removed-line count is 0, so no disguised modifications). Keyword scan of added lines for mode/bridge/router/gate: zero hits. grep "listnames" in the mechanism source: zero hits.
- K8 (no L3 claim; explicit Criterion 0 disclaimer): verbatim; disclaimer present in SEALED_EVAL. No L3 claim is made anywhere in the lane docs.
- Supplementary 7.8 (default action disabled, roster enabled; expected C15 = 0.000; not a kill bar): the committed defrecall_nodef.zag diff is a single line forcing the default condition false; committed runnodef results show C15 = 0.000. Holds.

## Attack axis 2: Commit-order self-check

- b63f80289 (prereg freeze): 2026-10-02 07:11:30 UTC. Contains PREREG_DEFRECALL.md and NAMECHECK.md only from this lane (it also swept in two BATTERY-E4 files staged by a concurrent worker in the shared index; disclosed by the lane; no implementation content). No implementation.
- f3320caf8 (Amendment 1): 07:19:23 UTC. Exactly one file (PREREG_DEFRECALL_AMEND1.md), committed alone, before any battery generation or implementation build.
- 2320c3454 (implementation): 07:19:31 UTC. Exactly one file (defrecall_contestant.zag). This is the first commit in which any DEFRECALL source appears.
- 6582398e9 (sealed evaluation + judge brief): 07:23:54 UTC.
- Ordering is strict: b63f80289 < f3320caf8 < 2320c3454 < 6582398e9. Prereg strictly precedes implementation. No implementation file predates the freeze. ORDERING VERIFIABLE. The accidental BATTERY-E4 files in the prereg commit are a shared-index hygiene blemish, not an ordering violation.

## Attack axis 3: The "zero goal handlers" claim and the extensional-equivalence caveat

Code inspection of the committed implementation (extracted via git show from 2320c3454):

- grep "listnames": zero hits. grep for all 10 fresh sealed entity names: zero hits.
- The default action (lines ~1253-1284) fires iff: known==0 (head not in the six existing handler heads fact, fact2, hop2, conflict, zemprod, zemclass) AND the prompt is bare (p1, p2, p3 all empty, i.e. no "|" parameters) AND the roster is non-empty. It then enumerates the roster comma-joined. `ans` is initialized to UNKNOWN, so an empty roster leaves UNKNOWN with no trace line. No question string or goal string is referenced anywhere in the trigger.
- The `known` flag mirrors the existing v6 dispatch heads only; it encodes no new question semantics (K-C0A holds).

Independent adversarial probes (my own build from the committed source, sha256 3d629deda888c18d19ff95ce9819829f2c268cf8e459330b7c573c3892cd57d7, byte-identical to the committed sealed binary; fresh entities Aaaa, Bbbb, never in any battery; /tmp only):

- Bare "recall" -> "Aaaa,Bbbb" (roster deduped: Aaaa exposed twice, appears once)
- Bare "summarize" -> "Aaaa,Bbbb" (novel bare prompt, fires)
- Bare "x" -> "Aaaa,Bbbb" (meaningless bare prompt fires: the trigger is content-blind)
- Bare "what are you" -> "Aaaa,Bbbb" (multiword bare prompt fires)
- Bare "listnames" -> "Aaaa,Bbbb"
- Bare "fact" (known head, empty params) -> UNKNOWN (dispatch-miss is required, not just bareness)
- Parameterized "foo|bar" -> UNKNOWN (abstention preserved)
- Empty roster + bare "listnames" -> UNKNOWN, no trace line, no hallucination

The trigger is exactly the structural condition in the source, and it is genuinely general: it fires for any bare prompt including content-free ones ("x"), which a renamed listnames handler keyed on the goal string could not do without an enumerated synonym list, and the source contains zero such strings. There is no hidden structural trigger beyond "bare prompt plus dispatch miss plus non-empty roster".

The qualification: on the sealed battery, exactly ONE test item is a bare prompt (the C15 "listnames" probe; verified: 1 of 68). So extensionally, on this battery, the default action is equivalent to a listnames handler. The lane states this honestly in JUDGE_BRIEF ("Honest limitation") and SEALED_EVAL. The generality evidence is therefore intensional (zero goal-string branches, content-blind trigger) plus the dev-probe demonstration (prereg 7.4, which I reproduced independently above), not sealed-battery discrimination. This is the named qualification on the verdict. A future battery with several diverse bare prompts across capabilities would be needed to discriminate extensionally.

## Attack axis 4: The Amendment 1 seed change

- The amendment's causal story is independently verified: I built a world_gen variant with seed 71503461337031 and ran it; it aborts with exit code 2 and "DSL EXHAUSTION FAILED: old language expresses transform", exactly as claimed. The check exists at line 399 of the frozen world_gen.zag.
- The amended selection procedure (candidates 71503461337031, 71503461337032, ... in increasing order; first valid battery taken) is deterministic and was followed: 2 candidates tried, first valid taken, recorded in SEALED_EVAL and NAMECHECK. No other selection criterion.
- The change cannot bias C15: the DSL-exhaustion check concerns only the random Zem transform (capabilities 10, 12, 16). The C15 exposure pattern is structural and seed-independent (entity indices 0-8 appear in expo events; index 9 never does; verified in the frozen world_gen.zag source comments for f/k events and empirically on the sealed battery). The roster dedupes, so variation in per-entity occurrence counts across seeds cannot change C15. The bar (0.900) sits below the honest 0.947 ceiling on every seed. NO BIAS.

## Attack axis 5: Determinism and hashes

- 3/3 byte-identical stripped reply streams and trace files: verified by recomputation from committed files (hashes above, matching SEALED_EVAL exactly).
- Build determinism: my fresh build of the committed implementation source with the pinned znc produced a binary with sha256 3d629deda888c18d19ff95ce9819829f2c268cf8e459330b7c573c3892cd57d7, byte-identical to the committed sealed binary (the RENDER_SHA in JUDGE_BRIEF). Reproducible.
- Arena rebuild from the frozen source reproduces the refreeze-record hash (see axis 1). HOLD.

## Attack axis 6: The ablation

- defrecall_abla.zag is a surgical 3-line delta (the three roster_touch call sites in learn_fact and learn_rel commented out), verified by diff against the committed implementation.
- Committed runabla results: C15 item replies UNKNOWN, C15 = 0.000, total 54/68 = 0.794, every other capability byte-identical to the v6 fresh baseline. The roster is causally necessary; the default action with an empty roster hallucinates nothing. The supplementary default-action-disabled run (defrecall_nodef.zag, 1-line delta) scores C15 = 0.000 with the roster enabled, proving the default action is the goal-completion path and no hidden handler carries the goal. HOLD.

## Attack axis 7: Knowledge vs architecture (roster-empty and roster-partial behavior)

Probed with my own build (see axis 3):

- Empty roster + bare prompt: UNKNOWN, no trace line, no hallucination. The default action depends on the roster being non-empty; it invents nothing.
- Partial roster (2 names): enumerates exactly what is present ("Solo,Alone"), with correct trace lines. The mechanism volunteers persistent knowledge, nothing more.
- Population paths: verified roster_touch fires from learn_fact (f events) and learn_rel (r events; endpoints both added). Dedup confirmed.
- Conclusion: the "volunteer persistent knowledge" behavior depends on nothing beyond the roster contents and the structural dispatch condition. No hidden state, no briefing reads, no researcher-supplied names. HOLD.

## Minor blemishes (do not affect the verdict)

1. Stale seed labels: results.txt headers say "seed 71503461337030" (arena scorer label) although the runs are on the fresh seed-632 battery; the world_gen variant's line-1117 proof label also still says 71503461337030 (only the line-265 seed literal was changed). Cosmetic; measurements are on the fresh battery (verified via fresh entity names in the runs).
2. The prereg freeze commit swept in two BATTERY-E4 files staged by a concurrent worker (disclosed by the lane; later commits used pathspec isolation).
3. A concurrent worker's commit (f461e812d, H5R2-SKEPTIC2) deleted competitive_arena/ from the git index after the lane ran. I verified the working-copy frozen sources are byte-identical to the committed CA-2 refreeze (c4e5a650e), so the lane's "1-line diff against the frozen source" claim holds substantively; my arena rebuild from that source reproduces the refreeze hash.

## Scope

DEFRECALL remains a CANDIDATE only: L2 goal infrastructure (persistent roster plus a general default recall action), explicitly not L3 (K8 disclaimer holds), no TNN-2 substrate claim, no TNN-beats-LLM claim, canonical 0.573 unmoved. The original spec's multi-step tool protocol remains unimplemented by the frozen battery (recorded honestly in the prereg section 8). The autonomy demonstrated is handler-free goal completion via a general default action, and it generalizes to novel bare prompts as demonstrated.
