# BUILD / USE NOTES for the PROPERTY-ZAG modules

Lane: `propertyzag/`. Pure Zag, i32 only, flat `[]u8` arenas, `while` loops
only, if-nesting at most 3.

## Frozen-core linking, and the audit

A harness that owns `main` cannot concatenate a frozen core that also owns
`main`. The rename is mechanical and word-boundary only, applied by
`sed -E -f`:

| file | rule set | symbols renamed |
|---|---|---|
| `compression_exec/tnn2_frozen_ref.zag` | `ren_t2.sed` | `z_alloc get32 set32 emit i64s e64 main`, each prefixed `z2_` |
| `cogops_learnosc2/c8_base.zag` | `ren_c8.sed` | `z_alloc get32 set32 main`, each prefixed `z8_` |
| `cogops_learnosc2/c8_world.zag` | `ren_c8.sed` | same four |
| `cogops_learnosc2/c8_learn.zag` | `ren_c8.sed` | same four |
| `cogops_rescueaware/c15_base.zag` | byte-identical to `c8_base.zag` | same four |

ROUND-TRIP AUDIT, done in `tb.sh`: the derived `z2_core.zag` is passed through
`ren_t2_inv.sed` and compared with `cmp` against the original frozen file. The
build prints `ROUNDTRIP-OK` only if the round trip is byte-identical. The
frozen files themselves are never written to.

## How another lane calls these modules

Concatenation order matters (no forward declarations). Put the frozen core
first if you need its primitives, then the library, then your `main`:

```
cat YOUR_RENAMED_CORE.zag \
    pz_lib.zag pz_desc.zag pz_bat.zag pz_act.zag \
    pz_gen.zag pz_oracle.zag pz_meta.zag \
    YOUR_MAIN.zag > YOUR_UNIT.zag
znc --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache YOUR_UNIT.zag
```

### 1. Descriptors: point the battery at your arena

```
D  = pz_desc_tnn2();     // compression_exec/tnn2_frozen_ref.zag
D  = pz_desc_c15();      // cogops_rescueaware/c15_base.zag fact store
D  = pz_your_descriptor();   // build your own
```

Descriptor header cells are named by the `PZ_D_*` accessors in `pz_desc.zag`
(byte offsets). Set at minimum:

- `PZ_D_NOLO NCAP NOFF NSZ EOFF ESZ ECAP ASZ` (table geometry)
- `PZ_D_LCNT ECNT ALIVE TAGF SENT` (ledger cells and field indices)
- `PZ_D_MODE` = 1 for a node/edge arena, 0 for a degenerate record arena
- `PZ_D_NRULE` and the rules, via `pz_rule(D,i,tag,field,kind,flag)`
- legal tags via `pz_tset`, legal edge kinds via `pz_kset`
- `PZ_D_RESV` = count of reserved low node indices excluded from the live-count
  comparison (tnn2 reserves node 0 and node 1)
- for PZ-I13: `PZ_D_LEARN DEP ROOTF BEQ TRUEF FALSEF SEQK`

Rule kinds: `PZ_K_OPAQUE` (no check), `PZ_K_FRAME` (must be a frame operand,
`>= D_FBASE`, whose decoded slot stays inside the node table), `PZ_K_OPFRAME`
(either a frame operand or an opaque literal; the alias scan still applies),
`PZ_K_NODE` (sentinel, 0, or a live node index). Rule flag `PZ_F_ALIAS` marks
a field for the frame-operand scans (I09b, I08).

**Field indices are i32 indices into the record, not byte offsets.** The frozen
core's `ng`/`eg` take byte offsets. Getting this wrong is the single easiest
way to produce a silently wrong battery; it was made here and is documented in
the prereg amendment.

### 2. Buffers

```
TXT = pz_alloc(262144)   // text
SC  = pz_alloc(256)      // scratch, cells documented at the top of pz_bat.zag
REC = pz_alloc(3072)     // 192 machine-readable records, 16 bytes each
WK  = pz_alloc(32768)    // work buffer for the peeling passes, node-indexed
```

### 3. Detect, diagnose, contain

```
pz_beg(SC);                                   // zero the scratch
n     = pz_scan(W,D,WK,REC,TXT,SC);           // DETECT, returns total violations
pz_report(REC,SC,TXT,"MY-TAG");               // EXPLICIT DIAGNOSTICS
acts  = pz_act(W,D,REC,SC,TXT);               // CONTAIN / REPAIR
n2    = pz_scan(W,D,WK,REC,TXT,SC);           // re-scan, must be clean
h     = pz_arena_hash(W,D);                   // live-state hash
```

`pz_scan` writes into `SC` cell 8 the number of records actually stored (capped
at 192) and cell 12 the total number of violations. Read cell 12, never cell 8,
for the true count. `pz_sreset` deliberately preserves `SC` cells 0 and 4 (text
cursor and flushed byte count); an earlier version cleared them and silently
truncated every report after the first re-scan.

Useful primitives on their own:

```
pz_quarantine(W,D,n)       // tombstone a node and free its incident edges
pz_kill_edge_at(W,D,e)     // neutralise one edge, keep the ledger honest
pz_rebuild_counts(W,D)     // recompute the header counters from the tables
PZ_POISON()                // 1023, a tag outside every declared legal set
```

### 4. Generators

```
pz_stream(S,base,idx)                  // derive a reproducible PRNG stream
pz_gen_graph(W,D,S,n,m,well)           // random topology; well=1 must stay clean
pz_gen_inject(W,D,S,family)            // family 0..5, the charter-113 scenarios
pz_gen_perm(S,B,off,n)                 // Fisher-Yates bijection on [0,n)
pz_mapp(P,off,n,v)                     // apply that bijection
pz_gen_reorder(S,A,scratch,n)          // Fisher-Yates reorder of 12B records
pz_gen_world(A,S,nsub,nrel,nd,rbase,clen)  // random fact store
pz_fact(A,s,r,o)                       // append one fact, capacity 128
```

PRNG: xorshift32, `pz_srand` warms the state 8 times, all outputs masked to
31 bits so no sign extension can make the stream host-dependent.

### 5. Independent oracles

```
pz_or_ret(A,rel,obj,out,oo)  -> out      // every subject with (s,rel,obj), fact order
pz_or_vfy(A,C,OUT)           -> void     // OUT[0] = 1 iff every chain step matches
pz_or_cnt(A,rel,sb,so,nsubs,seen) -> seen // seen[4000] = distinct-object count
```

Written from the contract with different control flow from the frozen
implementations (count-then-fill, early exit, lane-local dedup). The frozen
implementations are NOT ground truth; a disagreement is reported, not resolved
by seniority.

### 6. Metamorphic transforms

```
pz_meta_rename(A,P,off,n)               // M1 entity bijection
pz_meta_rerel(A,P,off)                  // M4 relation bijection
pz_gen_reorder                          // M2 observation reorder
pz_meta_distract(A,S,nd,relbase,entbase)  // M3 irrelevant distractors
```

A behaviour change under any of these is a HIDDEN DEPENDENCY (charter 164).

### 7. Output

Use `_zag_print`. `_zag_raw_syscall` is inert on this host and a lane whose only
output path is a raw write produces an EMPTY log while reporting success. Every
driver in this lane ends with

```
pz_eflush(SC,TXT);
if(pz_get(SC,4)<1){ ... FAIL ...; return 1; }
```

## Reproduction

```
sh tb.sh pz_bat            # battery against tnn2
sh tb.sh pz_meta           # metamorphic against tnn2
sh tb.sh pz_diff "$PWD/build/z8_base.zag $PWD/build/z8_world.zag $PWD/build/z8_learn.zag"
```

Then run each binary three times and compare the sha256 of stdout.