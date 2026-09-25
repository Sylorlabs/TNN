# F33 SRS — Frozen hyperparameters & design decisions

Recorded BEFORE the first training run (2026-09-25). Authority:
`fork_round/PREREG_FORKROUND.md` §3 (F33) + `ideas/grok_forks.md` Fork 2
(authoritative on mechanism detail).

## Ledger keying (exact)
- Key = (m, s): m = min(4, f1/200) ∈ {0..4}, s = min(3, f6/250) ∈ {0..3}
  (survivor uses f6, NOT f7). Key index = m*4 + s → 20 keys.
- f1, f6 are the §4 index-level features (thousandths), same definitions as
  frozen `pl_features`/`ft_features8`.
- Key is computed from the item's DEPTH-1 features and STORED on the item;
  deeper arrivals reuse the stored key (features never re-enter after d=1).

## Inits (before first run)
- (n,k) ledger: n=0, k=0 per key → cold C* = ρ(0,0) = 500 for all keys.
- Residual tables: δ_d = 0 for all (key, d_idx); all transition sums 0.
- Per-item state: empty.

## ρ
- ρ(k,n) = (k+1)*1000/(n+2), integer division (operands non-negative,
  truncation = floor). Codomain [1,998]; cold start 500.

## Training (train_f33.zag, single deterministic pass over features.tsv)
- features.tsv SHA-256 `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
  (5240 rows; the fork brief and PREREG_FORKROUND.md §2 carry the value with
  `…e65a897d` — matches on-disk; the prereg's `…e65e897d` is a transcription
  typo, as previously documented by F20/F21).
- Rows processed in FILE ORDER. Only heldout=0 cells train (heldout is
  per-item consistent in the data: 0 mixed ids — verified pre-run).
- Per released training cell (rel4=1), update order per cell:
  emit C → observe (rel4, correct4) → update ledger/transition sums →
  recompute δ for that (key, d_idx).
- Depth-1 cell: key from (f1,f6); C* = ρ(k_key, n_key) from CURRENT ledger
  (previous items only); C = C* (π=0 at d=1: f3=0 verified in data);
  then n_key++, k_key += y. Key/C*/f8 stored per item REGARDLESS of release
  (C* is a ledger lookup, defined for every item); (n,k) updated on released
  outcomes only.
- Depth-d cell (d_idx>0): π = min(400, 1_{f3>0}·50 + max(0, f8−f8^(1))/8)
  with f8^(1) the stored depth-1 trauma baseline; if released:
  C = clamp(C* + Σ_{j=1..d_idx} δ_j − π, 1, 999), δ frozen from previous items.
- Transition update at depth-d training cell (d_idx>0), using the item's
  stored d_prev state (rel_p, C_p, y_p):
  if rel_p==1: n_all++, ΣC_all += C_p, k_all += y_p.
  if rel_p==1 and current rel4==1: n_stay++, ΣC_stay += C_p, k_stay += y_p.
  (Correctness is constant on released paths — verified 0 changes / 3467
  adjacent released pairs pre-run — so y_p is the right label.)
  Then recompute δ_d for (key, d_idx).
- δ recompute (exact integer rules, truncating toward 0):
  E_d  = tdiv(ΣC_stay,n_stay) − tdiv(ΣC_all,n_all)
  ΔA_d = tdiv(k_stay·1000,n_stay) − tdiv(k_all·1000,n_all)
  δ_d  = clamp(ΔA_d − E_d − 3, −40, +40).
- EMPTY DENOMINATORS: if n_stay==0 or n_all==0 → δ_d = 0 ("the depth is
  skipped"). (Literal alternative δ=−3 from the bare buffer is rejected:
  "skipped" means no shift; also the cold start would otherwise shift with
  zero data.)
- d_prev = the item's previously processed depth (data is grouped by id,
  depths ascending: d/2 in practice).
- Defensive (never triggers on frozen data; deterministic): cell at d>1 with
  no stored item state → skipped.

## Params baked (mt_f33_params.zag, generated — never hand-edited)
- f33_cstar(key): ρ(k,n) at end of training, 20 values.
- f33_delta(key, d_idx): end-of-training δ, 20×7 (d_idx 0 → 0).
- Final (n,k) per key recorded as comments in the params file.

## Eval policy (policy_f33.zag)
- Interface `<polbin> <items> <depth> <gate01> <out.tsv>`; gate01 MUST be 0
  (rc=64 otherwise). M4 release skeleton (release iff L_t == L_1) — B9.
- cert = "f33-srs". TSV columns identical to mech.zag.
- Depth 1: features at t; key from (f1,f6); C* = f33_cstar(key); conf =
  clamp(C*,1,999); per-item row (id, m, s, cstar, f8) APPENDED to the
  on-disk state file (see below).
- Depth d>1: read per-item state by id → (m,s,cstar,f8_1); π per formula;
  cum = Σ_{j=1..d_idx} f33_delta(key,j); conf = clamp(cstar + cum − π, 1, 999).
- Per-leg driver with deterministic on-disk per-item state: state path =
  dirname(out.tsv) + "/.f33state_<A|B>.tsv" (variant from the out filename's
  _A/_B suffix; fallback "X"). Deleted at eval run start by the wrapper.
  Legs run in fixed depth order (depth-1 legs before deeper legs), so f8^(1)
  always exists. Defensive: id missing from state → key from current
  features, cstar from frozen ledger, f8_1 = f8 (π trauma term 0).
- A/B byte-identical: _A and _B legs use separate state files with identical
  content.

## §5 go/no-go (training checkpoint) — pre-registered
- Liveness: ≥10% of the 120 trainable (key, d_idx∈1..6) cells have δ_d ≠ 0
  at end of training (the residual is doing something).
- Cap-bind: |δ_d|=40 binds on <25% of cells, else "the fork is already
  false" per the ideas file.
- Ledger moved: some key has n>0.
- Training run TWICE → byte-identical params .zag (gates §8).

## Falsifier operationalizations (pre-registered, before eval)
- (a) Non-stationarity: recompute δ per (key,d_idx) from EVAL moments with
  the EXACT integer rules above (C = conf column at d_prev; stayers =
  released at both d_prev and d; key from the eval depth-1 state file).
  Adjudicated only at depths with ≥200 pooled released transitions.
  Mismatch iff |applied − recomp_uncapped| > 42 (truncation slack 2 + cap 40).
  Cells with empty eval denominators excluded. KILL iff mismatches on >1/4
  of adjudicated key-depth cells.
- (b) Cross-family pooling: per analysis family F ∈
  {admit,revoke,logic,trap,cost,redteam,P,O,D}, per (key,d_idx) with
  n_stay≥8, n_all≥8 in BOTH the family-restricted and pooled eval moments:
  flip iff sign(E_F) strictly opposes sign(E_pooled) (zeros neutral).
  A depth counts for F if ≥1 key flips. KILL iff any family flips on ≥3
  depths. Full flip table reported regardless.
- (c) KILL iff eval strict B3 violations ≥ NEC m9's 6 (verified on frozen
  analyzer against sr_round/arch/results m9 legs).

## Evals
- `run_eval.sh f33full <policy_bin> 33 0` (gate 0 = MT-CONF-equivalent, no gate).
- Bars: B1–B9, B4b, amended B8 (§4b), B13; recorded B12, B3pi. Deltas vs NEC m9.
- NEC m9 reference legs: `training/sr_round/arch/results/*_m9_*`.
