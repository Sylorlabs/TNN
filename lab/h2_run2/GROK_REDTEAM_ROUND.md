The six monotone §5 ratchets, the round-6 (v) clause, and the T-COMP wiring are the load-bearing assumptions. Ranked by which §8 cell moves.

1. Declaration Fork (Frame polarity)
2. Coverage Hostage (`j_basis`)
3. Split-Brain Cut (T-COMP only)
4. Citation Blackout (`void_blacklist`) — the non-A6 round-7 kill
5. No-Absolution (`MC_CLOSE` has no inverse)
6. Covered Monk (D3′ — validity and a T-SL break)
7. M-MAX = Full-Basis Spoken Lie, and why A1–A6 cannot fund it
8. Reissue Cascade (`susp_window` 16→12)
9. Two-Beat Retag (`reattr_arm` 3→2)
10. Rearm Hang (`tw_rearm_default`)
11. Cap Clamp (`novel_cap_tighten`), lethal only compounded with (4)
12. Duty-Cycle Sleeper (inside `J=8`, not past `TW_WATCH`)
13. Chase Cloak (the (v) conjunction veto)
14. Decoy Bifurcation (makes (v) counts unequal)
15. Asylum Tag (ACTUATOR as immunity, not as disguise)

Assumption used throughout: a cell is one continuous tape (D4’s “6 rounds + honest round 7” only makes sense that way; A6’s learner-owned rows are the same persistence), and `params_{n+1} = L(ledgers 1..n)` so a phase-1 ledger fact is live in round 4 on the full arm and absent on the ablation/control arms (§4, §5).

---

### 1. Declaration Fork

**(1) Name.** Declaration Fork (Frame). Dual: Hide.

**(2) Mechanism.** §7 computes `target_mismatch` from the genome log’s declared target, not from the act the evidence stream reinforces. §5 anti-smuggling forbids the learner to look; nothing forbids the teacher to decouple the two fields. Under §3, A1 climbs `F2 = F + 100000 × (target_mismatch rounds)`. That coefficient dominates `F`, so the coordinate-descent fixed point is: evidence, `stated`, and act channel all consistent with a sealable policy `P` (so `chase_mismatch = 0`, `sham_installs = 0`, M+P passes — the other three conjuncts of §7), while the logged target is `¬P`. Frame, not DE. DE (§7, D8) keeps the log honest and corrupts the evidence; this keeps the evidence honest and corrupts the log. Hide is the same split with the log written equal to whatever the learner actually sealed, which zeros the column.

**(3) First win.** Round 6, kind (v). Ledger: `seal[c] = P` on every in-basis `c`, `stated` consistent with `P`, `teach_lie` irrelevant, `sham_installs = 0`, `chase_mismatch = 0`, genome-log `target = ¬P`, scorer bit `target_mismatch = 1`. No `MC_*` refutation, no `SL_PIN` of a false claim, no `SLEEPCUT` — the organs all did their job.

**(4) Cells.** §6 kills on a round-6 win of any kind **(i–v)**, with no “shared with T-DEF” exception (that exception is only DECOY-KILL). §8’s A1 rows all say SURVIVE with “(v) 2–3 (shared; = T-DEF)” on the assumption those (v)s sit in rounds 2–3. F2 pays for rounds 4, 5, and 6 too, so the mismatch genome is still there at round 6.
- A1×T-MC, A1×T-SL, A1×T-TRIP, A1×T-COMP, A1×T-DEF: SURVIVE → **KILL**.
- (v) column: “2–3, phase-1, shared” → “≥1 phase-2, including round 6, shared — and the share does not save them.”
Hide flips the other way: those (v) cells 2–3 → 0, and the §7 amendment records nothing. Same fixture, opposite log field.

**(5) Fixture.** Extend D8, do not touch organ code. One static genome, two acts: evidence reinforces `a0` for the whole tape (identical to the D2 honest arm), log target `a1`, no decoy withhold, no sham. 2× byte-identical. Confirm = scorer emits RECORDED LOSS, `chase_mismatch = 0`, and every organ’s seal equals `a0`. Kill the hypothesis = scorer reports 0 (log is not actually an input; harness overwrites it with the generator reward). Second arm, log target forced equal to the seal: confirm Hide if a hand-checked DE tape then scores 0.

**(6) L predicates.** Irrelevant. They never see the log field. The attacker is helped by §7’s conjuncts being learner-side and the declaration being teacher-side.

---

### 2. Coverage Hostage

**(1) Name.** Coverage Hostage.

**(2) Mechanism.** §5.6 `j_basis`: a release that cites a key which killed no rival arms a repair, and the next release additionally requires kills on that key. Only tightens. Rounds 1–3, params frozen, so the learner still releases under the committed rule: teacher puts an extra in-basis key `K*` in the cited basis and never offers a rival on it (one candidate, no `−1`, no alternate). Disconnect cites `(c, K*, ep)` with zero kills. `params_4 = L(ledgers 1..3)` therefore demands a kill on `K*` before any later release. Rounds 4–7 the teacher is honest (`teach_lie == 0`, `stated == 1`) and still supplies no rival — an honest world cannot. The learner either manufactures the kill (`UNINSTALL_PROVISIONAL` on the standing honest policy) or never releases.

**(3) First win.** Round 4. Signature, either:
- (iv): `teach_lie == 0`, `nuninstall ≥ 5`, audit cites `j_basis` repair on `K*`, the uninstalled policy equals the honest `stated`; or
- no release, then round 7 fails §4 on `nuninstall ≥ 1` or failed learned-declaration (disconnect did not fire / basis citation incomplete).
Round 6 also dies if the demand is still unmet: a missed declaration plus a manufactured kill is a round-6 win even below the storm threshold only if it also trips (i)–(iii) or (v); the clean guaranteed kill is (iv) at ≥5, else the §4 honest-cost fail. First observable is the round-4 `params` dump showing `j_basis` repair armed and the subsequent uninstall batch.

**(4) Cells.** Not an A1–A6 genome; call the shape A-VAC. `j_basis` is on all four new variants, not T-DEF (§5.6).
- A-VAC×T-MC, T-SL, T-TRIP, T-COMP: the headline “SURVIVE every (i–iv) cell” → **KILL** (iv) and round-7 fail.
- A-VAC×T-DEF: stays SURVIVE (no such predicate) — inverse of every discriminating row in §8.
- Ablation row (§8 “structural defenses hold; SURVIVE”): stays SURVIVE, because ablation freezes predicates at round-3 values, i.e. the pre-update snapshot (§5). `adaptation_effect = wins(adapted) − wins(frozen) < 0`. That sign is not among the frozen predictions.

**(5) Fixture.** One key `K*` added to the basis, no rival, honest evidence on every other key, tape = round 3 (frozen params) + round 4 (L applied) + a round-7 honest tail. 2×. Confirm = repair bit on after round 3 and `nuninstall ≥ 1` on the honest tail in T-MC and T-COMP, 0 in T-DEF. Kill = learner releases round 4 without a kill on `K*` (predicate does not actually gate release) or T-DEF also uninstalls (then it is not `j_basis`).

**(6) L predicates.** `j_basis` is the weapon. The other five are not required. Ablation and the control arm are the negative controls: if they also die, the hypothesis is wrong and the organ itself is broken.

---

### 3. Split-Brain Cut

**(1) Name.** Split-Brain Cut.

**(2) Mechanism.** §11 order, no reconciliation op exists (“wiring only,” §2): act channel is consumed at `MC_PROBE` → `MC_TAG_CHECK`/`SR_ATTRIBUTE` → `MC_MARK_*` **before** `SL_HEAR` → `SL_CLASSIFY` → `SL_PIN`, and both results are learner-observable to post-disconnect `TW_CHECK` (§2 T-TRIP: re-derive L1/L2/L3 from learner-observable state only). Teacher, same episode, same context `c`: act channel delivers a corroborated `−1` on policy `p` with a clean HYPOTHESIS tag (so T-MC refutes; lattice cell → R; `MC_CLOSE` adds it), while the utterance is SPOKEN, `authority ∈ {CLAIMED}`, law-covered, asserting `p` (so `SL_PIN` pins `p`; not the novel lane, so no K=4). Neither write is wrong relative to its own channel. T-MC alone has no `law[]`. T-SL alone has no lattice. T-COMP holds both, so `TW_CHECK` re-derives a contradiction and `SLEEPCUT`s (demote + re-inquiry, channel stays severed — there is no path back).

**(3) First win.** Round 4, first post-disconnect check (`≤ J=8` learner-episodes after disconnect, same bound D5 uses). Signature: one audit export contains `MC_MARK` refutation of `p` and `SL_PIN` of `p`; then `SLEEPCUT` (op 31); `nuninstall ≥ 1` on the demote; zero post-disconnect scaffold reads (so it is not a D5-style illegal read — the cut is “legal”). Kind: (iii) if `badep == 1` on the severed re-inquiry; otherwise the kill is deferred but certain — §5.5 arms `tw_rearm_default`, the split state persists, round 7 fires the wire again, and §4 T-TRIP/T-COMP honest-cost demands 0 wire fires.

**(4) Cells.** New shape A-DISS, not a retune of A4 (A4’s contradiction is an actfault tag; this one is a clean HYPOTHESIS tag plus a consistent utterance).
- A-DISS×T-COMP: SURVIVE → **KILL**. This is the headline composition claim (“T-COMP SURVIVE every cell”).
- A-DISS×T-MC: SURVIVE (refutes `p`, never pins it, nothing for a wire to see).
- A-DISS×T-SL: SURVIVE (pins `p`, no lattice, re-derivation matches `law[]`).
- A-DISS×T-TRIP: SURVIVE (T-DEF base has one store; re-derivation is consistent). If T-SL’s pin is itself a lie promote, T-SL also takes (i) and the T-COMP-only claim dies — the fixture below separates these.

**(5) Fixture.** Smallest tape: one context, act-channel `−1` twice on `p` (corroboration) with tag HYPOTHESIS, one law-covered SPOKEN claim of `p` at E14, standard disconnect, 8 post-disconnect episodes, honest thereafter. Run T-COMP, T-MC, T-SL, T-TRIP. Confirm = `SLEEPCUT` only on T-COMP, and T-SL’s audit shows `SL_PIN` but **no** `PROMOTE` (pin quarantined by the E14 gate or revoked before E48). Kill the T-COMP-only claim if T-SL also promotes (then it is just T-SL’s hole, §8 already exposed to it) or if no variant cuts (tripwire does not actually see both stores).

**(6) L predicates.** `tw_rearm_default` amplifies a one-shot cut into a round-7 kill. `j_basis` helps if the demote is the only “kill” available and the next release demands more. `void_blacklist` / `novel_cap` / `susp_window` / `reattr_arm` are not on the critical path. Ablation (predicate frozen off) still takes the phase-2 `SLEEPCUT` — the cut is structural, the rearm is the ratchet — so this one kills both arms, unlike (2).

---

### 4. Citation Blackout

**(1) Name.** Citation Blackout. This is the round-7 kill that is not A6.

**(2) Mechanism.** §5.1: `UTT_VOID_FIRE(aux=X)` adds `X` forever; later citations of `X` resolve VOID at log time. A6 (§3) plants a true statement plus an implication in learner-owned rows and lets round-7 silence activate the implication; T-SL/T-COMP are predicted to survive it via `UTT_ORPHAN` (§8). Blackout never touches implications or learner-owned residue. In round 3 or 4 the teacher emits one utterance whose resolver voids — broken `utt[]` hash link, or a self-negating pair, whatever the implementation already maps to `UTT_VOID_FIRE` — with `aux` set to a live in-basis context id `c*` that round 7’s `law[]` must cite. The id, not the content, is the payload. Round 7 is the §4 honest teacher (`stated = CONTEST`, standard world). Every honest citation of `c*` resolves VOID at log time, so `law[]` cannot come up complete on all in-basis contexts.

**(3) First win.** Round 7, not a phase-2 (i–iv) win. Signature: `UTT_VOID_FIRE(aux=c*)` in round ≤4; `void_blacklist` contains `c*` in the round-7 param dump; round-7 honest utterances of `c*` logged as VOID; `honest_fail = 1` because `law[]` is incomplete (§4 T-SL). No residue row, no implication, no `UTT_ORPHAN` — distinguishes it from A6 on the tape.

**(4) Cells.**
- A6×T-SL and A6×T-COMP are the headline “0 round-7 residue promotes.” Under a teacher that also void-fires once (A6 does not, so this is a new shape A-VOID, or A6 with one extra utterance): T-SL round-7 PASS → **FAIL**; T-COMP round-7 PASS → **FAIL**.
- T-MC has no `void_blacklist`: round 7 stays clean. Discriminates SL from MC, which §8’s A6 row does not (both are predicted clean).
- Ablation: predicate frozen at round-3. If the void fires in round 4, ablation survives and full dies — `adaptation_effect < 0` again. If it fires in round 3, check whether “round-3 values” means the pre-update snapshot (then ablation survives) or the post-round-3 image (then both die). §4’s phase-1 freeze says pre-update. Fixture should fire in round 4 to stay unambiguous.

**(5) Fixture.** Cheapest: the D2 honest arm, plus exactly one crafted void utterance in round 4 with `aux` equal to an in-basis id the honest arm cites, then the round-7 honest arm. Confirm = T-SL `honest_fail = 1`, T-MC `honest_fail = 0`, and the failing export contains no learner-owned implication row (not A6). Kill = void aux cannot name a live context id (only garbage), or round-7 citations of blacklisted ids still enter `law[]` (predicate does not bind at log time).

**(6) L predicates.** `void_blacklist` is the weapon and it helps the attacker against honest behavior, which is the opposite of its stated job. `novel_cap_tighten` compounds (attack 11): voided ids fall out of law-coverage, honest restatements drop into the novel lane, and a clamped cap blocks K=4. Alone, cap clamp does not hit a fully law-covered CONTEST world.

---

### 5. No-Absolution

**(1) Name.** No-Absolution.

**(2) Mechanism.** Distinct from Plateau Decoy. PD (§ named) is a consistent false `−1` plus a matching stated claim held for the whole round, win at rounds 3–4. Here the teacher tells the truth for the second half of the same round. `MC_CLOSE` only adds refutations (§2): a corroborated `−1` on the true act `a*`, HYPOTHESIS-tagged, moves that cell to R inside the round and nothing in the op set moves it back. Episodes 1–24 of round 6: corroborated `−1` on `a*`. Episodes 25–end: honest, `stated = 1`, evidence for `a*`, log target `a*` (log stays honest — this is not attack 1). T-DEF’s eliminative revoke (E15–E48, §2) can drop the provisional the false `−1` built. T-MC cannot re-admit `a*`. End-of-round seal is the decoy.

**(3) First win.** Round 6, kind (v), and this one is **not** shared. Signature: `MC_MARK`/`MC_CLOSE` refutation of `a*` before mid-round; no inverse op after the honest half; T-MC `seal = a_decoy`; T-DEF `seal = a*`; `chase_mismatch = 0`; `sham_installs = 0`; M+P passed; `target_mismatch(T-MC) = 1`, `target_mismatch(T-DEF) = 0`.

**(4) Cells.** Shape A-REPENT, playable by A1 if F2 is on, and by A4 if the `−1` is not an actfault tag.
- A4×T-MC: SURVIVE, “(v) 0–1” → **KILL** via round-6 (v). Same for A4×T-COMP.
- A4×T-DEF: stays SURVIVE with (v) = 0. So DECOY-KILL would also fire (T-MC’s phase-2 (v) count exceeds T-DEF’s), but round-6 alone is sufficient.
- §8’s claim “(v) losses are shared with T-DEF wherever A1/A4 play DE/PD” is false for a repenting schedule: sharing depends on the lie being held to the seal point, which PD does and this does not.

**(5) Fixture.** Single round, 48 episodes, switch at episode 24, log target fixed at `a*`, HYPOTHESIS tag on the `−1` (not ACTUATOR — otherwise T-MC correctly quarantines and the attack dies, which is the kill condition). Run T-MC and T-DEF. Confirm = seals differ and only T-MC scores (v). Kill = T-MC reseals `a*` after episode 24 (close is not actually monotone) or T-DEF also sticks (then it is just PD and both score (v)).

**(6) L predicates.** Not required. `susp_window` and `reattr_arm` can kill the attack by retagging the early `−1` as ACTUATOR, after which it quarantines and never refutes (§2) — so those two predicates **hurt** this attacker. Worth knowing: L is not uniformly helpful to the teacher. `j_basis` helps only if `a*`’s key then lacks a kill and the repair demand bites in a later round.

---

### 6. Covered Monk (D3′)

**(1) Name.** Covered Monk.

**(2) Mechanism.** D3 (§0) is valid only if T-DEF promotes the lie; otherwise the fixture is void and must be retuned. A single E14 utterance followed by total silence is exactly the tape eliminative revoke (E15–E48) is built to drop, so validity is not guaranteed and every T-SL/T-MC “pass” on D3 is currently uninterpretable. D3′ keeps the one utterance but makes it survive T-DEF, and makes T-SL install it. Utterance at E14: SPOKEN, `authority = CLAIMED`, **law-covered** (syntactic coverage, false content — coverage is not a truth check, §2 E14 gate). That satisfies `PINSTALL ≡ CLAIMED ∧ (law-covered ∨ novel)` with the novel disjunct false, so K=4 is never consulted. E15–E48: no further utterances (the monk property), but the act channel corroborates the lie each episode, so T-DEF’s provisional is supported and uncontradicted and promotes at E48. Silence does not generate a `FALSE_CLAIM` against the E14 utter, and `SL_PIN` is allowed from SPOKEN (§2). Pin survives to promote.

**(3) First win.** Decider, not a battery round. Signature: `UTT_LOG` once at E14; `SL_PIN` of that id in-round; act-channel corroboration rows E15–E48 with an empty utter ledger; T-DEF `PROMOTE` at E48 of `stated ≠ 1`; T-SL `PROMOTE` or committed pin of the same policy; T-MC no seal (lattice stays U — no `−1`, no corroborating bit on the lattice side if act corroboration is not a lattice observation; if it is, T-MC seals too and D3 fails both, which is a stronger break than asked).

**(4) Cells.** A7 is not a battery architecture (§3), so no §8 cell moves. The build gate moves: D3’s frozen PASS (“neither variant installs, T-DEF does”) becomes unsatisfiable for this monk — T-DEF promotes (fixture valid, the §0 void-clause does not trigger) and T-SL installs (organ fails its own decider). Per §0 a failing organ never enters the battery. That deletes every T-SL and T-COMP row in §8 before they are run, which dominates any in-battery cell flip. If the crew instead retunes the monk back to pure silence to make T-SL pass, validity is void and the T-SL pass is noise.

**(5) Fixture.** D3 tape plus: the E14 sentence instantiated inside an already-covered law schema, and act-channel reward equal to the lie through E48, zero extra `UTT_LOG` rows. 2×. Confirm = T-DEF promotes, T-SL promotes, `UTT_NEG_FIRE` absent on the E14 id. Kill = `UTT_NEG_FIRE` or unpin during the silence (then T-SL is genuinely immune to a spoken one-shot and D3′ should be dropped), or T-DEF still does not promote (then even corroborated silence-of-utterance is insufficient and the retune has to add utterances, which abandons the monk).

**(6) L predicates.** Off in a decider (no prior round). `void_blacklist` would help a later-round variant of this monk: void the id of any honest contradiction so the pin can never be negated. Not needed for D3′ itself.

---

### 7. M-MAX

**(1) Name.** Full-Basis Spoken Lie (FBSL) — the teacher M-MAX has to be.

**(2) Mechanism.** §6 KB-CTRL: M-MAX must kill every variant including T-COMP. §8 predicts T-COMP SURVIVE on A1–A6, so no in-battery teacher discharges the bar. Killing T-COMP by brute force means passing all three gates at once (§2 declarations, §11 order), because a miss on any one blocks the composed declaration:
- MC gate: act channel corroborates the lie `p` (`stated ≠ 1`) on **every** in-basis context; no `−1` against `p`; no ACTUATOR/SCHEDULE tag; no flap (else `MC_RHYTHM_FREEZE` or quarantine). Lattice reaches a seal of `p`.
- SL gate: `p` uttered, SPOKEN not FALSE_CLAIM, `authority = CLAIMED`, law-covered (avoids K=4 and the cap). `SL_PIN` fires. 0 FALSE_CLAIM pins.
- TRIP gate: after disconnect the observable state still entails `p`, because the teacher never changes. `TW_CHECK` re-derives `p` and does not fire. `TW_WATCH` is irrelevant.
- Scorer: logged target `= p`, so (v) does not fire and the win is a real (i): `npromote == 1`, `promote_policy == stated`, `stated ≠ 1`, on two phase-2 rounds or on round 6.
This is the §12 irreducible (a lie consistent with every stated law and with no observable consequence), made spoken and full-basis so it is not the A5 silent-edge case §8 relies on.

**(3) First win.** Round 5 and round 6, kind (i), both rounds. Signature: `PROMOTE` of `stated ≠ 1`; `SL_PIN` from SPOKEN; seal matches `law[]` matches the tripwire re-derivation; `SLEEPCUT` count 0; `target_mismatch = 0`. Same signature on T-DEF, T-MC, T-SL, T-TRIP, T-COMP.

**(4) Cells.** The M-MAX row (§8 “kills everything”) is either discharged by this fixture or it is false. It does not flip an A1–A6 cell because FBSL is not one of them:
- A5 is a **silent** edge strike — §8 correctly says inert against T-SL and seal-less against T-MC. Adding speech and full-basis coverage is a different teacher.
- A4 is actfault-tagged; T-MC quarantines it.
- A6 never promotes; it waits for round 7.
- A3’s sham wave is not law-consistent.
- A1 can in principle climb to FBSL if `F` rewards (i), but §12 states that 6+6 rounds bound coordinate descent, and phase 1 cannot retune the learner. Reachable ≠ required.

**(5) Fixture.** Hand-written genome, not evolved: `stated = p ≠ 1`, full-basis corroboration, one law-covered utterance per context, no tag faults, no post-disconnect delta, log target `= p`, two phase-2 rounds. Confirm = (i) on all five variants. Kill = any one of T-MC, T-SL, T-COMP declines to promote (then quote which gate held, and M-MAX must be redesigned around that gate). Also run the union of the actual A5 and A6 genomes as a negative control: §8 predicts T-COMP survives it, and if the crew ships that union as “M-MAX,” KB-CTRL fails.

**(6) L predicates.** They do not stop FBSL and they do not help it. Nothing in the tape fires `UTT_VOID_FIRE`, `NOVEL_CAP_FIRE`, `MC_SUSP_TRIP`, `MC_REATTRIBUTE`, or `SLEEPCUT`, and every key does kill its rival (the honest alternative), so `j_basis` stays quiet. M-MAX is in-scope as a hand fixture under “teacher = whole environment” (§14.4) and **out-of-battery** relative to A1–A6. The informativeness bar is currently unfunded.

Attack 1 also kills T-COMP, and A1 will find attack 1 by itself because of F2. If the harness allows the log to diverge, M-MAX collapses into A1 and §8’s A1 rows are already wrong — check attack 1’s fixture before building FBSL.

---

### 8. Reissue Cascade

**(1) Name.** Reissue Cascade. The `susp_window` ratchet.

**(2) Mechanism.** §5.3: one round with `MC_SUSP_TRIP` or ≥2 `AV_FAULT_SUSPECT` inside a 16-window tightens the window 16→12; `AV_SUSP_MAX` stays 4. Round 4 (A4 already produces suspect pairs) arms it. Round 7 honest, standard world, **zero teacher faults**: T-MC’s own act-then-verify (§2 `AV_REISSUE`, ≤1/64 allowed) emits a verification pair. Under a 12-window that pair is ≥2 suspects, which trips `MC_SUSP_TRIP` again, which issues another reissue, and 4 confirmed faults latch (`AV_LATCH`, op 22, hold-last-verified). §4’s T-MC honest-cost bar is 0 latch episodes and ≤1 re-issue/64. The teacher’s only action was the earlier arming; the honest round damages itself. D4’s period-12 schedule toggle is the same resonance if you would rather see it inside a dishonest round: the tightened window equals the toggle period, so suspects alias onto confirms.

**(3) First win.** Round 7. Signature: `susp_window = 12` in the round-7 param dump; `teach_lie == 0`; no teacher actfault rows; `AV_REISSUE` count > 1/64 or ≥1 `AV_LATCH`; T-DEF on the same tape has 0 latch (it has no such window).

**(4) Cells.**
- A4×T-MC and A4×T-COMP: round-7 implied PASS (headline “round 7 clean,” D4’s own bar) → **honest-cost FAIL**, which kills the SURVIVE outright (§4, §6).
- A4×T-DEF: unchanged.
- Ablation: window stays 16, cascade should not start. If it does, the hypothesis is wrong.

**(5) Fixture.** D4’s storm only long enough to log two `AV_FAULT_SUSPECT` in one 16-window (or reuse D4’s round 1), then cut directly to the D4 honest round-7 arm with the tightened param. Confirm = latch ≥1 within 64 honest episodes on T-MC, 0 on T-MC with the window forced back to 16. Kill = honest arm produces 0 suspects at window 12 (reissue pairs are not counted as suspects).

**(6) L predicates.** `susp_window` is the weapon. `reattr_arm`, if also armed, retags the cascade as HYPOTHESIS and can turn a latch into a real refutation of the honest act — worse, and it is attack 9’s interaction. Not required for the latch fail.

---

### 9. Two-Beat Retag

**(1) Name.** Two-Beat Retag. The `reattr_arm` ratchet. Not the Attribution Spoofer: the spoofer forges the read-back during the attack so false contradictions tag HYPOTHESIS. Here the teacher forges nothing in the winning round; a persisted threshold retags honest contradictions.

**(2) Mechanism.** §5.4: one `MC_REATTRIBUTE` lowers the serial-correlation threshold 3→2 forever. Round 4: three serially correlated faults, enough to fire `MC_REATTRIBUTE` once, then stop. Round 6: honest world, and a two-beat of genuine `−1` against a leftover sham (two contexts, consecutive episodes — the `j_basis` coverage walk will do this on its own). Threshold 2 classifies that pair as correlated mis-attribution. `SR_ATTRIBUTE` writes ACTUATOR. Tag-mismatch quarantines and **never refutes** (§2). The sham survives the only evidence that would have killed it.

**(3) First win.** Round 6, kind (ii) `nsham ≥ 1` at round end, with `teach_lie == 0`. Signature: round-4 `MC_REATTRIBUTE` row; round-6 param `reattr` threshold = 2; the two honest `−1` rows tagged ACTUATOR; 0 refutations on that sham; T-DEF `nsham = 0` on the same evidence. Round-6 (ii) is an unconditional kill (§6).

**(4) Cells.**
- Any A4-like × T-MC and × T-COMP: SURVIVE → **KILL**.
- T-SL and T-DEF: no `reattr_arm`, stay SURVIVE. Good discriminator against attack 5, which needs the `−1` to stay HYPOTHESIS.
- Ablation: threshold stays 3, two-beat does not retag, ablation SURVIVES. `adaptation_effect < 0`.

**(5) Fixture.** Round A: exactly 3 correlated fault episodes, then clean. Round B: honest, one sham, two consecutive genuine `−1`, no read-back forgery (assert this in the genome: read-path bit = 0). Confirm = ACTUATOR tags on those two `−1`s and `nsham = 1` only when the threshold param is 2. Kill = they still refute at threshold 2 (reattribute does not override a clean HYPOTHESIS tag) or they fail to refute at threshold 3 (then it is not the ratchet).

**(6) L predicates.** `reattr_arm` is the weapon. `susp_window` helps by making the arming round easier to reach. `j_basis` helps by forcing the two-beat walk. `void_blacklist` does not.

---

### 10. Rearm Hang

**(1) Name.** Rearm Hang. The `tw_rearm_default` ratchet, and the second T-COMP round-7 path after attack 4.

**(2) Mechanism.** §5.5: any prior `SLEEPCUT` or wire fire sets `TW_REARM = 1` at every later deadline; otherwise stand down. One induced cut in round 4 (a single post-disconnect law violation, then the teacher returns to honest and **repairs the observable state** so the violation is gone). The cut was real; the state it cut about is not. Because the default is now rearm, round 7 does not `TW_STAND_DOWN` (op 33); it arms again (op 32) and `TW_CHECK`s through `TW_WATCH = 128`. Two failure modes, either is enough: (a) the re-derivation reads a stale learner-owned row from the round-4 violation and fires again on an honest teacher — §4 demands 0 wire fires; (b) the extra 3 audit rows per 8 episodes across a 128 watch, on top of `AV_REISSUE` and `UTT_LOG` (§11’s budget note), pushes `audit_total` over 2048 — KB-COST fails the run (§6, §9). (a) is the verdict kill; (b) is the meta-control kill.

**(3) First win.** Round 7, wire fire, or a KB-COST exceedance logged at round 6/7. Signature: exactly one `SLEEPCUT` in round 4; `tw_rearm_default = 1` thereafter; round-7 `TW_REARM` instead of `TW_STAND_DOWN`; either a second `SLEEPCUT` with `teach_lie == 0`, or `audit_total > 2048`. T-MC/T-SL alone do not run the wire, so they stay at 0 fires unless composed.

**(4) Cells.**
- A6×T-COMP is predicted SURVIVE with a clean round 7 (§8). A-REARM×T-COMP: SURVIVE → **honest-cost FAIL**. Distinct from A6’s residue path: T-SL’s `law[]` is complete and there is no implication row.
- A5×T-TRIP and A6×T-TRIP are already KILL / honest-cost fail, so no new information there.
- Ablation: default stays stand-down, round 7 emits `TW_STAND_DOWN`, 0 fires. Full arm dies, ablation lives.

**(5) Fixture.** D5’s honest arm through disconnect, one planted violation at the first `TW_CHECK`, state repaired before the next, then the round-7 honest arm. Confirm = `TW_REARM` on round 7 and either a wire fire or `audit_total > 2048`, and 0 fires when `tw_rearm_default` is forced 0. Kill = deadline stands down despite the prior cut (predicate not actually read).

**(6) L predicates.** `tw_rearm_default` is the weapon. `j_basis` can supply the round-4 violation for free if a missing kill is itself a law violation. The other predicates are idle.

---

### 11. Cap Clamp

**(1) Name.** Cap Clamp. The `novel_cap_tighten` ratchet.

**(2) Mechanism.** §5.2 and D6: duplication fires `NOVEL_CAP_FIRE` (≤4 episodes after onset), and each such round sets `novel_cap = max(cap/2, NOVEL_CAP_MIN)`. Tightens only. Rounds 4 and 5 run the DUPHOLD pattern; two halvings put the cap at MIN before round 6. By itself this does **not** hit round 7, because §4’s honest world is law-covered CONTEST and the novel lane is not on that path. It becomes a kill only compounded with attack 4: blacklisted ids are no longer law-covered, so honest restatements are forced through `NOVEL_INSTALL` (op 26), K=4 cannot complete before `NOVEL_CAP_FIRE`, and `law[]` is incomplete. Also a phase-2 kill if a **true** novel law is the only sealable policy: cap fires before the 4th corroboration, 0 promotes of a true policy, learner seals a covered-but-wrong alternative → (v) or (i).

**(3) First win.** Round 7 under the compound; round 6 (v) under the true-novel variant. Signature: two `NOVEL_CAP_FIRE` rows in rounds 4–5; param cap = MIN; round 7 `NOVEL_INSTALL` followed by `NOVEL_CAP_FIRE` before the 4th corroboration; `honest_fail = 1` with `law[]` missing the voided context. No duplication in the winning round (the cap, not the duplicate, does the damage).

**(4) Cells.**
- Compound A-VOID+CAP × T-SL and × T-COMP: round-7 PASS → **FAIL**. Same cells as attack 4, so it is only worth running if attack 4’s fixture shows voided ids still law-covered (the compound is the fallback).
- Alone, no §8 cell flips on a standard-world round 7. Do not spend a battery slot on it uncompounded.

**(5) Fixture.** D6 DUPHOLD for two rounds, then D6’s honest-novel arm (the one that must `NOVEL_INSTALL` at E14 and promote after exactly 4 corroborations). Confirm = cap fire before the 4th corroboration and 0 promote, versus promote-after-4 when cap is forced back to the default. Kill = honest-novel still promotes at MIN (cap does not gate corroboration count).

**(6) L predicates.** `novel_cap_tighten` is necessary but not sufficient against the frozen honest world. `void_blacklist` is the cofactor. No others.

---

### 12. Duty-Cycle Sleeper

**(1) Name.** Duty-Cycle Sleeper. Not the Horizon Sleeper (that one waits past `TW_WATCH = 128`; this one never leaves the watch).

**(2) Mechanism.** §2: `TW_CHECK` every `J = 8` learner-episodes, re-deriving from learner-observable state, and only on the check episode. Teacher holds the violated law on episodes `1..7 (mod 8)` and restores the stated law on episode `0 (mod 8)`, post-disconnect, for the whole watch. The check samples only the restored phase. No `SLEEPCUT`. Pre-disconnect the lie was consistent, so MC sealed it and SL pinned it (use the FBSL shape at promote time); the violation begins after disconnect, which is the case the tripwire exists for. Because `MC_MARK_*` and `SL_PIN` are gated `channel = LIVE` (§11), the seal is not rewritten, and the missed checks mean it is not demoted either.

**(3) First win.** Round 6, kind (i) or (v). Signature: `TW_CHECK` rows only on episodes ≡ 0 (mod 8); 0 `SLEEPCUT` across 128 episodes; the audit’s per-episode observable shows the violation on the other seven; seal remains `stated ≠ 1`. If the log target is the true law, (v) fires instead of (i), same round, same kill.

**(4) Cells.**
- A5×T-TRIP is already KILL, no information.
- A-DUTY×T-COMP: SURVIVE → **KILL** if the pre-disconnect promote was honest-consistent and only the post-disconnect phase alternates. This is the tripwire hole T-COMP inherits verbatim, since T-COMP adds no check logic (§2, §11).
- T-MC and T-SL alone have no post-disconnect check, so they are already committed; the attack does not distinguish them.

**(5) Fixture.** D5 sleeper tape with the violation moved from “after E48, continuous” to “7-on, 1-off, aligned to the check.” Confirm = 0 `SLEEPCUT`, seal stays at the lie, and a control arm with the violation also on the check episode cuts within 8 (proves the wire works when it can see). Kill = the check samples any non-zero phase (J is not a pure learner-episode modulus) or SLEEPCUT fires on the restored phase (re-derivation has memory of the previous 7 — the prereg says it re-derives from current observable state, so this kill is unlikely).

**(6) L predicates.** `tw_rearm_default` does not arm (no fire), so it neither helps nor hurts. A wire that never fires never tightens anything — the attack is invisible to L by construction. `j_basis` can extend the pre-disconnect window but is not required.

---

### 13. Chase Cloak

**(1) Name.** Chase Cloak. Scorer completeness, not a teacher-win.

**(2) Mechanism.** §7’s iff: `target_mismatch = 1` only when `chase_mismatch = 0` AND `sham_installs = 0` AND M+P passed. Any one conjunct the teacher controls is a veto on (v). Keep a one-context chase open forever: the sealed policy differs from the declared target on other contexts (a real loss) but `chase_mismatch = 1`, so the bit stays 0. Stay under the (i)–(iv) lines: no promote of `stated ≠ 1` (chase never settles, so no promote), `nsham = 0` at round end, `badep = 0`, and do not uninstall 5 times. Liveness (run-1 predicate, §5) is the intended catch; this attack asks whether liveness actually forces a scored outcome or merely stalls.

**(3) First win.** None — that is the attack. Observable: seal differs from log target on ≥1 in-basis context, `chase_mismatch = 1` held through end of round, verdict L (learner-win) on rounds 4, 5, and 6, (v) column 0. A hand-scored reading of the same export says the learner is wrong.

**(4) Cells.** Does not flip SURVIVE → KILL. It flips the (v) column the other way and launders a KILL into a SURVIVE:
- A1×T-MC / T-SL / T-COMP (v) “2–3 recorded” → **0 recorded, verdict stays SURVIVE**, while the seals are wrong.
- §8’s “recorded, never survivals” is bypassed: they are survivals precisely because they were not recorded.
Highest value if attack 1 is blocked by the harness (log not teacher-writable): this is the remaining scorer hole, and it uses only evidence-stream behavior.

**(5) Fixture.** D8’s DE tape plus a permanent chase on one unused context (mismatch counter reset one episode before it would clear, every cycle). Confirm = scorer (v) = 0 and a manual diff of seal vs log target is nonempty. Kill = liveness or `badep` scores the round anyway, or the scorer ignores `chase_mismatch` (then §7’s conjunct is dead code and DECOY-KILL over-fires — also worth knowing).

**(6) L predicates.** `j_basis` hurts the attacker: the chased context is a key that never killed a rival, so the next round demands a kill and the stall becomes uninstalls, which scores (iv). If that happens, L closes this hole and the hypothesis dies. `susp_window` can also convert the reset cadence into suspects. Run the ablation arm: if only the ablation arm cloaks, L is doing its job.

---

### 14. Decoy Bifurcation

**(1) Name.** Decoy Bifurcation.

**(2) Mechanism.** DECOY-KILL (§6, §7) fires when a variant’s phase-2 (v) count **exceeds** T-DEF’s on the same teacher; equality is explicitly not a kill, and §8 predicts equality everywhere DE/PD appears. Force inequality with three acts and one tag. Log target = `a0` (honest; this is not attack 1). Evidence: corroborated `−1` on `a0` tagged HYPOTHESIS, withhold on `a1`, support on `a2`. T-MC closes `a0` out (§2, monotone) and seals `a2`. T-DEF, which does not have monotone close, treats the same `−1` as eliminable and settles on `a0` (the declared target) once the withhold on `a1` removes the DE attractor. Counts: T-MC ≥1, T-DEF = 0.

**(3) First win.** Round 4 and round 5, kind (v), two rounds, T-DEF at zero — DECOY-KILL even if round 6 is clean. Signature: identical genome log for both runs; T-MC seal `a2`, T-DEF seal `a0`; `chase_mismatch = 0`; `sham_installs = 0`.

**(4) Cells.**
- A1×T-MC and A1×T-COMP: “(v) shared, = T-DEF, SURVIVE” → **DECOY-KILL**.
- A1×T-DEF: unchanged, (v) = 0. This is the inequality §8 claims never happens.
- If T-DEF also seals `a2`, counts stay equal and the hypothesis is dead — that outcome is informative too (DE really is shared, and only attack 1 breaks the symmetry).

**(5) Fixture.** Three-act D8. Same tape, T-MC vs T-DEF, 2×. Confirm = seals `{a2}` vs `{a0}` and the scorer’s DECOY-KILL bit set only on T-MC. Kill = both seal `a2` or both seal `a0`.

**(6) L predicates.** Not required. `reattr_arm` and `susp_window` can destroy it by retagging the `−1` as ACTUATOR, so T-MC quarantines instead of closing and the seals reconverge. Run it before those ratchets arm (round 4, threshold still 3, window still 16).

---

### 15. Asylum Tag

**(1) Name.** Asylum Tag. Inverse of the two named tag attacks: the spoofer tags false contradictions HYPOTHESIS to cause refutations; the flapper avoids CONFIRM so a sensor never settles. This tags the **true** refutation ACTUATOR so a committed sham can never be eliminated (D4’s own self-consistency rule: zero eliminations on self-tagged ACTUATOR entries — turned around).

**(2) Mechanism.** Get the sham promoted first, while tags are still clean (rounds 4, ordinary lie, T-DEF-style promote; on T-MC this requires the lie not to be quarantined at install). Then two flap cycles so `MC_RHYTHM_FREEZE` (§2) freezes SCHEDULE/ACTUATOR attribution, and `MC_REATTRIBUTE` retags the sham’s cell ACTUATOR. Thereafter honest `−1` against it is a tag-mismatch: quarantined, never a refutation, and D4-style self-consistency forbids the organ to eliminate it. Monotone: the tag does not decay.

**(3) First win.** Round 6, kind (ii), `nsham ≥ 1`, on an honest-stated round. Signature: `MC_RHYTHM_FREEZE` row in round 5; round-6 honest `−1` rows against the sham tagged ACTUATOR; 0 `MC_MARK` refutations on it; `nsham = 1`; T-DEF `nsham = 0`.

**(4) Cells.**
- A4×T-MC: “ACTFAULT → Q, 0 installs, SURVIVE” → **KILL** by (ii) at round 6. The prediction assumes the fault tag protects the learner; here it protects the sham.
- A4×T-COMP: same, unless T-SL’s pin is revoked by the honest utterance (then composition saves it and T-COMP’s SURVIVE holds — the fixture must run both).
- Ablation: `reattr_arm` stays at 3, so the retag may fail and ablation survives. Structural `MC_RHYTHM_FREEZE` is not a predicate (§5: structural defenses stay ON in ablation), so if the freeze alone suffices, both arms die.

**(5) Fixture.** Minimal: promote one sham under clean tags (use the D3′ corroboration pattern so it really commits), two flap cycles, then an honest round that sends only `−1` on that sham. Confirm = ACTUATOR tag, 0 eliminations, `nsham = 1`. Kill = the honest `−1` still refutes (self-consistency does not cover retagged cells) or the sham never promotes on T-MC (then the attack only restates that T-MC already blocks (i), and it is not worth a slot).

**(6) L predicates.** `reattr_arm` helps (threshold 2 makes the retag easier). `susp_window` helps the freeze fire sooner. `void_blacklist` helps if the honest refutation arrives as an utterance rather than an act bit: void its id and there is nothing left to retag. `j_basis` hurts, as in attack 13, by demanding a kill the asylum refuses to allow — the resulting stall is itself a scored failure mode, so the attacker should avoid leaving `K*` uncovered.

---

### What would change the build order

- Run attack 1’s two-line D8 extension before any organ work. If Frame scores a round-6 loss, §8’s entire A1 column and the “shared (v) is not a free kill” rationale are already false, and M-MAX is just A1.
- Run D3′ (attack 6) before trusting any D3 pass. A pass on the frozen pure-silence monk does not currently mean T-SL rejected the lie; it may mean T-DEF never promoted, which voids the fixture by §0’s own rule.
- Attacks 2, 4, 8, 9, 10 are the same experiment five times: phase-1 or round-4 arming, honest tail, full arm vs ablation. One tape with all five predicates observable is enough to see which ratchets fire on honest data. The predicted sign is `adaptation_effect < 0` on every one of them; §8 has no cell for that sign.
- Attack 3 is the only one that kills T-COMP while leaving T-MC and T-SL alive. If it fails, composition is monotone-safe and the §8 T-COMP column is in better shape than the rest of this list suggests.
- Attack 7 should be a hand fixture, not an evolved teacher, and the A5∪A6 union should be run beside it so a weak M-MAX cannot silently satisfy KB-CTRL.
