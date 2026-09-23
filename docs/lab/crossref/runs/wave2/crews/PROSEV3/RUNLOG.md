# RUNLOG — T2-PROSEV3 (prose v3 replication crew)

- Crew: T2-PROSEV3
- Program: TNN cross-reference, Wave 2 (Tier 2), authorized by Micah's 2026-09-22 "run everything" ruling.
- Started: 2026-09-22 ~21:05 PDT
- Clean checkout dir: ~/workspace/scratch-crossref/T2/PROSEV3/clean/
- Run dir: ~/workspace/scratch-crossref/T2/PROSEV3/crew/
- TMPDIR=/home/hatch/workspace/tmp_commit (never /tmp)
- FROZEN PREREG: sylorlabs/TNN branch tnn-native-lab, commit 7b2100d09911c5c10252c5756c7def288e70bd1f
- Evidence pin (T2-PROSEV3): 4be6b0cf128d5a443c9e67486f63520816535cca (API-verified)
- znc: /home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1

## Committed claims under test (PREREG_TIER2.md §T2-PROSEV3, authoritative)
- Verdict KB3-VIABLE FAIL (2/4), v1 pinned (commit 4be6b0cf128d, API-verified).
- Honest prereg deviation: implementation expanded the coreference trigger beyond
  the preregistered order change; 6/11 fixed CORE items came from the unregistered
  expansion (C2 attribution confounded); frozen A0/A1 comparisons -> no scored
  headline result changed; tier-3 tolerant fallback carried essentially all
  recovery but raised wrong-value verdicts 8->30/912 while converting ~463
  unknowns into values.
- METHOD (Type A): rerun the v3 battery from committed sources in clean checkout;
  verify the FAIL (2/4) and reproduce the deviation's quantitative footprint
  (6/11 CORE, 8->30/912 wrong-value).
- RULE: REPRODUCED if FAIL (2/4) holds and the deviation footprint matches;
  PARTIAL if the deviation's impact differs from recorded (name it).

## Pin verification (done BEFORE any run)
- 2026-09-22 ~21:4x PDT: `gh-api GET /repos/sylorlabs/TNN/commits/4be6b0cf128d`
  -> SHA 4be6b0cf128d5a443c9e67486f63520816535cca, date 2026-09-22T03:28:39Z,
  message "prose-learning v3: pure-Zag repair verdict — KB3-VIABLE FAILS (2/4)".
  Commit message corroborates the prereg: A3 mastery .8026/.8947/.9123/.9956 vs
  v1 .8289/.9649/.8947/.8772 -> beats v1 on 2/4 (step, muse-native); "5 CORE
  items from the order change, 6 from the expansion".
- Package tree at that commit: docs/lab/docs/lab/prose-learning/v3/ (300 files;
  note the doubled docs/lab/ prefix — known commit-script double-prefix quirk).
- v2 frozen source (needed for A0/A1 legs) at docs/lab/prose-learning/v2/src/
  (non-doubled): prose_learn2.zag + oracle2.py + build.sh + R33_NATIVE_*.zag.
  The committed v3/run_legs.sh references ../v2/src/prose_learn2 — that relative
  path only resolves in the crew's pre-commit working layout; in the committed
  tree the v2 package is NOT under docs/lab/docs/lab/. My driver will use
  absolute paths to both committed sources (no source edits).

## Timeline

### 21:05-21:35 PDT — clone attempts, wiped twice
- 21:05: created clean/ + crew/ + ~/workspace/tmp_commit. Confirmed znc at the
  mandated path. ~/workspace/tnn-lab is NOT a git repo (no .git) -> fresh clone needed.
- 21:08: started unauthenticated `git clone --branch tnn-native-lab --no-checkout`
  (repo is public; other crews GOALB/SENSESINT/CHAMP/TRACKA cloning in parallel).
  Slow (~1.5 MB/min with 40+ parallel clones on the VM).
- 21:30: killed all-branches clone at 124MB; restarted --single-branch.
- ~21:35-21:40: clean/tnn VANISHED (dir mtime 05:21 UTC); GOALB/CHAMP/TRACKA
  clean dirs also emptied; SENSESINT's survived. VM uptime later showed a reboot
  at ~03:50 UTC — environment instability, not my action.
- Pivoted: SENSESINT's surviving clone is a sparse+shallow checkout at the frozen
  prereg commit 7b2100d09911c5c10252c5756c7def288e70bd1f with the v3 commit as a
  dangling object. A local `git clone` from it FAILED (early EOF on fetch-pack —
  sparse/shallow weirdness), so did not use it as a source. Non-interference kept:
  never touched their run outputs.
- Observed sibling crews' faster pattern: codeload.github.com tarballs at exact
  pin SHAs (PARAMS crew). Adopted for robustness.

### ~21:40 PDT — tarball download #1, reboot truncation
- Started background curl of https://codeload.github.com/sylorlabs/TNN/tar.gz/4be6b0cf128d5a443c9e67486f63520816535cca
  -> clean/v3pin.tar.gz. Reached 104MB by 05:47 UTC.
- 05:48 UTC: VM REBOOTED (uptime reset). Download truncated (gzip: unexpected end
  of file). crew/ files survived (RUNLOG, prereg docs, API tree JSONs).

### ~21:50 PDT — tarball download #2 (resume loop, background proc_a1d63e1fad95)
- Restarted with `curl -C -` resume in an 8-attempt loop.
- (pending)

## Still to do
1. Verify tarball (gzip -t), extract to clean/tnn.
2. Verify extracted files: checksums.sha256 inside the v3 package (302 files) +
   git blob SHAs via API for src files (have v3/src tree SHA 2b151cac83bdb232d2fa77711973585fbfdd736d).
3. Confirm the v3 commit is an ancestor-equivalent of the frozen prereg for the
   v3/v2 paths (diff the v3 subtree if a full git history is available; else
   record that replication is against the evidence pin 4be6b0cf128d directly,
   which is what the tier-2 prereg names).
4. Build prose_learn2 (v2, for A0/A1) and prose_learn3 (v3, for A2/A3) from
   committed sources with the pinned znc. No .zagd/binary copies.
5. Write my own run driver (mirrors committed run_legs.sh, absolute paths,
   outputs to crew/runs/): 4 legs x (4 champ sources x 5 reps + 7 sub-batteries
   x 5 reps), cmp byte-identical gates.
6. Score with committed score_legs.py; compare every VERDICT.md figure:
   - A3 vs v1: 183/204/208/227 vs 189/220/204/200 -> 2/4 (step +4, muse-native +27)
   - Ablation deltas table (C1 +0.00-0.06, C2 0, C4 +0.30-0.56)
   - SUB-CORE 11/24 -> 22/24 (A2); SUB-DISTR 65/240 -> 199/240 (A3)
   - Wrong-value 8 -> 30 / 912; unknowns 523 -> 60 (~463 converted)
   - ABS-3 9/11/11/11 all legs; KB3-NOSILENT; KB3-BYTEID 5/5
7. Deviation footprint: (a) CORE attribution 5+6=11 via committed oracle3.py
   subcore proof logs; (b) 8->30/912 + ~463 from my scored logs.
8. Byte-identical check: my rep logs vs committed runs/ logs (16 champ + 28 sub
   per leg... actually 4 legs x (16 champ + 28 sub) = 176 committed logs).
9. Write VERDICT.md; final message restates the complete verdict.

## 2026-09-23 ~23:35–00:40 PDT — replication execution (post-compaction session)

### Evidence package verification
- Tarball `clean/v3pin.tar.gz` (1,476,167,212 bytes) `gzip -t` clean; extracted to `clean/tnn/`.
- Background checksum job: **303/303 files OK** against committed `checksums.sha256`
  (`crew/checksums_verify.log`).
- Evidence pin API-verified: `4be6b0cf128d5a443c9e67486f63520816535cca`
  (2026-09-22T03:28:39Z; message: `KB3-VIABLE FAILS (2/4)`).
- Frozen prereg pin API-verified: `7b2100d09911c5c10252c5756c7def288e70bd1f`
  (2026-09-22T22:54:44Z). Prereg docs (SCOPE.md, PREREG_TIER2.md T2-PROSEV3
  section) read from this pin — authoritative.
- v3 source tree SHA @evidence: `2b151cac83bdb232d2fa77711973585fbfdd736d`;
  v2 source tree SHA @both pins: `380d2339e34fa8df1fa685163799f10b56471158`.
- v1 `false_ids_<s>.txt` blob-identical @4be6b0cf and @7b2100d
  (`6878d9869439…`); used for A0 (committed run_legs.sh relied on working-tree
  symlinks excluded from the package).
- Notable: at 7b2100d, `docs/lab/prose-learning/v3/` contains only VERDICT.md
  (doc-sweep annotations added; all quantitative claims unchanged). The full
  package is replicated from the prereg-named evidence pin 4be6b0cf128d.
- Fresh-clone caveat: the evidence tree is a SHA-verified codeload extract,
  not a git clone (40-crew clone stampede made full clones infeasible; earlier
  attempts hit early-EOF / vanished dirs / VM reboot). All content is
  pinned by API tree SHAs + the 303/303 checksum gate, and the rebuilt
  binaries are byte-identical to the committed PROOF.md SHAs (below).

### Builds (pinned znc, from committed sources, no copied binaries)
- `crew/build/v3/prose_learn3`: exit 0.
  SHA-256 `a5cff7cde60074176b5a1c480ea58ed263fb22514c0a29992301e8b4ae82dc72`
  — **byte-identical to committed src/PROOF.md**.
- `crew/build/v2/prose_learn2`: exit 0.
  SHA-256 `8dbb02fda28f32f88f10e2aa23668c308efd4b59d5369697e210b71cf8e1a901`
  — **byte-identical to committed src/PROOF.md**.
- R33 substrate files md5-identical between v2 and v3 packages.
- Built in `crew/build/` (copies of committed .zag); `clean/tnn` untouched.
  `.zagd.semantic-ready` artifacts exist only under `crew/build/*` (never
  committed, not deliverables).

### Runs (crew/run_all.sh; mirrors committed run_legs.sh, absolute paths,
### outputs to crew/runs/, 5 reps everywhere, cmp hard gates)
- Smoke: A3 champ_grok (v3 m2) byte-identical to committed
  `runs/A3/champ_grok_rep1.log` on first try.
- A3: 55/55 5/5 byte-identical reps; 55/55 logs byte-identical to committed.
- A1: 55/55 5/5; 55/55 byte-identical.
- A2: 55/55 5/5; 55/55 byte-identical.
- A0: 55/55 5/5; 55/55 byte-identical (A0 false_ids from frozen v1 inputs).
- **Total: 220/220 logs byte-identical to the evidence package.** Zero RNG.
  TMPDIR=/home/hatch/workspace/tmp_commit throughout.

### Scoring + independent Zag verification
- `crew/score_all.py` replicates committed `score_legs.py` logic exactly
  (clean paths; A0 false_ids from committed frozen v1 inputs), plus
  wrong-value vs unknown/other breakdown.
- `crew/build/verify/verify3.zag`: independent pure-Zag verifier (pinned znc;
  champ mode: clean/wrong-value/other counts from PROBE lines + false_ids;
  core mode: want-rule counts from test file). Build notes: Zag uses
  `fn main()i32` (not `->`), no `"\n"` escapes in literals, byte arenas with
  p32/g32 instead of `as []i64` casts.
- `crew/assert_all.sh`: 17 Zag-verified assertions — **ALL PASS**.
- Zag verifier agrees with the Python scorer on every figure.

### Deviation footprint (causal)
- CORE 11/24→22/24: replicated per-id fixed set
  {2,3,5,7,9,10,13,16,17,18,23}, zero regressions, residual misses {19,21}.
- Narrow-trigger diagnostic build (`crew/build/v3narrow/`, expansion lines
  removed, order change kept): sub_core m1 → 16/24, fixes exactly
  {2,5,9,10,13}. The other 6 fixed ids {3,7,16,17,18,23} are therefore caused
  by the unregistered expansion. **5 registered + 6 unregistered = 11.**
- Wrong-value: A1 8/912 → A3 30/912 (Zag-verified). Unknown/other: 523 → 60;
  463 converted (Zag-verified).

### Deliverables
- `crew/VERDICT.md`: **REPRODUCED** — KB3-VIABLE FAIL (2/4); full deviation
  footprint match (6/11 CORE attribution causally isolated, 8→30/912
  wrong-value, ~463 unknowns→values).
- `crew/RUNLOG.md`: this file.
- No live-workstream files modified. No binaries/`.zagd` in deliverables.

### Open / not done
- True `git clone` of the evidence pin was not obtained (infrastructure
  stampede); replication rests on API tree SHAs + 303/303 checksums +
  byte-identical rebuilt binaries and logs. Recorded as a caveat, not a gap
  in the evidence chain.
- The committed oracle3.py was not rerun (Python oracle is the original
  crew's instrument; the tier-2 method requires the Zag battery rerun, which
  is complete). The m0-vs-v2 gate-(a) correction (14/15, id-17 sub_core) was
  not re-exercised since no scored run uses v3 m0.
