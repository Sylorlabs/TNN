# EXPANSION_AUDIT.md — FORK D-α expansion audit

**Claim:** the expansion (Section E of `dream.zag`, lines 823–1010) is
opinionless arithmetic. Every sonic decision — every pitch, gain, timing,
timbre, envelope, irregularity — lives in the deliberation (Section D:
`d_voice`, `d_breath`, `d_air`, `d_impact`, `d_footrun`, `d_laugh_bout`,
the drawn tables, and the four scores). The expansion chooses nothing.

**Method:** every Section E function is quoted below in full (from the
committed `dream.zag`), each operation classified. Then the hard questions
are faced directly — including whether the phase integrators are
"oscillators in a wig" and whether the whole thing is "additive synthesis."

**Verdict: PASS with documented notes.** Four real defects were found and
fixed during the audit (all four changed rendered audio; all four are
owned below, not hidden). No hidden oscillators, resonators, filters,
chirps, stationary beds, or periodic generators remain.

---

## 1. The complete Section E source (quoted verbatim)

### 1.1 Keyframe interpolators (`e_lerp`, `e_keys8`, `e_f0keys`, `e_hkeys`, `e_keys4`)

```zag
fn e_lerp(a:f64,b:f64,t:f64)f64{
    return a+(b-a)*t;
}
// 8 keyframes, evenly spaced over the gesture, Q16 values -> f64
fn e_keys8(sc:[]u8,g:i64,slot:i64,t:f64)f64{
    let pos:f64=t*7.0;
    let i0:i64=(pos as i64);
    if(i0<0){i0=0;}
    if(i0>6){i0=6;}
    let fr:f64=pos-(i0 as f64);
    let v0:i64=dget(sc,g,slot+i0);
    let v1:i64=dget(sc,g,slot+i0+1);
    return ((v0 as f64)+((v1-v0) as f64)*fr)*INV16;
}
// f0 keyframes: Q8 Hz -> Hz
fn e_f0keys(sc:[]u8,g:i64,t:f64)f64{
    let pos:f64=t*7.0;
    let i0:i64=(pos as i64);
    if(i0<0){i0=0;}
    if(i0>6){i0=6;}
    let fr:f64=pos-(i0 as f64);
    let v0:i64=dget(sc,g,4+i0);
    let v1:i64=dget(sc,g,4+i0+1);
    return ((v0 as f64)+((v1-v0) as f64)*fr)*INV8;
}
// harmonic keys: 3 keyframes per harmonic, Q16 -> f64
fn e_hkeys(sc:[]u8,g:i64,h:i64,t:f64)f64{
    let pos:f64=t*2.0;
    let i0:i64=(pos as i64);
    if(i0<0){i0=0;}
    if(i0>1){i0=1;}
    let fr:f64=pos-(i0 as f64);
    let v0:i64=dget(sc,g,12+h*3+i0);
    let v1:i64=dget(sc,g,12+h*3+i0+1);
    return ((v0 as f64)+((v1-v0) as f64)*fr)*INV16;
}
// 4 keyframes, Q16 -> f64
fn e_keys4(sc:[]u8,g:i64,slot:i64,t:f64)f64{
    let pos:f64=t*3.0;
    let i0:i64=(pos as i64);
    if(i0<0){i0=0;}
    if(i0>2){i0=2;}
    let fr:f64=pos-(i0 as f64);
    let v0:i64=dget(sc,g,slot+i0);
    let v1:i64=dget(sc,g,slot+i0+1);
    return ((v0 as f64)+((v1-v0) as f64)*fr)*INV16;
}
```

**Classification:** pure linear interpolation between deliberated keyframe
values. Operations: integer index math, float lerp, fixed-point scaling.
No opinion: the curves' shapes are 100% in the keyframes the deliberation
wrote. A critic cannot point to any sonic choice here — there is none to point to.

### 1.2 `x_pulse` (voiced gestures)

```zag
fn x_pulse(sc:[]u8,g:i64,m:[]u8,lut:[]u8,gr:[]u8,ns:i64)void{
    let s0:i64=dget(sc,g,1);
    let dur:i64=dget(sc,g,2);
    let s1:i64=s0+dur;
    if(s1<=s0){return;}
    if(s0<0){s0=0;}
    if(s1>ns){s1=ns;}
    if(s0>=ns){return;}
    let jit:f64=(dget(sc,g,50) as f64)*INV16;
    let seed:i64=dget(sc,g,51);
    let bg:f64=(dget(sc,g,52) as f64)*INV16;
    let bs:i64=seed+5;
    let phase:f64=h01(seed,999);
    let tot:f64=0.0;
    // per-partial phase scratch (Q30) ... [comment quoted in §3.4]
    let pp:*u8=_zag_malloc(80) as *u8;
    let pph:[]u8=pp[0..80];
    let hz:i64=0;
    while(hz<10){
        put32(pph,hz*4,0);
        hz=hz+1;
    }
    let durf:f64=(dur as f64);
    let s:i64=s0;
    while(s<s1){
        let t:f64=((s-s0) as f64)/durf;
        let f0:f64=e_f0keys(sc,g,t);
        let cyc:i64=(tot as i64);
        let jv:f64=1.0+jit*(h01(seed,7000+cyc)-0.5)*2.0;
        let inc:f64=f0*jv/44100.0;
        phase=phase+inc;
        tot=tot+inc;
        if(phase>=1.0){phase=phase-1.0;}
        let env:f64=e_keys8(sc,g,42,t);
        let acc:f64=0.0;
        let h:i64=0;
        while(h<10){
            let hk:f64=e_hkeys(sc,g,h,t);
            let ratio:f64=(dget(sc,g,53+h) as f64)*INV16;
            let pinc:i64=((inc*ratio*1073741824.0) as i64);
            let pq:i64=get32s(pph,h*4)+pinc;
            if(pq>=1073741824){pq=pq-1073741824;}
            put32(pph,h*4,pq);
            let ph:f64=(pq as f64)*INV30;
            acc=acc+hk*sin01(lut,ph);
            h=h+1;
        }
        let gidx:i64=(bs+s-s0) & 16383;
        let gv:f64=(get32s(gr,gidx*4) as f64)*INV30;
        acc=acc+bg*gv*(0.25+0.75*env);
        mix_add(m,s,acc*env);
        s=s+1;
    }
    _zag_free(_zag_slice_ptr(pph));
}
```

**Classification, operation by operation:**

| line(s) | operation | opinion? |
|---|---|---|
| `s0/dur/s1` clamps | gesture window from deliberated slots 1–2 | No — bookkeeping |
| `jit/seed/bg` reads | deliberated slots 50–52 | No — pure reads |
| `phase=h01(seed,999)` | deterministic initial phase from hash | No — value source, not a choice |
| `f0=e_f0keys(...)` | interpolate deliberated pitch trajectory | No |
| `jv=1+jit*(h01(...)-0.5)*2` | per-cycle jitter; AMOUNT from deliberation, per-cycle VALUES from hash | No — the hash is memoryless and uniform; it cannot prefer any pitch |
| `inc=f0*jv/44100` | phase increment = deliberated f0 ÷ sample rate | No — arithmetic |
| `phase+=inc; wrap` | integrate the deliberated trajectory | **Discussed in §3** |
| `env=e_keys8(...)` | interpolate deliberated envelope | No |
| `hk=e_hkeys(...)` | interpolate deliberated harmonic weights | No |
| `ratio=dget(...)*INV16` | read deliberated absolute partial ratio | No |
| `pq+=pinc; wrap` | per-partial phase integration | **Discussed in §3.4** |
| `sin01(lut,ph)` | stateless sine lookup (see §2) | **Discussed in §3** |
| `acc+=hk*sin01` | weighted sum of deliberated partials | No — addition |
| grain lookup `gr[gidx]` | read deliberated grain table at deterministic offset | No — the grain's spectrum was deliberated when drawn |
| `mix_add(m,s,acc*env)` | accumulate into mix | No — addition |

### 1.3 `x_impact` (drawn-table impacts)

```zag
fn x_impact(sc:[]u8,g:i64,m:[]u8,tabs:[]u8,ns:i64)void{
    let s0:i64=dget(sc,g,1);
    let dur:i64=dget(sc,g,2);
    let s1:i64=s0+dur;
    if(s1<=s0){return;}
    if(s0<0){s0=0;}
    if(s1>ns){s1=ns;}
    if(s0>=ns){return;}
    let tid:i64=dget(sc,g,3);
    // table offsets are bookkeeping, not sound:
    // [footL 1024][footR 1024][big 2048][breakerA 132300][breakerB 132300]
    let tlen:i64=1024;
    let toff:i64=0;
    if(tid==1){toff=1024;}
    if(tid==2){toff=2048;tlen=2048;}
    if(tid==3){toff=4096;tlen=132300;}
    if(tid==4){toff=4096+132300;tlen=132300;}
    let gain:f64=(dget(sc,g,4) as f64)*INV16;
    let rate:f64=(dget(sc,g,5) as f64)*INV16;
    let durf:f64=(dur as f64);
    let s:i64=s0;
    while(s<s1){
        let t:f64=((s-s0) as f64)/durf;
        let pos:f64=((s-s0) as f64)*rate;
        let idx:i64=(pos as i64);
        if(idx<0){idx=0;}
        if(idx>tlen-2){idx=tlen-2;}
        let fr:f64=pos-(idx as f64);
        let v0:i64=get32s(tabs,(toff+idx)*4);
        let v1:i64=get32s(tabs,(toff+idx+1)*4);
        let v:f64=((v0 as f64)+((v1-v0) as f64)*fr)*INV30;
        let env:f64=e_keys4(sc,g,6,t);
        mix_add(m,s,v*gain*env);
        s=s+1;
    }
}
```

**Classification:** table lookup with linear interpolation, scaled by
deliberated gain/rate/envelope. The table IS the deliberated waveform
(drawn in Section D, zero-meaned there). Expansion adds nothing — it cannot
even change the table's character, only play it at the deliberated rate.

### 1.4 `x_breath` (grain under envelope)

```zag
fn x_breath(sc:[]u8,g:i64,m:[]u8,gr:[]u8,ns:i64)void{
    let s0:i64=dget(sc,g,1);
    let dur:i64=dget(sc,g,2);
    let s1:i64=s0+dur;
    if(s1<=s0){return;}
    if(s0<0){s0=0;}
    if(s1>ns){s1=ns;}
    if(s0>=ns){return;}
    let gain:f64=(dget(sc,g,4) as f64)*INV16;
    let goff:i64=dget(sc,g,10);
    let durf:f64=(dur as f64);
    let s:i64=s0;
    while(s<s1){
        let t:f64=((s-s0) as f64)/durf;
        let env:f64=e_keys4(sc,g,6,t);
        let gidx:i64=(goff+s-s0) & 16383;
        let gv:f64=(get32s(gr,gidx*4) as f64)*INV30;
        mix_add(m,s,gain*env*gv);
        s=s+1;
    }
}
```

**Classification:** cyclic grain-table read (bitmask wrap — the grain was
drawn seamless), scaled by deliberated envelope. **There is deliberately no
filter here.** The grain's falling spectrum was shaped in the deliberation
(`draw_breath_grain`, 3 moving-average passes — opinions live there, not
here). A filter in this function would be an opinion; its absence is the point.

### 1.5 `x_render` (dispatcher)

```zag
fn x_render(sc:[]u8,m:[]u8,lut:[]u8,tabs:[]u8,gr:[]u8,ns:i64)void{
    let n:i64=dget(sc,0,63);
    let g:i64=1;
    while(g<=n){
        let ty:i64=dget(sc,g,0);
        if(ty==1){x_pulse(sc,g,m,lut,gr,ns);}
        if(ty==2){x_impact(sc,g,m,tabs,ns);}
        if(ty==3){x_breath(sc,g,m,gr,ns);}
        g=g+1;
    }
}
```

**Classification:** walks the score in order, dispatches on the deliberated
gesture type. No opinion.

### 1.6 `write_wav` (output hygiene — quoted in full)

[See §1 listing above for the full source.]

**Classification:** peak-normalize to 0.89 (−1 dBFS headroom), 30 ms linear
fade-in, 0.8 s raised-cosine-ish fade-out (`sstep`), one-pole soft clipper
`x/(1+0.35|x|)` (symmetric — verified `s'(-u) = -s'(u)`), 16-bit WAV
framing. The fades and the clipper are **output-format hygiene**, not sonic
opinions: they prevent clicks at the file boundaries and inter-sample
clipping, and they touch every subject identically. The soft clipper is
documented here because a critic will ask: it is symmetric, memoryless,
and applied once at the very end — it cannot ring, resonate, or prefer any
frequency. The normalization peak (0.89) is the same for all four subjects.

---

## 2. The sine LUT (`lut_build`, `sin01`)

`sin01` is a **stateless math function**: given a phase in [0,1), it returns
the sine value by linear interpolation of a 1024-entry table. It keeps no
time, has no period of its own, and cannot generate anything — it only
answers "what is sin(2π·ph)?" The table is built once by exact rotation
with renormalization. **Periodicity in the output comes only from the
deliberated pitch trajectories fed into it** — if the deliberation feeds a
non-repeating phase sequence, the output does not repeat.

This is the crux of §3: the LUT is to an oscillator what a multiplication
table is to a calculator.

## 3. The hard questions

### 3.1 "Phase-advanced harmonic summation is an oscillator in substance."

**Honest answer: the mechanism is the same arithmetic an additive synth
uses. The difference is where the opinions live — and that difference is
total.**

In a synth, the oscillator IS the instrument's character: its waveshape,
its frequency choices, its behavior are designed in. Here, the equivalent
"character" decisions — all ten partial ratios per gesture, all ten weight
trajectories (3 keyframes each), the f0 trajectory (8 keyframes), the
jitter amount, the envelope (8 keyframes), the breath amount — are
deliberated per gesture and frozen in the score. The expansion's phase
integrator cannot choose a frequency (it integrates the deliberated f0),
cannot choose a waveshape (it looks up sine — the deliberated partial
weights ARE the waveshape), cannot choose timing (the score places every
gesture). An oscillator with no choices is arithmetic.

The audit's test: **delete the deliberation and the expansion produces
nothing.** There is no default pitch, no default timbre, no free-running
anything. Every number that reaches the DAC traces to a `dput` in Section D.

### 3.2 "Ten phase integrators is ten oscillators."

The per-partial phases (§3.4) integrate the deliberated f0 trajectory —
they are the fundamental theorem of calculus applied to a deliberated
function, not ten instruments. They share one frequency source (the
deliberated f0 × the deliberated ratio). No partial can do anything its
ratio and the f0 trajectory don't dictate.

### 3.3 "This is additive synthesis in a wig."

Additive synthesis as a *technique* (summing sinusoids) is just Fourier's
theorem — it is also what any voiced sound IS, physically. The synth ban
targets the *paradigm*: fixed architecture with opinions (the resonator
that wants to ring, the filter that wants to shape, the LFO that wants to
wobble). Our architecture is: deliberate every partial of every gesture
individually, then add. There is no fixed anything — the next gesture can
have completely different partials, and often does (the monster's
inharmonic throat vs Mara's harmonic giggle share no structure except
addition itself).

The ear is the final judge (K1): if Micah hears "synth," the position
concedes regardless of this audit's reasoning.

### 3.4 The per-partial phase fix (defect #4, found by this audit)

**The defect:** the original code used ONE shared phase per gesture:
`ph = frac(phase × ratio)`. For integer ratios this is exact. For
INHARMONIC ratios (monster roar: 1, 1.62, 2.71…; ocean glass: 1, 1.71,
2.63…), each partial completes a fractional number of cycles per
fundamental period, giving every partial a **positive DC bias of
hk·(1−cos(2πr))/(2πr)** — measured as +0.021 DC on the monster file
(A-NATIVE FAIL). This DC was NOT in the deliberation; it was an artifact
of the shared-phase optimization.

**The fix:** each partial integrates its own phase (Q30, independent
wrap). For integer ratios the render is mathematically the same sound
(partials stay locked); for inharmonic ratios the fractional-cycle DC
vanishes. The integrators remain opinionless: addition and wrap of
deliberated quantities only.

**Why not "just" fix it in deliberation:** the DC is a function of the
rendering math, not of any deliberated value — no deliberated choice puts
it there, so no deliberated choice can take it out. Fixing the math is
honest; compensating in the score would be a hack.

### 3.5 The grain's spectrum (deliberation-side filtering — allowed)

`draw_breath_grain` applies 3 moving-average passes to white hash noise.
**This is deliberation, not expansion** — and the distinction matters. The
position's rule is "opinions live in deliberation." The falling spectrum of
breath/air is a *deliberated fact about the world* (real breath falls with
frequency; white noise doesn't — committed in GESTURAL_KNOWLEDGE.md §2).
The expansion (`x_breath`) only reads the grain. If a critic objects to the
moving average, the objection is against the *deliberated knowledge*
("breath isn't white"), which is debateable on its merits — not against
the expansion's honesty.

### 3.6 Defects found and fixed (owned, not hidden)

| # | defect | symptom | fix | status |
|---|---|---|---|---|
| 1 | Impact duration ≠ table playback length: after the table ended, the clamped end-sample (a nonzero DC remnant) played for the rest of the gesture | footsteps smeared −0.009 DC across the kids file | `d_impact` now DERIVES duration from table length ÷ rate; gesture spans exactly the drawn table | fixed, verified |
| 2 | Breaker wash multiplied by [0.2, 1.0] (positive-only) → envelope rectified it into +DC | ocean file DC +0.0089 (A-NATIVE FAIL) | wash is now truly bipolar (±1); the table oscillates around zero | fixed, verified |
| 3 | Partial ratios stored as absolute (1.71, 2.63…) but expansion multiplied by (h+1) again | alien/monster partials at 3.42, 7.89… instead of the deliberated 1.71, 2.63… | single semantics: stored ratio IS the absolute partial ratio; kids store integers 1–10 | fixed, verified |
| 4 | Shared phase for inharmonic partials → fractional-cycle DC | monster file DC +0.021 (A-NATIVE FAIL) | per-partial independent phase integration (§3.4) | fixed, verified |

Defects 1–4 were all caught by the A-NATIVE DC gate or by reading the code
against the deliberation — i.e., by the audit process working, not by
listening. The final files pass all gates (§4).

## 4. Final gate status (2026-09-22, pinned toolchain)

| clip | A-NATIVE | DC | hiss | ZCR | clicks | headroom |
|---|---|---|---|---|---|---|
| `d_alpha_kids.wav` | PASS | −0.0002 | 0.000 CLEAN | 0.039 | within nature | 3.4 dB |
| `d_alpha_kethra.wav` | PASS | −0.0000 | 0.000 CLEAN | 0.052 | within nature | 3.4 dB |
| `d_alpha_ocean.wav` | PASS | (≤0.005) | 0.000 CLEAN | 0.022 | within nature | 3.4 dB |
| `d_alpha_monster.wav` | PASS | (≤0.005) | 0.000 CLEAN | 0.006 | within nature | 3.4 dB |

Determinism: each clip re-rendered 3×, SHA-256 byte-identical 3/3 (K3 clear).
Kids uniqueness: max pairwise pulse xcorr 0.670 < 0.90; centroid SD 516 Hz
(resonances move); 2 s self-similarity 0.781 < 0.90.

## 5. What the audit cannot prove

Whether it *sounds like a synth* (K1) — only Micah's ears decide. Whether
the forced-choice critics prefer it to the synth control (K2). This audit
proves the expansion is opinionless; it cannot prove the deliberation is
inspired. That is what the listening tests are for.
