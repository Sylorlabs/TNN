#!/usr/bin/env python3
"""verify_critic.py — independent mechanical oracle for the self-critique leg.
Checks structural properties only: hole count, ranking order, test lengths,
manifest agreement, CRITIC_DONE, and 5/5 md5-identical logs. It does NOT
re-derive the suspicions — that is the binary's job (limitation documented
in PREREG.md)."""
import re, sys, hashlib, glob

def fail(msg):
    print("ORACLE_FAIL:", msg); sys.exit(1)

logs = sorted(glob.glob("runs/critic_r*.log"))
if len(logs) != 5: fail(f"expected 5 run logs, found {len(logs)}")
md5s = set()
for p in logs:
    md5s.add(hashlib.md5(open(p, "rb").read()).hexdigest())
if len(md5s) != 1: fail(f"logs not byte-identical: {md5s}")
print("ORACLE: 5/5 byte-identical", list(md5s)[0][:12])

text = open(logs[0]).read()
holes = re.findall(r'CRITIC_HOLE,rank=(\d+),id=(\d+),severity=(\d+),title="([^"]*)",evidence="([^"]*)",test="([^"]*)"', text)
if len(holes) != 8: fail(f"expected 8 holes, found {len(holes)}")
print("ORACLE: 8 holes emitted")

for rank, hid, sev, title, ev, test in holes:
    if len(test) < 20: fail(f"hole id={hid}: test too short ({len(test)} chars)")
    if not title or not ev: fail(f"hole id={hid}: empty title/evidence")
print("ORACLE: all holes carry title, evidence, test>=20 chars")

order = [(int(s), int(i)) for _, i, s, _, _, _ in holes]
expect = sorted(order, key=lambda t: (-t[0], t[1]))
if order != expect: fail(f"ranking wrong: got {order}, want {expect}")
print("ORACLE: ranking is severity-desc, id-asc", order)

ranks = [int(r) for r, _, _, _, _, _ in holes]
if ranks != list(range(8)): fail(f"ranks not 0..7: {ranks}")

m = re.search(r"CRITIC_MANIFEST,holes=(\d+)", text)
if not m or int(m.group(1)) != 8: fail("manifest holes!=8")
if "CRITIC_BLOCKED" in text: fail("CRITIC_BLOCKED emitted")
if "CRITIC_DONE" not in text: fail("CRITIC_DONE missing")
if "CRITIC_DIGEST,fnv1a=" not in text: fail("digest missing")
print("ORACLE: manifest=8, no BLOCKED, DONE present")
print("ORACLE_PASS: all mechanical checks green")
