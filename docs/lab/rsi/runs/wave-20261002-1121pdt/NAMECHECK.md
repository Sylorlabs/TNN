# NAMECHECK.md: wave-20261002-1121pdt standing rules

These rules bound every worker in this wave. Written by the coordinator at wave open.

1. PURE ZAG ONLY, owner red line. No Python anywhere: not glue, analysis, verifiers, harnesses, fixtures. A prereg pre-authorizing Python tooling is VOID ON SIGHT. Any forbidden-interpreter invocation makes that lane's scientific wave automatically PROCESS-FAIL and its measurements quarantined; clean safebin reproduction required for canonical promotion. No de minimis exception (a single no-op python3 invocation is a PROCESS-FAIL).

2. TOOLCHAIN GUARD (2026-09-30 governance): every worker at startup runs bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh and export PATH="$HOME/safebin", records in its NAMECHECK.md Step 0 the outputs of `which python3` (must resolve to NOTHING) and `which znc` (must resolve to the safebin path). "Guard ok" without that evidence is not a pass.

3. FORK TESTING: enumerate EVERY branch and fork, local and remote, and run the frozen test battery against each. Report per-fork: branch name, commit, PASS/FAIL, what broke.

4. IMAGE JUDGE: Micah judges all image work. Surface image candidates only as sealed blind A/B pairs, randomized, mapping sealed, only when coded, tested, and ready. Never adopt on metrics alone. Never surface a recycled render as fresh; every JUDGE_BRIEF.md carries RENDER_SHA, FIRST_RENDERED_WAVE, COMPONENT_LINEAGE, NEW_KNOWLEDGE_CLAIM; re-certifications are labeled RE-CERTIFICATION.

5. PREREG COMMIT-ORDER SELF-CHECK: run over your wave's commits before any verdict. A prereg file's first commit must strictly precede its implementation files' first commits. Failures are UNVERIFIABLE ORDERING and cannot be adopted this wave.

6. DEBATE GROUP mandatory every wave: advocate FOR each adoption, skeptic AGAINST, judge renders a reasoned ruling with numbers cited. Debate transcript committed with the wave record. The skeptic's provenance probe ("What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?") must appear; a transcript lacking it is void. A debate overturns a coordinator verdict only with cited evidence.

7. Per candidate: PROPOSE (what changes, metric moved, cost, frozen KILL BAR before implementation, never moved after); TEST in pure Zag, zero randomness in decision paths, byte-identical reruns; RED TEAM every candidate (knowledge-vs-architecture confounds, metric gaming); VERDICT adopt only on clean PASS with zero regressions; COMMIT adopted changes locally with evidence. Hunt FREE LUNCHES first, then INTELLIGENCE TRADES (10x cost for genuine new capability is good); NEVER trade intelligence for speed; efficiency only as fuel for more intelligence.

8. DOCUMENTATION RULE: no em-dashes anywhere in loop docs. Use plain sentences, colons, or parentheses. Shell-only byte check via docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.

9. Frozen lanes without Micah's approval: no CAUSALV7 or version treadmill; no N+1 repair generations (3 such trigger ARCHITECTURE REVIEW); no new semantic cases in response to downgrades (no SUB, DIV, PARITY, 2-threshold COND); never weaken a frozen kill bar; never count a prereg threshold as achieved before frozen execution; FW1-FW9 is a regression battery, establishes no generality.

10. RED LINES: no spend, no publish, no contacting outsiders, no purchases/bookings, no irreversible commitments, never push to GitHub, never touch Google Drive.

## TECHNICAL CONSTRAINTS (from AGENTS.md, mandatory for all Zag work)

- The pinned znc has a name/layout-dependent _zag_print miscompile; never use _zag_print for dynamic content, format numbers into ONE preallocated output buffer with cursor-returning emit helpers then a single _zag_raw_syscall write, and byte-verify every binary's stdout.
- Never use `as *i32` + q[0..n] slice construction inside functions; use u8-backed cells with little-endian ig/is pack/unpack helpers.
- `as []f64`/`as []i64` on []u8 does NOT rescale .len.
- WAV PCM16 reads use a 2-byte getter.
- 2026-10-02, LPROBE lane: 7-deep nested ifs with !=/<= + function call in innermost condition trigger spurious error[E0204]; workaround = hoist sub-conditions into flag lets, nesting 3 or fewer, hoist call results into locals.
- 2026-10-02, DEVANG lane: FOURTH defect: negated conjunction !(A && B) in a while condition miscompiles; workaround = De Morgan rewrite as (... != ... || ... != ...), verify loop result on known input, grep all new Zag for `while.*!(`.
- Capacity-plan: problems x 40 + teaching under 1024 nodes until the reclamation frontier lands.
- ma_base.zag is not self-contained; harnesses must supply a minimal ev_query.

## Wave-specific notes

- Disk incident at wave open (~19:00 UTC 2026-10-02): disk hit 100%; root cause five stale wave-20261002-0821pdt worktrees (6.6GB each, ~33GB total). Fix: verified 16 prior lane branches intact, removed stale worktrees with git worktree remove --force (recoverable). All 17 lane worktrees rebuilt as sparse checkouts (~37-53MB each). Lesson: prune stale wave worktrees at wave close; default to sparse checkouts.
- Live scaling runs in the main worktree and ~/workspace/tnn-rsi-wt-s5fix must not be disturbed; lane workers forbidden from writing there.
- Runtime instability: two lane workers killed this wave by daemon restart-drain exec rejections (sensory 11/18, sensory-recovery 18/18); per the instability protocol, no third re-dispatch: H5 rolls to next wave. Debate convened inline as three voices for transcript safety.
