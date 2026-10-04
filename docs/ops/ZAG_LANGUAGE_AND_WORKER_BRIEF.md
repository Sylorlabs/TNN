# ZAG LANGUAGE REFERENCE + WORKER BRIEF
**Verified empirically on this host 2026-10-03. Read before writing any Zag.**

## 0. HARD RULE: PURE ZAG

All scientific computation must be Zag. Shell/git only for orchestration.

```sh
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
tnn_pure_zag_report     # must print: VERDICT: PURE-ZAG-CLEAN
```

Forbidden: python, node, bun, deno, tsc, cc, gcc, rustc, julia, perl, ruby, R,
make, cmake, ... They are shimmed to hard-fail (exit 127). If one runs during an
experimental wave that is a **PROCESS-FAIL**, even if harmless.

## 1. BUILD AND RUN

```sh
ZNC=/Users/Shared/micah/Documents/TNN/.bin/znc
$ZNC --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache X.zag
./X
```

**`--target macos-arm64` is MANDATORY.** Without it the compiler silently emits
x86-64 Linux ELF; compile reports success, run fails with `exec format error`.

Harness (does this for you, and checks determinism):
```sh
/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh X.zag --rep 3
```
`--rep 3` asserts 3/3 byte-identical stdout. Determinism is a preregistered bar.

Zag files are **concatenated**, not imported. No forward declarations. Order
matters. Exactly one `fn main(` per final translation unit.

## 2. TYPES - THE COMPLETE SET

| Type | Notes |
|---|---|
| `i32` | The only arithmetic type. Everything is i32 fields in a `[]u8`. |
| `i64` | decimal formatting, syscall args |
| `u8` | byte-store element |
| `[]u8` | THE universal container. Strings and byte arrays are both `[]u8`. |
| `*u8` | raw pointer from `_zag_malloc` |
| `void` | |

**There are NO floats** (no f32/f64). Use i32 fixed-point or exact integer
cross-multiplication for rational comparison. Example of exact rational compare:
`if(n1*(u2+2) < n2*(u1+2)){ /* n1/(u1+2) < n2/(u2+2) */ }`

**No arrays, no structs, no enums, no maps/dicts, no generics, no closures, no
`[][]u8`.** Every "record" is a byte-offset convention over a flat arena.

## 3. THE THREE IDIOMS YOU WILL USE CONSTANTLY

### 3.1 Allocation
```zag
fn z_alloc(n:i32)[]u8 {
  if(n<1){ return ""; }
  let p:*u8=_zag_malloc(n) as *u8;
  if(p==null as *u8){ return ""; }
  let b:[]u8=p[0..n];
  let i:i32=0;
  while(i<n){ b[i]=0; i=i+1; }
  return b;
}
```

### 3.2 Little-endian i32 cell access
```zag
fn get32(b:[]u8,off:i32)i32 {
  return (b[off] as i32)|((b[off+1] as i32)<<8)|((b[off+2] as i32)<<16)|((b[off+3] as i32)<<24);
}
fn set32(b:[]u8,off:i32,v:i32)void {
  b[off]=v as u8; b[off+1]=(v>>8) as u8; b[off+2]=(v>>16) as u8; b[off+3]=(v>>24) as u8;
  return;
}
```

### 3.3 Arena layout convention (this IS TNN's memory model)
```zag
fn WSZ()i32 { return 110656; }
fn NN()i32  { return 1024; }             // node capacity
fn NE()i32  { return 4096; }             // edge capacity
fn noff(n:i32)i32 { return 64+n*40; }    // node n record, 40 bytes
fn eoff(e:i32)i32 { return 41024+e*16; }  // edge e record, 16 bytes
fn loff(l:i32)i32 { return 106560+l*32; }
```

## 4. OUTPUT

### 4.0 READ THIS FIRST - `_zag_raw_syscall` IS INERT ON THIS HOST

Every existing canonical lane writes its results with:
```zag
fn o_flush(b:[]u8,c:i32)void {
  _zag_raw_syscall(1,1,(_zag_slice_ptr(b) as i64),c as i64,0,0,0); return;
}
```
**On this host that call produces NO OUTPUT and returns success (rc=0).** It is
not an error, it is silence. Any lane whose only output path is `o_flush`
therefore emits an EMPTY log and still reports success.

Verified directly:
```zag
let bb:[]u8=z_alloc(64);
bb[0]=79; bb[1]=75; bb[2]=10;           // "OK\n"
_zag_raw_syscall(1,1,(_zag_slice_ptr(bb) as i64),3 as i64,0,0,0);
_zag_println("D_println_OK");
```
prints ONLY `D_println_OK`. The `OK` never appears.

**THE FIX - use `_zag_print` instead. This is the required portable shim:**
```zag
fn o_flush(b:[]u8,c:i32)void {
  _zag_print(b[0..c]);
  return;
}
```

### 4.1 PROOF THIS SHIM IS CORRECT (this settles blocker B13)

The lane `cogops_learnosc2/c8_full.zag` (340948 bytes of text, a large
flat-arena learner) was rebuilt on this macOS/arm64 host with the SINGLE
substitution above and run. Result:

```
reference c8_run1.txt (Linux x86_64 era): ae0ae3bf0a82c31b6d53d14dba97e6abfb953273259d624f4869c48fb15e4ae7  3344 bytes
this host, macOS/arm64:                  ae0ae3bf0a82c31b6d53d14dba97e6abfb953273259d624f4869c48fb15e4ae7  3344 bytes
*** BYTE-IDENTICAL ***
```

Three consequences, all important:

1. **Blocker B13 is RESOLVED and was overstated.** The canonical corpus is
   fully reproducible on this host. Cross-platform determinism holds.
2. **The compiler is NOT miscompiling flat-arena indexed reads.** A separate
   worker reported "silent miscompilation of indexed reads" (barrier B16). That
   claim is DOUBTED and probably an artifact of the broken output path or of the
   reporter's own harness: this 340KB flat-arena program executes and produces
   byte-exact results. Re-verify before building architecture on B16.
3. **Any result computed on this host with an unpatched `o_flush` is
   uncitable.** Re-run with the shim.

### 4.2 Both output styles

**(a) Simple, for static lines.** `_zag_println` EXISTS and works:
```zag
fn main()i32 { _zag_println("R32_ZNC_PROBE_OK"); return 0; }
```

**(b) Dynamic content: still use ONE buffer, but flush with `_zag_print`.**
The discipline of formatting into one preallocated buffer and writing once is
correct and worth keeping; only the final call must change.
```zag
fn o_i64(b:[]u8,c:i32,v:i64)i32 {
  let neg:i32=0; let x:i64=v;
  if(x<0){ neg=1; x=0-x; }
  let n:i32=1; let t:i64=x;
  while(t>=10){ t=t/10; n=n+1; }
  let e:i32=c+neg+n; let p:i32=e-1; let y:i64=x;
  if(y==0){ b[p]=48; }
  while(y>0){ b[p]=(48+(y-(y/10)*10)) as u8; y=y/10; p=p-1; }
  if(neg==1){ b[c]=45; }
  return e;
}
fn o_app(b:[]u8,c:i32,s:[]u8)i32 {
  let i:i32=0; while(i<s.len){ b[c+i]=s[i]; i=i+1; } return c+s.len;
}
fn o_nl(b:[]u8,c:i32)i32 { b[c]=10; return c+1; }
fn o_flush(b:[]u8,c:i32)void {
  _zag_raw_syscall(1,1,(_zag_slice_ptr(b) as i64),c as i64,0,0,0); return;
}
```

Other builtins: `_zag_malloc(n)`, `_zag_slice_ptr(b)`, `_zag_raw_syscall(nr,a1..a6)`,
`_zag_print(s)` (string literals only), `_zag_eprintln(s)`,
`_zag_i64_to_str(v)` -> newline-terminated string,
`_zag_read_file(path)`, `_zag_write_file(path,b)`, `_zag_file_exists(path)`,
`_zag_strlen(s)`, `_zag_arg(i)`, `_zag_argc()`.

## 5. CONTROL FLOW GOTCHAS (these are pinned-compiler workarounds)

- **NO `for` loop.** Only `while(cond){ ... }`.
- **NO `!(A&&B)` in while conditions.** Use De Morgan: `(!A || !B)`.
- **if-nesting <= 3.** Hoist call results into a `let` first.
- `&&` and `||` do exist in `if` conditions.
- **No `!` on compound expressions in `while`.**
- `return;` written explicitly even in `void` functions.
- Casts: `v as i32`, `p as *u8`, `null as *u8`.
- **`[]u8 as *u8` is forbidden** - use `_zag_slice_ptr`.
- Recursion works and is used in the frozen core.
- Strings are NOT null-terminated `[]u8`. For syscalls convert with `z_cstr`.
- Exactly one `fn main(` per translation unit.

## 6. FILE IO (if you need it)
```zag
fn z_cstr(s:[]u8)[]u8 {           // make null-terminated copy for syscalls
  let b:[]u8=z_alloc(s.len+1);
  let i:i32=0; while(i<s.len){ b[i]=s[i]; i=i+1; }
  b[s.len]=0; return b;
}
fn fopen_r(path:[]u8)i64 { let cp:[]u8=z_cstr(path); return _zag_raw_syscall(2,(_zag_slice_ptr(cp) as i64),0,0,0,0,0); }
fn fclose(fd:i64)void { _zag_raw_syscall(3,fd,0,0,0,0,0); return; }
```
Prefer `_zag_read_file` / `_zag_write_file` when a path suffices.

## 7. FROZEN CORES YOU BUILD ON

| Core | Path | Lines | sha256 (first 12) |
|---|---|---|---|
| COGOPS frozen prefix | `cogops_learnosc2/c8_learn.zag` | 1331 | `750cb01d086f` |
| COGOPS base arena | `cogops_rescueaware/c15_base.zag` | 174 | `fc1f6e73...` |
| Contract module | `hook_phase1/hq_module.zag` | 326 | `4200e21f...` |
| TNN-2 frozen ref | `compression_exec/tnn2_frozen_ref.zag` | 1591 | `a29972ca8183` |
| L3-SUF (CODE-FROZEN) | `l3_suf_intermediate/src/` | ~2500 | see CODEFREEZE.md |

All under `docs/lab/research-lead/overnight-20260928/`.

Key COGOPS functions: `specialize_ret/vfy/cnt`, `ret_spec/vfy_spec/cnt_spec`,
`plan_find/plan_new/plan_drop`, `try_family`, `learn_bindings`, `execute_plan`,
`compose`, `g_tag/g_nneeds/need_f`, `apply_kind1/apply_kind3`, `snap_out/out_eq_snap`.

Key TNN-2 functions: `alloc_node/alloc_raw/link_edge`, `res_op`, `execute/exec_val`,
`t2_trial/t2_try_verify/mp_run`, `promote_graph`, `t2_gather`, `ev_query`,
`ev_observe/ev_teach/ev_act`, `revise_on_contradict/t2_revise_graph`, `evict_node`,
`rec_evict`, `tnn2_init`.

## 8. KNOWN ARCHITECTURAL BLOCKERS (do not rediscover; cite these)

- **B1 node-id / frame-slot namespace collision.** `res_op` reads `op>=10000`
  as a frame slot; trial literals are node ids. Workspace hits node id 10000 at
  ~1400 decoys; at `>=1000` in the smaller E1+D1 engine at ~140 MAPs. Makes
  5k/10k MAP scaling INCORRECT, not merely slow. (C299, C375.)
- **B2 global O(N) scans dominate.** N=28 takes 75-92s vs 0.3s predicted.
  Superlinear: O(N^2) MAP attempts x O(NE) scans. N=100 incomplete after 7min.
- **B3 old GEN arena hard-dimensioned for 4 MAPs.** nm=5..7 silent wrong
  answers, nm=8 panic. Superseded by GEN-REDIM (C429/C434).
- **B6 interpreter scratch overflow at program length 7.** `z_alloc(64)` too
  small; needs 128. One-line fix, genuine source-level stack overflow. (C398/C405.)
- **B7 eviction tie-break cannot hold 6 sequential new facts.** (C75.)
- **B12 frozen TNN-1 has no world-driver interface.** (C141.)
- **B13 RESOLVED 2026-10-03.** Canonical lanes DO reproduce on this host: c8_full.zag
  rebuilt with the `_zag_print` shim gives byte-identical output (see section 4.1).
- **B14 ledger mint pipeline deletes instead of appending.** Guard now installed
  at `mint_guard/mint_guard_v2.sh`. Ledger restored to C410.

## 9. THE CENTRAL NEGATIVE RESULT (context for L3 work)

The canonical ledger records **"L3 achieved anywhere: zero."** Every L3-adjacent
claim contains an explicit researcher-bounding admission:

- C285 killed C284: creation was "MENU SELECTION over 5 ops."
- C459 L3-INR-SEALED: "L3-KILLED," reclassified L2+; "incomplete-disambiguation
  trap."
- C287: "REPEAT schema researcher-enumerated; does not clear C0-B open-form bar."
- C397 GPI-3: "the learner did not invent the WRAP/SEQUENCE strategies (those
  are the frozen templates)."
- C335: "the criterion form (extremum over recency) is researcher-authored."

**Therefore: an L3 claim is only credible if the NOVEL FORM ITSELF is not
enumerable from source.** Selecting among researcher-written operators, filling
templates, or brute-force search over a fixed DSL are all explicitly NOT L3.

## 10. WORKER RULES

### 10.0 ISOLATION IS MANDATORY (wave-1 failure, do not repeat)

Wave 1 had six workers all running `git checkout -b` in the SAME directory.
They corrupted each other's branches: preregs landed on other lanes, branches
moved under active work, two workers rebuilt history. You MUST use a private
worktree:

```sh
WT=$(/Users/Shared/micah/Documents/TNN/TNN/tools/lane.sh new <your-lane-name>)
cd "$WT"          # <-- ALL your git and all your files happen in here
```

Inside that worktree, `git rev-parse --show-toplevel` must be the worktree path,
NOT /Users/Shared/micah/Documents/TNN/TNN. If it is the main repo, stop and fix
your setup before doing any work.

- Never `git checkout` in the main repo. Never switch branches there.
- Never touch another lane's files or worktree.
- Never `git commit -a`. Always explicit pathspecs.
- Your lane directory is `docs/lab/research-lead/overnight-20260928/<your-lane>/`.

### 10.1 MANDATORY EXPERIMENT TIMEOUTS (wave-2 lesson)

Wave 2 aborted mid-experiment and left two Zag binaries running as orphans
(`./p5` for 2h28m, `./t2` for 2h13m, ~90% CPU each, ppid=1). Nobody would ever
collect them. On a 10-core box that is ~1.8 cores burned for 4+ hours, and later
workers could not get CPU as a result.

**Every experiment run MUST go through the watchdog, which enforces a hard
wall-clock limit and kills the whole process group:**

```sh
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
$W reg myexp 600 ./my_binary        # 600s limit; TIMEOUT -> rc=124, killed
$W status                            # load, live runs, orphans
$W reap                              # kill orphans past the grace period
```

Rules:
- Pick the limit from your prereg and DO NOT extend it after seeing a miss.
  A timeout is recorded as FAIL/TIMEOUT exactly as the prereg specified.
- If the watchdog reports `status=EMPTY`, you produced zero bytes. That is NOT a
  result. Fix the output path (see 4.0) before interpreting anything.
- If your binary prints nothing and returns 0, you have the silent-empty-output
  defect, not a passing experiment.

### 10.2 THE MACHINE IS SHARED - plan for contention

This host is NOT dedicated to TNN. Measured concurrent foreign load includes a
colima/qemu Linux VM at 170-380% CPU running an unrelated build, 5+ opencode
sessions, Codex, Brave renderers, and vite/tauri dev servers. Load average has
been observed at 14-25 on 10 cores.

Consequences:
- Assume you get a fraction of a core at times. Do not launch 40 parallel jobs.
- Prefer many SHORT experiments over a few long ones, and always behind a timeout.
- Re-measure rather than trusting the earlier "40 concurrent compiles" figure -
  that was measured on an idle machine and does not hold under contention.
- If your work is blocked, it is more likely resource starvation than a logic
  bug. Check `$W status` before you spend time debugging your own code.



- Your goal is NOT to make the hypothesis pass. Faithfully implement the
  preregistered hypothesis. If it fails, REPORT THE FAILURE. Do not move bars.
- Prereg BEFORE implementing. Freeze fixtures, predictions, kill bars,
  baselines, ablations. Commit the prereg alone.
- New claim IDs: **use the C5xx block or higher.** C377-C466 are contested by
  the pending reconciliation and MUST NOT be minted.
- Report: STATUS, COMMITS, RESULTS, VERDICT, BOUNDARIES, NEXT EXPERIMENT.
  Be concise. Facts over prose. No marketing language.
