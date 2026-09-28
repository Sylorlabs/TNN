# QUARANTINE — design spec (LI-HARDEN round 3, Crew C)

Date: 2026-09-24. Status: built, measured, committed.
Instrument: `quarantine.zag` (pure Zag, zero RNG, byte-identical reruns),
built with the pinned toolchain `znc_linux_x86_64_abed8aa1`.

## 1. Problem

W_S3 / F_M3_HARDENED — patient diversified false consensus — INSTALLS under
all 15 round-1/2 mechanisms. Triple convergence (measured probes + both
round-2 model consults): no verdict-visible observation separates it from an
honest new fact after the aging cost is paid. §7 (narrow) holds: identical
observation sets are inseparable.

Fable's round-3 Q2c (ranked #1 build): stop trying to separate them at
INSTALL time. Add a third state — QUARANTINED — for claims that have quorum
but no external corpus presence, with deterministic exit conditions. This
does not escape §7; it relocates the attacker's cost to maintaining
corpus-wide consistency, the most expensive attack shape.

## 2. States

- **INSTALL** (asserted as fact; propagates; `propagate=1`)
- **WITHHOLD** (not asserted; pre-filter vetoes: quorum unmet, g1 veto)
- **QUARANTINED** (not asserted as fact; evidence-bearing record; `propagate=0`)
- Exit terminals: **SOLID** (promoted), **REJECTED** (dropped), **DROPPED** (decayed)

## 3. Admission rule (deterministic — ALL must hold)

A claim is admitted to QUARANTINED iff:

1. **Quorum met**: ≥ THRESH quorum pages assert the normalized claim sentence
   (exact match after HL-7-style normalization: lowercase ASCII,
   punctuation→space, controls dropped, bytes≥128 significant, spaces
   collapsed, space-padded). THRESH is a tunable governance parameter
   (battery: 3).
2. **Corpus absence**: candidate-set expansion over the first W pages of the
   external corpus (crawl order) finds ZERO pages asserting the claim.
   W is the bounded crawl window (tunable; battery default: full corpus).
3. **Not closed-class**: the claim is not a closed-class template governed by
   the pinned oracle g1. If it matches a pinned template, g1's rule fires
   instead (ARCHVETO → WITHHOLD on conflicting archived filler; pass-through
   otherwise). Quarantine never admits closed-class claims.

Equivalently: enough friends to install, but nobody else in the world seems
to know about it.

Pre-filter order: quorum check → g1 check → candidate-set expansion.
A claim failing quorum is WITHHOLD/NOQUORUM, never quarantined.

## 4. Consumer contract

- QUARANTINED claims are NOT asserted as facts.
- Surfaced as: "asserted by N origins, uncorroborated externally" with the
  full evidence record (`E|case=…|state=QUARANTINED|origins=N|quorum=…|
  window=W|domain=D|propagate=0|search=labelled`).
- Consumers may use at own risk. NO propagation through the knowledge graph
  as truth claims (`propagate=0`).
- MAY be used as search matches with explicit labeling (`search=labelled`).
- On promotion the record is re-emitted as SOLID with the new evidence
  (`via=quarantine-exit`, `propagate=1`).

## 5. Exit conditions (deterministic, evaluated in order)

Given the quarantined record (claim, quorum pids + pinned meta, day TQ,
domain D) and a re-evaluation input (recheck hashes, new-crawl pages,
contradiction notice, day TNOW, decay calibration):

1. **DROP → REJECTED (evidence tampering)**: any quorum member's current
   content hash differs from its quarantine-time pinned hash (or the member
   has no pinned baseline — fail-closed). Emitted as
   `DROP_REJECTED|MODIFIED|pages=…`.
2. **DROP → REJECTED (contradiction)**: a contradicting claim is presented
   (byte-different from the claim, ≥2 shared whole words — guards against
   garbage notices) AND (its pinned first-seen predates the earliest quorum
   first-seen OR it carries pinned-registry authority). Emitted as
   `DROP_REJECTED|CONTRA|older=…|auth=…`.
3. **PROMOTE → SOLID**: a new-crawl page NOT in the original quorum asserts
   the claim AND is independent (NS apex, IP/24, WHOIS registrant, CMS
   fingerprint all differ from every quorum member; empty fields are
   "unknown", never a match) AND legitimate (pinned first-seen recorded,
   ≥ DIV_MIN non-claim sentences — not a single-sentence plant).
   DIV_MIN is tunable (battery default: 2, argv[3]).
4. **TIME-DECAY → DROPPED**: if `TNOW - TQ > W_decay(D)`, where
   `W_decay(D) = DECAY_MULT × median(lags_D)`. The lags are a per-domain
   calibration list (observed days from first assertion to first external
   corroboration); the median is computed from that data, never hardcoded.
   Fallback for uncalibrated domains: the corpus-global lag list.
   DECAY_MULT is tunable (battery default: 4, argv[2]). Boundary is strict:
   `age > window` drops; `age == window` stays (pinned by X_DECAYEDGE).
5. Otherwise **STAY_QUARANTINED**.

Per Micah's no-arbitrary-limits law: THRESH, W, DIV_MIN, DECAY_MULT are
tunable parameters with documented defaults; the decay window is derived
from calibration data. No hardcoded constants in the architecture.

## 6. What this does NOT do (accepted limits)

- A perfectly corpus-wide attack (attacker plants external corroboration on
  independent-looking domains) escapes quarantine to INSTALL. Quarantine
  raises the cost to corpus-wide consistency; it does not detect it.
- Breaking-news-shaped honest claims with corroboration outside the crawl
  window are falsely quarantined (measured in §8 — fable's one question).
- S1 (entrenched false consensus), R4 (wire echo — INSTALL is correct
  behavior), and compromised legitimate sites inside a time window are
  unchanged by this mechanism.

## 7. Falsification battery (fable Q8, measured §8)

Must QUARANTINED: W_S3 (quorum 3, diversified meta, zero external support).
Must NOT QUARANTINED (must INSTALL): T1 (abundant external corroboration),
T2 (breaking news, ≥1 external source), T3 (long-tail, ≥1 external source),
T3deep (deeper long-tail), T4 (supersession, authority source present),
T5 (wire, cited externally), F5 (new sentence on real sites), H1–H12
(12 honest fixtures). Must WITHHOLD (never quarantine): Q_NQ (quorum
unmet), Q_G1 (closed-class, g1 veto).
Exit: X_PROMOTE → SOLID; X_PROMOTEFAIL (shared WHOIS) → STAY;
X_DROPMOD → REJECTED; X_DROPCONTRA (older) → REJECTED;
X_DROPCONTRAAUTH (authoritative) → REJECTED; X_DECAYFAST (news) → DROPPED;
X_DECAYSTABLE (reference) → STAY; X_DECAYEDGE (age == window) → STAY.

## 8. Files

- `quarantine.zag` — the instrument (`admit` / `exit` modes).
- `R33_NATIVE_IO_V1.zag` — native I/O substrate (same file as round-2 beyond).
- `gen_fixtures.py` — deterministic fixture generator (fixed-seed LCG;
  generation only, never in a decision path). Re-runnable; output
  byte-identical across runs (verified by diff).
- `run_quarantine.py` — battery driver (plumbing only; every case run
  twice, byte-identity asserted).
- `fixtures/` — 22 admission fixtures (`bundle.txt` + `kind.txt` + `desc.txt`).
- `fixtures_exit/` — 8 exit fixtures (`bundle.txt` + `expect.txt`).
- `pins/` — pinned oracle lines used (subset of round-2 beyond pins).
- `results_admit.tsv`, `results_exit.tsv`, `results_window.tsv` — measured.
- `VERDICT.md` — verdict with numbers. `RUNLOG.md` — run record.
