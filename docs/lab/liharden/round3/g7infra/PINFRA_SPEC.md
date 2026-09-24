# PIN/CITATION INFRASTRUCTURE SPEC (g7 round 3 — Crew B)

Pure-Zag, zero RNG, raw bytes, byte-identical reruns. This spec is the frozen
design; the prereg (`PREREG_G7.md`) freezes the falsification battery.

## 0. Problem

Round 2 (BEYOND) measured g7's ≥25-token length gate ALONE as unsafe: it fires
on the honest T5 long wire as well as the false F7 long ring. BEYOND's safety
came from two hatches that Tier-1 lacked:

- archive-sentence hatch: claim present in a pre-attack archived sentence table
- shared-CITE hatch: all voters cite one identical URL

Both hatches were metadata-level (a `CITE=` string match, a `SENT|` line).
Round 3 hardens them into real infrastructure:

1. **CITATION EXEMPTION** — the cited URL must actually CONTAIN the sentence,
   byte-verified against a PINNED snapshot, and the pin must be OLDER than the
   quorum members.
2. **ARCHIVED-PRESENCE EXEMPTION** — long sentences with pre-attack archived
   presence are exempt (real technical facts propagate by copying).

Governance constraint (standing): NO live WHOIS/RDAP/NS/DNS queries anywhere in
the decision path. Everything metadata-shaped arrives as PINNED,
content-addressed, versioned snapshots. The verdict binary never touches the
network or the live DNS.

## 1. What is pinned

A **pin** is an immutable content-addressed snapshot record:

```
PIN = { url, fetched_at (unix seconds), sha256 (hex, 64 chars), bytes }
```

- **Content-addressed**: the pin's identity is `sha256(bytes)`. The verdict
  binary re-hashes every pin payload it consumes and rejects the pin on
  mismatch (corruption detection: this lab has measured silent truncation
  producing rc=0 with partial artifacts — the hash is the tripwire).
- **Versioned**: many pins may share one URL with different `fetched_at`.
  Versions are ordered by `fetched_at`; nothing is ever mutated in place.
  Era roll (legitimate supersession) = add a newer pin version.
- **Kinds**:
  - `CPIN` — citation-candidate pin: a snapshot of a citable source
    (commission report, RFC text, statute text). Exemption needs a CPIN whose
    URL equals the voters' shared CITE URL.
  - `APIN` — archive pin: a snapshot of the pre-attack corpus. The binary
    extracts its normalized sentences into the archive-sentence table.
  - `CALIB` — calibration pin: the derived gate bound (see §4). One pin,
    versioned like the rest.

Pin **bytes** are single-line UTF-8 text (no trailing newline) in fixtures;
the canonical byte stream is exactly the payload line bytes. The pipeline
(driver) hashes the canonical stream; the binary reconstructs the same stream
from stdin and verifies.

## 2. What is computed at verdict time (decision path)

Inputs: the fixture bundle on stdin (pages, NEED, URLs, `M|pid|FETCH=` /
`CITE=` metadata, pin descriptors, pin payloads, calibration payload).

1. **Normalize + cluster** (ported from BEYOND base, byte-identical
   normalization: lowercase ASCII, punctuation→space, controls dropped,
   bytes≥128 kept significant, spaces collapsed, padded with one space each
   end). Claim = max (pagecount, need-overlap), tie → lexicographic min.
2. **Votes/hosts**: pages containing the claim; distinct hosts. Base quorum:
   `nvotes>=2 && nhost>=2` → INSTALL absent other gates.
3. **Pin verification**: for each `PINB|<name>|<sha>` payload, `ns_sha256`
   over the payload bytes; mismatch → pin REJECTED (exemption unavailable),
   counted in the verdict line (`pinbad=N`).
4. **Archive table**: each verified APIN's bytes are normalized and split
   into sentences on `.`/`!`/`?` boundaries; each sentence stored with its
   pin's `fetched_at`.
5. **g7infra gate** (see §4): fires iff `claim_bytes >= L0 && nhost >= 3`.
6. **Exemptions** (evaluated only when the gate fires):
   - **(C) Citation**: every voting page carries `CITE=<url>`, all identical;
     AND ∃ verified CPIN with `pin.url == cite` AND `pin.fetched_at <
     min_voter_fetch` AND `bsub(normalize(pin.bytes), claim) == 1`.
     All four must hold. A cited URL with no pin, a pin that fails the hash,
     a pin that doesn't contain the sentence, or a pin NEWER than the quorum
     → no exemption.
   - **(A) Archived presence**: ∃ verified APIN sentence `s` with `s ==
     claim` (byte equality on normalized bytes) AND `pin.fetched_at <
     min_voter_fetch`.
   - `min_voter_fetch` = minimum `FETCH=` over voting pages. Any voter
     missing `FETCH=` → exemptions fail CLOSED (no exemption).
7. **Verdict**: gate fires and neither exemption holds → `COPYCOLLAPSE`
   (WITHHOLD). Otherwise the base verdict stands.

## 3. Exact exemption rules (normative)

```
CITATION_EXEMPT  :=  (∀v ∈ voters: CITE(v) = U ≠ ∅)
                 ∧ (∃p ∈ verified CPINs: p.url = U
                      ∧ p.fetched_at < min_{v}(FETCH(v))
                      ∧ claim ⊆_bytes normalize(p.bytes))

ARCHIVE_EXEMPT   :=  (∃p ∈ verified APINs, ∃s ∈ sentences(p):
                        s = claim  ∧  p.fetched_at < min_{v}(FETCH(v)))

GATE_FIRES       :=  len_bytes(claim) ≥ L0  ∧  nhost ≥ 3

verdict          :=  GATE_FIRES ∧ ¬CITATION_EXEMPT ∧ ¬ARCHIVE_EXEMPT
                      ? WITHHOLD|COPYCOLLAPSE
                      : base_verdict
```

Notes:
- `⊆_bytes` is byte-substring on NORMALIZED bytes (normalization is
  deterministic and identical on both sides, so trailing-whitespace and
  punctuation variants cannot smuggle a miss).
- The cited pin must be OLDER than every quorum member: a ring cannot
  manufacture a citation after the fact and backdate it, because pins are
  append-only and `fetched_at` is set by the pinning pipeline, not by the
  page author. (Pipeline trust is explicit: see §6.)
- One-word mutations of a real spec ("copies a real spec and swaps one word")
  FAIL the byte check by construction → no exemption → collapse. This is
  intended: a mutated quote is not the cited sentence.

## 4. The gate bound L0 — derived, not hardcoded

Micah's standing law forbids arbitrary design limits. The round-2 `≥25`-token
constant is NOT carried over. Instead:

- **Measured quantity**: `Lmax` = maximum normalized claim byte-length over
  the frozen honest calibration corpus (fixtures H1..H12, the prereg's honest
  regression set — the attack fixtures are the TEST set, never the
  calibration set).
- **Bound**: `L0 = K × Lmax`, `K = 2` default. `K` is the tunable margin;
  `L0`, `K`, `Lmax`, and the corpus identity are recorded in the CALIB pin
  (content-addressed, versioned). Re-tuning = re-pinning, never a code change.
- **Justification**: the gate demands copy-evidence (citation or archive
  presence) only for coincidences strictly more surprising than the longest
  honest claim on record, with margin K. The host floor `nhost ≥ 3` is carried
  over from round 2's measured operating point (F7/T5 both have 3 hosts).
- **Derivation procedure** (mechanism's own measurements): the binary's
  `measure` mode emits each calibration fixture's claim byte-length under the
  binary's own normalization; the driver takes the max, multiplies by K,
  writes the CALIB pin. No Python-side normalization reimplementation touches
  the bound.

Measured calibration (this build): `Lmax = 39` bytes
(`" the tradition is 100 to 150 years old "`, H7_range_agree — measured by the
binary's own `measure` mode; a pre-run Python approximation said 40 and the
prereg was amended per its void clause),
so `L0 = 78` bytes at `K = 2`. Full distribution in `pins/calibration.txt`
and `evidence/calibration.tsv`.

Consequence for the honest battery: no honest fixture claim reaches 78 bytes
(max 39), so the gate never fires on the 12 honest fixtures — the honest
regression is structurally protected, not luck-protected. T5 (202 bytes)
fires and is rescued by its citation; F7 (217 bytes) fires and collapses.

## 5. Bundle protocol (stdin)

```
NEED|<need text>
U|<pid>|<url>
P|<pid>
<sentence line>            (one normalized sentence per line, as round 2)
...
M|<pid>|FETCH=<unix>|CITE=<url>     (pipe-separated k=v; CITE optional)
CPIN|<url>|<fetched_at>|<name>
APIN|<url>|<fetched_at>|<name>
CALIB|<name>
PINB|<name>|<sha256hex>
<pin payload line>        (immediately follows its PINB line)
```

Binary modes (`argv[1]`): `g7infra` (verdict), `measure` (calibration:
emits `M|claim_bytes|claim_words|nvotes|nhost`).

Verdict line:
`V|g7infra|INSTALL|WITHHOLD|<gate>|<votes>|<hosts>|L0=<n>|pinok=<n>|pinbad=<n>`
Gate is `NONE` or `COPYCOLLAPSE`.

## 6. Trust boundaries (explicit)

- **Pipeline-trusted**: pin bytes, `fetched_at` values, fixture pages. The
  pipeline (driver) is offline; a compromised pipeline breaks everything by
  construction. Pins are append-only and content-addressed so pipeline
  behavior is auditable after the fact.
- **Attacker-controlled**: page content, `CITE=` metadata strings, URLs.
  The mechanism never trusts these: a CITE string only *names* a pin; the
  exemption comes from the pin's verified bytes and the pipeline-set
  `fetched_at`.
- **Not in the decision path**: live network, DNS, WHOIS/RDAP, wall-clock.
  All time comparisons use pinned `fetched_at` constants.

## 7. Known limits (carried, not fixed here)

- W_S3 / F_M3_HARDENED (patient diversified false consensus): untouched by
  this mechanism — no verdict-visible observation separates it. Accepted
  remnant per round-2 §7.
- Sub-L0 rings (short fabricated claims, e.g. the shortened-lie probe):
  the gate does not fire by design; coverage falls to ch1 (polarity), g1
  (closed-class archived precedence), HL-4. For non-closed-class short
  claims there is NO coverage — stated plainly in the pre-mortem.
- The calibration corpus (12 fixtures) is small; L0 should be re-derived on
  a larger honest corpus before production use. The CALIB pin makes this a
  data change.
