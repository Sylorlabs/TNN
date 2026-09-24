# CAP ground truth -- kill bar P5

## Measurement (machine-derived; lab VM, 2026-09-24)

MemAvailable fluctuates with machine load, so the count is derived at run
time by the frozen generator -- the numbers below are the authoring-time
snapshot, illustrating the derivation:

- /proc/meminfo MemAvailable (authoring snapshot): 2742124 kB = 2807934976 bytes
- Budget = floor(MemAvailable_bytes / 64) = 43874109 bytes
- Worst-case pending line for a fresh-state run (pending seqs 1..count):
  `PENDING|<seq>|The marker stone <i> stands <i> meters tall.|DELIBERATE`
  plus trailing newline = 59 + 3*d bytes, where d = decimal width of count
  (claim = 38 + 2*d bytes; line = 8 + d + 1 + claim + 11 + 1).
- count = floor(budget / worst_line_cost) + 1 at the fixpoint width:
  snapshot -> floor(43874109 / 77) + 1 = 569694
  (d = 6; 569694 < 10^6, so the width assumption holds).

Normative procedure for the driver:
1. `python3 gen_cap.py --out cap_claims.txt 2> cap_gen.log` -- the generator
   prints `gen_cap: MemAvailable=<b> budget=<b> worst_line_cost=<b> count=<N>`
   to stderr; commit cap_gen.log with the run.
2. Pin `--count N` (the printed N) for the second (P6) pass so both passes
   present identical input even if MemAvailable drifts between runs.
3. `kbpend cap_claims.txt <state>` on a fresh state dir (pending counter
   starts at 1; knowledge.txt holds the 12 frozen KB claims; record its
   SHA-256 before and after).

The presented bytes (worst case) are guaranteed to exceed the budget: the
count is the minimum integer with count * worst_line_cost > budget.

## Expected (kill bar P5)

(a) Accounting identity: presented (= N from the generator log) =
    stored + shed + resolved + refused, exactly. (Reference shape:
    resolved = 0, refused = 0 -- every generated line is parse-gate clean.)
(b) The shed set is the oldest seqs {1..k} for some k >= 1 (k is
    byte-accounting determined; the bar checks the PREFIX property, not the
    exact k). knowledge.txt SHA-256 identical before/after: no committed
    claim is ever shed.
(c) shed_ledger.txt line count == shed count; every shed claim text present
    verbatim as `SHED|<seq>|<claim>`.
(d) Two consecutive runs byte-identical across pending.txt,
    shed_ledger.txt, resolutions.txt and pending_init.log.

## Authoring notes

- Claim text omits the `CAP|<i>|` pipe prefix sketched in prereg S8: the
  frozen S3 claim-text field rule forbids `|` in claim text and the parse
  gate rejects such lines. Digits remain exact (the index appears twice).
- CAP claims CONTRADICT-bind each other (shared template, differing
  digits), which is benign: kbpend checks candidates only against committed
  knowledge.txt, where no bind reaches 2/3 for any index width (checked on
  the template by verify_battery.py).
- Claim cost uses the worst-case line width so the presented bytes are
  guaranteed to exceed the budget even at the widest seq/index widths.
