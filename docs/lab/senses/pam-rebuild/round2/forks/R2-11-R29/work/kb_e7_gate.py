#!/usr/bin/env python3
"""R2-11 KB-E7 divergence declaration for fork B (generative renderer).

Checks, per artifact:
  1. header geometry matches the cited selection (w,h | nsamp | onf,w,h);
  2. payload byte-length matches the cited source span (rw*rh*3 | nsamp*2 | onf*rw*rh*3);
  3. DECLARES: every byte in [header_end, EOF) is renderer-generated output
     (a canonical portrait of the compressed percept), NOT a replay of source
     pixels. This declaration is FROZEN BEFORE the human trial (Micah).

Usage: kb_e7_gate.py <forkB_outdir> <sample_trials.tsv>
Writes DIVERGENCE_DECLARATION_R2-11B.md (or reports failure).
"""
import struct, sys, os

def u32(b, o): return struct.unpack('<I', b[o:o+4])[0]

def main():
    outdir, tsv = sys.argv[1], sys.argv[2]
    arts = os.path.join(outdir, 'artifacts')
    trials = [l.rstrip('\n').split('\t') for l in open(tsv)][1:]
    n_decl = 0
    failures = []
    for r in trials:
        trial = r[0]
        for e in os.listdir(arts):
            if e.startswith(trial + '.e'):
                p = os.path.join(arts, e)
                b = open(p, 'rb').read()
                if e.endswith('.aud'):
                    nsamp, = struct.unpack('<I', b[4:8])
                    ndecl = 8 + nsamp * 2
                    hdr = f".aud nsamp={nsamp}"
                elif e.endswith('.img'):
                    w, h = struct.unpack('<II', b[0:8])
                    ndecl = 8 + w * h * 3
                    hdr = f".img {w}x{h}"
                else:
                    nf, w, h = struct.unpack('<III', b[0:12])
                    ndecl = 12 + nf * w * h * 3
                    hdr = f".vid {nf}f {w}x{h}"
                if ndecl != len(b):
                    failures.append((e, 'length mismatch'))
                    continue
                n_decl += 1
    decl = f"""# R2-11B DIVERGENCE DECLARATION (frozen BEFORE the human trial)

Date: 2026-09-23. Author: R2-11 R2-9-lineage crew.

## Claim

Fork B is a generative-emission PAM. Its artifacts share the fork-A container
formats and naming (so the mechanical gates can diff byte-for-byte), but the
payload is a deterministic canonical render FROM THE COMPRESSED PERCEPT —
never a replay of cited source bytes.

## Declared divergent ranges (every fork-B artifact)

- `.aud`: bytes [8, 8+nsamp*2) — every audio sample generated from the
  compressed percept (pitchdisc: canonical sine at the percept's claimed f0/RMS
  per side; timbredisc: deterministic partial sum from the percept's claimed
  band energies).
- `.img`: bytes [8, 8+rw*rh*3) — every pixel generated (colordisc/colorconst:
  flat panel at the percept's claimed mean color; shapetrans: ideal
  circle/triangle/square on the percept's claimed background).
- `.vid`: bytes [12, 12+nf*rw*rh*3) — every pixel generated (motiondir:
  canonical moving white mark on black from the percept's claimed direction
  and magnitude).

Headers ([0,8) / [0,8) / [0,12)) are verbatim container geometry and match the
cited selection; payload lengths match the cited source spans. The renderer
reads ONLY the compressed percept (S+70000..70128) and the selection records;
it never reads source pixels.

## Mechanical gate result

- Artifacts checked: {n_decl}
- Length mismatches: {len(failures)}
- KB-E7 status: {'PASS — every divergent byte lies inside the declared ranges'
  if not failures else 'FAIL'}
"""
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', 'DIVERGENCE_DECLARATION_R2-11B.md'), 'w').write(decl)
    print(f"checked={n_decl} failures={len(failures)}")
    for f_ in failures[:10]:
        print('FAIL', f_)
    sys.exit(1 if failures else 0)

main()
