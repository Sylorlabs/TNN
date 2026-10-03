# REPORT: NT-PORT-PRESSURE (E8.1) -- the NT1 rule on the continuing learner under capacity pressure, with rule-structured families

## Verdict

**PORT-PASS-STRUCT** per the frozen verdict mapping (PREREG Section 8).
K1, K2, K3, K4, K5 all hold. This is the preregistered directional
prediction (PORT-PASS-STRUCT), and -- like NT1, NT-D2, NT-PORT, and
NT-PRESSURE before it -- EVERY frozen numeric prediction matched
exactly, including the full 5-bin eviction histogram and all three
arms' retest partition scores.

## Frozen results (3/3 byte-identical)

- Run digest: `bc213a0e7ef05c159f264f3d31ca1f1c298734ec562f77031f34bafe8d438b17`
- Binary digest: `a100673a3ca8e0a93b4a85e4e799e7d21d5c43577017700037293f466fd28082`
- Source digest: `f91df3ee5cc6838cf47afac8dcc06a21845f2bf5ba7b49e127d1cc1d56c19ee6`

```
NTPP PORT ttcA=2 probeA=8 nevict=14 bprobe=10 phev=0
NTPP PORT RET c=2 nc=2 u=4 forget=0
NTPP PORT EVHIST 144=3 146=3 147=3 149=3 150=2
NTPP NOADDR ttcA=2 probeA=8 nevict=0 bprobe=14 phev=0
NTPP NOADDR RET c=2 nc=2 u=0 forget=4
NTPP NOADDR EVHIST
NTPP FRESH ttcA=2 probeA=8 nevict=0 ttcB=2 bprobe=14
NTPP FRESH RET c=2 nc=0 u=0 forget=6
NTPP K1=1 K2=1 K3=1 K4=1 K5=1
NTPP VERDICT=PORT-PASS-STRUCT
```

Prediction vs actual: NO misses. PORT nevict 14 = 14 (12 pigeonhole
lower bound + 2 traced revolving-door overhead); c 2/2; nc 2/2;
u 4/4; forget 0; phev 0; histogram bins 144/146/147/149 = 3,
150 = 2, all other subjs (in particular all phase-1-link subjs
100..119) at 0. NOADDR bprobe 14 = 14; c 2/2; nc 2/2; u 0/4;
forget 4. FRESH ttcB 2 = 2; bprobe 14 = 14; c 2/2; nc 0/2; u 0/4;
forget 6. The prereg hand-traces (Sections 5.1/5.2/5.3) reproduced
the binary exactly on all three arms.

Note (informational, not a bar): PORT bprobe = 10/14 after the 3
fixed B passes, consistent with the traced end state (novel links
144,146,147,149 absent at end of pass 3, present only via D1
checkpoint; they return on the next teaching). The retest scores
queries, not link presence, and is unaffected.

## Kill-bar evaluation

- K1 (learnability): PASS. ttcA_port = 2 (1..50), probeA_port = 8/8;
  ttcB_fresh = 2 (1..50), bprobe_fresh = 14/14. No VOID.
- K2 (PORT retention of uncontested structure): PASS. nc_port = 2/2,
  u_port = 4/4. The chains sharing substructure with contradicted
  chains (A2 via shared link (101)->102; A4 via shared link
  (105)->106) answer correctly, and all four untouched chains
  answer correctly.
- K3 (PORT selective revision, not erasure): PASS. c_port = 2/2
  (100->130->132, 104->131->133: revision completed in pass 3 via
  ref accumulation across D1 eviction boundaries) AND forget = 0.
- K4 (pressure exercised, eviction discipline): PASS. nevict_port =
  14 = the traced port minimum; phev_port = 0 (white-box: all 14
  victims are novel subjs 144,146,147,149,150; zero phase-1-link
  subjs evicted across all passes).
- K5 (discriminative validity): PASS. NOADDR fails K2 and K3
  (u = 0/4, forget = 4: four untouched 2-hop chains destroyed by
  novel-key aliasing; the failure is structural, in addressing, not
  the update rule -- revision still works, c = 2/2, and B is fully
  learned, bprobe = 14/14). FRESH fails K2 (nc = 0/2, u = 0/4,
  forget = 6: B-learning alone preserves nothing A-only). The
  three arms have three sharply distinct signatures; the apparatus
  discriminates.

## What this establishes

1. **The NT1 rule survives the port to rule-structured families
   under pressure.** Entry-local error-driven evidence revision +
   dedicated addressing (ported as D1+D2) preserves 2-hop chains
   with shared substructure at 1.2x capacity pressure: contradicted
   chains revise, chains sharing links with contradicted chains
   retain through the agreed shared links, untouched chains are
   never eviction candidates, nothing is needlessly forgotten.
2. **The fragility source is addressing, again, now structurally.**
   NOADDR (identical update rule, overlapping map) learns B
   perfectly (bprobe 14/14, revision 2/2) yet destroys four
   untouched multi-hop chains: aliasing one link breaks every
   query composing through it, although no contradiction touched
   those chains. This is the ML0/NT1 fragility finding lifted from
   isolated pairs to structured knowledge.
3. **Retention comes from lifetime memory, not from B containing
   the answers.** FRESH (same rules, reset between families)
   learns B to criterion yet forgets all six A-only queries. PORT's
   retention is attributable to the memory/rules, not the workload.
4. **The victim-set moral replicates on structured families.**
   PORT's 14 evictions are all re-taught-every-pass novel links
   (forget-free churn); no live phase-1-link structure is ever
   evicted, with no protection flag, no task identity, no
   importance logic anywhere in the learner (audit grep clean).

## What broke / what needed to change

Nothing in the rule set broke: the D1+D2 port required NO changes
to handle rule-structured families. The only adaptation vs
NT-PORT/NT-PRESSURE is the workload itself (links + 2-hop query
procedure instead of bare key-value probes) and the three-arm
harness (PORT/NOADDR/FRESH per the E8.1 sketch). One trace-level
finding: under the fixed 3-pass B protocol, 4 novel links are
absent at retest (present only via D1 checkpoint); this is the
expected revolving-door end state, not a defect -- the retest
queries never traverse those links.

## Honest boundaries (from PREREG Section 9, unchanged)

- The LINKS are memorized associations; what is rule-STRUCTURED is
  the family (taught 2-hop chains with shared substructure; answers
  require composing links). No rule INDUCTION tested; no L2/L3
  claim. Retention/revision/eviction dynamics over structured
  knowledge only.
- Single capacity point (CAP=20, 1.2x); single contradiction
  magnitude; pressure-envelope scaling already covered by
  NT-PRESSURE (to 5x, memorized pairs).
- Port covers the associative instance memory only (NT-PORT
  boundary stands: contlearn2 schema machinery and H-CONTLIFE-1
  hash-table memory remain unported).
- Whether LIFO's tenure principle holds when novel links are NOT
  re-taught every pass remains the preregistered open boundary,
  NOT tested here.
- NOADDR's 32-slot table vs PORT's 20-slot table: the arm
  difference under test is the address map, not capacity; NOADDR
  never fills its table (nevict = 0), so capacity cannot explain
  its failure signature.

## Recommended follow-up (preregistered)

- Probe the "genuinely low-value" boundary: novel links NOT
  re-taught every pass -- does LIFO still pick the right victims,
  or does tenure-protection become a liability? (preregistered
  open boundary across NT-PORT/NT-PRESSURE/this lane)
- Graded contradictions on structured families (E8.3 direction):
  partial link contradictions and interleaved families with no
  task labels.
- Port D1+D2 toward H-CONTLIFE-1's hash-table memory if an
  evidence-machinery design can be made minimal; test interaction
  with schema discovery/retire.

## Provenance

- Prereg frozen alone: commit `4460908ca` (PREREG.md + NAMECHECK.md
  only), strictly before implementation. Commit-order self-check:
  verified below (prereg commit strictly precedes this commit).
- Implementation + results: this commit. Pure Zag, safebin-only
  PATH, pinned znc 2026.07.0-dev (same build as
  NT1/NT-D2/NT-PORT/NT-PRESSURE). Zero forbidden-executable
  invocations.
- Source: `ntpp_full.zag`, written to PREREG Sections 2-4 (D1+D2
  port verbatim from nt_port/nt_port_full.zag; novel element is the
  rule-structured family workload + 2-hop query + PORT/NOADDR/FRESH
  harness). One self-caught display-field bug fixed pre-build
  (FRESH out[28] held phev instead of bprobe; K1 always read the
  intended field; the frozen binary was built only from the
  corrected source).
- Build: `znc ntpp_full.zag -o ntpp_bin` (exit 0; benign
  zagd-unavailable warning only); 3/3 runs byte-identical (cmp),
  exit 0, zero stderr.
- Audit grep for protection/task-label/freeze/importance/mode
  logic: clean (matches are disclosure comments only); "python"
  appears once, in the header comment "Pure Zag. No Python.";
  compiler-defect workarounds honored.
- Commits local only, explicit pathspecs, never pushed.
