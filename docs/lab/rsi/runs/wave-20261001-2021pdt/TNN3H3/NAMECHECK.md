# NAMECHECK.md: TNN3H3 lane, wave-20261001-2021pdt

## Step 0: Worker toolchain guard (MANDATORY, before any other work)

- Setup run: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh` -> SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
- PATH set to `/home/hatch/safebin` for all work
- `which python3` returns NOTHING (exit 1). Confirmed: python3 and python absent from PATH
- Toolchain verification: PASS. No forbidden executable is reachable
- Task type: WRITING ONLY (PREREG_H3.md). No computation, no binaries, no implementation files. Pure-Zag constraint observed trivially

## Step 1: Working copy and git rules

- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab
- Write ONLY inside docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H3/ (new files only: NAMECHECK.md, PREREG_H3.md)
- NEVER push. Never git reset --hard. Never rebase. Do NOT git commit; coordinator commits

## Step 2: Documentation rule

- No em-dashes anywhere in lane documentation. Checked before finalizing

## Step 3: Task scope

- Write the H3 prereg with MANDATORY SUBSTRATE VERIFICATION as prereg section 2, quoting exact source lines, line numbers, hashes, measured deletion set
- Verification source: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag, expected SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
- If verification (a) shows unification is already the case, or (c) shows no post-deletion construction path: STOP, report SUBSTRATE-ABSENT or SUBSTRATE-ALREADY-UNIFIED with evidence, do NOT write bars
- If verification passes: draft PREREG_H3.md with frozen kill bars modeled on H1/H5 preregs, sealed family requirements, three-valued verdict rule, sealed evaluation as the only verdict path

## Step 4: Deliverables

- [x] NAMECHECK.md (this file)
- [x] PREREG_H3.md: NOT-FROZEN with SUBSTRATE-ALREADY-UNIFIED (item a) and SUBSTRATE-ABSENT (item c) verdict and full verification evidence. No bars frozen.
- Em-dash check: grep for U+2014 across lane files returns nothing. PASS.
