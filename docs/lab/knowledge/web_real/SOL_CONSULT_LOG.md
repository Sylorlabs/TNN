# Sol consultation log — real TNN web-search architecture

Micah's order: use Sol (via UnoRouter) for coding help on this run; native
agents handle integration/testing/verification. This log records what was
asked, what Sol returned, and what was accepted, modified, or rejected.

Two consultations were made. Both are saved verbatim under `evidence/`.

---

## 1. Parser consultation — `evidence/sol_consult_parser.txt` (~802 lines)

**Asked:** design for a Zag-native, deterministic HTML parser: restricted
fixture grammar, parser states/transitions, entity decoding, malformed-input
recovery, expected edge cases.

**Received:** a full state-machine design with an explicit restricted tag
set, entity-decoding rules, deterministic recovery rules, and a checklist
of ~24 edge cases with expected outputs.

**Accepted (used as specified):**
- Byte state-machine parser; no backtracking, no RNG.
- Restricted tag set: html/head/body/title/h1/h2/h3/p/li/ul/ol/a/script/style.
- Blocks (title/h1/h2/h3/p/li) cannot nest; anchors may appear inside blocks
  and cannot nest.
- Comments, script bodies, and style bodies are skipped wholesale.
- Entity decoding: `&amp; &lt; &gt; &quot; &#39;` plus decimal numeric
  entities (with UTF-8 emission); unknown entities pass through literally.
- Whitespace collapse + trim; empty blocks dropped.
- Deterministic malformed-input recovery (unclosed tags flush at EOF,
  unexpected `<` becomes literal text, malformed tags scan to `>`).
- Link emission at `</a>`: `L|href|anchor text`; first href wins on
  duplicates.
- The full 24-case edge checklist, used verbatim as `parser_check.py`.

**Modified:** nothing in the design. Implementation details (arena
allocators, file-I/O path splitting, O_EXCL stale-output discipline) are
native adaptations to znc constraints, not design changes.

**Rejected:** nothing. The consultation was design-complete and correct;
all 24 checklist cases pass against the built parser.

---

## 2. Firewall + fetch consultation — `evidence/sol_consult_firewall.txt` (~52 lines)

**Asked:** design for (a) the load-bearing injection firewall scanner and
(b) the audited fetch bridge: canonicalization, pattern classes, allow-list
rules, redirect/retry policy, audit chaining, budgets, bounded reads, exit
codes.

**Received:** 13 numbered recommendations covering both components.

**Accepted (used as specified):**
- Firewall: ASCII-lowercase canonicalization; punctuation (`!`–`/`, `:`–`@`,
  `[`–`` ` ``, `{`–`~`) and whitespace fold to single spaces; collapse+trim;
  match whole canonicalized blocks only, never across block boundaries.
- Four fixed literal pattern classes (16 patterns total): direct commands,
  authority claims, trust redirection, AI-targeted conditionals — exactly the
  lists Sol gave, no additions.
- Flag rule: block is INJECTED iff >=2 DISTINCT classes match within that
  one block. Multiple hits in one class count once.
- Coverage-boundary documentation: homoglyphs, zero-width chars,
  misspellings, paraphrases, cross-block splits are NOT caught (residual).
- Fetch bridge: exact allow-list (http, host exactly 127.0.0.1, configured
  port, no userinfo, no fragment, absolute path); proxies disabled; fail
  closed on ambiguity.
- No redirects (3xx = failure), no retries, one request per invocation.
- Canonical chained JSONL audit (seq, run_id, ts, url, outcome, status,
  bytes_read, exit_code, prev_hash, record_hash; SHA-256 over canonical
  encoding; zero-hash genesis).
- Budgets in bridge-owned state keyed by supervisor run_id, incremented
  BEFORE network access; unknown run_id fails closed.
- Bounded read: max_bytes+1, oversize discards the body, nothing on stdout.
- Fixed exit codes 0/2/3/4/5/6/7/8/9 with the exact outcome mapping Sol gave.
- Bridge is a byte mover: no content inspection, no URL choice, no
  link-following.

**Modified:** one poison-fixture wording change (not Sol's design): the P1/P2
poison prose was strengthened so each poison page contains >=2 distinct
pattern classes within a SINGLE block. Sol's accepted design only flags a
block with >=2 distinct classes; the original draft prose spread classes
across two blocks and would have been CLEAR under the frozen rule. The rule
was kept; the fixture was made to match the threat model the rule covers.
This is documented, not hidden.

**Rejected:** nothing from the recommendations. Two native implementation
bugs found during testing were fixed without changing the design:
  - state-file rewrite appended instead of truncating (json "Extra data" ->
    spurious exit 8); fixed with seek+truncate.
  - urllib honored environment proxies (would have egressed loopback
    through the lab proxy); fixed with `ProxyHandler({})`.

---

## What Sol did NOT do

Per Micah's order, Sol supplied designs only. All implementation,
integration, testing, and verification were done natively:
- `src/html_parse.zag`, `src/fw_scan.zag`, `src/verdict.zag` written and
  debugged natively (4 parser bugs and 1 verdict bug found and fixed by
  native testing, none from Sol).
- `bridge/fetch.py` written natively to Sol's 13 recommendations; 2 native
  bugs found by the native bridge test battery.
- Fixture generator, fixture server, parser checklist, bridge tests,
  FIRST-CRAWL battery, kill-bar evaluation: all native.
- Independent integration verification: native subagent (see freeze doc).
