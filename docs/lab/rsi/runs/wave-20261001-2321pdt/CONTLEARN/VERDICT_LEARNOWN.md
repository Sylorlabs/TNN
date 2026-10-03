# VERDICT_CONTLEARN: learner-owned structural workspace probe

Wave: wave-20261001-2321pdt. Lane: CONTLEARN. Date: 2026-10-01.
Prereg: PREREG_LEARNOWN.md, frozen alone at commit 408ffdcdc.
Implementation: `lo_driver` built from the byte-identical frozen core plus
the fixture driver, one logged znc invocation. No H10/H11 implementation,
no new cognitive machinery, no frozen-core edits.

## Per-bar results

| Bar | Result | Evidence |
|-----|--------|----------|
| K0 commit order | PASS | Prereg committed alone at 408ffdcdc. All implementation files first appear after that commit. `git merge-base --is-ancestor 408ffdcdc HEAD` true. |
| K1a one learner, one process | PASS | 6 spawns total, exactly 3 per mode; each TREAT rep is one process for the whole 92-event run. Transcripts contain no PID (pid_leak_check=0). |
| K1b one build | PASS | `znc_invocations.log` holds exactly 1 entry (the pre-run build); 0 new entries during the 6 runs. |
| K1c audit, no task labels | PASS | AUDIT_PASS on all 6 runs (92/20 events through the choke points). Masked queries carry the frozen parameters expected=-2, flags=1 (supervisor disconnect, disclosed; not a task label). Empty argv; empty env via `bash -c 'exec -c'`. |
| K2a frozen ISA boundary | PASS | SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd` verified before implementation, immediately before the build, and after all runs; `git diff f4de7ff46` on the frozen path empty throughout. |
| K2b driver audit | PASS | 0 cognition functions; 0 ns(/link_edge/alloc_node calls; 0 new node tags, edge types, opcodes, modes/bridges/routers/handlers/semantic cases; switch/match count 0. |
| K2c source delta | PASS | Cognition lines added 0, deleted 0, net 0. Single persistent workspace (the frozen arena); all learner-state structures in frozen formats, counted by census. |
| K2d pure Zag | PASS | Zero Python/C/JS/Rust at every stage; `which python3` empty under safebin PATH (NAMECHECK.md Step 0). |
| K3 no regression | PASS | 2021pdt `cl_driver` re-run read-only 3/3: stdout SHA-256 `53ff2c990e4f7f8d29c8b1bb809cf6616226b9f6bd3dd28d06210dc54446bc44` (matches 2021pdt), REUSE_COUNT 30 with R1C 6, R2C 3, R3C 3, R4C 12, R5C 6. |
| K4a store, unsupervised | PASS | STORE_OK 13/13: 7x map(6001+i,202) and 6x map(8001+i,402) promoted under masked queries with alive DEP edges to licensing facts. |
| K4b reuse, unsupervised | PASS | REUSE_OK 20/20 masked probes return stored values across 3 task families, serving node verified. |
| K4c ablation | PASS | REUSE2_ORIG 0/20 (<= 2) and REUSE2_NEWV 20/20 (>= 18). Deleting the serving structures dropped original-value reuse to zero while the machinery still retrieves successor values. |
| K4d nostore control | PASS | K4D_MISS 20/20, K4D_UNCERT 20: every probe on the fresh arena took the true miss path. |
| K5 machinery sanity | PASS | TREAT UNCERT count 0; final census within budget (no eviction). |
| K6 determinism | PASS | 3/3 byte-identical transcripts per mode (SHA-256 match); FNV-1a checksums equal; exit 0 on all 6 runs; zero stderr bytes; no PID/timestamps/paths in transcripts. |

## Verdict

**BUILD-PASS: LEARNOWN-DEMONSTRATED.** All of K0 through K6 pass.

The exact frozen claim, per the prereg: on the fixed disclosed 92-event
treatment script, with the per-query supervisor disconnected (every query
masked: expected=-2, flags=1), the frozen TNN-2 core's event-triggered
machinery stores 13/13 chain structures as MAPs with DEP citations in the
single persistent arena, retrieves 20/20 stored values by masked query
across 3 task families, and after in-arena deletion of the serving
structures (contradiction: supersede marks plus MAP-cell tombstone and
revision) the masked reuse of original values drops to 0/20 while the
machinery still retrieves the 20 successor values; the nostore control
shows 0/20 reuse with 20 UNCERT misses; 3/3 byte-identical.

What this verdict does NOT claim (per prereg sections 1 and 7): no learner
agency in the causal sense (H2-v2/H3 stand on the byte-identical source:
no learner-created state influences any store, accept, or retrieve
decision); no procedure execution at query time (Attack 6 carried forward:
reuse is exact-hit retrieval of machinery-taught facts via `activate`);
no unsupervised integration beyond the disclosed script; no L3 and no
generality. The event script is disclosed, not a sealed adversarial world.

## Step toward learner-owned, stated plainly

Versus the 2021pdt QUALIFY, this wave removes the per-query answer keys and
shows the store/retrieve/reuse mechanics do not depend on them: 13/13
structures stored, 20/20 retrieved, and reuse causally dependent on the
stored structures (in-arena deletion drops original-value reuse to 0/20).
The workspace is the single frozen arena, owned by learner state in the weak
H10 sense (resident in the learner's arena, manipulated only through the
frozen event interface), with no independent subsystem state formats and no
new modes, bridges, or handlers. The strong sense of learner-owned (the
learner decides or authors) is not demonstrated and is not claimed.

## Deviations from the prereg

None. The driver implements exactly the frozen event script (92/20 events;
audit counters confirm). No errata.

## Follow-ups for the coordinator

- None required by this lane. The standing H10 question (what a
  learner-owned structural workspace must beat) now has a second measured
  baseline: unsupervised store 13/13, masked reuse 20/20, ablation-verified
  dependence on stored structures, byte-identical determinism.
- Recorded, not authorized here: the red-team-suggested masked variant was
  exactly this probe; the remaining open direction is sealed adversarial
  worlds for the three new mechanisms (the post-freeze battery), which this
  disclosed-script battery must not be cited for.
