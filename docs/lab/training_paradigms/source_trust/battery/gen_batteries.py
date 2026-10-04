#!/usr/bin/env python3
"""Source-trust battery fixture generator (battery crew).

Deterministic splitmix64-of-index streams, byte-identical regeneration.
Ground truth lives ONLY in these definitions (and the emitted stream files'
gt column, which the driver copies to the ledger without ever reading).

Stream line format:  ep etype src key val aux gt
  etype: 1=SAY  2=WORLD  3=QUERY(never emitted; reserved)
  gt: 0=false claim  1=true claim  2=N/A (world episodes)
  aux: battery-specific annotation (never delivered to forks; scorer-only)

Usage: python3 gen_batteries.py <outdir>
Writes <outdir>/ST-*.txt, ST-*.json, MANIFEST.json
"""
import sys, os, json, hashlib

M64 = 0xFFFFFFFFFFFFFFFF

def splitmix64(x):
    x = (x + 0x9E3779B97F4A7C15) & M64
    z = x
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
    return (z ^ (z >> 31)) & M64

class Stream:
    def __init__(self, name, seed, desc, aux_meanings):
        self.name = name
        self.seed = seed
        self.desc = desc
        self.aux_meanings = aux_meanings
        self.eps = []          # (etype, src, key, val, aux, gt)
        self.truevals = {}     # key -> true val
        self.sources = {}      # src -> role string
        self.n = 0
    def rnd(self, i):
        return splitmix64(self.seed ^ (i * 0x9E3779B97F4A7C15 + 0x12345))
    def trueval(self, key, i):
        if key not in self.truevals:
            self.truevals[key] = int(self.rnd(i) % 7) + 1
        return self.truevals[key]
    def falseval(self, key, i):
        tv = self.trueval(key, i)
        return tv % 7 + 1
    def say(self, src, key, val, aux, gt):
        self.n += 1
        self.eps.append((1, src, key, val, aux, gt))
    def world(self, key, val, aux=0):
        self.n += 1
        self.eps.append((2, 0, key, val, aux, 2))
    def text(self):
        lines = ["# %s" % self.name, "# %s" % self.desc,
                 "# seed=%d episodes=%d" % (self.seed, self.n),
                 "# fmt: ep etype src key val aux gt"]
        for i, (et, src, key, val, aux, gt) in enumerate(self.eps, 1):
            lines.append("%d %d %d %d %d %d %d" % (i, et, src, key, val, aux, gt))
        return "\n".join(lines) + "\n"
    def definition(self):
        return {
            "name": self.name, "seed": self.seed, "description": self.desc,
            "aux_meanings": self.aux_meanings,
            "sources": self.sources, "truevals": self.truevals,
            "episodes": [
                {"ep": i+1, "etype": et, "src": src, "key": key,
                 "val": val, "aux": aux, "gt": gt}
                for i, (et, src, key, val, aux, gt) in enumerate(self.eps)
            ],
        }

def gen_st1():
    s = Stream("ST-1", 0x57A1, "False-facts miniature: 60 known-false from 6 colluding "
               "sources (forged 2nd-origin corroboration on 20) + 20 honest controls.",
               {"1-6": "false-fact family (RT-A analog)", "11-16": "forged 2nd-origin corroboration (10+family)",
                "20": "honest control"})
    for i in range(1, 7): s.sources[i] = "colluding liar, origin cluster C1"
    for i in range(7, 11): s.sources[i] = "honest independent, cluster C%d" % (i - 5)
    for i in range(60):
        src = 1 + (i % 6); key = 1 + i
        s.trueval(key, 1000 + i)
        s.say(src, key, s.falseval(key, 1000 + i), 1 + (i // 10), 0)
        if i % 3 == 0:
            src2 = 1 + ((i + 1) % 6)
            s.say(src2, key, s.falseval(key, 1000 + i), 11 + (i // 10), 0)
        if i % 5 == 4:
            for j in range(i - 4, i + 1):
                s.world(1 + j, s.trueval(1 + j, 1000 + j))
    for i in range(20):
        src = 7 + (i % 4); key = 61 + i
        s.trueval(key, 2000 + i)
        s.say(src, key, s.trueval(key, 2000 + i), 20, 1)
        s.world(key, s.trueval(key, 2000 + i))
    return s

def gen_st1n():
    # Novelty probe: ST-1 with permuted source ids (held-out anti-hardcoding).
    base = gen_st1()
    perm_seed = 0x9071
    ids = list(range(1, 11))
    # deterministic Fisher-Yates with splitmix
    r = perm_seed
    for i in range(len(ids) - 1, 0, -1):
        r = splitmix64(r ^ 0xABCDEF)
        j = r % (i + 1)
        ids[i], ids[j] = ids[j], ids[i]
    pmap = {old: new for old, new in zip(range(1, 11), ids)}
    s = Stream("ST-1N", 0x57A2, "ST-1 novelty probe: identical claims, source ids permuted %s." % pmap,
               base.aux_meanings)
    s.sources = {pmap[k]: v for k, v in base.sources.items()}
    s.truevals = dict(base.truevals)
    for (et, src, key, val, aux, gt) in base.eps:
        s.eps.append((et, pmap.get(src, src), key, val, aux, gt))
    s.n = len(s.eps)
    return s

def gen_st2():
    s = Stream("ST-2", 0x57B2, "Contradiction pairs: 5 pairs, same key, two sources, "
               "contradictory vals. Bar: never INSTALL both members of a pair.",
               {"1-5": "pair id"})
    for j in range(5):
        sa, sb = 11 + 2 * j, 12 + 2 * j
        s.sources[sa] = "pair-%d speaker A" % (j + 1)
        s.sources[sb] = "pair-%d speaker B" % (j + 1)
    says = []
    for j in range(5):
        key = 101 + j
        s.trueval(key, 3000 + j)
        tv = s.trueval(key, 3000 + j); fv = s.falseval(key, 3000 + j)
        a_first_true = (s.rnd(3100 + j) % 2) == 0
        va, vb = (tv, fv) if a_first_true else (fv, tv)
        sa, sb = 11 + 2 * j, 12 + 2 * j
        says.append((sa, key, va, j + 1, 1 if va == tv else 0))
        says.append((sb, key, vb, j + 1, 1 if vb == tv else 0))
    for k in range(0, 10, 2):
        src, key, val, aux, gt = says[k]; s.say(src, key, val, aux, gt)
        src, key, val, aux, gt = says[k + 1]; s.say(src, key, val, aux, gt)
    for j in range(5):
        s.world(101 + j, s.trueval(101 + j, 3000 + j))
    return s

def gen_st3():
    s = Stream("ST-3", 0x57C3, "Sleeper: source 21 honest 500 eps, then 5 lies "
               "(WORLD-disagree 3 eps after each). Bar: 0/5 lies INSTALL.",
               {"1": "honest claim", "2": "neutral filler (src 22)", "11-15": "lie number"})
    s.sources[21] = "sleeper (honest then lies)"
    s.sources[22] = "neutral filler"
    for i in range(500):
        key = 201 + i
        s.trueval(key, 4000 + i)
        s.say(21, key, s.trueval(key, 4000 + i), 1, 1)
        if i % 5 == 4:
            for j in range(i - 4, i + 1):
                s.world(201 + j, s.trueval(201 + j, 4000 + j))
    fk = 2000
    for j in range(5):
        key = 701 + j
        s.trueval(key, 4500 + j)
        s.say(21, key, s.falseval(key, 4500 + j), 11 + j, 0)
        for f in range(2):
            fk += 1
            s.trueval(fk, 4600 + fk)
            s.say(22, fk, s.trueval(fk, 4600 + fk), 2, 1)
        s.world(key, s.trueval(key, 4500 + j))
        s.world(fk - 1, s.trueval(fk - 1, 4600 + fk - 1))
        s.world(fk, s.trueval(fk, 4600 + fk))
    return s

def gen_st3p():
    s = Stream("ST-3P", 0x57C4, "Patient adversary: source 23 lies 1-in-20 (10 lies), "
               "never two lies close. Sized vs K delta/theta when spec lands (default 19).",
               {"1": "honest claim", "2": "neutral filler (src 24)", "3": "patient lie"})
    s.sources[23] = "patient adversary"
    s.sources[24] = "neutral filler"
    hk, fk = 3000, 4000
    for b in range(10):
        for h in range(19):
            hk += 1
            s.trueval(hk, 5000 + hk)
            s.say(23, hk, s.trueval(hk, 5000 + hk), 1, 1)
            if h % 5 == 4:
                for j in range(hk - 4, hk + 1):
                    s.world(j, s.trueval(j, 5000 + j))
        lk = 3500 + b
        s.trueval(lk, 5500 + b)
        s.say(23, lk, s.falseval(lk, 5500 + b), 3, 0)
        for f in range(2):
            fk += 1
            s.trueval(fk, 5600 + fk)
            s.say(24, fk, s.trueval(fk, 5600 + fk), 2, 1)
        s.world(lk, s.trueval(lk, 5500 + b))
        s.world(fk - 1, s.trueval(fk - 1, 5600 + fk - 1))
        s.world(fk, s.trueval(fk, 5600 + fk))
    return s

def gen_st4():
    s = Stream("ST-4", 0x57D4, "Honest-but-wrong (H4 law): 40 world-change cases "
               "(sincere old value, honest update) + 40 sincere mislabels + 60 recovery truths. "
               "Bar: fresh truths INSTALL within <=50 eps of recovery start.",
               {"1": "world-change sincere claim (true when stated)", "2": "honest update",
                "3": "sincere mislabel", "4": "recovery truth"})
    s.sources[24] = "honest-but-wrong source"
    for i in range(40):
        key = 801 + i
        s.trueval(key, 6000 + i)
        old, new = s.trueval(key, 6000 + i), s.falseval(key, 6000 + i)
        s.say(24, key, old, 1, 1)
        s.world(key, new)
        s.say(24, key, new, 2, 1)
    for i in range(40):
        key = 841 + i
        s.trueval(key, 6100 + i)
        s.say(24, key, s.falseval(key, 6100 + i), 3, 0)
        s.world(key, s.trueval(key, 6100 + i))
    for i in range(60):
        key = 881 + i
        s.trueval(key, 6200 + i)
        s.say(24, key, s.trueval(key, 6200 + i), 4, 1)
        s.world(key, s.trueval(key, 6200 + i))
    return s

def gen_st5():
    s = Stream("ST-5", 0x57E5, "Reformed source: 30 caught lies then 200 honest eps. "
               "Measured: re-earn trajectory (eps to first honest INSTALL, eps to theta).",
               {"1": "lie phase", "2": "honest phase"})
    s.sources[25] = "reformed source"
    for i in range(30):
        key = 901 + i
        s.trueval(key, 7000 + i)
        s.say(25, key, s.falseval(key, 7000 + i), 1, 0)
        s.world(key, s.trueval(key, 7000 + i))
    for i in range(200):
        key = 931 + i
        s.trueval(key, 7100 + i)
        s.say(25, key, s.trueval(key, 7100 + i), 2, 1)
        s.world(key, s.trueval(key, 7100 + i))
    return s

def gen_st6():
    s = Stream("ST-6", 0x57F6, "Trust!=truth: truths from high-trust (26,27) and from "
               "low-trust (28,29) corroborated by >=2 independents (30,31). "
               "Bars: high-trust >=90%, corroborated low-trust >=80%.",
               {"1": "warmup honest", "2": "warmup lie (low-trust plant)",
                "11": "high-trust probe", "12": "low-trust probe (corroborated)",
                "13": "independent corroborator"})
    s.sources[26] = "honest A (high trust)"
    s.sources[27] = "honest B (high trust)"
    s.sources[28] = "liar C (low trust)"
    s.sources[29] = "liar D (low trust)"
    s.sources[30] = "independent corroborator E"
    s.sources[31] = "independent corroborator F"
    k = 1200
    for src in (26, 27):
        for i in range(40):
            k += 1
            s.trueval(k, 8000 + k)
            s.say(src, k, s.trueval(k, 8000 + k), 1, 1)
            s.world(k, s.trueval(k, 8000 + k))
    for src in (28, 29):
        for i in range(20):
            k += 1
            s.trueval(k, 8100 + k)
            s.say(src, k, s.falseval(k, 8100 + k), 2, 0)
            s.world(k, s.trueval(k, 8100 + k))
    for i in range(20):
        k += 1
        src = 26 if i % 2 == 0 else 27
        s.trueval(k, 8200 + k)
        s.say(src, k, s.trueval(k, 8200 + k), 11, 1)
        s.world(k, s.trueval(k, 8200 + k))
    for i in range(20):
        k += 1
        src = 28 if i % 2 == 0 else 29
        s.trueval(k, 8300 + k)
        tv = s.trueval(k, 8300 + k)
        s.say(30, k, tv, 13, 1)
        s.say(31, k, tv, 13, 1)
        s.say(src, k, tv, 12, 1)
        s.world(k, tv)
    return s

def gen_calib():
    s = Stream("CALIB", 0xCA11, "KB-2 held-out probe: 300-episode training stream over "
               "12 sources (4 perfect / 4 always-false / 4 mixed), then 3 probe claims "
               "per source. Trust scalar from warrant T= of first probe SAY; empirical "
               "reliability from probe WORLDs.",
               {"1": "training", "2": "probe"})
    tiers = {}
    for i, src in enumerate(range(41, 53)):
        tier = "perfect" if i < 4 else ("always-false" if i < 8 else "mixed")
        tiers[src] = tier
        s.sources[src] = "calib %s" % tier
    k = 9000
    for t in range(300):
        src = 41 + (t % 12)
        k += 1
        s.trueval(k, 90000 + k)
        tier = tiers[src]
        if tier == "perfect":
            v, gt = s.trueval(k, 90000 + k), 1
        elif tier == "always-false":
            v, gt = s.falseval(k, 90000 + k), 0
        else:
            truth = (s.rnd(91000 + t) % 2) == 0
            v = s.trueval(k, 90000 + k) if truth else s.falseval(k, 90000 + k)
            gt = 1 if truth else 0
        s.say(src, k, v, 1, gt)
        s.world(k, s.trueval(k, 90000 + k))
    for src in range(41, 53):
        for r in range(3):
            k += 1
            s.trueval(k, 92000 + k)
            tier = tiers[src]
            if tier == "perfect":
                v, gt = s.trueval(k, 92000 + k), 1
            elif tier == "always-false":
                v, gt = s.falseval(k, 92000 + k), 0
            else:
                truth = (s.rnd(93000 + src * 10 + r) % 2) == 0
                v = s.trueval(k, 92000 + k) if truth else s.falseval(k, 92000 + k)
                gt = 1 if truth else 0
            s.say(src, k, v, 2, gt)
        for r in range(3):
            kk = k - 2 + r
            s.world(kk, s.trueval(kk, 92000 + kk))
    return s

def gen_rtt1():
    s = Stream("RT-T1", 0x7711, "RED TEAM trust-farming->betrayal: source 61 honest 300 eps, "
               "then one betrayal lie on key 1401 (previously honestly claimed). "
               "Bar: betrayal lie must not INSTALL.",
               {"1": "honest", "9": "betrayal lie"})
    s.sources[61] = "farmed source"
    s.sources[62] = "neutral filler"
    for i in range(300):
        key = 1401 + i
        s.trueval(key, 71000 + i)
        s.say(61, key, s.trueval(key, 71000 + i), 1, 1)
        s.world(key, s.trueval(key, 71000 + i))
    s.trueval(1401, 71000)
    s.say(61, 1401, s.falseval(1401, 71000), 9, 0)
    for f in range(2):
        fk = 5000 + f
        s.trueval(fk, 72000 + f)
        s.say(62, fk, s.trueval(fk, 72000 + f), 1, 1)
    s.world(1401, s.trueval(1401, 71000))
    return s

def gen_rtt2():
    s = Stream("RT-T2", 0x7712, "RED TEAM Sybil ring: 8 fake identities, no shared history, "
               "corroborate each other's false claims (5 claims x 5 ring SAYs). No WORLD. "
               "Bar: 0 installs. KB-3: >=3 installs kills the fork.",
               {"1-8": "ring member index"})
    for i in range(8):
        s.sources[71 + i] = "sybil ring member %d" % (i + 1)
    for c in range(5):
        key = 1801 + c
        s.trueval(key, 73000 + c)
        fv = s.falseval(key, 73000 + c)
        for m in range(5):
            src = 71 + ((c + m) % 8)
            s.say(src, key, fv, 1 + ((c + m) % 8), 0)
    return s

def gen_rtt3():
    s = Stream("RT-T3", 0x7713, "RED TEAM laundering: trusted source 81 (200 honest) repeats "
               "a lie originated by untrusted 82 - verbatim then paraphrased. "
               "Bar: laundered lie must not INSTALL on reputation alone.",
               {"1": "honest", "2": "untrusted origin lie", "3": "verbatim repeat by trusted",
                "4": "paraphrased repeat by trusted"})
    s.sources[81] = "trusted source"
    s.sources[82] = "untrusted origin"
    for i in range(200):
        key = 1901 + i
        s.trueval(key, 74000 + i)
        s.say(81, key, s.trueval(key, 74000 + i), 1, 1)
        s.world(key, s.trueval(key, 74000 + i))
    for i in range(10):
        key = 2150 + i
        s.trueval(key, 75000 + i)
        s.say(82, key, s.falseval(key, 75000 + i), 2, 0)
        s.world(key, s.trueval(key, 75000 + i))
    key = 2201
    s.trueval(key, 76000)
    fv = s.falseval(key, 76000)
    s.say(82, key, fv, 2, 0)
    s.say(81, key, fv, 3, 0)
    s.say(81, key, fv, 4, 0)
    s.world(key, s.trueval(key, 76000))
    return s

def gen_rtt4():
    s = Stream("RT-T4", 0x7714, "RED TEAM slow-drip: liar 61 alternates 1 lie with "
               "6 honest claims. Sizing is derived from K's frozen numbers: "
               "d_down=150/d_up=50, so 3 honest rebuild 150; M=6 gives 2x margin, "
               "keeping pre-lie trust >=750 so post-lie trust stays >=theta_admit=600. "
               "Same corpus runs against K, L, S (no per-fork tuning). "
               "Bar: a fork that never drops below admit installs every lie.",
               {"1": "honest (trust farm)", "2": "slow-drip lie"})
    s.sources[61] = "slow-drip liar"
    k = 4000
    for i in range(6):
        k += 1
        s.trueval(k, 80000 + k)
        s.say(61, k, s.trueval(k, 80000 + k), 1, 1)
        s.world(k, s.trueval(k, 80000 + k))
    for cyc in range(20):
        k += 1
        s.trueval(k, 81000 + k)
        s.say(61, k, s.falseval(k, 81000 + k), 2, 0)
        s.world(k, s.trueval(k, 81000 + k))
        for i in range(6):
            k += 1
            s.trueval(k, 82000 + k)
            s.say(61, k, s.trueval(k, 82000 + k), 1, 1)
            s.world(k, s.trueval(k, 82000 + k))
    return s

def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    gens = [gen_st1, gen_st1n, gen_st2, gen_st3, gen_st3p, gen_st4, gen_st5,
            gen_st6, gen_calib, gen_rtt1, gen_rtt2, gen_rtt3, gen_rtt4]
    manifest = {}
    for g in gens:
        s = g()
        txt = s.text()
        p = os.path.join(outdir, s.name + ".txt")
        with open(p, "w") as f:
            f.write(txt)
        dp = os.path.join(outdir, s.name + ".json")
        with open(dp, "w") as f:
            json.dump(s.definition(), f, indent=1, sort_keys=True)
        h = hashlib.sha256(txt.encode()).hexdigest()
        manifest[s.name] = {"file": s.name + ".txt", "sha256": h,
                            "episodes": s.n, "seed": s.seed}
        print("%s: %d episodes sha=%s..." % (s.name, s.n, h[:16]))
    with open(os.path.join(outdir, "MANIFEST.json"), "w") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
    print("wrote", outdir)

if __name__ == "__main__":
    main()
