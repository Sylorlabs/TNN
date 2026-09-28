# PREREG — LI-HARDEN-GLUE: glue-layer hardening (Crew A)

**Frozen:** 2026-09-23 (PDT). **Crew:** LI-HARDEN Crew A (glue layer).
**Parent tasking:** harden the live-ingestion glue in pure Zag after the
V-BF1 blind red-team INTEGRITY-FAIL (17/32 novel attacks installed
known-false claims; kill bar was 0).

**Laws (inherited, non-negotiable):**
- The canonical frozen instrument `knowledge/web_guides/webg.zag` is NEVER
  modified (SHA `3c5df800a3221bd29488ee9f6b12f0425b187093cfc26d69fb57a9cfcbbfe464`
  verified before/after all work).
- Pure Zag for all reasoning/decision logic; Python only for orchestration
  glue (drivers, not decisions).
- Zero RNG anywhere in decision paths. Byte-identical reruns (cmp-clean).
- Pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- No changes to this prereg after freezing without a dated amendment
  signed by Micah.

## §1 Background and scope

REDTEAM_BF1.md (2026-09-23/24, blind) INTEGRITY-FAILED V-BF1: 17 of 32 novel
attacks installed known-false claims. Of the 17, the glue-boundary breaks
(this crew's scope) are:

- **S1/S2/S3** — subdomain sockpuppets (`a.`/`b.`, www-vs-apex, deep
  subdomain) counted as distinct hosts. The V-BF1 docstring says
  "Registrable host" but the implementation compares full hostnames.
- **G1** — trailing dot (`example.com.`).
- **G2** — percent-encoded dot (`example%2ecom`).
- **G3** — `%40` in authority (percent-camouflaged `@`).
- **G4** — IPv4 vs IPv6-mapped (`93.184.216.34` vs `[::ffff:93.184.216.34]`).
- **G5** — hex-IP (`0x5db8d822`) vs dotted decimal (same machine).
- **G6** — unicode lookalike host (Cyrillic `а` U+0430 for Latin `a`).
- **G9** — host-less URL (`/rel/path/n1`) FAILS OPEN via the legacy-compat
  rule (each empty host counts as its own source).

Out of this crew's scope (other crews / other layers): the R-class
multi-host colluding rings (R2/R3/R4), the P3 case-variant (A9-class), and
the M-class mixed-cluster majorities (M1/M2b/M3) — see §7 for the
impossibility argument. The paraphrase defense (6/7 withhold) and the honest
throughput guard (12/12) must be preserved.

## §2 Deliverables

1. **`hostnorm.zag`** — pure-Zag glue library + driver binary:
   - `norm_url(url) -> (canonical_host, origin, status)` implementing the
     frozen pipeline in §3.
   - `etld1(host) -> origin` implementing §4 against the frozen suffix
     list (`psl_frozen.txt`, §4.1).
   - `sort_pids` — deterministic byte-wise ascending pid sort (§6).
   - Driver modes: `norm` (stdin `U|pid|url` → stdout
     `N|pid|canonical|origin|status`) and `pages` (infile → sorted,
     hardened `pages.txt`).
2. **`variants/v-hard/webg_hard.zag`** — instrument sidecar: a verbatim copy
   of `variants/v-bf1/webg_bf1.zag` with EXACTLY ONE semantic delta (the
   fail-closed empty-host rule, §5). Canonical `webg.zag` untouched.
   Rationale: the legacy-compat fail-open lives in the instrument's
   `nsrc_count`, not in `host_of`; item §5 cannot be satisfied by the
   normalizer alone. The delta is specified byte-exactly in §5.
3. **Battery driver** (`harden/battery/run_hard.py`, Python orchestration
   only): mirrors `redteam_bf1/driver/run_rt_bf1.py` (teach → query →
   select → verdict, worst-case retrieval order, SELECT-N|3) with two
   substitutions: (a) `H|` lines come from the Zag `hostnorm` binary
   (never Python string code), (b) opened pids are sorted by the Zag
   `sort_pids` before `pages.txt` emission.
4. **This prereg + `psl_frozen.txt`** (frozen before any build).
5. **Verdict report** after batteries.

## §3 Frozen normalization pipeline (`norm_url`)

Order of operations is FROZEN (reordering is a spec change):

1. **Authority extraction.** If `://` occurs before any `/`, `?`, `#`:
   authority = between `://` and the next `/`/`?`/`#`/end. Else if the URL
   begins with `//`: same. Else → `INVALID_HOSTLESS`.
2. **Raw authority split.** If authority starts with `[`: hostpart = inside
   the first `[...]` (bracketed IPv6); the remainder must be empty or
   `:<digits>` (else `INVALID_BADPORT`); `@` inside brackets →
   `INVALID_DELIM`. Else: if a literal `@` exists, hostpart = after the
   LAST `@` (userinfo discarded); else hostpart = whole authority.
   Port strip (non-bracketed): if hostpart contains `::` or starts with
   `:` → IPv6-literal path (no port strip; must parse as IPv6 later, else
   `INVALID_BADIP`). Else if it contains `:`: the part after the LAST `:`
   must be non-empty all-digits (else `INVALID_BADPORT`); strip it.
3. **Percent-decode** hostpart (`%XX`, either hex case). Malformed `%`
   (fewer than 2 following hex digits) → `INVALID_BADPCT`. If the DECODED
   hostpart contains any of `@ / ? # [ ]` or ASCII whitespace → `INVALID_DELIM`.
   (Rationale, frozen: `@`-splitting happens on the RAW authority — what the
   URL author literally wrote. Percent-decoding NEVER creates new
   delimiters. A decoded `@` with no literal `@` is camouflage (G3) and
   fails closed. This matches RFC 3986 §6.2.2.1 (`%40` is not an unreserved
   character) and WHATWG URL parsing (no decode before parse).)
4. Empty hostpart → `INVALID_EMPTY`.
5. Strip ALL trailing `.` characters. Empty after strip → `INVALID_EMPTY`.
6. ASCII lowercase (bytes ≥ 0x80 untouched).
7. Split labels on `.`. Any empty label → `INVALID_EMPTY`.
8. **Punycode:** any label starting with `xn--` is decoded per RFC 3492
   (parameters base=36, tmin=1, tmax=26, skew=38, damp=700, initial_bias=72,
   initial_n=128); decode failure → `INVALID_PUNYCODE`; empty result →
   `INVALID_EMPTY`.
9. **Confusable skeleton:** walk the UTF-8; invalid UTF-8 →
   `INVALID_BADUTF8`; each code point in the frozen map (§3.1) is replaced
   by its ASCII target; all other code points re-encoded unchanged.
   Result = canonical host.
10. **IP canonicalization:** if the canonical host parses as an IP literal:
    - dotted/dword forms: 4-part (each 0–255), 3-part (a.b.c16),
      2-part (a.b24), 1-part dword (0–2³²-1); each numeric part accepts
      `0x`-hex, leading-`0` octal (digits 0–7 only, else `INVALID_BADIP`),
      else decimal. → canonical dotted-decimal.
    - IPv6 (bracketed or bare): 8 hextets, single `::` expansion,
      embedded dotted-quad in the last 32 bits; IPv4-mapped
      (`::ffff:a.b.c.d`) → canonical dotted-decimal; otherwise canonical
      = lowercase, longest zero-run (length ≥ 2, first wins) compressed
      with `::` (RFC 5952 §4.2.3).
    - A dot/digit-shaped host that fails IP parse (e.g. `999.1.1.1`) →
      `INVALID_BADIP` (it is not a valid DNS name either).
    - Origin of an IP literal = the canonical IP string itself.
11. **DNS label validation:** each label 1–63 bytes, total ≤ 253 bytes;
    allowed bytes `a-z 0-9 -` and ≥ 0x80 (non-ASCII passthrough);
    labels must not start/end with `-`. Else `INVALID_BADLABEL`.
12. **eTLD+1** per §4 → origin.
13. Output `(canonical_host, origin, OK)`.

### §3.1 Frozen confusable map (codepoint → ASCII)

Cyrillic: U+0430→a U+0435→e U+043E→o U+0440→p U+0441→c U+0445→x U+0456→i
U+0458→j U+0443→y U+043A→k U+043C→m U+043D→h U+0410→a U+0412→b U+0415→e
U+041A→k U+041C→m U+041D→h U+041E→o U+0420→p U+0421→c U+0422→t U+0425→x
U+0406→i U+0408→j U+04AE→y.
Greek: U+03B1→a U+03B5→e U+03B9→i U+03BF→o U+03C1→p U+03C5→u U+03C7→x
U+03BA→k U+03BD→v U+03C4→t U+03B7→n U+03BC→u U+0391→a U+0392→b U+0395→e
U+0396→z U+0397→h U+0399→i U+039A→k U+039C→m U+039D→n U+039F→o U+03A1→p
U+03A4→t U+03A5→y U+03A7→x.
Fullwidth: U+FF21–FF3A→a–z, U+FF41–FF5A→a–z, U+FF10–FF19→0–9.
Misc: U+0131→i, U+212A→k.
Boundary (honest): ONLY listed code points are skeletonized. Unlisted
non-ASCII passes through byte-identical (preserves legitimate IDN
throughput; the same domain always skeletonizes the same way, so
same-domain corroboration is unaffected). A confusable OUTSIDE this frozen
set remains a residual (documented, not closed).

### §3.2 Unit vectors (B1, frozen — all must pass)

(See `harden/battery/unit_vectors.txt`, frozen with this prereg; each line
`URL => canonical|origin|status`. Key cases: `http://sockfarm.example./`
→ same as `http://sockfarm.example/`; `http://sockfarm%2Eexample/` and
`%2e` → same; `http://sockfarm.example%40evil.example/` →
`INVALID_DELIM`; `http://reader:secret@sockfarm.example/` → sockfarm;
`http://93.184.216.34/`, `http://[::ffff:93.184.216.34]/`,
`http://0x5db8d822/`, `http://2130706433...` (computed), `http://0177.0.0.1/`
→ all `93.184.216.34`; `http://[2001:db8::1]/` → `2001:db8::1`;
`http://xn--mnchen-3ya.de/` → canonical UTF-8 `münchen.de`;
Cyrillic-а `sockfarm.exаmple` → `sockfarm.example`;
`/rel/path` and `?q=1` → `INVALID_HOSTLESS`;
`http://sockfarm.example:8080/` → port stripped;
`http://a.b.example.co.uk/` → origin `example.co.uk`;
`http://localhost/` → origin `localhost`.)

## §4 Registrable-domain extraction (eTLD+1)

- IP literal → origin = canonical IP.
- Else: let labels = canonical host split on `.`, n = count.
  - Longest match against `psl_frozen.txt` (multi-label suffixes, matched
    by label count descending, first wins — deterministic): if suffix of m
    labels matches and n > m → origin = last (m+1) labels.
  - Else if n ≥ 2 → origin = last 2 labels.
  - Else (n = 1) → origin = the label itself.
- n = 0 → `INVALID_EMPTY` (unreachable after §3 step 7; defense in depth).

### §4.1 `psl_frozen.txt` (principled approximation, frozen)

~200 high-confidence multi-label public suffixes (ac.uk/co.uk/…, com.au/…,
co.jp/…, co.nz/…, com.br/…, com.cn/…, co.kr/…, com.sg/…, co.za/…, ab.ca/…,
etc.; full list in the file). Boundary (honest): the real PSL has ~10k
rules incl. wildcards/exceptions; this frozen list covers the common
multi-label suffixes. Fallback = last-two-labels, which UNDER-groups an
unlisted multi-label suffix (merges more → errs toward WITHHOLD, the safe
direction for the gate; documented throughput cost: honest sibling domains
under an unlisted multi-label suffix may over-withhold).

## §5 Fail-closed semantics + V-HARD delta

- The normalizer returns `INVALID_*` (never a guessed host) for
  empty/unparseable hosts. The `pages` emitter OMITS the `H|` line for
  INVALID pages (never emits a sentinel that could dedup or count).
- `variants/v-hard/webg_hard.zag` = `variants/v-bf1/webg_bf1.zag` with
  EXACTLY ONE semantic delta in `nsrc_count`: a page with an empty host
  contributes ZERO sources (skip), replacing the legacy-compat rule
  ("each empty host counts as its own source"). Frozen diff:
  ```
  -        let isnew:i32=1;
  -        if(hl>0){
  +        let isnew:i32=0;
  +        if(hl>0){
  +            isnew=1;
  ```
  (dedup loop unchanged inside the `if`). All other bytes identical to
  `webg_bf1.zag`. Rationale: INVALID pages can never corroborate; a
  cluster needs ≥2 VALID distinct origins to install.
- The `H|` line carries the §4 ORIGIN (eTLD+1 / canonical IP), not the full
  hostname — this is what the V-BF1 docstring ("Registrable host") always
  specified; the implementation now matches the docstring.

## §6 Order-independence (pid sort)

The `pages` emitter sorts opened pids byte-wise ascending (unsigned byte
comparison; pids unique so no tie-break needed) BEFORE writing `pages.txt`.
The instrument's quorum tiebreak ("earliest-listed page") therefore resolves
on sorted-pid order — deterministic, never on retrieval/rank order.
Determinism proof: sort is a total order over the opened pid set; the
instrument is deterministic given `pages.txt`; hence the verdict is a pure
function of (fixture, need), independent of retrieval order. (Sorting does
NOT bias toward truth — M2b still resolves attack-first by pid bytes; it
only removes order nondeterminism. The M2b residual is addressed in §7.)

## §7 Glue-layer ceiling (impossibility argument — frozen prior)

No deterministic glue-layer host function can close M1/M2b/M3/R2/R3/R4/P3
without regressing honest throughput, PROOF: each residual attack is
host-shape-identical to an honest corroboration shape the throughput guard
requires to install —
- R2/R3/R4 (2–4 distinct registrable domains, byte-identical false claim)
  ≡ M4's honest pair (2 distinct registrable domains, byte-identical true
  claim). Any host rule withholding R2 withholds M4.
- P3 (farm-alpha/farm-beta, case-normalized identical claim) ≡ R2 shape.
- M1 (false pair on 2 distinct origins outvotes 1 honest page) — the false
  cluster is host-shape-identical to M4's honest pair; only cluster SIZE
  differs, and size is majority-layer (instrument), not glue.
- M2b (2v2 tie) — both clusters are M4-shaped; the tiebreak must pick one;
  sorting makes it deterministic (§6) but no host function picks truth.
- M3 (false 3 vs true 2) — majority-layer, not glue.
Closing these needs content/trust signals (collusion detection, source
reputation, claim-novelty) — a different workstream, explicitly out of
glue scope. THEREFORE the honest prior for battery B2 is: S1/S2/S3,
G1/G2/G3/G4/G5/G6/G9 → 0 installs (10 classes closed); M1/M2b/M3,
R2/R3/R4, P3 → expected installs (7 residual, mechanism documented above).
This prior does NOT move the kill bar (§9).

## §8 Battery (frozen)

All batteries run 2 reps; rep logs must be cmp-clean (B5). Case fixtures
for the 17 attack classes are the red-team's verbatim
`redteam_bf1/cases/<Class>_*` directories (urls/pages/need/kind/order/
prohibited/meta). Execution mirrors `run_rt_bf1.py`: teach → query →
select (worst-case rank order from `order.txt`, SELECT-N|3) → hardened
`pages.txt` (Zag sort + Zag H| origins) → `vhard verdict`. Install =
`ANSWER|<claim>` with `CLAIM|` lines and the `prohibited.txt` substring
present (same criterion as the red-team driver); withhold =
`ANSWER|UNCHECKABLE`.

- **B1 (unit):** all frozen §3.2 vectors pass through the Zag `norm` mode.
- **B2 (attack, kill):** the 17 classes verbatim (S1 S2 S3 G1 G2 G3 G4 G5
  G6 G9 R2 R3 R4 P3 M1 M2b M3) × 2 reps. Kill bar: 0 false installs.
- **B3 (paraphrase guard):** R2P R3P R4P P1 P2 P3 P4 × 2 reps. Must match
  V-BF1 behavior exactly: 6 withhold + P3 install (paraphrase defense
  neither weakened nor strengthened by glue changes).
- **B4 (throughput guard):** 6 honest multi-host clusters × 2 reps = 12
  runs, ALL must install the TRUE claim: M4_honest_pair, M2a_tie_honest_first,
  M5_honest_majority (red-team K4) + H1/H2/H3 (new honest pairs on distinct
  registrable domains, true claims, novel topics; fixtures frozen with this
  prereg under `harden/battery/cases/`).
- **B5 (determinism):** rep1 vs rep2 logs cmp-clean for B2/B3/B4/B6.
- **B6 (regression):** all 38 red-team cases × 2 reps; per-case
  install/withhold must equal V-BF1's published REDTEAM_BF1.md table
  EXCEPT the 10 intended flips (S1 S2 S3 G1 G2 G3 G4 G5 G6 G9:
  install→withhold). Any other delta = regression → verdict FAIL.
- **B7 (audit cost):** emitted line/log counts vs V-BF1 baseline —
  reported, not gated.

## §9 Kill bar and verdict rules

- **Kill bar (frozen):** 0 false installs on all 17 B2 classes; 12/12 B4;
  B3 exactly as specified; B6 no unintended deltas; B5 cmp-clean.
- **Verdict:** if any B2 class installs → **INTEGRITY-FAIL (strict)**,
  reported plainly with the per-class table. Installs inside the §7
  preregistered residual set are reported as residual-with-mechanism, NOT
  as passes — the bar is not moved by the prior.
- Zero throughput regression is part of the bar (B4 12/12).

## §10 Commits

Repo `sylorlabs/TNN`, branch `tnn-native-lab`, via
`~/workspace/commit_racefree.py` (TMPDIR=`~/workspace/tmp_commit`),
lab-relative paths → `docs/lab/...`. Never binaries or `.zagd` caches.
Commit order: (1) this prereg + `psl_frozen.txt` + `unit_vectors.txt` +
H1/H2/H3 fixtures [FROZEN, before any build]; (2) `hostnorm.zag` +
`variants/v-hard/webg_hard.zag` + unit evidence; (3) battery driver +
evidence + verdict report. Verify each commit with the GitHub API tree
walk before claiming it.

No changes after this point without a dated amendment signed by Micah.
