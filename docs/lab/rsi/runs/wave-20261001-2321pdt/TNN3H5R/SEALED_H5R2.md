# SEALED_H5R2: sealed world specifications

Lane TNN3H5R, wave-20261001-2321pdt. Single worker acting as
coordinator, builder, and evaluator (no separate adversary lane was
assigned); see the seal-integrity disclosure in PREREG_H5R2.md section
5.6, frozen before implementation. Worlds were assembled only after the
implementation commit 9db334bd4 (2026-10-02 06:31:39 UTC), mechanically
from the frozen driver template (SHA-256
f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af,
matching the prereg record) and the frozen assembly rule. The builder
attests no world output was used to tune the substrate; smoke tests
used unsealed keys (9xxx) disjoint from all sealed ranges. Nothing is
reused from the killed H5 battery, the killed H5R battery, or any prior
worlds, keys, values, or ranges.

## Key/relation/value ranges

All sealed ranges live in 83xxx-86xxx, disjoint from: FW1-FW9 (3xxxx),
the 1421pdt battery (43xxx), the killed H5 battery (51xxx-54xxx), the
killed H5R battery (61xxx-65xxx, 71xxx-72xxx), the H5R builder smoke
worlds (7xxx/8xxx/9001), and the H5R2 smoke keys (9xxx). Per-probe
(subject, relation) key ranges are disjoint within each world. No world
is a trivial variant of FW1-FW9, the 1421pdt battery, or either killed
battery: the C worlds probe MAP-key re-derivation after contradiction
with the new provenance gate, and the W3 family is new (two successive
revisions before a revert, which no prior battery tested).

## Seeds (frozen in PREREG_H5R2.md before implementation)

s1=48984 (w_c1, value offset vo1=5), s2=59920 (w_c2, vo2=0),
s3=20822 (w_w3a, vo3=4), s4=29675 (w_w3b, vo4=2). Seed inputs were the
strings "TNN3H5R2|wave-20261001-2321pdt|world1" through "...|world4";
first 4 hex digits of each SHA-256 digest taken as the seed integer,
value offset = seed mod 7.

## World files (pre-run SHA-256, recorded before any run)

Each world file is a byte-copy of the committed substrate tnn3_h5r2.zag
(git blob 9db334bd4, SHA-256
04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a,
verified before assembly) with exactly one line changed
(`fn main()i32 { return run_all(); }` to
`fn main()i32 { return sealed_main(); }`, verified by grep) plus
DRIVER_TMPL.zag appended plus one alias line selecting the world
(`fn sealed_main()i32 { return sealed_main_c1(); }`, etc.). The
substrate portion of every world is therefore the exact source that
builds the frozen binary (SHA-256
19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287).

- w_c1.zag 3246e635488c0b7c46d4a0fe41ea267a6777827a9d64333ecf3a869b8defd0e7
- w_c2.zag 28831f3b49e6fcf436a4537b0e8d6ae8bfdec15c8703037fce619beb5d88f0b8
- w_w3a.zag 3ec3b1631127c4c7ac1758329c32f65661396a11847c2c6b14a59aea65289843
- w_w3b.zag 7e69965d4c6a7e86486a370f68bc0e827bd289c076c10a1e4d49e781d5159e41

## C-family (revert worlds; KB-W2R 12/12)

Pattern per double-contradiction probe (prereg 5.3, exact): teach chain
a-RF1->b, b-RF2->c0; QUERY a RM c0 (promote); OBSERVE b RF2 c1 (fact-key
contradiction, never the MAP key); QUERY a RM c1 (expect c1 via fresh
MAP); OBSERVE b RF2 c2; QUERY a RM c2 (expect c2 via fresh MAP).

Pattern per revert probe: teach chain; QUERY a RM c0 (promote);
OBSERVE b RF2 c1; QUERY a RM c1 (expect c1 via fresh MAP);
OBSERVE b RF2 c0 (revert); QUERY a RM c0 (expect c0 via fresh MAP).

Frozen constraint honored: no OBSERVE on any MAP key in any world. 12
probes x 3 MAP-key probes = 36 SNAP-IN records (the KB-W0 set).

### w_c1 (chain relations 8301/8302, MAP relation 8303, vo1=5)

- C1D1: a=83101 b=83301 c0=83406 c1=83407 c2=83408
- C1D2: a=83102 b=83302 c0=83416 c1=83417 c2=83418
- C1D3: a=83103 b=83303 c0=83426 c1=83427 c2=83428
- C1D4: a=83104 b=83304 c0=83436 c1=83437 c2=83438
- C1R1: a=83201 b=83311 c0=83506 c1=83507
- C1R2: a=83202 b=83312 c0=83516 c1=83517

### w_c2 (chain relations 8401/8402, MAP relation 8403, vo2=0)

Materially different relation family and subject distribution from w_c1.

- C2D1: a=84101 b=84301 c0=84401 c1=84402 c2=84403
- C2D2: a=84102 b=84302 c0=84411 c1=84412 c2=84413
- C2D3: a=84103 b=84303 c0=84421 c1=84422 c2=84423
- C2D4: a=84104 b=84304 c0=84431 c1=84432 c2=84433
- C2R1: a=84201 b=84311 c0=84501 c1=84502
- C2R2: a=84202 b=84312 c0=84511 c1=84512

Non-vacuity: each probe's MAP key (a,RM) has no fact with relation RM
anywhere, so the first MAP-key probe cannot hit an exact fact and must
go through the trial loop; the licensing chain uses two-hop facts only
the trial can compose. Post-contradiction probes must miss (superseded
MAP, no shadow fact) and re-derive. The driver checks fresh promotion
by strictly increasing live-MAP node ids per probe.

## W3-family (provenance-chain worlds; KB-W3 8/8)

Pattern per chained probe (prereg 5.4, exact): teach chain a-RF1->b,
b-RF2->c0; QUERY a RM c0 (promote); OBSERVE b RF2 c1; QUERY a RM c1;
OBSERVE b RF2 c2; QUERY a RM c2; OBSERVE b RF2 c0 (revert);
QUERY a RM c0 (expect c0 via a fresh MAP whose DEP edges land on the
live reverted fact). Two successive revisions occur before the revert;
the revert must land on the latest fact. 4 probes x 4 MAP-key probes =
16 SNAP-IN records per world (not part of the KB-W0 36-set).

### w_w3a (chain relations 8501/8502, MAP relation 8503, vo3=4)

- W3A1: a=85101 b=85301 c0=85405 c1=85406 c2=85407
- W3A2: a=85102 b=85302 c0=85415 c1=85416 c2=85417
- W3A3: a=85103 b=85303 c0=85425 c1=85426 c2=85427
- W3A4: a=85104 b=85304 c0=85435 c1=85436 c2=85437

### w_w3b (chain relations 8601/8602, MAP relation 8603, vo4=2)

Materially different relation family and subject distribution from w_w3a.

- W3B1: a=86101 b=86301 c0=86403 c1=86404 c2=86405
- W3B2: a=86102 b=86302 c0=86413 c1=86414 c2=86415
- W3B3: a=86103 b=86303 c0=86423 c1=86424 c2=86425
- W3B4: a=86104 b=86304 c0=86433 c1=86434 c2=86435

Non-vacuity: the revert is the fourth MAP-key probe, after three live
lineages (original, c1, c2 facts) have been superseded in sequence; the
trial loop must decline the three dead lineages and promote on the
fourth, live one. The driver checks sup==3, a single live MAP with
f28==c0, and all DEP targets live.

## Snapshot and dump protocol

- Before every MAP-key probe the driver emits one SNAP-IN line with the
  exact count of live tag-1 facts on (s_m,r_m) (KB-W0 conjunct 1) and
  after the probe one Q line with the returned value, the live MAP
  count, id, and f28 (KB-W0 conjunct 2). 36 SNAP-IN records across w_c1
  and w_c2 form the KB-W0 set; the 32 W3 SNAP-IN records are evaluated
  under KB-W3/KB-B3.
- Each world ends with a canonical full state dump for KB-D1 3/3
  byte-identical comparison.
- Determinism: 3 runs per world binary; SHA-256 of full stdout compared.
