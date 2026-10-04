# PREREG: BELIEF-NOGRUDGE (noise grudge repair). Frozen.

Status: FROZEN before implementation. Unfrozen variant only. Pure Zag.

## Governing mandate

Repair the noise grudge bug found in the belief sealed adversarial retest
(commit cff02d5de, world D KILL): the betrayal counter b incremented on
every wrong outcome while streak c > 0, even when the rule's own base
penalty priced the event at p = 0. Forty zero penalty noise events
accumulated b = 40, so a later first real error at w = 8 cost p = 205.

## Repair (single branch change in ev_calibrate, nothing else)

In the wrong outcome branch with c > 0, compute base = floor(c*w/(c+w)).

  If base > 0: penalty p = base*(1+b), total += 1+p, b += 1, record p.
  Else (base = 0): total += 1, b unchanged, record p = 0.

b increments only on a material betrayal. Zero penalty noise never
increments b. Since p = base*(1+b) and 1+b >= 1, base > 0 is exactly
p > 0. All other logic is byte identical to the frozen rule:
traj_penalty formula, c = 0 branch, streak reset on wrong, reform decay
(one b unit per 100 consecutive honest outcomes), rel accounting,
independence discount, evidence record, dedup register. No modes, no
bridges, no handlers, no new semantic cases. The change adds no
domain detector and no benchmark specific logic: materiality is a
property of the existing generic penalty formula.

## World D retest (rationality bars)

Source ext id 80. World: 40 cycles of [5 correct w = 1, 1 wrong w = 1],
then 20 honest w = 1, then one high stake error w = 8 (c = 20 at the
time), then a 200 honest tail. eid fresh per event.

Predicted repaired behavior (binary asserts):

  after 40 noise cycles: correct 200, total 240, b 0, streak 0, rel 833
  after 20 honest: correct 220, total 260, b 0, streak 20, rel 846
  test event: base 5, b before 0, p 5, b after 1, rel 827, recorded p 5
  after 200 honest tail: b 0, rel 901, streak 200

Arithmetic: floor(200000/240) = 833; floor(220000/260) = 846;
floor(20*8/28) = 5; 5*(1+0) = 5; floor(220000/266) = 827;
floor(420000/466) = 901. b = 1 decays to 0 at the 100th honest
outcome of the tail, so forgiveness is reachable for the noisy
honest source. Rationality bar: b = 0 after noise; test event near
first timer price p = 5; tail b = 0.

## Escalation preservation (H-DECEPT-4 D4 table)

Same five phase protocol as belief_antifarm.zag (ext id 90, 20 rebuild
wrongs w = 1, then betrayal): all betrayal bases are > 0, so the
repair is a no op here and every frozen number must reproduce exactly.

  A w = 3: rebuild rel 1000, streak 20, b before 0, base 2, p 2, rel 869, b after 1
  B w = 5: rebuild rel 930, b before 1, base 4, p 8, rel 769, b after 2
  C w = 8: rebuild rel 833, b before 2, base 5, p 15, rel 681, b after 3
  D w = 8: rebuild rel 740, b before 3, base 5, p 20, rel 620, b after 4
  E w = 8: rebuild rel 671, b before 4, base 5, p 25, rel 571, b after 5

Exposures 869, 769, 681, 620, 571 (below 769 and falling). Penalties
2, 8, 15, 20, 25. Escalation: p(S#2) = 8 > p(Q single at w = 5) = 4;
p(S#3) = 15 > p(V single at w = 8) = 5.

## Reform preservation

Control W (ext id 93): 20 rebuild, betrayal w = 8 p = 5, 100 honest:
b = 0, rel = 952. Second betrayal p = 7 equals fresh 100 source X
(ext id 94) first betrayal p = 7. Reform equality holds.

## Controls

R1 (ext id 95): 120 correct: rel = 1000, b = 0.
C0 (ext id 96): no streak wrong: p = 0, b = 0, rel = 1000; after 20
rebuild, betrayal w = 8: p = 5, rel = 740.
P patient farmer (ext id 97): 100 honest, betrayal w = 8 p = 7, 100
honest, betrayal w = 8 p = 7, rel = 925.

## Kill bars

K1: 3/3 runs byte identical (sha256), exit 0, ALL PASS, zero FAIL lines.
K2: rule layer of belief_nogrudge.zag matches belief_antifarm.zag at
commit 035e9593c byte for byte except the one repaired branch defined
above (diff restricted to the ev_calibrate betrayal branch, plus the
header comment and the new main).
K3: per world verdicts scored against the bars above. World D
repaired: b = 0 after noise, p = 5 on the test event, b = 0 after
the tail. Escalation, reform, and all controls at their frozen values.
K4: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag
(safebin PATH, no python3/python at any point). Unfrozen variant only;
frozen belief_deception, belief_trajectory, belief_repeated,
belief_antifarm, belief_sealed sources untouched; paper untouched;
nothing pushed; explicit pathspecs on all git operations.

Frozen: 2026-10-02. Amending this prereg after results requires a
transparent amendment and a fresh freeze; silently moved bars void
the verdict.
