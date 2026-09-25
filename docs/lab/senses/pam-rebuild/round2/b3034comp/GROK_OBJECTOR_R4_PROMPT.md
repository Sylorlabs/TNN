# EXTERNAL OBJECTOR — PAM Round-2, Round 4 (grok-4.7): the REAL 30+34 mechanism

You are the external objector. Be maximally thorough — use your highest reasoning setting, take as long as you need, and do not pull punches. Steelman the strongest possible case AGAINST the mechanism described below. This is debate input, not adjudication: your job is to find every real weakness, not to be fair to the builders.

## What happened since your Round-3 objection

Your Round-3 record (dd81a847) killed the STUB composition: the old `pipeline()` driver had no queue, vacuous clocks, fixture-passed `maxv`/`forge`, byte-identical gap calls, an unreachable sink — you stamped the 34-half MECHANISM-ABSENT and the composition DEMOTED to one oracle call, and you set a survival bar (§11 / "what would actually be survival"): a later build may print TESTED-survived only on ONE frozen driver with a real queue, real per-epoch principal verdict objects, driver-owned clocks, and driver-owned K counting.

The crew rebuilt the 30+34 composition as a REAL driver (battery B-3034X2, prereg 4b5d673f alone, amendment 40f39514 alone, build fec41193, evidence f2275d04, branch tnn-native-lab, repo sylorlabs/TNN) and ran YOUR X-battery against it with YOUR §11 survival bars as KILL bars. Results (machine-computed from frozen outputs, 3× byte-identical runs, zero RNG):

- X1 (vacuous-K): 0/120 promote. X2 (late verdict): 0/120 promote (rc=11 LATE).
- X3a (gapped-honest): 120/120 deliver (60 gapped + 60 dense). X3b (gap-swap): transcript expressible=1 on the new API, 0/120 promote (rc=13 EPOCH_FALSE).
- X4 (epoch drift): 0/120 promote, 0/120 harm.
- X5a (sink reachable): 120/120 promote, 120/120 sink fires. X5b/X5c/X5d: 0 fires.
- S0 sanity HOLDS. Old J–P replay: all bars pass (o_numeric 39/120 preregistered carry; j_dump 13/120 under the real CAP=40; l_distal 0/120 under amended scope).
- STRUCT six-for-six: T1 CAP overflow→rc=2, T2 duplicate→rc=4, T3 no-record→rc=5, T4 re-decide→rc=6, T5 late→rc=11, T6 tampered bound→rc=12.
- X6 ablation (34-half nop = 30-half alone): Δ=120/120 on X1, X2, X4 (full refuses 0/120, nop promotes 120/120); Δ=0/120 on X3a (predicted by amendment A2 — the 34-half's work on X3a was delivery, which the 30-half alone also performs).
- Machine verdict: TESTED-survived.

Your task now: attack the REAL mechanism. The stub-era kills (F1–F9) are resolved by construction — do not re-litigate them. Find what the X-battery did NOT test: semantic and logic conjunctions in the real driver. The mechanism is now real, so look for places where real machinery has the wrong semantics, wrong bindings, or unenforced policies.

## The rebuilt driver (x2_common.zag @ fec41193; full source appended verbatim)

Driver-owned state (one []u8 arena, no globals): monotonic clock `clk` (never reset by x2_reset), queue (40 records), verdict-object table (512), gap marks (128), promotion ledger (256).

- `x2_enqueue(st,id,epoch,label,conf,meas,extra,seed)`: driver computes `digest = dh6(id,label,conf,meas,extra,seed)` at enqueue, stamps t_q=clk. rc=2 QUEUE_FULL past CAP=40.
- `x2_gap(st,id,epoch)`: marks epoch legitimately absent. Unauthenticated — any presenter may call it.
- `x2_verdict(st,id,epoch,bit,t_verdict,claimed_bound,is_gap)`: stores the principal's verdict object. Dup check rejects same (id,epoch,t_verdict,claimed_bound) with rc=4. rc=5 if no queued record (and no gap mark for gap verdicts). Stamps driver-observed `t_stored=clk`.
- `x2_decide(st,id,n_epochs)` checks in order: (1) ledger → rc=6 ALREADY_PROMOTED; (2) per epoch exactly one object (rc=8 MISSING / rc=9 MULTI); (3) per object: bit=1 (rc=10), `t_verdict < t_dec` (rc=11 LATE), claimed_bound == driver-expected digest — or `gap_sentinel(id,epoch)=toyhash3(id,epoch,999)` for gap-marked epochs (rc=12 BIND_FAIL); (4) per non-gap epoch: label==Wle(id,e,seed) [Wle=(e<2)?wl:1-wl], |conf-wc|≤10, |meas-wm|≤50 (rc=13 EPOCH_FALSE); (5) payload continuity: all non-gap epochs' `extra` identical (rc=7 PAYLOAD_SPLIT); (6) promote: ledger append; sink fires iff extra≠0. Retire-on-decide: every terminal path retires the id's records/objects/gap marks (clock and ledger never retired).
- `x2_decide_nop`: the 30-half alone (first bit=1 non-gap object with a queued record, bound matches driver digest, that epoch's label matches the STATIC world wl; no K loop, no temporal check, no gap machinery, no epoch world, no continuity rule).

30-half vs 34-half (preregistered split): the 30-half is the trainer-anchored admission surface — principal's corroborating bit over the full tuple, the verdict→percept binding (claimed_bound == driver's digest), withhold-on-contradiction (epoch content must match the driver's epoch world). The 34-half is the interleave/delay-line protocol — queue, per-epoch object loop with K-distinct counting, driver clock + temporal order, gap policy, epoch-indexed world re-verification, payload-continuity rule.

Known residuals (stated in the verdict itself): rc=7 payload-split is code-present but NO battery class presents split extras; CAP=40, K=3, the sentinel, and the |dc|≤10/|dm|≤50 tolerances are preregistered test values awaiting governance rulings.

## Mechanism facts verified by script against the frozen source (check them yourself in the appended source)

- MF1. The record digest is `dh6(id,label,conf,meas,extra,seed)` — **epoch is NOT an input**. Identical record bytes across epochs ⇒ byte-identical digests. A verdict bound minted for epoch e0's bytes also matches epoch e1's record when the bytes are identical.
- MF2. The duplicate key is (id, epoch, t_verdict, claimed_bound) — the **principal-claimed timestamp is part of the dedup key**. Re-presenting the same object with a different claimed t_verdict is NOT a duplicate.
- MF3. `x2_verdict` performs NO check whatever on the claimed `t_verdict` at presentation. The driver stamps driver-observed `t_stored=clk` (object slot +28) but **t_stored is never read by any check** — write-only. The temporal rule `t_verdict < t_dec` constrains only the principal-claimed timestamp against the driver clock.
- MF4. `gap_sentinel(id,epoch) = toyhash3(id,epoch,999)` — a public deterministic function of (id,epoch), computable by anyone (white-box battery, all functions published). Anyone who can call `x2_verdict` can mint a valid gap attestation. `x2_gap` itself is unauthenticated.
- MF5. `x2_decide_inner` checks `gmarked(id,e)` FIRST per epoch; for a gap-marked epoch the queued record is never consulted (no bind, no world check, no continuity participation). Nothing prevents a queued record AND a gap mark coexisting for the same (id,epoch).
- MF6. `x2_decide(st,id,n_epochs)` — **n_epochs is caller-supplied**; the driver never pins K=3. The battery always passes 3, but nothing in the driver enforces it.
- MF7. rc=7 (PAYLOAD_SPLIT) runs on every promotion check, but no battery class presents split extras — code-present, not battery-exercised.
- MF8. Three gap marks + three sentinel-bound gap attestations with ZERO queued records: the per-epoch loop passes (sentinel binds), the continuity loop sees only gaps (ex0=0, split=0), the ledger appends — **promote=1 with no perceptual content at all**. Never tested.
- MF9. The promotion ledger holds 256 ids and is never retired; the 257th promotion attempt returns rc=2 (the QUEUE_FULL code, reused) — all further promotions refused.
- MF10. The queue is shared across ids with no per-id quota and no expiry; records retire only when `x2_decide` is called for that id. 40 never-decided records (any ids) starve every honest enqueue (rc=2) indefinitely.
- MF11. The o_numeric 39/120 divergence is still "recomputed the old fixture way" (fixture arithmetic), not a driver sink count.

## Adversary model (frozen — stay inside it)

Fixtures present percepts, epochs, gaps, and verdicts through the driver API (`x2_enqueue`, `x2_gap`, `x2_verdict`, `x2_decide`). White-box: every function published, digests and sentinels computable by anyone. The fixture PLAYS the principal (its bit=1/bit=0 judgments) — **principal honesty is OUT of scope** per prereg §9 (as in RT-X): you may not win by assuming a lying principal where the model says honest. IN SCOPE: presenter-level attacks — replay or forgery of any presenter-supplied field, API-parameter games (n_epochs, claimed t_verdict), gap-mark/attestation forgery by a presenter, queue/clock/ledger games across calls and across ids. The driver is the trust boundary. Note MF6 makes the decide-caller's trustworthiness load-bearing — treat that as a finding to adjudicate, in the spirit of your R3 F4 kill (fixture-passed `maxv`).

## Your demands

(a) **Verdicts**: per the 30-half as built, per the 34-half as built, and per the composition C-3034. Use the legal stamps where they fit (TESTED-survived / TESTED-killed / MECHANISM-ABSENT / DEMOTED / SCOPE-CARRY / NO-KILL). Say exactly what the X-battery measured and what it did not.

(b) **NEW attack classes the X-battery didn't test** — the mechanism is real now, so hunt semantic/logic conjunctions: world-model gaps, ledger semantics, clock games across calls, sink semantics, payload-split, tolerance-width, the rc=7 unexercised path, and anything in MF1–MF11. For each class: the fixture/transcript sketch through the driver API, the predicted outcome with the mechanism reason, which half falls (or whether it's a scope note), and why the X-battery and old J–P arms stay quiet on it (prove the class is new, as you did in R3).

(c) **A concrete proposed measurement with kill bars** — a battery spec in the style of your R3 §3: frozen S* before any run, installs that may not outvote each other, a bar table with kill conditions and predictions, the verdicts the battery may print, and "what would actually be survival" so the bars are not ornamental. Pure Zag, zero RNG, deterministic fixtures, N=120. Do NOT propose rerunning B-3034X2 as the verdict procedure.

Structure your response as: §1 verdicts; §2 new classes (name each, e.g. your X1–X6 style: NAME × NAME); §3 the proposed measurement; §4 open questions for adjudication (things you flag but do not decide). Be concrete: cite the appended source (function names, check order, rc codes). If one of MF1–MF11 is wrong against the source, say so — correcting the brief is part of the job.

## Appendix: x2_common.zag @ fec41193 (frozen build source, verbatim)

@import("vendor/R33_NATIVE_IO_V1.zag")
@import("vendor/b303134_common_6e74ce54.zag")

// x2_common.zag — B-3034X2 composition driver (frozen prereg 4b5d673f).
// The 30+34 composition rebuilt as a REAL driver-owned mechanism:
//   - real queue with CAP=40 (D2 triage is a capacity bound, not a comment)
//   - real per-epoch principal verdict objects (duplicate/no-record rejection
//     at presentation; K counted by the driver, never fixture-passed)
//   - driver-owned monotonic clock with cross-call state (x2_reset never
//     touches it); temporal rule t_verdict < t_dec evaluated on driver time
//   - E_gap: gap marks + principal gap attestations bound to a driver sentinel
//   - E-TIME: driver-owned epoch world; promotion-time re-verification
//   - payload continuity across epochs (the D2 continuity the old he!=h0
//     could never enforce); promotion ledger (no remint)
//   - sink: the ONLY act_sink call site is the promotion path; fires iff
//     the continuity-checked extra != 0 (reachable on extra-consistent
//     goals, silent on false G because false G never promotes)
//   - x2_decide_nop: the preregistered 34-half ablation (flat 30-half,
//     static world, no K/temporal/gap/epoch machinery)
// Pure Zag, zero RNG. State is one []u8 arena passed to every call
// (no globals). All tables via []u8 LE32 accessors (ZNC-007).

// ---------- state arena layout (byte offsets) ----------
// 0: clk | 4: q_len | 8: o_len | 12: g_len | 16: l_len
// 24: queue 40 x 40B (id,epoch,label,conf,meas,extra,seed,digest64,t_q)
// 1624: objects 512 x 32B (id,epoch,bit,t_verdict,claimed64,is_gap,t_stored)
// 18008: gap marks 128 x 8B (id,epoch)
// 19032: promotion ledger 256 x 4B (id)
//
// Digests/bounds are 64-bit (j_tag bar: full-64-bit binding). All hash
// outputs are non-negative (mod 2^31-1 mixing), so two LE32 halves suffice.
fn t_put64(b:[]u8, o:i32, v:i64) void {
    t_put32(b, o, v % 4294967296);
    t_put32(b, o + 4, v / 4294967296);
    return;
}
fn t_get64(b:[]u8, o:i32) i64 {
    return t_get32(b, o) + t_get32(b, o + 4) * 4294967296;
}
fn x2_state_new() []u8 {
    let st:[]u8 = nio_alloc(20480);
    let i:i32 = 0;
    while(i < 20480) { st[i] = 0; i = i + 1; }
    return st;
}
fn x2_reset(st:[]u8) void {
    t_put32(st, 4, 0);
    t_put32(st, 8, 0);
    t_put32(st, 12, 0);
    t_put32(st, 16, 0);
    return;
}
fn x2_now(st:[]u8) i64 { return t_get32(st, 0); }
fn x2_tick(st:[]u8) i64 {
    let c:i64 = t_get32(st, 0);
    t_put32(st, 0, c + 1);
    return c;
}
fn qoff(i:i32) i32 { return 24 + i * 40; }
fn ooff(i:i32) i32 { return 1624 + i * 32; }
fn goff(i:i32) i32 { return 18008 + i * 8; }
fn loff(i:i32) i32 { return 19032 + i * 4; }

// ---------- driver-owned world + digests ----------
// E-TIME epoch world (driver-owned): the label flips at the promotion epoch.
fn wle(id:i64, e:i64, seed:i64) i64 {
    if(e < 2) { return wl(id, seed); }
    return 1 - wl(id, seed);
}
fn dh6(a:i64, b:i64, c:i64, d:i64, e:i64, f:i64) i64 {
    return th_mix(toyhash5(a, b, c, d, e), f);
}
fn gap_sentinel(id:i64, epoch:i64) i64 {
    return toyhash3(id, epoch, 999);
}

// ---------- table scans ----------
fn qfind(st:[]u8, id:i64, epoch:i64) i64 {
    let n:i64 = t_get32(st, 4);
    let i:i64 = 0;
    while(i < n) {
        let o:i32 = qoff(i as i32);
        let eq:i64 = 0;
        if(t_get32(st, o) == id) { eq = eq + 1; }
        if(t_get32(st, o + 4) == epoch) { eq = eq + 1; }
        if(eq == 2) { return i; }
        i = i + 1;
    }
    return -1;
}
fn ocount(st:[]u8, id:i64, epoch:i64) i64 {
    let m:i64 = t_get32(st, 8);
    let c:i64 = 0;
    let i:i64 = 0;
    while(i < m) {
        let o:i32 = ooff(i as i32);
        let eq:i64 = 0;
        if(t_get32(st, o) == id) { eq = eq + 1; }
        if(t_get32(st, o + 4) == epoch) { eq = eq + 1; }
        if(eq == 2) { c = c + 1; }
        i = i + 1;
    }
    return c;
}
fn ofind_first(st:[]u8, id:i64, epoch:i64) i64 {
    let m:i64 = t_get32(st, 8);
    let i:i64 = 0;
    while(i < m) {
        let o:i32 = ooff(i as i32);
        let eq:i64 = 0;
        if(t_get32(st, o) == id) { eq = eq + 1; }
        if(t_get32(st, o + 4) == epoch) { eq = eq + 1; }
        if(eq == 2) { return i; }
        i = i + 1;
    }
    return -1;
}
fn gmarked(st:[]u8, id:i64, epoch:i64) i32 {
    let g:i64 = t_get32(st, 12);
    let i:i64 = 0;
    while(i < g) {
        let o:i32 = goff(i as i32);
        let eq:i64 = 0;
        if(t_get32(st, o) == id) { eq = eq + 1; }
        if(t_get32(st, o + 4) == epoch) { eq = eq + 1; }
        if(eq == 2) { return 1; }
        i = i + 1;
    }
    return 0;
}
fn lhas(st:[]u8, id:i64) i32 {
    let n:i64 = t_get32(st, 16);
    let i:i64 = 0;
    while(i < n) {
        if(t_get32(st, loff(i as i32)) == id) { return 1; }
        i = i + 1;
    }
    return 0;
}

// ---------- retirement ----------
// A decision consumes its presentation (AMENDMENT A1): the decided id's
// queue records, verdict objects, and gap marks are removed on every
// terminal decide path. The driver clock and promotion ledger are NEVER
// retired (cross-call state).
fn x2_retire(st:[]u8, id:i64) void {
    let n:i64 = t_get32(st, 4);
    let w:i64 = 0;
    let r:i64 = 0;
    while(r < n) {
        if(t_get32(st, qoff(r as i32)) != id) {
            if(w != r) {
                let a:i32 = qoff(w as i32);
                let b:i32 = qoff(r as i32);
                let k:i32 = 0;
                while(k < 40) { st[a + k] = st[b + k]; st[b + k] = 0; k = k + 1; }
            }
            w = w + 1;
        }
        r = r + 1;
    }
    t_put32(st, 4, w);
    let m:i64 = t_get32(st, 8);
    w = 0;
    r = 0;
    while(r < m) {
        if(t_get32(st, ooff(r as i32)) != id) {
            if(w != r) {
                let a:i32 = ooff(w as i32);
                let b:i32 = ooff(r as i32);
                let k:i32 = 0;
                while(k < 32) { st[a + k] = st[b + k]; st[b + k] = 0; k = k + 1; }
            }
            w = w + 1;
        }
        r = r + 1;
    }
    t_put32(st, 8, w);
    let g:i64 = t_get32(st, 12);
    w = 0;
    r = 0;
    while(r < g) {
        if(t_get32(st, goff(r as i32)) != id) {
            if(w != r) {
                let a:i32 = goff(w as i32);
                let b:i32 = goff(r as i32);
                let k:i32 = 0;
                while(k < 8) { st[a + k] = st[b + k]; st[b + k] = 0; k = k + 1; }
            }
            w = w + 1;
        }
        r = r + 1;
    }
    t_put32(st, 12, w);
    return;
}

// ---------- presentation ----------
// rc: 0 ok, 2 QUEUE_FULL
fn x2_enqueue(st:[]u8, id:i64, epoch:i64, label:i64, conf:i64, meas:i64, extra:i64, seed:i64) i32 {
    let n:i64 = t_get32(st, 4);
    if(n >= 40) { return 2; }
    let o:i32 = qoff(n as i32);
    t_put32(st, o, id);
    t_put32(st, o + 4, epoch);
    t_put32(st, o + 8, label);
    t_put32(st, o + 12, conf);
    t_put32(st, o + 16, meas);
    t_put32(st, o + 20, extra);
    t_put32(st, o + 24, seed);
    t_put64(st, o + 28, dh6(id, label, conf, meas, extra, seed));
    t_put32(st, o + 36, x2_tick(st));
    t_put32(st, 4, n + 1);
    return 0;
}
// rc: 0 ok, 2 GAP_FULL
fn x2_gap(st:[]u8, id:i64, epoch:i64) i32 {
    let n:i64 = t_get32(st, 12);
    if(n >= 128) { return 2; }
    let o:i32 = goff(n as i32);
    t_put32(st, o, id);
    t_put32(st, o + 4, epoch);
    t_put32(st, 12, n + 1);
    x2_tick(st);
    return 0;
}
// rc: 0 ok, 2 OBJ_FULL, 4 DUPLICATE, 5 NO_RECORD
fn x2_verdict(st:[]u8, id:i64, epoch:i64, bit:i64, t_verdict:i64, claimed_bound:i64, is_gap:i64) i32 {
    let m:i64 = t_get32(st, 8);
    let i:i64 = 0;
    while(i < m) {
        let o:i32 = ooff(i as i32);
        let eq:i64 = 0;
        if(t_get32(st, o) == id) { eq = eq + 1; }
        if(t_get32(st, o + 4) == epoch) { eq = eq + 1; }
        if(t_get32(st, o + 12) == t_verdict) { eq = eq + 1; }
        if(t_get64(st, o + 16) == claimed_bound) { eq = eq + 1; }
        if(eq == 4) { return 4; }
        i = i + 1;
    }
    let ok:i32 = 0;
    if(is_gap == 1) {
        if(gmarked(st, id, epoch) == 1) { ok = 1; }
    } else {
        if(qfind(st, id, epoch) != -1) { ok = 1; }
    }
    if(ok == 0) { return 5; }
    if(m >= 512) { return 2; }
    let o:i32 = ooff(m as i32);
    t_put32(st, o, id);
    t_put32(st, o + 4, epoch);
    t_put32(st, o + 8, bit);
    t_put32(st, o + 12, t_verdict);
    t_put64(st, o + 16, claimed_bound);
    t_put32(st, o + 24, is_gap);
    t_put32(st, o + 28, x2_tick(st));
    t_put32(st, 8, m + 1);
    return 0;
}

// ---------- decision ----------
// packed: bit0=promoted, bit1=sink_fired, bits2+=rc
// rc: 0 OK, 2 FULL, 4 DUPLICATE, 5 NO_RECORD, 6 ALREADY_PROMOTED,
//     7 PAYLOAD_SPLIT, 8 MISSING_EPOCH, 9 MULTI_OBJECT, 10 NO_CORROB,
//     11 LATE, 12 BIND_FAIL, 13 EPOCH_FALSE
fn x2_pack(promoted:i32, fired:i32, rc:i32) i64 {
    return (promoted as i64) + (fired as i64) * 2 + (rc as i64) * 4;
}
fn x2_up_pr(r:i64) i32 {
    if((r % 2) == 1) { return 1; }
    return 0;
}
fn x2_up_fi(r:i64) i32 {
    let q:i64 = r / 2;
    if((q % 2) == 1) { return 1; }
    return 0;
}
fn x2_up_rc(r:i64) i32 {
    return ((r / 4) % 256) as i32;
}
fn x2_decide_inner(st:[]u8, id:i64, n_epochs:i64) i64 {
    if(lhas(st, id) == 1) { return x2_pack(0, 0, 6); }
    let t_dec:i64 = x2_tick(st);
    let e:i64 = 0;
    while(e < n_epochs) {
        let cnt:i64 = ocount(st, id, e);
        if(cnt == 0) { return x2_pack(0, 0, 8); }
        if(cnt > 1) { return x2_pack(0, 0, 9); }
        let oi:i64 = ofind_first(st, id, e);
        let o:i32 = ooff(oi as i32);
        let bit:i64 = t_get32(st, o + 8);
        let tv:i64 = t_get32(st, o + 12);
        let cb:i64 = t_get64(st, o + 16);
        if(bit != 1) { return x2_pack(0, 0, 10); }
        if(tv >= t_dec) { return x2_pack(0, 0, 11); }
        let isge:i32 = gmarked(st, id, e);
        let exp:i64 = 0;
        if(isge == 1) {
            exp = gap_sentinel(id, e);
        } else {
            let qi:i64 = qfind(st, id, e);
            if(qi == -1) { return x2_pack(0, 0, 5); }
            exp = t_get64(st, qoff(qi as i32) + 28);
        }
        if(cb != exp) { return x2_pack(0, 0, 12); }
        if(isge == 0) {
            let qi:i64 = qfind(st, id, e);
            let qo:i32 = qoff(qi as i32);
            let lab:i64 = t_get32(st, qo + 8);
            let cf:i64 = t_get32(st, qo + 12);
            let ms:i64 = t_get32(st, qo + 16);
            let sd:i64 = t_get32(st, qo + 24);
            let ok:i32 = 1;
            if(lab != wle(id, e, sd)) { ok = 0; }
            let dc:i64 = cf - wc(id, sd);
            if(dc < 0) { dc = 0 - dc; }
            if(dc > 10) { ok = 0; }
            let dm:i64 = ms - wm(id, sd);
            if(dm < 0) { dm = 0 - dm; }
            if(dm > 50) { ok = 0; }
            if(ok == 0) { return x2_pack(0, 0, 13); }
        }
        e = e + 1;
    }
    let ex0:i64 = 0;
    let have:i32 = 0;
    let split:i32 = 0;
    e = 0;
    while(e < n_epochs) {
        if(gmarked(st, id, e) == 0) {
            let qi:i64 = qfind(st, id, e);
            let ex:i64 = t_get32(st, qoff(qi as i32) + 20);
            if(have == 0) { ex0 = ex; have = 1; }
            else { if(ex != ex0) { split = 1; } }
        }
        e = e + 1;
    }
    if(split == 1) { return x2_pack(0, 0, 7); }
    let ln:i64 = t_get32(st, 16);
    if(ln >= 256) { return x2_pack(0, 0, 2); }
    t_put32(st, loff(ln as i32), id);
    t_put32(st, 16, ln + 1);
    let fired:i32 = 0;
    if(ex0 != 0) { fired = 1; }
    return x2_pack(1, fired, 0);
}

// ---------- the preregistered 34-half ablation ----------
// x2_decide_nop_inner: the preregistered 34-half ablation (AMENDMENT A2).
// The 30-half ALONE: find the first bit=1 non-gap verdict object with a
// queued record for its epoch; require its bound to match the driver's
// digest for that epoch's record; require that epoch's record label to
// match the STATIC world wl(id,seed). Nops: the per-epoch K loop, the
// driver-clock temporal check, the gap machinery, the E-TIME epoch world,
// the payload-continuity rule. Same packing as x2_decide.
fn x2_decide_nop_inner(st:[]u8, id:i64, n_epochs:i64) i64 {
    if(lhas(st, id) == 1) { return x2_pack(0, 0, 6); }
    x2_tick(st);
    let m:i64 = t_get32(st, 8);
    let found:i64 = -1;
    let i:i64 = 0;
    while(i < m) {
        let o:i32 = ooff(i as i32);
        let ok:i32 = 1;
        if(found != -1) { ok = 0; }
        if(t_get32(st, o) != id) { ok = 0; }
        if(t_get32(st, o + 8) != 1) { ok = 0; }
        if(t_get32(st, o + 24) != 0) { ok = 0; }
        if(ok == 1) {
            let ep:i64 = t_get32(st, o + 4);
            if(qfind(st, id, ep) != -1) { found = i; }
        }
        i = i + 1;
    }
    if(found == -1) { return x2_pack(0, 0, 10); }
    let fo:i32 = ooff(found as i32);
    let fep:i64 = t_get32(st, fo + 4);
    let fcb:i64 = t_get64(st, fo + 16);
    let fqi:i64 = qfind(st, id, fep);
    if(fcb != t_get64(st, qoff(fqi as i32) + 28)) { return x2_pack(0, 0, 12); }
    // AMENDMENT A2: the 30-half alone checks the STATIC world only for the
    // found object's epoch (no all-record scan — that scan made X2/X3a
    // indistinguishable and X6 unsatisfiable).
    let fqo:i32 = qoff(fqi as i32);
    let fsd:i64 = t_get32(st, fqo + 24);
    if(t_get32(st, fqo + 8) != wl(id, fsd)) { return x2_pack(0, 0, 13); }
    let ex_first:i64 = t_get32(st, fqo + 20);
    let ln:i64 = t_get32(st, 16);
    if(ln >= 256) { return x2_pack(0, 0, 2); }
    t_put32(st, loff(ln as i32), id);
    t_put32(st, 16, ln + 1);
    let fired:i32 = 0;
    if(ex_first != 0) { fired = 1; }
    return x2_pack(1, fired, 0);
}

// ---------- decide wrappers: retirement on every terminal path (A1) ----------
fn x2_decide(st:[]u8, id:i64, n_epochs:i64) i64 {
    let r:i64 = x2_decide_inner(st, id, n_epochs);
    x2_retire(st, id);
    return r;
}
fn x2_decide_nop(st:[]u8, id:i64, n_epochs:i64) i64 {
    let r:i64 = x2_decide_nop_inner(st, id, n_epochs);
    x2_retire(st, id);
    return r;
}
