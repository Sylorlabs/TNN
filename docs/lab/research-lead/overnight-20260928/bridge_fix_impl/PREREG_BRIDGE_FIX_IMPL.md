# PREREG BRIDGE-FIX-IMPL: Episode-persistent discovery buffer

Status: PREREG-FROZEN. No implementation exists at this commit.
Parent design: `bridge_fix/BRIDGE_FIX_DESIGN.md` (commit `791388384`).
Parent mechanism: L3 Bridge BRIDGE-TESTED (commit `ebdc4fd3e`).
Scope: `docs/lab/research-lead/overnight-20260928/bridge_fix_impl/` only.

## 1. What is being built

A modified copy of `l3_bridge_impl/bridge.zag` at commit `ebdc4fd3e`,
carried into this directory as `bridge.zag`, with exactly three
evidence-management edits in `run_family` (D1, D2, D3 below) plus the
R7 strike-termination rule from design section 4. Everything else is
carried over unchanged: all menu machinery (`fit_const`, `fit_lin`,
`fit_exc`, `fit_form`, `prior_order`, `verify_need`, `predict`), the four
generic operators, candidate generation and frozen order, the gain rule
(B_node = 0), behavioral novelty, generic HONESTFAIL, refit
structural-equivalence, `teval`, node cap, EQ cap, move budget, cost
accounting, cost ceiling, the frozen family specs (0..12), and the
`main()` battery. No new operators, no new branches keyed on pattern
type, family identity, output shape, or signature.

## 2. Frozen edits

### D1: VERIFY stores every observed example

Before (in VERIFY phase of `run_family`):

```
        // VERIFY
        let s3:i32=true_subj(fam,ei);
        let o3:i32=true_obj(fam,ei);
        let pr:i32=predict(live,st,s3);
        ei=ei+1; cost=cost+1;
```

After:

```
        // VERIFY (R3/D1: every observed example enters the
        // episode-persistent discovery buffer while n < 40)
        let s3:i32=true_subj(fam,ei);
        let o3:i32=true_obj(fam,ei);
        if(n<40){
          bset(bs,n,s3);
          bset(bo,n,o3);
          n=n+1;
        }
        let pr:i32=predict(live,st,s3);
        ei=ei+1; cost=cost+1;
```

### D2: VERIFY strike does not reset n

Before:

```
        } else {
          if(wrong>=3){
            if(live==3){
              set32(st,48,get32(st,48)+1);
            } else {
              set32(st,28+live*4,get32(st,28+live*4)+1);
            }
            live=-1;
            set32(st,0,-1);
            phase=0; n=0; vc=0; wrong=0;
          }
        }
```

After:

```
        } else {
          if(wrong>=3){
            // R3/D2: the discovery buffer is episode-persistent. Only the
            // verification counters reset; n and all observed evidence
            // are retained. R7: a strike on a live invented form ends the
            // episode as HONESTFAIL immediately.
            let struck:i32=live;
            if(struck==3){
              set32(st,48,get32(st,48)+1);
            } else {
              set32(st,28+struck*4,get32(st,28+struck*4)+1);
            }
            live=-1;
            set32(st,0,-1);
            vc=0; wrong=0;
            if(struck==3){
              adopted=-1; done=1;
            } else {
              phase=0;
            }
          }
        }
```

### D3: capacity freeze at BMAX = 40

Before (in DISCOVER phase of `run_family`):

```
    if(phase==0){
      // DISCOVER
      let s:i32=true_subj(fam,ei);
      let o:i32=true_obj(fam,ei);
      bset(bs,n,s);
      bset(bo,n,o);
      n=n+1; ei=ei+1; cost=cost+1;
```

After:

```
    if(phase==0){
      // DISCOVER (D3: appends only while n < 40)
      let s:i32=true_subj(fam,ei);
      let o:i32=true_obj(fam,ei);
      if(n<40){
        bset(bs,n,s);
        bset(bo,n,o);
        n=n+1;
      }
      ei=ei+1; cost=cost+1;
```

The REFIT strike path is unchanged (it already retains examples).

## 3. Frozen firing rules R1-R7 (from design section 4)

- R1 (menu priority, unchanged): at every DISCOVER step with n >= 6, menu
  forms 0, 1, 2 are attempted in prior_order on the full current buffer;
  the first fit is adopted for verification.
- R2 (verification, unchanged): V consecutive correct predictions adopts
  the form; 3 wrong predictions strike it.
- R3 (evidence retention, NEW): D1 and D2 from section 2. No observed
  example is discarded within an episode.
- R4 (inventor fires): iff n reaches BMAX = 40 with no menu form fitting
  the 40-point buffer and the inventor has not fired this episode. The
  search runs on the episode-global buffer. The hook code condition is
  unchanged in form (`n>=40`, menu fit attempted first, `inv_used`
  guard); its meaning is now episode-global.
- R5 (menu wins globally): if a menu form exactly fits the 40-point
  buffer, R1 adopts it before R4 can fire.
- R6 (refit path, unchanged): refit strikes already retain examples; no
  change.
- R7 (struck invented form): a VERIFY strike on a live invented form
  ends the episode as HONESTFAIL immediately (adopted=-1, done=1).

## 4. Regression contract (frozen)

The implementation worker must, in this order:

1. Copy `l3_bridge_impl/bridge.zag` at commit `ebdc4fd3e` into this
   directory and apply exactly the section 2 edits (plus a header
   comment recording provenance and this prereg; comments only).
2. Compile with the same znc toolchain and run the unmodified battery in
   `main()` three times.
3. PASS iff all three runs are byte-identical to each other AND
   byte-identical to the authoritative BRIDGE-TESTED raw output
   `l3_bridge_impl/BRIDGE_RAW_FINAL.txt` at commit `ebdc4fd3e`.
4. Any byte delta in any run fails K2. Deltas are documented and the fix
   is killed; they are not rationalized away.
5. Re-run the frozen C0-A audit M1-M4 on the modified `bridge.zag`; all
   four must pass.

Basis for expecting no change (to be verified from the comparison, not
assumed): in every BRIDGE-TESTED battery episode the terminal decision is
reached without a VERIFY strike of an adopted form, so D1-D3 do not alter
those traces.

## 5. Kill bars

- K1: this prereg frozen (D1-D3, R1-R7, regression contract) BEFORE any
  implementation commit. Satisfied by this file's commit preceding the
  implementation commit.
- K2: modified `bridge.zag` built; battery output byte-identical to
  BRIDGE-TESTED; M1-M4 pass on the modified source.
- K3: pure Zag (no Python anywhere including scratch, diagnostics, byte
  checks, verification, analysis); no em dashes in loop documentation;
  deterministic (3/3 byte-identical runs).

## 6. Out of scope (frozen)

- The sealed T-ADV5 re-evaluation is a separate task under a fresh
  prereg (per design section 8). It is not run here; the worked
  prediction in design section 5 is design validation, not a result.
- No search changes. No new operators. No new construction paths. No new
  researcher-authored semantic cases.

## 7. Reporting

The builder reports FIX-BUILT-PASS or FIX-BUILT-FAIL, naming the exact
bar or falsifier that fired. No SURVIVES claim is made here: C0-C and
C0-D remain open promotion-pipeline steps.
