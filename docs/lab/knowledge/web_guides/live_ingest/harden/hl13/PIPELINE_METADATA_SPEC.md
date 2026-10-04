# PIPELINE_METADATA_SPEC.md — HL-13 metadata pipeline contract

**Status:** SPEC (pipeline decision pending — goes to Micah via parent report).
**Date:** 2026-09-24. **Workstream:** LI-HARDEN WALL-HL13.
**Companion:** `VERDICT_HL13.md` (verdict-layer mechanism + measured calibration).

## 1. Why this spec exists

The HL-13 verdict gate (`verdictp` in `build/hl13.zag`) detects operator
coincidence across the winning quorum's metadata. The verdict logic is
complete, deterministic, and calibrated — but it can only see metadata the
**fetch pipeline emits into `pages.txt`**. Today the production glue is
forbidden to emit metadata, so the gate sees `META=NONE` and is inert.
That is a **pipeline governance decision**, not a verdict-logic problem:
no change to the verdict binary can substitute for the pipeline emitting
the fields. This spec is the pipeline-side contract, so the governance
decision is concrete: *emit these fields, in this format, with these
trust semantics* — or explicitly decline.

## 2. Field list

| Key | Name | Source | Trust | Gate feature |
|-----|------|--------|-------|--------------|
| `T` | timestamp (epoch seconds, canonical text) | page-asserted (`<meta>`/time tags) | UNTRUSTED | yes |
| `L` | link target (canonical URL of the cited source) | page-asserted / extractor | UNTRUSTED | yes |
| `A` | author / byline | page-asserted | UNTRUSTED | yes |
| `SH` | site header | page-asserted | UNTRUSTED | report-only |
| `PB` | publisher | page-asserted | UNTRUSTED | report-only |
| `CG` | CMS generator fingerprint | page-asserted / extractor-derived | UNTRUSTED | yes |
| `R` | WHOIS/RDAP registrant email | **fetcher-observed** (WHOIS/RDAP) | SEMI | yes |
| `NS` | nameserver apex | **fetcher-observed** (authoritative NS query) | SEMI | yes |
| `IP` | IP /24 of the fetched host | **fetcher-observed** (DNS+TCP) | SEMI | reserved |
| `AD` | ad/analytics IDs (GA, AdSense, GTM) | extractor-derived (page HTML) | UNTRUSTED | reserved |

`T/L/A/SH/PB/CG` already exist in the instrument's observation set.
`R` and `NS` are the fable W3 additions (cheapest §7 weakening,
~$0.01/query). `IP`/`AD` are reserved keys for future W3/W8 buildout;
the verdict parser accepts and ignores unknown keys, so emitting them
early is safe.

## 3. Line format and placement

Metadata lines are emitted into `pages.txt` **immediately after the `P|`
page marker they describe** (same convention as the existing fields):

```
P|r1|Australia guide A [r1]
H|farm-one.example
T|1700000000
L|https://press-a.example/story
A|Alice Vance
SH|PressA
PB|Press A Org
CG=CMS-A 4.0  →  CG|CMS-A 4.0
R|op-acct@operator-mail.example
NS|operator-dns.example
```

- One line per key per page. `R|` and `NS|` are single/two-letter keys
  following the existing `A|`/`CG|` convention.
- **Escaping:** values are raw text up to end-of-line. A literal `|` or
  `\` inside a value is backslash-escaped (`\|`, `\\`) by the emitter;
  the verdict layer unescapes before comparison (existing behavior).
- **Duplicates:** last wins (deterministic; matches verdict parser).
- **Missing fields:** emit nothing. Absent metadata is NEVER coincidence —
  the verdict gate treats missing values as non-matching by construction.

## 4. Canonicalization (emitter side)

The verdict layer normalizes (lowercase, whitespace-collapse) before
comparing, but the emitter MUST still canonicalize:

- `R`: lowercase the registrant email; strip display-name wrappers
  (`"Name" <mail@x>` → `mail@x`); emit the RAW value even when it is a
  privacy-proxy string (`REDACTED FOR PRIVACY`, `WHOISGUARD`, …).
  **Do not launder at fetch time** — the verdict applies the
  privacy-proxy exclusion list, and the raw value stays in the audit trail.
- `NS`: emit the **apex** (registrable domain) of the authoritative
  nameserver, lowercased, no trailing dot:
  `ns1.cloudflare.com` → `cloudflare.com`.
- `T`: epoch seconds as canonical decimal text (existing behavior).

## 5. Provenance and trust levels

| Level | Meaning | Fields |
|-------|---------|--------|
| UNTRUSTED (page-asserted) | the page says this about itself; the attacker controls it | T, L, A, SH, PB, CG, AD |
| SEMI (fetcher-attested) | observed by OUR fetch infrastructure (WHOIS/RDAP/DNS), not asserted by the page; attacker can change it only by changing infrastructure (cost) | R, NS, IP |

**Why page metadata is attacker-controlled and cannot be treated as
trusted identity:** every `T/L/A/SH/PB/CG` value is bytes the site
operator chose to publish. A ring operator sets three different bylines,
three CMS fingerprints, three link targets for ~$0 and ten minutes.
Coincidence on these fields is evidence of *shared operation*, not of
*truth* — which is exactly why HL-13 uses it to block, never to promote.
`R`/`NS` are harder to diversify (registrar accounts, DNS migration,
~2h + ~$50 per fable's estimate), which is why they are the marginal-gain
features — but they are still operator-controlled, not identity.

## 6. R/NS acquisition (fetcher side)

- `R`: WHOIS or RDAP query per quorum domain at fetch time.
  Cost ~$0.01/query (fable W3 estimate). Cache responses keyed by
  (domain, date); **version the cache** — determinism requires that a
  rerun against the same evidence sees the same values.
- `NS`: authoritative NS query per quorum domain at fetch time; take the
  apex of the first nameserver. DNS cost is negligible; cache likewise.
- Both are per-domain, per-fetch — NOT per-claim. A 3-page quorum costs
  ~$0.03 in WHOIS fees.

## 7. Fail-open / fail-closed semantics

- **Absent metadata → fail OPEN.** If the pipeline emits no `R|`/`NS|`
  lines (or the WHOIS query fails, rate-limits, or times out), the
  verdict gate sees missing values and they contribute zero to every
  share count. The gate NEVER fires on missing data.
- **Malformed values → treated as missing** (verdict normalizes to empty).
- Rationale: the honest baseline (Crew B H1–H12, `META=NONE`) must keep
  installing 12/12. Fail-closed on missing metadata would convert every
  pipeline outage into a truth blackout.

## 8. Verdict-side policy (not pipeline, documented here for the contract)

The pipeline emits RAW values; the verdict binary applies policy:

- **R privacy-proxy exclusion:** registrant values normalizing to known
  proxy strings (`redacted for privacy`, `whoisguard`,
  `domains by proxy`, `privacy protect`, `contact privacy`,
  `withheld for privacy`, `data protected`) are treated as missing.
  Rationale: millions of unrelated honest domains share these strings;
  coincidence on them is meaningless.
- **NS provider whitelist:** apexes of large public DNS providers
  (`cloudflare.com`, `amazonaws.com` incl. `awsdns` hosts,
  `google.com`, `googledomains.com`) are treated as missing.
  Rationale: sharing Cloudflare is normal honest infrastructure (fable W11).
- **Gate rule:** block iff ≥2 of {A, CG, L, T, R, NS} reach share ≥3
  within the winning quorum (fable W3 rule; calibrated 2026-09-24).
  A lone shared byline, lone shared timestamp, or lone shared DNS
  provider NEVER blocks alone.

## 9. Linkage to fetch record

Each metadata line is bound to its page by position (lines following a
`P|<pid>` marker describe that pid until the next `P|`). The verdict
layer additionally requires the existing `INFO|DIVERSITY` and
`INFO|CANON` context. For audit: the (domain, fetch-timestamp,
WHOIS-cache-version) triple SHOULD be recorded in the fetch record so a
`GATE|OPCOIN|R+NS` decision is re-derivable.

## 10. What the governance decision must cover

1. May the production glue emit `T/L/A/SH/PB/CG` (page-asserted) metadata?
2. May the fetcher perform WHOIS/RDAP + NS queries and emit `R`/`NS`
   (adds ~$0.03 per 3-page quorum verdict; external dependency)?
3. Are `IP`/`AD` in scope now or reserved?
4. Who owns the R-proxy-exclusion and NS-whitelist lists (verdict
   policy, versioned with the binary)?

Until (1) is yes, HL-13 is inert on production traffic by design.
