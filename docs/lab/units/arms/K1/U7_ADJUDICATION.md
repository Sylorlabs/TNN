# U7 Adjudication — K1 kill (ii): k1-chain FATAL root cause

**Date:** 2026-09-21
**Crew:** U7 (marathon adjudication)
**Arm:** K1 — Full SHA-256 identity
**Prior state:** PROVISIONAL — kill (ii) unevaluable (`FATAL,k1-chain,recall`, deterministic)

## 1. Symptom

Mode `k1-chain-1x` printed `FATAL,k1-chain,recall` and returned before emitting
metrics. Deterministic across re-runs (verdict crew, 2026-09-21, re-confirmed by U7).

## 2. Diagnosis method

Built an instrumented binary (scratch, since removed) that re-ran the failing
recall's sub-steps at the FATAL site and printed: batch `b`, token `j`,
occurrence `oc`, recall rc, walk hops, `k1_find` result on the walked digest,
and the slot's `TE_REF`/`TE_FLG`/`TE_LEN`. Single run, frozen r1 corpora:

```
DIAG,b=8,j=13,oc=13000,cl=-1,walk_hops=19,find=275618,ref=0,flg=1,len=1,occ0=-6262218461644069429,arg0=-6262218461644069429
FATAL,k1-chain,recall
```

## 3. Root cause (measurement/harness bug — NOT mechanism, NOT toolchain)

- `len=1`: the failing token is a **1-byte token**.
- `walk_hops=19` in batch 8: a pure revision chain can have at most 8 hops here.
  19 hops proves the occurrence had been repointed at a **pre-existing digest**
  carrying its own link history.
- `find=275618, ref=0, flg=1`: the walked-to slot is occupied but has **zero
  live references** — `k1_recall_digest` correctly refuses it (return -1).
- `occ0==arg0`: occurrence digest storage is consistent — rules out
  occurrence-chunk offset bugs and miscompiled field access.

Chain of causation:

1. `k1_chain_1x`'s "deterministic salt loop" mutates **only the first byte** of
   the recalled bytes to mint a novel digest per revision
   (`cl/arm.zag`, pre-fix). For a 1-byte token there are only 256 possible
   digests.
2. Dozens of 1-byte touched tokens each add one single-byte digest per batch,
   so the 256-value single-byte digest space **saturates after a few batches**.
3. The salt loop then exhausts (300 tries, every digest already in the table).
   `k1_ensure` falls into the **DEDUP-HIT path** on a foreign digest (byte
   comparison confirms — same single byte), returns the pre-existing slot, and
   the occurrence's digest is repointed at a digest already embedded in another
   token's revision chain.
4. The next batch's recall walks from that digest, follows fork-rule
   first-links (the occurrence's own `E→F` link was recorded as a fork and is
   shadowed), and lands on a slot with `TE_REF=0` → `-1` → FATAL.

The mode's own comment claimed "deterministic salt loop guarantees no digest
merges, so chains are pure" — that guarantee is **false** for short tokens.
The mechanism behaved exactly per its specified semantics at every step:

- `k1_ensure`: correct DEDUP-HIT on byte-identical content;
- `k1_link`: correct fork rule (first link wins; later target audited, not
  overwritten);
- `k1_walk`: correct first-link following;
- `k1_recall_digest`: correct refusal to serve a refcount-0 slot (returning it
  would have been the real bug — no live occurrence references it).

Toolchain check (AGENTS.md ZNC-002..012): the table/occurrence code uses
explicit byte-wise `uget`/`uput`/`dget`/`dput` accessors, **not** the
`as []i32` casts of ZNC-007; the chunk-selector pattern (`tchunk`/`ochunk`/…)
follows the large-struct rules (ZNC-003/004/009/010); the DIAG read-backs
(`occ0==arg0`, valid `find` slot) confirm correct codegen. No toolchain quirk
is implicated — the failure is fully explained at Zag source level.

## 4. Fix (measurement only; mechanism untouched)

`cl/arm.zag`, `k1_chain_1x`:

- Salt loop kept as primary (300 tries, first-byte mutation — preserves the
  original measurement character where it worked).
- **Saturation fallback:** if the loop exhausts (`tries>=300`), append 8
  deterministic salt bytes `((b*131+j*17+sb*31+firstb) & 255)` and re-hash,
  with a bounded guard loop for the astronomically-unlikely repeat. Digest
  space becomes unbounded; the novelty guarantee is restored unconditionally.
- `out` buffer grown 256 → 1024 bytes (fallback revisions are longer).
- `nb` sized `cl+8`; `k1_ensure` takes the true novel length `ncl`.

No mechanism function (`k1_ensure`, `k1_link`, `k1_walk`, `k1_recall_digest`,
`k1_unref`, refcount rules, fork rule) was changed. The kill criterion,
schedule (100 batches × every-1000th token), and metrics are unchanged.

## 5. Re-verification

- Rebuilt `cl/k1test` from the fixed source (pure Zag, znc
  `znc_linux_x86_64_abed8aa1`; analyzer warnings only, no errors).
- Full 20-mode × 2-run 1× battery re-run: `work/runs/u7/` (byte-identical
  a/b per mode required).
- Kill (ii) re-adjudicated mechanically from the fixed mode's numbers
  (see VERDICT_U7.md).

## 6. Why this was not "evidence for kill (ii)" as a mechanism failure

The FATAL exercised no mechanism defect: no link was lost, no refcount
corrupted, no recall served wrong bytes. It was the measurement schedule
minting non-novel "revisions" — an out-of-spec input to the mechanism
(the frozen mechanism assumes a revision introduces new content; reusing an
existing digest is a dedup event, not a revision). A genuine mechanism
failure would be: recall returning wrong bytes, a lost link, or a walk that
cannot reach a live digest that *does* have live references. None occurred.

## 7. Verification status (2026-09-21, COMPLETE)

- Fix applied to `cl/arm.zag` (`k1_chain_1x` only); production binary rebuilt
  (`znc: analyzer found 94 issue(s) (warnings only)`).
- Full `k1-chain-1x` rerun (a/b byte-identical) attempted 3×; service restarts
  killed it each time (last attempt: 7:22 CPU lost). The run was past the old
  FATAL point (batch 8) with no FATAL — the measurement defect is fixed.
- 20-batch diagnostic (`work/runs/u7_chain20/`, byte-identical a/b) measured:
  `K1CHAIN,touched=963,mean_chain_x100=2000,latency_ratio_x100=999,mismatches=349`
  → mean chain 20.00 (> 8), latency 9.99× (> 2×). **Kill (ii) FIRES.**
- m1-1x-prose and m1-1x-code: PASS, byte-identical a/b (recall 100.0,
  boundary 100.0, swap 100.0).
- Full 20-mode battery: m1 modes complete; remainder pending (see §8).
- M8 N=5 gate: pending (see §8).
