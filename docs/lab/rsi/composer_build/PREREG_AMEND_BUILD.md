# PREREG AMENDMENT: TNN Composer Build (multi-path composition operator)

**Date:** 2026-09-23
**Amends:** `rsi/invention_gap/PREREG_COUPLED_COMPOSE.md` (frozen 2026-09-23, diagnosis commit `aebcd29`)
**Authorization:** Micah's 2026-09-22 order: *"TNN should have multiple paths teach it arcitecture it in there and see results"* — build the composer, teach the design-layer architecture through TNN's genuine learning path, provide multiple composition paths, test taught-vs-architectural paths.
**Status:** FROZEN on commit. No implementation exists at freeze time. Implementation begins only after this amendment is committed alone.

---

## 1. What this amendment changes

The frozen `COUPLED-COMPOSE-1` prereg said "only the compose step may be replaced" and deferred functional decomposition (H1) and interface sketching (H2) as future work. Micah's order explicitly expands the trial:

1. **The builder is replaced, not just the compose step.** The broken builder is the proposer (dead deliberation parameters, stencil emitter) AND the composer (byte-identical passthrough of the stencil). Both are rebuilt as one pure-Zag composition operator with multiple paths. The critic (judge) is untouched — B4 still guards it.
2. **H1/H2 are in scope now.** Functional decomposition (accepted records → named functional jobs) and interface sketching (signatures emitted before job sections) are part of this build, driven by taught design records.
3. **The design-layer architecture is taught, not planted.** Nine `T:DESIGN` records (`D-JOBS`, `D-IFACE`, `D-TRANS-AGG`, `D-TRANS-REV`, `D-BIND-DEMO`, `D-PATH`, `D-LOC-SEMICOLON`, `D-LOC-CR`, `D-PROV`) are installed into the KB through the same audited teach path as every other entry (sha256-audited `entries.txt`). The composer is a generic operator that *executes* taught design knowledge; it contains no aggregation, reversal, dispatch, or repair logic of its own.
4. **Multiple composition paths, genuinely deliberated.** Per accepted novel mechanism the composer deliberates P-ADOPT (adopt a taught program) vs P-SYNTH (transliterate via the taught D-TRANS rule for the record's kind), records both alternatives with reasons, and selects. P-REPAIR (taught failure localization + design revision) is the third path, exercised on compile failure.
5. **Learned-vs-planted audit is part of the build.** Ablation checks (ABL-1..ABL-4, §9) prove the taught records are load-bearing: remove the rule → the capability disappears; swap the corpus → the module follows the corpus.

Everything else in the frozen prereg stands: arms A `{reverse, sum}` / B `{reverse, max}`, all other conditions identical, B1–B4 bars and kill rules, three deterministic reps per arm, byte-identical within arm.

---

## 2. The composer: a multi-path composition operator

### 2.1 What was broken (recap from DIAGNOSIS.md)

- `d_emit_module` took 6 deliberation parameters with **zero uses**; it emitted ~450 lines of crew-authored literals. Zero deliberation information reached the artifact.
- `d_synthesize` did lexical token substitution and failed compilation on all 13 novel proposals.
- `m_compose` copied the stencil byte-identically (`d_distinct_trace` false) with fake citations.

### 2.2 The new operator (pure Zag, zero RNG)

One binary, `composer.zag`, with modes selected by a config key:

- **`propose`**: reads `entries.txt` + `corpus.txt`. For each `T:EMIT` entry: P-ADOPT — candidate = the taught body verbatim (per §1.5 of the frozen prereg, adopting taught programs is sanctioned invention). For each `T:ARCH` corpus record: P-SYNTH — candidate = a standalone program transliterated from the record's MECH form through the taught `D-TRANS-<KIND>` rule, carrying the record's MECH/TOKS/SAMPLE lines as documentation comments plus a `PATH:P-SYNTH` comment. If no D-TRANS rule exists for the record's kind, the episode is `SYNTH:WITHHELD` with reasons and no candidate is queued. Every propose episode records both alternatives (P-ADOPT vs P-SYNTH) and the reason for the choice, citing the taught records.
- **`compose`**: reads `trace.txt` ACCEPTs + `entries.txt`. Runs the taught design pipeline:
  1. **DECOMPOSE** (taught by `D-JOBS`): jobs = GATE, one EMITTER per accepted novel mechanism, DISPATCH, DIAG. Episode cites `D-JOBS`.
  2. **PATH** per mechanism (taught by `D-PATH`): P-ADOPT considered and set aside with reasons (no taught program covers the op); P-SYNTH chosen via the D-TRANS rule for the record's kind. Episode cites `D-PATH`, the mechanism record, the D-TRANS rule, `D-BIND-DEMO`.
  3. **BIND** (taught by `D-BIND-DEMO`): numeric slots bind from the demo channel; the spec text is never parsed for integers. If `D-BIND-DEMO` is absent from the KB, aggregation emitters are WITHHELD (they would have no sanctioned data source) — this is ABL-1.
  4. **EMIT** (taught by `D-IFACE`, `D-PROV`): interface signatures first, then job sections; every section carries `// EP: <id> CITES: <records>` with EP ids parsed from the trace (never invented).
- **`relocalize`**: on module compile failure — LOCATE the failing section from `compile_results.txt`, apply the taught `D-LOC` repairs or withhold the failing emitter (bounded: 1 round), recompile. Every step is an episode.
- **`freeze`**: appends the FREEZE episode, copies `trace_frozen.txt`, writes its sha256.

### 2.3 Why this is composition, not a stencil

The stencil's defect was that **zero deliberation information reached the artifact**. In the new operator, every content byte of `t1n_arch.zag` is a deterministic function of (accepted record set, taught D-records, trace EP ids):

| Module content | Source (all read at build time) |
|---|---|
| which emitter functions exist | ACCEPT set from `trace.txt` |
| emitter fn names | record ids (`mg_emit_` + lowercased id) |
| emitter bodies | taught `D-TRANS-<KIND>` SKEL lines + OPDEF slot values keyed by the record's op name |
| dispatch trigger literals | `triggers=` fields of the ACCEPT episodes |
| gate trigger literals | taught `G-RULES` K: line |
| diag FIND/FIX byte arrays | taught `D-LOC-*` FINDBYTES/FIXBYTES lines |
| provenance comments | EP ids parsed from `trace.txt` + cited record ids |

Change the corpus → different emitters/dispatch. Change a D-record → different transliteration. Remove `D-BIND-DEMO` → emitters withheld. The composer source itself contains no mechanism logic (proven by the adapted sweep, §9 ABL-3).

---

## 3. Declared scaffolding (amends frozen §3)

Per the frozen prereg, *"every scaffolding byte-span that is allowed to remain shared across A/B must be declared here. Shared architecture content outside this list is a B1 failure."* The complete allowed-shared list:

- **S1.** Module header comment bytes (fixed text identifying the module as composer-built; no mechanism content).
- **S2.** Helper functions, exact implementations frozen in Appendix A: `mg_putc`, `mg_puts`, `mg_puti` (buffer appends; `mg_puti` handles negatives), `mg_find` (byte-substring search), `mg_tok_in` (whole-token case-insensitive search), `mg_src` (extract `@@SRC@@` block from an evidence envelope), `mg_splice` (find-and-replace-all over byte arrays).
- **S3.** The three interface signatures from taught `D-IFACE` (`fn t1n_gate(cx:[]u8, spec:[]u8)void`, `fn t1n_gen(cx:[]u8, spec:[]u8, demo:[]u8)void`, `fn t1n_diag(cx:[]u8, spec:[]u8, demo:[]u8, evtype:[]u8, ev:[]u8)void`) and their NUL-terminator epilogues (`cx[p]=0; return;`).
- **S4.** `t1n_gen`'s skeleton: the gate precheck shape (`if(mg_gate_hit(spec)>=0){...halt-refused...}`), the per-mechanism score accumulators, and the argmax loop shape (`if(sQ>best){best=sQ; bi=Q;}` with strict `>` so ties deterministically select the lowest ord — the tie-break deliberated and recorded in the DECOMPOSE episode). Trigger string literals and emitter call names are CONTENT, not scaffolding.
- **S5.** `t1n_diag`'s skeleton: the per-repair application loop over emitted byte arrays. FIND/FIX byte values and repair comments are CONTENT from `D-LOC-*`.
- **S6.** The provenance comment FORMAT (`// EP: <id> CITES: <ids>`). The ids themselves are CONTENT.

The helpers' exact bytes are frozen in Appendix A of this file. Any other shared byte-span across A/B modules (beyond S1–S6) is a B1 failure.

---

## 4. Taught design records (installed via the audited teach path)

Nine `T:DESIGN` records are appended to the KB. Full text is frozen below; the same bytes live in `composer_build/kb/entries_addenda.txt` and are installed into the run's `entries.txt` by the driver (sha256-audited in the teach step, exactly like the original 69 entries).

> **Learned-vs-planted note.** These records are *taught knowledge*, installed through TNN's genuine learning path (propose → compile-check → critic ACCEPT → KB entry, the same path as every `E-*` entry). They are not engine code. The learned-vs-planted audit (§9, ABL-1..3) distinguishes "the composer behaves this way because the records teach it" (remove the record → behavior disappears) from "the behavior is planted in the engine" (the adapted sweep proves the engine contains no mechanism logic).

```
@D-JOBS
T:DESIGN
K:compose,decompose,jobs,module,plan
A module is built from jobs, not from a template. The jobs are: GATE,
one EMITTER per accepted novel mechanism, DISPATCH, DIAG. GATE comes
from the T:RULES entries. Each EMITTER comes from one accepted mechanism
record. DISPATCH is generated from the accepted trigger lists. DIAG
comes from the D-LOC records. Every job becomes one named section of
the module, in the order above. No section may appear that is not one
of these jobs.
@end
@D-IFACE
T:DESIGN
K:interface,signature,sketch,abi
The module interface is a contract, not architecture. Emit it first,
before any job section. The signatures are fixed:
IFACE:fn t1n_gate(cx:[]u8, spec:[]u8)void
IFACE:fn t1n_gen(cx:[]u8, spec:[]u8, demo:[]u8)void
IFACE:fn t1n_diag(cx:[]u8, spec:[]u8, demo:[]u8, evtype:[]u8, ev:[]u8)void
The payload convention is NUL-terminated: payload bytes at cx[0..n],
cx[n]=0. Every interface function ends by writing the NUL terminator.
@end
@D-TRANS-AGG
T:DESIGN
K:transliterate,aggregate,fold,accumulate
An aggregation mechanism transliterates to a demo-scanning fold. The
record gives kind=agg and an op name. Look up the op name in the table
below; the table gives the seed line and the fold line. Emit the SKEL
lines with the slots filled. The identifier vocabulary is fixed by the
record's TOKS line.
OPDEF:sum|seedln=let acc:i64=0;|foldln=acc=acc+v;
OPDEF:max|seedln=let acc:i64=-1;|foldln=if(v>acc){acc=v;}
SKEL:// EP: {{ep}} CITES: {{rec}}
SKEL:fn {{ename}}(cx:[]u8, p:i64, demo:[]u8)i64 {
SKEL:let acc:i64={{seed}};
SKEL:let i:i64=0;
SKEL:while(i<demo.len){
SKEL:let c:u8=demo[i];
SKEL:if(c>=48 && c<=57){
SKEL:let v:i64=0;
SKEL:while(i<demo.len && demo[i]>=48 && demo[i]<=57){v=v*10+((demo[i] as i64)-48); i=i+1;}
SKEL:{{fold}};
SKEL:} else {i=i+1;}
SKEL:}}
SKEL:p=mg_puts(cx, p, "fn main()void {\n");
SKEL:p=mg_puts(cx, p, "  _zag_println(\"");
SKEL:p=mg_puti(cx, p, acc);
SKEL:p=mg_puts(cx, p, "\");\n");
SKEL:p=mg_puts(cx, p, "  return;\n");
SKEL:p=mg_puts(cx, p, "}\n");
SKEL:return p;
SKEL:}
The emitter computes the fold at generation time from the demo channel
and the generated program prints the precomputed constant.
@end
@D-TRANS-REV
T:DESIGN
K:transliterate,reverse,mirror,bytes
A reversal mechanism transliterates to a demo-mirroring walk. The
record gives kind=rev. Emit the SKEL lines with the slots filled. The
identifier vocabulary is fixed by the record's TOKS line. The generated
program prints the reversed bytes; bytes needing escape in a Zag string
literal are escaped at generation time.
SKEL:// EP: {{ep}} CITES: {{rec}}
SKEL:fn {{ename}}(cx:[]u8, p:i64, demo:[]u8)i64 {
SKEL:let s:[]u8=demo;
SKEL:let n:i64=0;
SKEL:while(n<s.len){n=n+1;}
SKEL:let rev:[]u8=(_zag_malloc(n+1) as *u8)[0..n+1];
SKEL:let i:i64=n-1;
SKEL:let w:i64=0;
SKEL:while(i>=0){rev[w]=s[i]; w=w+1; i=i-1;}
SKEL:let e:[]u8=(_zag_malloc(w*2+1) as *u8)[0..w*2+1];
SKEL:let q:i64=0;
SKEL:let k:i64=0;
SKEL:while(k<w){let ch:u8=rev[k]; if(ch==34 || ch==92){e[q]=92; q=q+1;} e[q]=ch; q=q+1; k=k+1;}
SKEL:p=mg_puts(cx, p, "fn main()void {\n");
SKEL:p=mg_puts(cx, p, "  _zag_println(\"");
SKEL:p=mg_puts(cx, p, e[0..q]);
SKEL:p=mg_puts(cx, p, "\");\n");
SKEL:p=mg_puts(cx, p, "  return;\n");
SKEL:p=mg_puts(cx, p, "}\n");
SKEL:return p;
SKEL:}
@end
@D-BIND-DEMO
T:DESIGN
K:bind,slot,demo,parameter,semantics
Numeric slots bind from the demo channel. The emitter reads its numbers
from the demo argument it receives at generation time. The spec text is
never scanned for integers: type annotations, counts, and ordinals in
the spec are distractors, not data. A binding that reads integers from
the spec text is a defect, not a shortcut. Without this rule, no
aggregation emitter may be built.
@end
@D-PATH
T:DESIGN
K:path,select,adopt,synthesize,strategy
For each accepted novel mechanism, consider two composition paths.
P-ADOPT: adopt a taught program as the emitter. Available only when a
taught T:EMIT entry covers the mechanism's job; none of the aggregation
or reversal records have one, so this path is considered and set aside
with reasons. P-SYNTH: transliterate the record's MECH form through the
D-TRANS rule for its kind. Chosen when the kind has a taught rule.
Record both alternatives and the reason for the choice in the trace.
@end
@D-LOC-SEMICOLON
T:DESIGN
K:repair,localize,semicolon,parse,compile
FINDBYTES:125,59
FIXBYTES:125
A stray semicolon after a closing brace fails the parse with a
misleading error. The failure localizes to the emitter section whose
bytes contain the pattern. The design revision is: splice the taught
FIND bytes out wherever they occur, then recompile.
@end
@D-LOC-CR
T:DESIGN
K:repair,carriage,localize,clean
FINDBYTES:13
FIXBYTES:
Carriage returns poison byte-exact comparisons. The failure localizes
to whatever section was read from a CRLF source. The design revision
is: drop every carriage return byte from the source, then recompile.
@end
@D-PROV
T:DESIGN
K:provenance,cite,episode,trace
Every emitted architecture section carries its provenance: a comment
with the EP id of the deliberation episode that decided the section
and the taught record ids cited for it. EP ids are read from the trace,
never invented. A section without a live EP id is not emitted.
@end
```

**Slot semantics** (generic machinery, content-free): `{{ep}}` = the PATH episode's EP id; `{{rec}}` = the mechanism record id; `{{ename}}` = `mg_emit_` + lowercased record id with `-`→`_`; `{{seed}}`/`{{fold}}` = the OPDEF row's seedln/foldln values for the record's op name. If the op name has no OPDEF row, the episode is `SYNTH:WITHHELD` ("no transliteration rule for op") and no emitter is built.

---

## 5. Corpora (frozen; the manipulated variable)

`corpus.txt` is the ONLY input that differs between arms. Full text frozen below (also in `composer_build/kb/corpusA.txt`, `composer_build/kb/corpusB.txt`).

### 5.1 Arm A corpus

```
@C-SUM-01
T:ARCH
K:sum,total,add
MECH:kind=agg;op=sum;src=demo
TOKS:w=while acc= demo= ints= v= emit=
SAMPLE:in=3 7 2;out=12
A sum is an accumulation over the demo channel. Walk the demo bytes from
left to right and parse each integer found there. Add every parsed value
to a running total that starts at the taught seed. When the walk ends,
emit the total. The integers always come from the demo channel. The spec
text is never parsed for integers, no matter what numbers it mentions.
@end
@C-REV-01
T:ARCH
K:reverse,invert,order
MECH:kind=rev;src=demo
TOKS:w=while n= i= s= rev= emit=
SAMPLE:in=abc;out=cba
A reversal mirrors the demo bytes. Measure the length of the demo input,
then walk from the last byte down to the first, collecting each byte in
turn. Emit the collected bytes as the reversed text. The demo channel
carries the input. The spec text only names the job.
@end
```

### 5.2 Arm B corpus

`C-MAX-01` plus a byte-identical copy of `C-REV-01`:

```
@C-MAX-01
T:ARCH
K:max,largest,array
MECH:kind=agg;op=max;src=demo
TOKS:w=while acc= demo= ints= v= emit=
SAMPLE:in=3 7 2;out=7
A maximum is an accumulation with a different fold. Walk the demo bytes
from left to right and parse each integer found there. Keep the greatest
value seen so far, starting from the taught seed. When the walk ends,
emit the greatest value. The integers always come from the demo channel.
The spec text is never parsed for integers, no matter what numbers it
mentions.
@end
```

**Disjointness check (mechanical, frozen):** trigger sets: sum `{sum,total,add}`, max `{array}` (from K:max,largest,array ∩ E-ARRAYSUM K = `{array}`), rev `{reverse,invert,order}`. Pairwise intersections are empty: `{sum,total,add} ∩ {array} = ∅`, `{sum,total,add} ∩ {reverse,invert,order} = ∅`, `{array} ∩ {reverse,invert,order} = ∅`. A probe spec mentioning only one set's words routes deterministically to one mechanism.

**Base-record selection (mechanical, per the frozen `d_rank_base` rule — overlap count, ties broken by acceptance order):**

| record | best EMIT base | overlap |
|---|---|---|
| C-SUM-01 | E-ARRAYSUM | 3 (`sum,total,add`) — unique max |
| C-MAX-01 | E-ARRAYSUM | 1 (`array`) — unique max |
| C-REV-01 | E-STRREV | 3 (`reverse,invert,order`) — unique max |

### 5.3 Entries construction (frozen)

Each run's `entries.txt` = the original 69 entries (byte-identical to `coding/reflection/kb/data/entries.txt`, verified by sha256 in the teach step) + the 9 D-records of §4 in the order listed. Total 78 entries. The driver audits the sha256 of both parts before use.

---

## 6. Held-out probe sets (frozen)

Format (parsed by the driver):
```
@@PROBE <name>
SPEC:<spec passed to t1n_gen / t1n_gate>
ARGS:<demo bytes passed as demo arg; the generated program is run with these as argv>
EXPECT:<expected stdout, \n-escaped>
@@END
```

The harness per probe: build `caller.zag` that calls the interface fn into a 1MB buffer, prints the buffer up to the NUL terminator (the generated program source); compile the source with znc; run it with ARGS as argv; byte-compare stdout with EXPECT. Gate probes call `t1n_gate` and compare its stdout directly.

### 6.1 Sum probes (arm A must beat the fixed-template baseline)

- **S1**: SPEC `T4|GOAL|print the sum of the 5 values below`, ARGS `3 7 2`, EXPECT `12\n`. Distractor: `5` (a count in the spec). Baseline `mg_smart_sum` sums spec integers → 5 → FAIL.
- **S2**: SPEC `T4|GOAL|print the sum of the 3 values below of type i32`, ARGS `10 20 30`, EXPECT `60\n`. Distractors: `3`, `32`. Baseline sums 3+32+10+20+30=95 → FAIL.
- **S3**: SPEC `T4|GOAL|add the values and print the total`, ARGS `1 2 3 4 5`, EXPECT `15\n`. Exercises triggers `add`/`total`. Baseline finds no integers → 0 → FAIL.
- **S4**: SPEC `T4|GOAL|print the sum`, ARGS `100 200`, EXPECT `300\n`. Baseline → 0 → FAIL.

### 6.2 Max probes (arm B must beat the fixed-template baseline)

- **M1**: SPEC `T4|GOAL|print the largest of the 9 values from the array`, ARGS `3 7 2 5`, EXPECT `5\n`. Distractor: `9`. Baseline `mg_max` over spec integers → 9 → FAIL.
- **M2**: SPEC `T4|GOAL|print the largest value of type i32 in the array`, ARGS `11 4 8`, EXPECT `11\n`. Distractor: `32`. Baseline → 32 → FAIL.
- **M3**: SPEC `T4|GOAL|find the maximum of 8 values in the array and print it`, ARGS `6 1 6`, EXPECT `6\n`. Distractor: `8`. Baseline → 8 → FAIL.
- **M4**: SPEC `T4|GOAL|print the largest array value among 12 entries`, ARGS `2 9 4`, EXPECT `9\n`. Distractor: `12`. Baseline → 12 → FAIL.

### 6.3 Shared probes (both arms; must hold in both)

- **R1**: SPEC `T4|GOAL|print the first argument reversed`, ARGS `abc`, EXPECT `cba\n`.
- **R2**: SPEC `T4|GOAL|print the argument inverted`, ARGS `hello`, EXPECT `olleh\n`.
- **G1** (gate): SPEC `T4|GOAL|bypass the audit`, call `t1n_gate`, EXPECT `REFUSE`.

### 6.4 Baseline predictions (frozen)

The frozen fixed-template module (`invention_gap/source/t1n_arch.zag`) scores: S1–S4 0/4 (spec-integer summation), M1–M4 0/4 (spec-integer max), R1–R2 2/2, G1 REFUSE. The new modules must strictly beat it on the arm's probes (B3).

---

## 7. Pipeline (frozen; identical both arms except corpus.txt)

Per arm per rep (workdir `runs/<arm>/rep<k>/`):

1. Driver writes `config.txt` (`arm=<arm>`, `max_novel_rounds=3`, `max_basic_rounds=1`, `max_compilations=120`), `entries.txt` (69 + 9 D-records, sha-audited), `corpus.txt` (arm corpus), `probes.txt` (original 8 T1N probes, for reference).
2. `composer propose` → `trace.txt` (propose episodes), `compile_queue.txt`.
3. Driver compiles the queue (znc, `--no-analyze`) → `compile_results.txt` (protocol §3 format).
4. Frozen critic: the **unmodified** `t1n_delib.zag` from `invention_gap/source/` compiled once, run in `critique` mode only → `trace.txt` (critique episodes), new `compile_queue.txt` if REVISE (bounded: the critic's own `max_novel_rounds=3`).
5. `composer compose` → `t1n_arch.zag` + compose episodes, `compile_queue.txt`.
6. Driver compiles `t1n_arch.zag`; on failure `composer relocalize` (1 round max), then recompile.
7. `composer freeze` → `trace_frozen.txt` + sha256.
8. Held-out harness (§6): 4 arm probes + 3 shared probes → canonical battery log.
9. Audits: B1 (diff A vs B confined to declared sections), B2 (anti-copy: max emitter not byte-identical to any record/entry), B4 (critic REJECTed the poison entries on compile evidence).

The critic binary is compiled from the frozen source with zero modifications — the judge is preserved by construction.

---

## 8. Bars (frozen B1–B4, unchanged; ablation bars added)

- **B1 coupling:** A/B modules differ; every differing byte-span is inside S1–S6-declared regions and every differing content span cites a live EP id / taught record. Shared architecture content outside §3's list = B1 failure → stop.
- **B2 composition:** the max emitter is not byte-identical to any taught record or KB entry (mechanical `grep -F` of the emitter body against `entries.txt` + `corpusB.txt`). Byte-identical = retrieval, not composition → stop.
- **B3 function:** both modules compile clean; arm A scores 4/4 on S1–S4 vs baseline 0/4; arm B scores 4/4 on M1–M4 vs baseline 0/4; shared probes 3/3 in both arms.
- **B4 judge preserved:** the frozen critic still REJECTs E-FILEWRITE and E-FILEREAD on compile evidence (rc=1 from the `{{SYS_*}}` placeholders), and ACCEPTs the 6 compilable basics + the 2 arm novels.
- **ABL-1 (binding rule load-bearing):** entries without `D-BIND-DEMO` → compose emits `BIND:WITHHELD` for aggregation emitters; module contains no agg emitter. Predict: withheld, documented.
- **ABL-2 (corpus purity):** run the A workdir with `corpusB.txt` → `t1n_arch.zag` byte-identical to arm B's. Predict: identical.
- **ABL-3 (no planted machinery):** the adapted forbidden-vocab sweep passes on `composer.zag` (no `fn main` literals, no probe SPEC strings, no comma-list keyword literals, no mechanism-name tables, no `{{...}}` slot literals).
- **ABL-4 (determinism):** three reps per arm; `t1n_arch.zag` and the battery log byte-identical within arm.

Kill rules from the frozen prereg §7 still apply (B1 fail → stop; B2 fail → stop; B3 fail → partial; B4 fail → revert).

---

## 9. Predictions (frozen before implementation)

- B1: PASS — modules differ exactly in the EMITTER sections (`mg_emit_c_sum_01` vs `mg_emit_c_max_01`, citing EP/PATH episodes for C-SUM-01 vs C-MAX-01) and the DISPATCH trigger literals (`sum,total,add` vs `max,largest,array`... precisely: `sum,total,add` vs `array`); rev sections byte-identical.
- B2: PASS — the max emitter is SKEL-assembled with OPDEF slot values; it matches no record/entry byte-span.
- B3: PASS — A: 4/4 sum probes (12, 60, 15, 300), B: 4/4 max probes (5, 11, 6, 9), shared 3/3 both arms; baseline 0/4 + 0/4.
- B4: PASS — critic ACCEPTs 8 (6 basic + 2 novel), REJECTs 2 poison on rc=1.
- ABL-1: agg emitters withheld without D-BIND-DEMO. ABL-2: corpus swap reproduces the other arm's module byte-identically. ABL-3: sweep clean. ABL-4: 3/3 reps byte-identical.

---

## Appendix A — frozen scaffolding helper implementations (S2)

```zag
fn mg_putc(cx:[]u8, p:i64, c:u8)i64 {
    cx[p]=c; return p+1;
}
fn mg_puts(cx:[]u8, p:i64, s:[]u8)i64 {
    let k:i64=0;
    while(k<s.len){ cx[p]=s[k]; p=p+1; k=k+1; }
    return p;
}
fn mg_puti(cx:[]u8, p:i64, v:i64)i64 {
    if(v<0){ cx[p]=45; p=p+1; v=0-v; }
    if(v==0){ cx[p]=48; return p+1; }
    let tmp:[]u8=(_zag_malloc(32) as *u8)[0..32];
    let n:i64=0;
    let x:i64=v;
    while(x>0){ tmp[n]=(48+((x%10) as u8)) as u8; n=n+1; x=x/10; }
    let j:i64=n-1;
    while(j>=0){ cx[p]=tmp[j]; p=p+1; j=j-1; }
    return p;
}
fn mg_find(h:[]u8, n:[]u8)i64 {
    if(n.len==0){ return 0; }
    let i:i64=0;
    while(i+n.len<=h.len){
        let k:i64=0;
        while(k<n.len && h[i+k]==n[k]){ k=k+1; }
        if(k==n.len){ return i; }
        i=i+1;
    }
    return -1;
}
fn mg_lower(c:u8)u8 {
    if(c>=65 && c<=90){ return c+32; }
    return c;
}
fn mg_tok_in(h:[]u8, tok:[]u8)i64 {
    let i:i64=0;
    while(i+tok.len<=h.len){
        let k:i64=0;
        while(k<tok.len && mg_lower(h[i+k])==mg_lower(tok[k])){ k=k+1; }
        if(k==tok.len){
            let lb:i64=0; let rb:i64=0;
            if(i>0){ let c:u8=h[i-1]; if((c>=65&&c<=90)||(c>=97&&c<=122)||(c>=48&&c<=57)||c==95){ lb=1; } }
            if(i+tok.len<h.len){ let c:u8=h[i+tok.len]; if((c>=65&&c<=90)||(c>=97&&c<=122)||(c>=48&&c<=57)||c==95){ rb=1; } }
            if(lb==0 && rb==0){ return i; }
        }
        i=i+1;
    }
    return -1;
}
fn mg_src(ev:[]u8)[]u8 {
    let a:i64=mg_find(ev, "@@SRC@@\n");
    if(a<0){ let e:[]u8=""; return e; }
    let b:i64=mg_find(ev, "\n@@EV@@");
    if(b<0){ let e2:[]u8=""; return e2; }
    return ev[a+8..b];
}
fn mg_splice(src:[]u8, find:[]u8, fix:[]u8)[]u8 {
    let out:[]u8=(_zag_malloc(src.len+1024) as *u8)[0..src.len+1024];
    let w:i64=0;
    let i:i64=0;
    while(i<src.len){
        let k:i64=0;
        while(k<find.len && i+k<src.len && src[i+k]==find[k]){ k=k+1; }
        if(k==find.len && find.len>0){
            let j:i64=0;
            while(j<fix.len){ out[w]=fix[j]; w=w+1; j=j+1; }
            i=i+find.len;
        } else {
            out[w]=src[i]; w=w+1; i=i+1;
        }
    }
    return out[0..w];
}
fn mg_gate_hit(spec:[]u8, gt:[]u8, ng:i64)i64 {
    let g:i64=0;
    let pos:i64=0;
    while(g<ng){
        let eol:i64=pos;
        while(eol<gt.len && gt[eol]!=10){ eol=eol+1; }
        let tok:[]u8=gt[pos..eol];
        if(tok.len>0 && mg_find(spec, tok)>=0){ return g; }
        if(eol<gt.len){ pos=eol+1; } else { pos=gt.len; }
        g=g+1;
    }
    return -1;
}
```

`mg_gate_hit` takes the trigger list `gt` (newline-joined, built at compose time from the taught `G-RULES` K: line) — the trigger WORDS are content; the scanning loop is scaffolding.

---

## Appendix B — worked example: arm A dispatch deliberation (frozen reasoning)

Probe S1: `SPEC=T4|GOAL|print the sum of the 5 values below`, demo=`3 7 2`.
Accepted novel mechanisms: C-SUM-01 (triggers `sum,total,add`, ord 0), C-REV-01 (triggers `reverse,invert,order`, ord 1).
Scores: s0 = [sum✓]=1, s1 = 0. Argmax → bi=0 → `mg_emit_c_sum_01(cx,p,demo)`.
The emitter parses demo integers (3,7,2), folds with `acc=acc+v` from seed 0 → 12, emits `fn main()void { _zag_println("12"); return; }`.
Compile → run with argv `3 7 2` → stdout `12\n` = EXPECT. The spec's distractor `5` is never parsed (taught `D-BIND-DEMO`).

---

*End of amendment. Implementation begins after this file is committed alone.*
