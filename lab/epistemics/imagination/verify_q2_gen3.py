#!/usr/bin/env python3
"""Independent GEN-3 (internal consistency) probe battery for Q2 designs.

2 consistency probes per design (24 total), computed by query functions
ported by reading imagine.zag (same ports as verify_imag.py, which were
verified line-by-line against ig_q_* above). Answers are derived from the
E-line attributes (the partition IS the emitted spec), then checked against
hand-traced expectations: any disagreement is investigated, not auto-fixed.
"""
import sys
sys.path.insert(0, '/home/hatch/workspace/tnn-lab/imagination')
import verify_imag as V

def parse(path):
    designs = {}
    with open(path) as f:
        for line in f:
            t = line.split()
            if t and t[0] == 'E' and len(t) == 14:
                mode, brief = int(t[1]), int(t[2])
                sc = designs.setdefault((mode, brief), V.Scene())
                sc.place(*[int(x) for x in t[4:]])
    return designs

# probe spec: (mode, brief, probe_name, query_fn_of_sc, hand_traced_expected, hand_rationale)
def probes():
    P = []
    # ---- mode 0 (machine) ----
    P.append((0, 1, "warmest element", lambda sc: V.q_warmest(sc, 0), 0,
              "r-b: 170,170,150 -> tie at 170 -> lowest index 0"))
    P.append((0, 1, "zone-7 occupancy", lambda sc: V.q_zonecount(sc, 7, 0), 1,
              "zones {1,4,7}: zone7 holds elem2 only"))
    P.append((0, 2, "warmest element", lambda sc: V.q_warmest(sc, 0), 2,
              "r-b: -110,-5,150,0 -> elem2 (the warm accent)"))
    P.append((0, 2, "zone-7 occupancy", lambda sc: V.q_zonecount(sc, 7, 0), 2,
              "both text zones at (500,833) -> zone 7"))
    P.append((0, 3, "audio contour", lambda sc: V.q_contour(sc, 0), 4,
              "262,262,349,523 strictly non-falling, last>first -> rising"))
    P.append((0, 3, "max-step index", lambda sc: V.q_maxstep(sc, 0), 2,
              "steps 0,87,174 -> k=2"))
    P.append((0, 4, "tension(0,1)", lambda sc: V.q_tension(sc, 0, 1, 0), 3,
              "262->523 = octave = 12 semitones -> tcode 3"))
    P.append((0, 4, "audio contour", lambda sc: V.q_contour(sc, 0), 3,
              "262,523,349 rises then falls, single interior peak -> arch"))
    P.append((0, 5, "topmost element", lambda sc: V.q_topmost(sc, 0), 0,
              "z: 200,120,0,0,0 -> elem0"))
    P.append((0, 5, "support(0)", lambda sc: V.q_support(sc, 0, 0), 1,
              "z=200; elem1 ztop=120+80=200>=180, size 80>=40, dx=dy=0 -> 1"))
    P.append((0, 6, "relation(0,3)", lambda sc: V.q_relation(sc, 0, 3, 0), 1,
              "dx=666,dy=333 same z; |dx|>=|dy|, dx>0 -> 1 (LEFT_OF)"))
    P.append((0, 6, "farthest pair", lambda sc: V.q_farthest(sc, 0), (0, 3),
              "zones {0,3,4,5}; cheby(0,5)=2 max -> elems (0,3)"))
    # ---- mode 1 (human) ----
    P.append((1, 1, "warmest element", lambda sc: V.q_warmest(sc, 1), 0,
              "all color 1003 -> warmth 2 tie -> lowest index 0"))
    P.append((1, 1, "zone-2 occupancy", lambda sc: V.q_zonecount(sc, 2, 1), 1,
              "zones {0,2,7}: zone2 holds elem1 only"))
    P.append((1, 2, "warmest element", lambda sc: V.q_warmest(sc, 1), 3,
              "2003,2003,2004 neutral(1); 1027 hue4 warm(2) -> elem3"))
    P.append((1, 2, "zone-7 occupancy", lambda sc: V.q_zonecount(sc, 7, 1), 2,
              "zones {1,4,7,7}: zone7 holds both text elems"))
    P.append((1, 3, "audio contour", lambda sc: V.q_contour(sc, 1), 4,
              "bins 26,26,26,27 non-falling, last>first -> rising"))
    P.append((1, 3, "max-step index", lambda sc: V.q_maxstep(sc, 1), 2,
              "bin steps 0,0,1 -> k=2"))
    P.append((1, 4, "tension(1,2)", lambda sc: V.q_tension(sc, 1, 2, 1), 2,
              "|20-19|=1 bin -> tcode(1)=2"))
    P.append((1, 4, "last-stable", lambda sc: V.q_laststable(sc, 1), 0,
              "tension(1,2)=2 != 0 -> 0"))
    P.append((1, 5, "support(0)", lambda sc: V.q_support(sc, 0, 1), 1,
              "chain 0->1->2 ends rel=0 -> 1"))
    P.append((1, 5, "relation(0,1)", lambda sc: V.q_relation(sc, 0, 1, 1), 5,
              "elem0 rel=5 (STACKED_ON) target elem1 -> 5"))
    P.append((1, 6, "relation(0,2)", lambda sc: V.q_relation(sc, 0, 2, 1), 1,
              "no explicit rels; zones 0 vs 2: col 0<2 -> 1 (LEFT_OF)"))
    P.append((1, 6, "farthest pair", lambda sc: V.q_farthest(sc, 1), (0, 2),
              "zones {0,1,2,3}; cheby(0,2)=2 max -> elems (0,2)"))
    return P

def main():
    dm = parse('/home/hatch/workspace/tnn-lab/imagination/logs/q2m.txt')
    dh = parse('/home/hatch/workspace/tnn-lab/imagination/logs/q2h.txt')
    ok = tot = 0
    print(f"{'mode':<6}{'brief':<7}{'probe':<20}{'ported':<10}{'hand':<10}{'match':<7}rationale")
    for mode, brief, name, fn, hand, why in probes():
        sc = (dm if mode == 0 else dh)[(mode, brief)]
        got = fn(sc)
        match = (got == hand)
        tot += 1
        if match: ok += 1
        flag = "OK" if match else "** MISMATCH **"
        print(f"{mode:<6}{brief:<7}{name:<20}{str(got):<10}{str(hand):<10}{flag:<7}{why}")
        if not match:
            print(f"    INVESTIGATE: ported={got} hand={hand}")
    print(f"\nGEN-3: {ok}/{tot}")

if __name__ == '__main__':
    main()
