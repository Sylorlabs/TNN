# README replacement text — STORAGE section (DRAFT, numbers pending final matrix)

## Proposed replacement for the "So what's the catch: STORAGE" section

### Old (to be struck)

> "So what's the catch: STORAGE ... ~220 bytes/fact (~92 slot + ~128 audit)"

### New

**Storage: knowledge now costs ~6 bytes per fact.**

Each fact TNN learns — a distinct thing it knows, with its meaning,
its confidence, and when it learned it — takes about 6 bytes of RAM.
A million facts fit in ~6 MB. Ten million in ~60 MB.

How we got here (all measured pure, deterministic, all tested�):
1. **Removed redundancy (92→36B):** The fact's ID was stored twice;
   the audit log was 70% zeros; constant fields were repeated per-fact.
   Removing these changed nothing — the information is identical.
2. **Replaced the audit ledger with a hash chain (36→12B):** The old
   ledger wrote 64 bytes per fact describing what was learned. But that
   description was derivable from the facts themselves, so we stopped
   writing it. A SHA-256 chain over the facts provides tamper evidence
   (the old ledger had none).
3. **Packed values by observed width (12→6B):** Each 4,096-fact chunk
   uses only as many bytes per value as its largest value needs.

What didn't change: every fact is still explicit, countable,
individually addressable, revisable, and deletable. Install speed
(~6.8 µs/fact) and recall speed (~11M probes/sec) are as fast or
faster. The knowledge is provably identical (byte-identical digests).

### What this does NOT claim

- This is RAM (process heap), not disk. Knowledge still disappears on exit.
  Persistence is a separate problem.
- The identity-index step assumes dense-sequential fact IDs. Sparse or
  external IDs need a hash fallback (documented crossover).
- "Bytes per fact" is the written/used basis. The allocator reserves
  slightly more (virtual); untouched pages may not be resident (RSS).
