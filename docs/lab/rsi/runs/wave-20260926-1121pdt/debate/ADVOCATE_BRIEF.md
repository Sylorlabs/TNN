# ADVOCATE BRIEF: wave-20260926-1121pdt debate

Role: advocate for the verdict slate. I argue FOR each draft verdict
(certification or re-certification). The skeptic argues against. The
judge decides. No verdict here is adopted by the brief itself.

Standing disclosure: this brief contains no em-dashes by loop rule.

## The skeptic's provenance probe (verbatim)

"What is the provenance of the artifacts under judgment, and what
exactly is new versus inherited?"

I answer it per item below, each from that item's committed provenance
header or record. The pattern across the slate: one genuine new item
(DP-1, orphaned from a dead wave and now recovered), everything else is
[RE-CERT] of standing process infrastructure or an honest historical
record. Nothing recycled is presented as new.

## 1. DP-1 doppler flyby: CERTIFY READY-FOR-JUDGE [NEW], queue for his ears

### Provenance answer (from the committed header in EVIDENCE_DP1_1721.md)

- RENDER_SHA: 994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771, independently re-hashed by the dossier worker across r1/r2/r3, exact match.
- FIRST_RENDERED_WAVE: wave-20260925-1721pdt. Confirmed by git-history grep: "doppler" and "flyby" return zero hits outside wave-20260925-1721pdt, and the WAV first appears as an added file in commit 02d1dcb31.
- COMPONENT_LINEAGE: D-AUD-3-substrate (synth.zag f76293f6061812aaaedeac59ae67440bf949b23c1bf9ebc7e60211df1c58f055, vendored byte-identical as sub/synth_base.zag, re-hashed by the dossier worker, exact match); then the full prior-ID list with statuses: R9, C1, C2v3, S11-IMG, S11-AUD, S13, S14, whirlpool-planform all QUEUED-UNJUDGED; S12, S12b, B1, DF-1, C-D19, ST-1 all DEAD; G1 STOOD-DOWN; D-VID-1 STOOD-DOWN. No JUDGED items listed. Nothing recycled and re-certified as new.
- NEW_KNOWLEDGE_CLAIM: "A frozen constant-velocity flyby rendered through a time-varying propagation delay adds motion-based realism to the D-AUD-3 bed via doppler pitch fall, inverse-distance loudness swell, and lateral pan at linear resampling cost." One sentence, present.

What is new versus inherited: inherited is the D-AUD-3 bed (vendored byte-identical, honestly labeled substrate). New is the time-varying propagation delay from a frozen trajectory producing measured doppler pitch fall, inverse-distance loudness swell, and lateral pan. The red team greps confirm repo-wide novelty: doppler 0 hits, flyby 0, variable-delay 0, fractional-delay 0.

### All 8 frozen bars pass, with margin

KB1 determinism: 3/3 variant WAV sha256 identical, 3/3 trace sha256 identical (eb375fd6...). KB2 no clipping: base_peak 21713, var_peak 21739, both under 32767, 0 clips. KB3 doppler ratio +/-3%: f_approach 52.500, f_recession 43.500, ratio_meas 1.207 versus ratio_exp 1.207, exact match of the analytic ratio. KB4 crest +/-1.5 dB: crest_ratio 0.994 (bounds 0.84140..1.18850). KB5 energy +/-2 dB: rms_ratio 1.007 (bounds 0.79433..1.25893). KB6 pure Zag, pinned compiler: token grep zero hits in DP-1-authored code, znc 498abcb5. KB7 cost <=2.0x: variant 6.726 s / baseline 3.603 s = 1.867x, under bar with margin. KB8 trace audit: 210/210 checkpoints, 0 mismatches at 1e-9 scale. The pure-Zag verifier independently outputs fails=0. No bar was moved; none was weakened.

### Prereg commit-order self-check: PASS

Prereg 18ad30fe3 (2026-09-26 00:58:46 UTC, single file PREREG_DP1_1721.md, committed alone) strictly precedes implementation 02d1dcb31 (2026-09-26 01:26:51 UTC, 18 files, all inside the DP-1 run dir, no other repo files touched). Twenty eight minutes separate them. Both are ancestors of tnn-native-lab HEAD. This is the order the tightened governance demands, and DP-1 satisfies it.

### Independent red team EXISTS and AGREES

REDTEAM_DP1_1721.md is an adversarial self-review that answers the strongest objection (S11-AUD mechanism-class overlap: static time-invariant room filtering versus time-varying source-motion delay; no shared code, parameter, or measurement), clears the ST-1 replay check and the substrate-vibrato collision, and confirms bar integrity (no gaming on KB3 tolerance; KB4/KB5 honest minimal-perturbation results; KB7 1.867x the closest bar). Its bottom line, quoted verbatim:

"No padding, no re-freeze, no bar movement, no frontier contact. DP-1
stands as [NEW] with all bars passing. READY-FOR-JUDGE."

### The one Python contact: disclosed no-contact contact, not a breach

EVIDENCE disclosure 2 and the dossier section 5 both record it: the 1721pdt worker used `python3 -c` once to count dash characters in its own draft fragment. Read-only. No modification, no analysis, no wave artifact written or touched. The dossier worker grepped the whole dp1 dir: the only "python" mentions are the KB6 token-grep bar text and the disclosure itself; no .py files, no scripts, no Python content in the .zag sources. Per P13/P15, a disclosed no-contact invocation is classified as a disclosed contact, not a breach, and the attestation reads "zero Python touched wave artifacts." The dossier worker (1121) attests the same for its own verification work: git, sha256sum, grep, and cat only. This is the class of contact the loop's own precedents already distinguish from a breach (compare the 0221pdt wave, where a python3 heredoc patched driver tooling and was ruled a red-line breach with that wave superseded). The contact belongs on the record, which is where it is; it does not void DP-1's bars, all of which were rendered and verified in pure Zag with the pinned znc.

### The S11-AUD thematic overlap: disclosed honestly

I flag it exactly as the red team does, because the red team and the dossier flag it themselves: S11-AUD is "physical-space propagation" (QUEUED-UNJUDGED) and DP-1 is also physical acoustics, so the themes overlap. The mechanism does not: S11-AUD is time-invariant filtering (fixed taps, fixed RT60); DP-1 is a time-varying delay from source motion that produces pitch shift, which no static filter can produce. The red team calls this "a real judgment call for the owner." The honest handling is to put that judgment call in front of his ears rather than resolve it by metric, which is what READY-FOR-JUDGE does. The red team's other honesty flags also travel with the verdict: the flyby is a new world event (a lifter), so it is content-adjacent, and the worker could not ear-check audibility. None of these are hidden; they belong to his listening verdict.

### Why READY-FOR-JUDGE and not adoption on metrics

Human ears are the kill bar for audio sensory candidates, per the standing sensory headspace rule. All 8 bars pass on the metric side. LISTENING_DP1.md is committed and poses the exact listening question: "Does the flyby make the planetvoice scene feel like a real place with something moving through it, or does it read as a synth effect pasted on?" Both WAVs are at the same fixed level with no normalization tricks. Certification does not adopt; it queues DP-1 for his verdict, which is the only verdict that counts.

### Orphan recovery is repair, not new work

wave-20260925-1721pdt died before any debate. LOOP_STATE.md has no section for it and no "DP-1" mention anywhere; the 1721pdt debate dir is empty; no debate transcript in any wave run dir mentions DP-1. DP-1 has never reached Micah. Recovering it into this wave's debate with a read-only dossier (nothing in the 1721pdt dir modified) repairs a dropped handoff. It creates no new mechanism, touches no frontier code, and moves no bar.

Recommendation: CERTIFY READY-FOR-JUDGE [NEW], queue for his ears with LISTENING_DP1.md.

## 2. Fork battery: CONFIRM [RE-CERT]

### Provenance answer

This is process infrastructure, not a candidate; its provenance is the pin record, and every pin held this wave. znc sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef on 36/36 PASS entries (single distinct value, byte-identical toolchain on every fork). Probe source sha 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919 on 36/36. The pure-Zag harness fork_battery.zag was extracted read-only from tnn-native-lab-wave-archive-20260923-2321pdt with sha f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738 (matches expected, no extraction anomaly), rebuilt with the pinned znc verified before use, and the built binary sha a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66 is byte-identical to prior waves. B2 recompile bin pin 75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2 on 36/36. Nothing new is claimed; the wave re-verifies uniform pins across all entries.

### The numbers

38 named entries. 36 PASS. 2 extraction FAILs: origin pull/1/head at 5802fec8401f28b4036b0dd5ebb23905610cab57 and origin pull/2/head at 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba. The cause is unchanged from the 0821pdt and 0521pdt waves: those trees lack the pinned toolchain path (non-TNN research-doc repos, no src/ dir). They are untestable by this battery, not evidence of a toolchain regression. 31 unique commits; 5 unique live commits; 5 live vs 33 fixture; all duplicates named explicitly with SHAs (per P1/P8): three entries share 9914322267e1358e5542a23c72ec51d1a9ae43df, two share 3947dca1a77c00818575dbc7476556c8278b8b7b, two share f875b34179f570ba1ad555262cd401ddc4a52848, four share bd30978748fa83bbea6e423a7074cf32b7304291. Nothing merged silently. On all 36 PASS entries: B1 stdout byte-identical (FORKBATTERY-OK 42), B2 rerun identical and recompile byte-identical, B3 check exit 0, NEG1 fails as required (E0002 unterminated string literal), NEG2 fails as required (stdout differs at char 1, line 1), fork-tree probe exit 0, harness VERDICT=PASS exit 0.

### Incidents handled by the evidence itself

Incident 1: the FETCH_HEAD-scoped fetch fast-forwarded the local remote-tracking ref origin/tnn-native-lab from 94625817c to 7ea4d2e61. It is a pure fast-forward to the true upstream tip; no local branch, worktree, or working-copy state was disturbed; the run-start value 94625817c was snapshotted first and that entry was tested at it. The worker disclosed it and performed no further fetches. Incident 2: two orchestrator script bugs (a redirect into a not-yet-created dir, and a `cut -d= -f2` parse of a single-line key/value output) spuriously marked entries FAIL in the first passes. The raw per-entry evidence files were correct in both passes, and verdicts were recomputed from those files with fixed parsing. Per P14, final verdicts rest only on post-incident artifacts with re-verified pin shas. The closing tip re-check was done: tips 006dfe02 and 7c19065e arrived after the testing window, were not extracted, and are flagged for next-wave pickup; the two tips inside the window (e7427101, 7ea4d2e61) were both tested PASS.

### Zero Python attestation

The worker attests: zero Python ran in the fork battery work. POSIX shell, git (read-only operations plus the one documented fetch), sha256sum, stat, grep, sed, cut, cmp, the pinned znc binary, and the rebuilt pure-Zag harness only. No accidental Python invocation this wave.

Scope stamp holds: this battery certifies toolchain and extraction stability only, not the contents of the merged commits.

Recommendation: CONFIRM [RE-CERT].

## 3. tnn_chat FIT: CONFIRM [RE-CERT]

### Provenance answer

Provenance is the frozen 38-fact closed-book probe chain, and all ten chain inputs are byte-exact on 02ee5ae59: baseline instrument c0776ad6..., decline instrument a87011fe..., kb.txt 3ef27296..., gaz.txt b75fd113..., R33 sources e6379ddb... and 9824f6db..., pinned znc 498abcb5... (the same pin the fork battery verified), and the three fixtures kb1_out30.txt 936c35e1..., kb2_inkb.txt 730e2d24..., kb5_nogame.txt b60198b0... (10/10 PASS against frozen shas). The chain inherits byte-exactness from the archive; what is new this wave is the carry-over verification across the merge range, plus the judge-ordered fixture relocation.

### The carry-over

Range 4bbbca69c..02ee5ae59: 21 commits (merge of origin tip 94625817c into 4bbbca69c). git diff restricted to the chain paths is empty: zero modifications, zero deletions, zero content changes, no mode-only changes. The merged-in upstream work is read-only and disjoint from the chain paths. Per precedent P12, determinism is cited rather than re-run, and per P16 the citation names its wave and path: the wave-20260925-1421pdt fresh re-run record at docs/lab/rsi/runs/wave-20260925-1421pdt/chat_fit/FIT_1421.md (evidence commit 9692f5d1d), quoted by the 0821pdt carry-over: 2/2 binary reproducibility (decline 20273a99..., baseline 1ada2fae...), 9/9 run-pairs byte-identical, KB1 30/30 specific declines, KB2 17/17, KB5 10/10. 10/10 chain inputs byte-exact at this wave's HEAD; 9/9 determinism cited from the certified fresh re-run. That is the full basis for RE-CERT.

### Fixture relocation done

Per the 0821pdt judge's directive, the three probe fixtures were copied (shell cp, no edits) from the pruneable path docs/lab/rsi/runs/wave-20260924-0521pdt/forks/scratch/fitchat0521/ to the durable never-prune path docs/lab/rsi/fit_authority/fixtures/, with sha256 verified before and after each copy. All three match their frozen pins (936c35e1, 730e2d24, b60198b0). Originals left in place; the manifest rows untouched. The pruneable-location caveat that traveled in prior FIT files is now discharged for the chain side of the record.

### Python attestation

Zero Python touched wave artifacts. Shell coreutils only (git, sha256sum, mkdir, cp, cat, ls). No python3 invocation of any kind, no Python scratch files including /tmp. Nothing is voided.

Scope stamp holds: this is not merge review of the merged-in work; it certifies the 38-fact closed-book probe chain only.

Recommendation: CONFIRM [RE-CERT].

## 4. Interactive TNN: CONFIRM [RE-CERT], EXISTS for supervised red-team probe chats only

### Provenance answer

This is an availability survey, not a candidate. Its provenance is the sha-verified inventory on the merged tip: baseline probe binary 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c (ELF 64-bit, runnable), decline-gate probe binary 20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7 (runnable, with its sibling source), frozen instrument sources tnn_chat.zag c0776ad6... and tnn_chat_decline.zag a87011fe... plus kb.txt 3ef27296... and gaz.txt b75fd113... all matching the authority manifest, and the pinned znc 498abcb5.... Nothing new is claimed.

### The negative finding

No source-level chat/REPL/interactive-loop entry point exists in src/zag/ or units/ on this tip. The single grep hit for "repl|interactive|chat" was the substring "repl" inside "replay" and "replication" in units/teachers/learner/forcepin/PINS_RDTDT_BRIEF.md: a false positive, not an entry point. The entry-point signature follow-up (fn main, stdin, readline, read_line, interactive_loop, repl_loop) returned zero files. The 21-commit merge range 4bbbca69c..02ee5ae59 contains zero commits touching src/ or units/, and no newly added file matches chat|repl|interactive. The survey revealed no change, so per the standing rule no probe chat was run; availability was verified, execution was not needed. The caveat for any future supervised probe chat travels with it: tnn_chat emits unflagged confabulations on out-of-KB questions, so this surface is for supervised red-team knowledge-vs-architecture diagnosis only, never a candidate for adoption.

### Python attestation

No Python was used anywhere in this work. Shell commands only: grep, file, sha256sum, git log, git diff, git show.

Recommendation: CONFIRM [RE-CERT], EXISTS for supervised red-team probe chats only.

## 5. No new candidates this wave: CONFIRM the coordinator's stand-down

### Provenance answer

The provenance of a stand-down is the lane survey record, per P17. The survey: no new prereg drafts in docs/lab/rsi/ since the 0821pdt wave; every lane remains stood down or gated (G1 sunshafts pending a genuinely new design idea; D-VID-1 pending a re-aimed prereg with a different mechanism; CV-P and COMP-2 adoption barred pending his ruling 6 on Python-mirror logic; B1-class re-freezes requiring the P9 bar reformulation; ST-1 DEAD on pristine evidence). Advancing any adoption while his six governance rulings are open would gamble with his explicit boundaries: rulings on the S7 strike, MD-SSD-1 keep-with-UNVERIFIABLE versus re-freeze, the S11 image pull, the S11-AUD pull, the C12 queue decision, and Python-mirror-developed logic are all his to make and all unmade. The only candidate motion this wave is the orphan recovery of DP-1 (item 1), whose prereg commit-order self-check was run and recorded above: 18ad30fe3 strictly before 02d1dcb31, each committed alone, PASS. So the wave's self-check is not vacuous this wave: it covers the recovered commits and it passes. No UNVERIFIABLE ORDERING anywhere.

The judge in prior waves called this stand-down discipline, not stagnation. The advocate agrees: a wave that certifies its pins, its chain, its survey, and recovers one honest orphan has done its work. Freezing adoption while his rulings are open is the loop honoring his authority, which is the precondition for all of this machinery.

Recommendation: CONFIRM the stand-down.

## 6. Record wave-20260925-1721pdt in LOOP_STATE as INCOMPLETE, no verdict tag

### Provenance answer

Per the 0221pdt backfill precedent (the only precedent for a wave that died without its debate), the record for the dead wave is a run record, not a verdict. The 1721pdt fork battery and FIT evidence from that night travel as superseded historical evidence with zero lineage weight into any future verdict. The one live item is DP-1, which this wave's debate recovers under item 1 and tags [NEW] there, so the lineage of DP-1 attaches to this wave's certification, not to the dead wave's record. No candidates, no judge rulings, no Micah-facing verdicts are attached to the 1721pdt section. His six pending governance rulings and his sealed blind verdicts are unchanged by it.

Recommendation: record INCOMPLETE, no verdict tag, per precedent.

## Closing

The slate is: one genuine new candidate recovered from an orphaned wave, with all 8 frozen bars passing, commit order clean, provenance complete, red team in agreement, and the honest caveats on the record; three standing process re-certifications (fork battery, FIT, interactive survey) with uniform pins and explicit Python attestations; a disciplined stand-down while his six rulings are open; and an honest historical record for the wave that died. The brief argues every one of these should pass. The judge decides.
