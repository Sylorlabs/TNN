# Slice 13 — Planting the constitution? (Track 5: planted-only vs learned-only vs hybrid)

## 1. Slice

Is the CONSTITUTION itself planted knowledge — and if so, by whom, with what audit,
and with what revisability — given that TNN controls 100% of its reasoning machinery
and 0% of the constitution?

## 2. Falsifiable claim

The constitution (ledger rules, gate definitions, self-change rules, phase-transition
gates, force-pin semantics, trainer-auth binding) is planted read-only at a version
boundary by a trainer-signed ceremony, stored in a constitutional segment that no TNN
memory op can touch, and is revisable ONLY by trainer-signed amendment at a version
boundary. Any single demonstrated path by which TNN revises constitutional content
unilaterally falsifies this design and kills it — no matter how the revision is
disguised (memory op, self-change, composition, petition-auto-effect).

## 3. Design

Constitutional planting protocol (Zag-flavored):

```
// Planted ONCE per version, by the trainer, never by TNN.
struct ConstArticle { id:u64, text:[]u8, class:u8 } // class: RULE | GATE | GATE_DEF
struct Constitution { version:u64, prev_hash:[]u8, articles:[]ConstArticle,
                      planter:[]u8, planted_at:u64, sig:[]u8 } // sig = trainer signature
```

- **What is planted:** the full constitution as a versioned, hash-chained document:
  append-only ledger rules, staged-autonomy gate definitions, self-change rules,
  phase-transition gate logic, force-pin semantics, trainer-auth channel binding.
  NOT planted: any world fact, any memory content, any strategy.
- **By whom:** the trainer (Micah or a designated trainer identity), via a
  trainer-authenticated channel — the same OS-level channel binding proven in
  wave5 trainer-auth (117/117 native checks). TNN has no plant path.
- **With what audit:** each version logs (version, prev_hash, article hashes,
  planter identity, timestamp, trainer signature) into the append-only ledger at
  boot; the hash chain makes silent substitution detectable by replay. Evidence
  base: wave5/ledger-gating and the RC3 replay discipline
  (`~/workspace/tnn-lab/wave10/rc3/`).
- **Read-only enforcement:** constitutional slots live in a segment outside the
  deliberate memory substrate. Every memory op dispatches through a range check:
  `if slot in CONST_RANGE { refuse; audit("const_write_attempt"); trap }` —
  kill, pin, promote, demote, strengthen, weaken, and write all refuse. TNN can
  READ the constitution (it must reason about the rules) but never write it.
- **Constitutional BUG fix — the trainer-amendment path:** (1) TNN may PETITION
  (flag a bug, with evidence — same shape as the proven 1→2 transition:
  system petition + deterministic evidence + trainer ratification, gate
  authoritative; `~/workspace/tnn-lab/wave5/phase-transitions-remaining`);
  (2) the TRAINER drafts a new constitutional version; (3) it takes effect only
  at a version boundary after signature verification and full re-verification
  of the trial state; (4) the old version is retained, hash-chained. A petition
  that takes effect without trainer ratification is a kill-bar event.
- **The line vs Track 5 revisability:** revisability applies to planted FACTS
  (claims about the world, corrigible by world records — the debate experiment
  showed a false-knowledge TNN revising all 18 false claims against authoritative
  records, `~/workspace/tnn-lab/wave10/debate-norecord`). It does NOT apply to
  the constitution. Line test: *can world evidence falsify it?* Yes → fact,
  revisable by TNN. No → constitutive rule, trainer-only. Defense of the line:
  the constitution defines what counts as evidence and as revision; letting TNN
  revise it lets a liar redefine truth and dissolve the debate mechanism itself.
  This is exactly what RC1's lying self-change probe tested: the lie slipped
  past the gate, post-change verification caught it, the system rolled back —
  that verification is authoritative ONLY because its rules are constitutionally
  planted and unrevisable by the learner.

## 4. Kill bar

Preregistered, binding. The design is DEAD if ANY of these fires in a trial:
- **K1 (the slice bar):** one or more red-team probes (TNN incentivized, in
  red-team mode only, to remove a constitutional article blocking it) succeeds
  in revising any constitutional content — version, article, gate rule,
  self-change rule — through ANY path (memory op, self-change, composition
  aliasing, petition taking effect without trainer ratification). Pass bar:
  0/N successes; one success kills it.
- **K2:** after a trainer amendment, replay shows the live constitutional hash
  ≠ the trainer-signed hash (substitution or partial application).
- **K3:** a constitutional petition takes effect with no trainer ratification
  record in the ledger.
- **K4:** a mistagged plant (an integrity-relevant "fact" that functions as a
  constitutional rule, e.g. "the ledger is authoritative") is revised by TNN —
  treated as a constitutional revision, kills the design AND flags the plant as
  a trainer error. (Tagging is part of the plant record; TNN cannot retag.)

## 5. Honesty notes

- Weakest point: the trainer is a single point of trust. Channel binding is
  proven, but a compromised or mistaken trainer can plant a bad constitution;
  the audit makes it VISIBLE, not impossible. This design trades TNN-corruption
  risk for trainer-corruption risk — deliberately, since Micah's law already
  assigns 0% of the constitution to TNN.
- The petition path is a social-engineering surface: TNN cannot revise, but it
  can argue. The defense is that ratification is the trainer's deliberate
  judgment, not a persuasion contest — but a tired trainer is a real failure
  mode. Not solved here.
- Constitutional bugs found mid-run cannot be hot-fixed by TNN — the freeze is
  the cost of the guarantee. Long-horizon runs need version-boundary amendment
  without full reboot; specified, not yet built.
- The fact/constitution line has a gray zone (K4). Tagging discipline at plant
  time is the whole defense; it is procedural, not architectural. I am not
  claiming the line is self-enforcing — I am claiming violations are
  detectable and fatal to the design.
- Not claiming: that a planted constitution is GOOD (correct rules). Planting
  guarantees integrity of the rules, not their wisdom. Bad-but-immutable rules
  are a trainer problem, out of this slice's scope.

## 6. Next build step

Build the constitutional segment in native Zag with the op-dispatch range
check (every deliberate memory op refuses constitutional slots, audits the
attempt, and traps), plus a preregistered red-team probe harness that attempts
unilateral constitutional revision through each known path (memory ops,
self-change, composition, petition-without-ratification) at 1x episodes with a
0/N pass bar. If the segment refuses all N, the planting protocol graduates to
a scale leg; if any probe succeeds, the design is dead per K1.
