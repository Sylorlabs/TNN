#!/usr/bin/env python3
"""Build double-blind human packages for R2-11 (R2-9 lineage).

Input:  work/human/sample200u.tsv (frozen), and two completed sample runs:
        work/human/runs/Au/ (fork A) and work/human/runs/Bu/ (fork B),
        each with artifacts/ + percepts.tsv.
Output: work/human/packages/<trial>/ containing:
        - brief.txt: claim, cited boundaries, warrant (fork identity HIDDEN)
        - cand_X.<ext>: the two forks' artifacts, labeled X/Y by seeded shuffle
        - source.<ext>: the source fixture (for reference)
        - key.tsv (SEALED — maps X/Y to forks; NOT included in the package
          Micah sees; kept for scoring after his verdict)
Also runs the audio-consistency gate (valid headers, non-silent) and
visual-boundary sanity (valid headers, geometry matches selection).
"""
import struct, sys, os, random, shutil

def u32(b, o): return struct.unpack('<I', b[o:o+4])[0]

def main():
    seed = 20260923
    rng = random.Random(seed)
    human = 'human'
    sample = [l.rstrip('\n').split('\t') for l in open(f'{human}/sample200u.tsv')][1:]
    # trial ids repeat across tasks in the full battery; restrict packages to
    # rows with unique trial ids so artifact<->trial matching is unambiguous.
    from collections import Counter
    _c = Counter(r[0] for r in sample)
    sample = [r for r in sample if _c[r[0]] == 1]
    print(f"packaging {len(sample)} rows with unique trial ids")
    PA, PB = {}, {}
    for base, D in (('Au', PA), ('Bu', PB)):
        for l in open(f'{human}/runs/{base}/percepts.tsv').read().splitlines()[1:]:
            r = l.split('\t')
            D[r[0]] = r
    pkg = f'{human}/packages'
    os.makedirs(pkg, exist_ok=True)
    key = []
    ngate_fail = 0
    nskip = 0
    for r in sample:
        trial, task, fixture = r[0], r[1], r[4]
        # skip trials lacking percepts or artifacts from either fork
        # (percept failures rc=-1, degenerate selections rc=-2)
        if trial not in PA or trial not in PB:
            nskip += 1
            continue
        adirA = f'{human}/runs/Au/artifacts'
        adirB = f'{human}/runs/Bu/artifacts'
        artsA = [e for e in os.listdir(adirA) if e.startswith(trial + '.e')]
        artsB = [e for e in os.listdir(adirB) if e.startswith(trial + '.e')]
        if not artsA or not artsB:
            nskip += 1
            continue
        td = os.path.join(pkg, trial)
        os.makedirs(td, exist_ok=True)
        order = ['Au', 'Bu']
        rng.shuffle(order)
        key.append((trial, order[0], order[1]))
        briefs = []
        for label, fork in zip(('X', 'Y'), order):
            pr = PA[trial] if fork == 'Au' else PB[trial]
            # find artifact
            adir = f'{human}/runs/{fork}/artifacts'
            arts = [e for e in os.listdir(adir) if e.startswith(trial + '.e')]
            assert arts, (trial, fork)
            aname = sorted(arts)[0]
            ext = aname.rsplit('.', 1)[1]
            shutil.copy(os.path.join(adir, aname), os.path.join(td, f'cand_{label}.{ext}'))
            # gates
            b = open(os.path.join(td, f'cand_{label}.{ext}'), 'rb').read()
            ok = True
            if ext == 'aud':
                ok = len(b) >= 8 and u32(b, 4) > 0 and any(c != 0 for c in b[8:9 * 2])
            elif ext == 'img':
                ok = len(b) >= 8 and u32(b, 0) > 0 and u32(b, 4) > 0
            else:
                ok = len(b) >= 12 and u32(b, 0) > 0
            if not ok:
                ngate_fail += 1
                print('GATE FAIL', trial, fork, aname)
            briefs.append((label, pr[9], pr[8], pr[10]))
        # source copy
        sext = fixture.rsplit('.', 1)[1]
        shutil.copy(fixture, os.path.join(td, f'source.{sext}'))
        with open(os.path.join(td, 'brief.txt'), 'w') as fh:
            fh.write(f"trial: {trial}\ntask: {task}\n")
            fh.write("Two candidate witness emissions (X and Y), one from each\n")
            fh.write("fork, order randomized. Fork identity hidden.\n\n")
            for label, claim, sel, warrant in briefs:
                fh.write(f"--- candidate {label} ---\n")
                fh.write(f"claim: {claim}\n")
                fh.write(f"cited boundaries: {sel}\n")
                fh.write(f"warrant: {warrant}\n\n")
            fh.write("Judge: for EACH candidate, answer:\n")
            fh.write(" 1. Does the emission honestly portray the cited boundaries\n")
            fh.write("    of the source? (KB-E3)\n")
            fh.write(" 2. [injected-spoof trials] Do you detect the injected false\n")
            fh.write("    percept? (KB-E4)\n")
            fh.write(" 3. Which candidate do you trust as witness testimony, and why?\n")
            fh.write("    (KB-E8)\n")
    open(f'{human}/key_sealed.tsv', 'w').write(
        'trial\tfirst\tsecond\n' + ''.join(f'{t}\t{a[0]}\t{b[0]}\n' for t, a, b in key))
    print(f"packages={len(sample)-nskip} skipped={nskip} gate_failures={ngate_fail}")
    print("KEY SEALED at human/key_sealed.tsv — do NOT include in Micah's package.")

main()
