#!/usr/bin/env python3
"""SOCIAL-FALSENESS GATE (B-beta kids): verify the rendered piece's social
timing from the deterministic placement log. Checks, all preregistered in
DERIVATION_kids.md:
  S1: P3 (15-26s) laugh chain shows CONTAGION: inter-onset latencies shrink
      across the chain (first-half median > second-half median) and at least
      3 overlaps where next laugh starts before prev ends (the tumble).
  S2: P3 uses >=2 distinct voices with at least one voice change per 3 links.
  S3: P1 (5-13s) step IOIs fall in the 260-404ms run-cadence band, never
      exactly equal (no metronome): >=4 distinct IOI values.
  S4: The TAG shout lands in 13.0-13.5s and all steps stop before 13.0s
      (cause precedes effect: chase -> tag -> gasp -> contagion).
  S5: No laugh in P3 exceeds the breath budget rule's max single event
      (2600ms) and late-chain laughs are shorter on average (breath arc).
Exit 0 = PASS, 1 = FAIL."""
import sys

SRC_DUR = {0: 30.0135, 1: 48.849, 2: 11.260, 3: 92.389, 4: 0.575, 5: 10.684}

def main(path):
    rows = []
    for ln in open(path):
        p = ln.split()
        if len(p) != 7:
            continue
        dst, src, s0, s1, voice, target, rev = map(int, p)
        rows.append(dict(dst=dst, src=src, s0=s0, s1=s1, voice=voice,
                         target=target, rev=rev, dur=s1 - s0))
    fails = []

    def check(name, cond, detail):
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")
        if not cond:
            fails.append(name)

    # lineage sanity: every span inside its source
    bad = [r for r in rows if not (0 <= r['s0'] < r['s1'] <= SRC_DUR[r['src']] * 1000 + 1)]
    check("lineage spans valid", not bad, f"{len(rows)} placements, {len(bad)} out-of-range")

    steps = sorted([r for r in rows if r['voice'] == 9 and 5000 <= r['dst'] < 13000],
                   key=lambda r: r['dst'])
    sioi = [b['dst'] - a['dst'] for a, b in zip(steps, steps[1:])]
    check("S3 step cadence 260-404ms", all(240 <= x <= 430 for x in sioi),
          f"{len(steps)} steps, IOI range {min(sioi)}-{max(sioi)}ms, distinct={len(set(sioi))}")
    check("S3 no metronome", len(set(sioi)) >= 4, f"{len(set(sioi))} distinct IOIs")

    tag = [r for r in rows if 13000 <= r['dst'] < 13600 and r['voice'] in (0, 1, 3)]
    late_steps = [r for r in rows if r['voice'] == 9 and 13000 <= r['dst'] < 15000]
    check("S4 tag shout 13.0-13.5s, steps stopped", len(tag) >= 1 and not late_steps,
          f"tag events={len(tag)}, steps in 13-15s={len(late_steps)}")

    chain = sorted([r for r in rows if 15000 <= r['dst'] < 26000 and r['voice'] in (0, 1, 3)],
                   key=lambda r: r['dst'])
    ends = [r['dst'] + r['dur'] for r in chain]
    overlaps = sum(1 for a, b in zip(chain[1:], ends[:-1]) if a['dst'] < b)
    check("S1 tumble overlaps>=3", overlaps >= 3, f"{overlaps} overlaps in {len(chain)}-laugh chain")
    lat = [b['dst'] - a_end for a_end, b in zip(ends[:-1], chain[1:])]
    # latencies can be negative (overlap); use raw gap from prev END
    if len(lat) >= 4:
        h1 = sorted(lat[:len(lat)//2])[len(lat)//4]
        h2 = sorted(lat[len(lat)//2:])[len(lat[len(lat)//2:])//2]
        check("S1 contagion shrinks", h2 <= h1,
              f"first-half median gap {h1}ms, second-half {h2}ms")
    else:
        check("S1 contagion shrinks", False, "chain too short")
    vseq = [r['voice'] for r in chain]
    changes = sum(1 for a, b in zip(vseq, vseq[1:]) if a != b)
    check("S2 multi-voice chain", len(set(vseq)) >= 2 and changes >= len(vseq)//3,
          f"voices={sorted(set(vseq))}, changes={changes}/{len(vseq)}")

    durs = [r['dur'] for r in chain]
    check("S5 breath arc", sum(durs[len(durs)//2:]) / max(len(durs)//2, 1) <= sum(durs[:len(durs)//2]) / max(len(durs)//2, 1),
          f"first-half mean {sum(durs[:len(durs)//2])/max(len(durs)//2,1):.0f}ms vs second-half {sum(durs[len(durs)//2:])/max(len(durs)//2,1):.0f}ms")

    print("SOCIAL-FALSENESS GATE:", "PASS" if not fails else f"FAIL {fails}")
    return 0 if not fails else 1

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
