# Design PROPOSAL 2026-09-21 — portable knowledge chunks

**Status: PROPOSED — Micah's idea, not law. Nothing here is built or frozen.**
**Author of the idea:** Micah. *"Users share knowledge chunks. Trainers or even TNN itself
categorize what is what for subjects like coding knowledge etc, so users can download,
edit, or delete chunks of TNN's brain with clear separation."*

## The idea in plain words

TNN's knowledge is made of chunks — deliberately committed units the memory system can
reference, retrieve, and reuse. Those chunks should be **portable and categorized**: a
user can download the "coding knowledge" chunks, edit them, delete them, or share them —
without touching the "math" chunks or anything else. Clear separation, user control.

## Why it slots into the architecture naturally

- The chunk is already the unit of knowledge (representation program, 2026-09-21).
- Installed-vs-learned already distinguishes who put a chunk there (trainer force-install
  vs learned). A downloaded chunk is just a new provenance: user-installed.
- The audit ledger already records every commit with evidence and episode — provenance
  for chunks exists.

## Load-bearing requirements

1. **Categorization.** Chunks carry subject categories (coding, math, ...). Categorized by
   trainers, or by TNN itself — both must be tested (test both, per standing rule).
   Categories must be real boundaries, not labels: the separability test below decides.
2. **Separability.** Deleting or replacing one category must not degrade others. Test:
   remove the coding chunks, verify math/memory/reasoning capabilities unchanged
   (byte-identical on unaffected probes). If categories leak, the categorization scheme
   fails its kill bar.
3. **Import integrity.** A downloaded chunk is untrusted until verified. Import must run
   the corruption-detection machinery (currently 64/64 kill rate on tampering), check
   ledger provenance, and assign a trust tier (multi-source trust tiers are already a
   planned follow-up). A chunk that fails verification is refused, not half-adopted.
4. **Edit semantics.** Editing a chunk is a deliberate revision: the old version stays in
   the ledger (append-only), the new version is a new commit with the user as author.
   Nothing is silently overwritten.
5. **Installed-vs-learned status.** An imported chunk arrives as installed (by the
   user/trainer who provided it), never as "learned by this TNN." The learner may later
   revise or reject it through the normal deliberate-revision path — but it may not
   misrepresent borrowed knowledge as its own learning.

## Open questions (for HTD treatment later)

- Who categorizes better: trainers, TNN itself, or a hybrid? (test both/all three)
- Granularity: one chunk per concept, or bundled subject packs? What breaks first?
- What does "edit" mean for a chunk other TNNs have already downloaded — versioning?
- Poisoned-share attack: a malicious chunk pack crafted to pass verification. Red-team it.

## What this is not

Not a model marketplace, not weights-sharing. Chunks are discrete, categorized,
audited units — the opposite of smearing knowledge across weights. That's what makes
download/edit/delete with clear separation possible at all.
