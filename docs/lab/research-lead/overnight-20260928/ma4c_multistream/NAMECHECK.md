# NAMECHECK: MA4C-MULTISTREAM (multi-stream validation of the K=3 proxy)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which perl` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which ruby` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which node` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary; verified 2026-10-03).
- `which git` returns `/home/hatch/safebin/git`; git write ops invoked via
  the resolved `/usr/bin/git` path (the safebin git symlink has a known
  EPERM failure mode on object/index writes per the 2026-10-03 workspace
  lesson; same tool, resolved path).
- `which awk` returns `/home/hatch/safebin/awk` (used only for reading
  printed integers out of audit lines; no scientific computation).
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging,
  znc invocation, binary execution, hashing, cmp/diff/grep audits,
  git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Lane location and commit discipline

Lane: `docs/lab/research-lead/overnight-20260928/ma4c_multistream/`
on branch `tnn-native-lab` (worktree `/home/hatch/workspace/tnn-rsi-gpi3`).
Nothing is pushed to GitHub; commits stay local with explicit
pathspecs. Commit order: this prereg commit contains ONLY PREREG.md
and NAMECHECK.md (Step 0 + Step 1 + design record). The implementation
(ms_*.zag) strictly postdates it. No frozen kill bar is evaluated
before its prereg commit.

## Design record (pre-prereg, no implementation run)

MA4c reached PROXY-LEARNER-DRIVEN with an honest boundary: K=3 is
exploratory, the unique integer separating measured ratios 2.94
(genuine, E735) vs 3.42 (adversarial, E795) on one W6 stream, with a
thin 1.9% margin on the genuine side. Multi-stream validation was
required before any generality claim. This lane runs that validation.

Stream definition: a W stream is the full 852-episode W realization.
Streams differ ONLY in the W Bernoulli seed
(20261026 -> 20261027, 20261028, 20261029, 20261030). Tiles, bands,
shuffles, X/Y/Z seeds, and all mechanism logic are frozen as
ma4c.zag. The W seed is set via s64(G,0,...) immediately before the W
trial fill and affects nothing else (each stream's trials are drawn
after an s64 reset; verified by code inspection of gen()).

Key mechanism insight found during design (from W6's SNAPWR + trigger
code, no new runs): the W6 trigger pattern is a seed-sensitive race.
At a block boundary, the trigger needs 3 consecutive active-cell
errors > 20, while the active-cell handoff (winner's smoothed score
dropping below the failing active cell's) resolves in ~3-4 episodes.
On W6 the E735 trigger won its race by ~1 episode and the B2
boundary (e=672) produced no trigger because the handoff won. Both
outcomes are fragile to Bernoulli noise. The prereg therefore
separates scenario-presentation (did the designed boundary triggers
occur?) from proxy-margin (did K=3 discriminate where triggers
occurred?), and adds fixed-episode write-only probes at the designed
decision points (0-indexed e=734, e=794) so the margin is measured
even where the race resolves differently.

MS audit (write-only, new in ms_*.zag): at each W trigger (pre-reseed)
and at the two fixed probe episodes, evaluates redun2a's EXACT firing
semantics over all valid (i,j) pairs (prot(j)=1, j!=i,
xcnt[j][i]>=5, wpart[j]>=wpart[i]): nvalid, the min-ratio pair
(num=xerr[j][i]*wpart[i], den=wpsm[i]*xcnt[j][i] as i64;
(0,0)->0, (num>0,0)->+inf), and K-bits K=1..5 = whether ANY valid
pair has num <= K*den (exactly the proxy's firing condition, since
firing is existential over pairs and monotone in K). PCT =
100*num/den of the min pair (i64; INF sentinel when den=0<num).
All computation in Zag; shell only reads printed integers.

B7: the 29-word list grep must return empty in ms_*.zag (same list as
MA4b/MA4c: coin, bias, heads, tails, shrink, prior, learn, meta,
cluster, outlier, typical, atypical, general, poisson, rate, lambda,
gauss, count, event, slot, family, distractor, shift, phase, regime,
original, interference, recover). Comments avoid the listed words.

## Build record

(recorded after the prereg commit; implementation has not begun)
