# Track 7 (PAM vision/hearing requalification) — Slice 01: PAM Archaeology

## 1. Slice

T7-Senses slice 01: the PAM archaeology search protocol — where to dig for
surviving PAM vision/hearing designs, what counts as a design vs a fragment,
how to catalog findings, and the verdict rule that decides "recoverable" vs
"fragments only" vs "confirmed absent."

## 2. Falsifiable claim

At least one complete, recoverable PAM vision or hearing design — a spec plus
runnable artifacts or parameter sets sufficient for a builder to reimplement
without inventing semantics — exists in the searchable locations (committed repo
history including dangling objects and stashes, workspace directories, and
Micah's pre-git session files) and will surface under the protocol below.
If the full five-layer sweep completes with documented coverage and no
DESIGN-class artifact appears, this claim dies and the standing becomes
"fragments only" or "confirmed absent." Recoverability is a precondition, not a pass —
no claim is made that a found design is automatically native-Zag compatible.

## 3. Design — the dig protocol

Five layers, run in order; each layer ends with a logged coverage list (what
was searched, by what command, what hit or didn't) so a negative result is
evidence, not vibes. Never search by name alone — a name sweep misses designs
filed under aliases; every layer pairs a name sweep with a content sweep.

- **L1 — committed repo history (fully automated).** In every sylorlabs repo
  under review (tnn, tnn-native-lab, zag, ghost_*): `git log --all
  --full-history` with path filters `*pam* *sens* *vision* *hearing* *audio*
  `*percept* *retina* *cochlea* *spectrogram*`; all local and remote-tracking
  branches; `git stash list` contents; `git fsck --lost-found` for dangling
  blobs/trees; reflog entries; tags. Content-grep every blob for the PAM keyword
  set: `PAM`, `percept`, `retina`, `cochlea`, `spectrogram`, `phoneme`,
  `convolution`, `feature map`, `edge detect`, `formant`, `V1`, `auditory cortex`.
  Log: SHA list of hits, or "zero hits across N refs, M blobs."
- **L2 — workspace directories.** Recursive name+content search over
  `~/workspace/tnn-lab/history/`, `~/workspace/tnn-lab/brain/`,
  `~/workspace/user/`, `~/workspace/your_files/`, and any archived experiment
  dirs, for the L1 name patterns plus legacy Torch-era filenames (`*.pt`,
  `*.pth`, `*.onnx`, `*.npz`, weight dumps) and prose design docs (`*.md`,
  `*.txt`, `*.pdf`). For every parameter dump, distinguish WITH
  provenance (training script committed alongside) from WITHOUT (the 76-torch
  failure mode — automatically FRAGMENT).
- **L3 — GitHub remote surface.** Via `gh-api`: all branches incl. closed/deleted
  refs, PR history (open, merged, and closed-unmerged), commit comments, release
  assets, and any gists on Micah's account mentioning PAM/perception keywords.
  Remote-only copies sometimes survive local pruning; a deleted branch's design
  doc is still a DESIGN if it meets the criteria.
- **L4 — Micah's pre-git session files (the one remaining lead, human-gated).**
  Procedure: request Micah to locate and point us at the session
  files/directories (path list or archive); once paths are known, run L1-style
  name+content search; log searched paths and the hit list.
  Cannot claim coverage until he provides access — that gap is logged explicitly,
  never silently dropped, and it is the ONLY layer allowed to delay the verdict.
- **L5 — draft/ephemeral surface.** `/tmp`, trash/recoverable-delete locations,
  workspace root stray files, uncommitted editor backups (`*~`, `*.bak`,
  `.swp`), tar/zip/archives anywhere under `~/workspace`, and `*.zagd`-style
  caches only if they contain source (not build outputs).

**Identification criteria.** A finding is a DESIGN only if it has BOTH:
(a) an explicit perceptual pipeline description — sensor input → feature extraction
→ representation → memory-interface contract (what the rest of TNN receives); AND
(b) runnable artifacts (code in any language) or a complete parameter set WITH
provenance (how produced, on what inputs).
Meeting only (a) = design-doc fragment; meeting only (b) = artifact fragment.
Torch-era imports without committed training provenance are fragments BY RULE,
per the established unrecoverability result. Anything else — prose notes, code
that names PAM but implements nothing, README mentions — is a FRAGMENT.

**Cataloging format** (one row per artifact, committed as a markdown table): ID
(`PAM-ARC-001`…), location (`path@git-ref` or `dir`), modality, class
(design/fragment), completeness (pipeline-spec? parameters? provenance?
runnable? — yes/no each), provenance rating, recoverability verdict (yes/no + one-line reason; zero-hit layers log coverage).

**Verdict rule.**
*Exists and recoverable*: ≥1 DESIGN-class artifact where a builder could rebuild
without inventing semantics — recoverability does not require native Zag or
current-law compatibility.
*Fragments only*: ≥1 FRAGMENT, zero designs.
*Confirmed absent*: all five layers completed with logged coverage and zero
DESIGN-class hits (L4 counts only after Micah grants access; before that the
verdict is "pending L4").
*Inconclusive*: any layer un-run for reasons other than documented human-gating.

## 4. Kill bar

The claim is KILLED if: L1–L3 and L5 complete with zero DESIGN-class hits AND L4
completes with Micah-provided access and zero DESIGN-class hits — with every
layer's coverage log committed. Partial completion yields "inconclusive pending
L4," not "confirmed absent." The kill bar fires on absence of designs, not on
designs being old or Torch-era: a rebuildable-but-incompatible design still
satisfies the claim.

## 5. Honesty notes

Micah's memory that he designed the senses is a lead, not evidence — human recall
is unreliable about completeness, and "I designed it" often means "I sketched it." Torch-era designs, if found, predate the
native-Zag/no-RNG laws and may be technically incompatible with the current
program (a recovered design is not automatically a qualifying design —
re-qualification is Track 7's separate job). Grep keyword sets can miss designs
filed under unexpected names; the alias sweep mitigates but doesn't eliminate
this, so the "confirmed absent" verdict always carries the residual risk of an
unsearched name. L4 is the weakest link: the dig cannot honestly claim
"confirmed absent" while the one remaining lead is unsearched — this is why the
verdict rule forbids killing the claim on a partial dig. Fragments may be
tantalizing (a coherent architecture sketch) without being recoverable — classify
by the criteria, not by hope. The protocol finds artifacts; it does not judge
them — whether a found design can be rebuilt natively and re-qualified belongs
to the downstream slices, and must not leak into the archaeology verdict.

## 6. Next build step

Run L1 first — it is fully automated, costs nothing, and immediately settles
whether anything survived in git (branches, stashes, dangling objects,
full-history grep across all sylorlabs repos): execute the command set, log the
coverage (refs searched, blob count, hit list), and commit the hit list or the
zero-hit report to the findings dir before touching anything that needs Micah's
involvement.
