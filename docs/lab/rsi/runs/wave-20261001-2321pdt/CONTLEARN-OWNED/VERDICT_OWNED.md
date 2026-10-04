# VERDICT_OWNED: machinery-disabled integration discrimination

Wave: wave-20261001-2321pdt. Lane: CONTLEARN-OWNED. Date: 2026-10-02.
Prereg: PREREG_OWNED.md, frozen alone at 3e837ff5c, amended and re-frozen
alone at d2fc968f4 (Amendment A1: audit count 104->98; tuples, bars, and
decision rule unchanged). Implementation: two binaries (`ow_treat` from
the machinery-disabled variant core, `ow_control` from the unmodified
frozen core) plus one fixture driver, two logged znc invocations, no
frozen-core edits, no new cognitive machinery.

## Per-bar results

| Bar | Result | Evidence |
|-----|--------|----------|
| K0 commit order | PASS | Prereg 3e837ff5c and re-freeze d2fc968f4 each committed alone; `git merge-base --is-ancestor d2fc968f4 HEAD` true; all implementation files first appear after d2fc968f4. |
| K1a one learner, one process | PASS | 6 spawns total (3 ow_treat, 3 ow_control), one process per full 98-event run; pid_leak_check=0. |
| K1b builds | PASS | `znc_invocations.log` holds exactly 2 entries (the two pre-run builds); 0 new entries during the 6 runs. |
| K1c audit, no task labels | PASS | AUDIT_PASS on all 6 runs (98/98 EV lines); masked queries carry the frozen parameters expected=-2, flags=1 (supervisor disconnect, disclosed; not a task label); empty argv; empty env. |
| K2a frozen ISA boundary | PASS | Frozen SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd` verified before implementation, immediately before the builds, and after all runs; git blob hash `b226b223cb3ee0be742af673653fb8ea8605f281` equals the f4de7ff46 freeze blob. |
| K2b driver audit | PASS | 0 cognition functions; 0 `ns(`/`link_edge`/`alloc_node` calls; 0 new node tags, edge types, opcodes, modes/bridges/routers/handlers/semantic cases; switch/match count 0. |
| K2c source delta | PASS | Cognition lines added 0, deleted 0, net 0 on the frozen path; the variant is a lane-dir measurement instrument (CO-5 verified), not an architecture change. |
| K2d pure Zag | PASS | Zero Python/C/JS/Rust at every stage; `which python3` empty under safebin PATH (NAMECHECK.md Step 0). |
| K3 no regression | PASS | 2321pdt `lo_driver` re-run read-only 3/3: stdout SHA-256 `1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9` (matches recorded value). |
| CO-1 TREAT integrates to the DEMONSTRATED bar | FAIL | STORE_OK_T 0/6, REUSE_OK_T 6/12, DELAYED_OK_T 6/12 (bar: 6/6, 12/12, 12/12). All 18 family-D masked probes took the true miss path. |
| CO-2 learner-mechanism evidence | PASS | Per-phase mechanism census complete and 3/3 consistent; the evidence unambiguously identifies which mechanisms did (and did not) fire (see below). |
| CO-3 determinism | PASS | 3/3 byte-identical transcripts per binary (TREAT `60a8b778a2b9ddaf629101912f20f45e7b7373ac0b09090b80a7dbb4705819ca`, CONTROL `54b3cd30d3a7ac06114ba128d488b2e9406056ed466d8f8ed3bf55eef003bcc1`); FNV-1a equal across reps; exit 0; zero stderr; no PID/timestamps/paths. |
| CO-4 control reproduces the bar | PASS | STORE_OK_C 6/6, REUSE_OK_C 12/12, DELAYED_OK_C 12/12 on the unmodified frozen core. |
| CO-5 machinery truly absent | PASS | Exact two-block source diff (variant-diff SHA-256 `3f385dc56367337f352da35ffd1b29bde0b7a124c68a42a57d717ad043cfaa75`); zero event-interface call sites by grep; zero MAP nodes on any of the 18 TREAT family-D probes. |

## White-box evidence: which mechanisms did the work

CONTROL: every integrated structure traces to the disabled machinery.
6 MAPs promoted; 24 alive DEP edges, of which 12 are construction
provenance (`t2_asm_chain` writes one DEP per step, frozen file line 371)
and 12 are promotion citations (`promote_graph` writes one DEP per
licensing fact, line 540). Zero UNCERT nodes, zero guides. The answers
served at REUSE/DELAYED are exact-hit retrievals of the machinery-taught
answer facts via `activate` (Attack 6 carried forward).

TREAT: the learner's own mechanisms did not integrate. Zero MAP nodes at
every phase. The only learner-side response to the 18 unintegrable masked
queries was the miss path: UNCERTAINTY nodes (6/12/18 across phases) plus
learner-constructed guides linked to POLICY_ROOT (6/12/18); the only DEP
edges are guide-to-UNCERTAINTY edges from `miss_inquire`. Standing
retrieval stayed intact: the 6 taught family-E facts were served 6/6 at
every probe phase (SANITY_E_T 6/6), so the integration failure is a
capability gap in the learner-owned set (standing structures, UNCERTAINTY
reification, guide construction/selection), not variant breakage. Final
alive node count 86 < 1024: no eviction; the missing structures are
evidence, not capacity.

## Verdict

**MACHINERY-DEPENDENT.** CO-4 passes and CO-1 fails: the continuing
learner stores the taught facts and serves them by standing retrieval,
but integrates 0/6 fresh 2-hop chains without the event-triggered
trial/promotion/P-INV machinery, while the unmodified frozen core
integrates 6/6 on the identical battery. The red-team QUALIFY stands,
strengthened by a clean discrimination: the integration work sits on the
researcher side of the control-plane line.

## Exact claim bound (frozen, per prereg section 8)

On the fixed disclosed 98-event battery, with the trial / promotion /
P-INV machinery verified absent from the event path, the continuing
learner integrates 0/6 fresh 2-hop chains (all probes take the true miss
path; zero MAPs; UNCERTAINTY/guide accumulation is the only learner-side
response), while the unmodified frozen core integrates 6/6 on the
identical battery with 6 MAPs and 24 machinery-written DEP edges; taught
1-hop facts are served 6/6 by standing retrieval in both conditions;
3/3 byte-identical.

Explicitly not shown: learner agency in the causal sense (H2-v2/H3
stand); procedure execution at query time; any L3 or generality claim; the
variant is a measurement instrument, not a proposed architecture.

## Deviations from the prereg

Amendment A1 (re-frozen alone at d2fc968f4 before any counted run):
audit-count arithmetic 104->98; the frozen tuple script, all bars, and
the decision rule are unchanged. The pre-amendment pilot runs (which
executed the exact frozen tuples but failed the wrong audit constant)
were discarded and not counted. No other deviations. No errata.

## Follow-ups for the coordinator

- None required by this lane. The standing question is now sharpened by
  a discrimination rather than a qualification: there is no
  learner-invoked trial/construct machinery in the frozen core (no
  `compose_try`; `t2_trial` is event-triggered researcher machinery), so
  learner-owned integration of a new experience currently has no
  mechanism to run on. Any future push toward LEARNER-OWNED must first
  propose a mechanism by which learner-created state initiates
  structure construction, per the constitution's learner-authority
  metric. Per the no-patch-treadmill rule, this verdict is followed by
  root-cause analysis, not by new handlers, modes, or opcodes.
- The 2321pdt CONTLEARN verdict's "step toward learner-owned, stated
  plainly" is superseded by this discrimination for the strong reading:
  the strong sense (the learner decides or authors) is now measured
  absent, not merely unclaimed.
