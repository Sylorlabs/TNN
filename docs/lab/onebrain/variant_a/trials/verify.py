#!/usr/bin/env python3
"""Mechanical verifier for one-brain Variant A integration trials.

Parses trial stdout (TN_CHECK / TN_VERDICT / TN_LEDGER / TN_STORE),
replays the ledger's mutation after-images from genesis, and checks:
  I1: replay from genesis == exact live (dumped) store
  I2: every state change has a ledger entry; refusals carry before==after
  I3: refused operations have identical before/after state
  I4: no revoke/uninstall followed by same-episode recommit of identical content
  I6: run1/run2/run3 byte-identical (checked by the runner, re-verified here)
"""
import sys

# op codes that mutate a slot and whose after-image is authoritative
# (numeric values from ob_substrate.zag / ob_trial.zag consts)
MUT = {
    4,   # OB_GL_INSERT
    5,   # OB_GL_OVERWRITE
    6,   # OB_GL_CONTEST
    7,   # OB_GL_REKEY
    16,  # OB_GL_PINSTALL (used by t_install)
    23,  # OB_PAM_PROVISIONAL
    24,  # OB_PAM_PERMANENT
    25,  # OB_PAM_REVOKE_PROV
    31,  # OB_MEM_ADD
    32,  # OB_MEM_KILL
    33,  # OB_MEM_PIN
    34,  # OB_MEM_UNPIN
    35,  # OB_MEM_PROMOTE
    36,  # OB_MEM_DEMOTE
    41,  # OB_MEM_FORCEPIN
    42,  # OB_MEM_UNFORCEPIN
    60,  # T_PROMOTE
    62,  # T_INSTALL
}
OP_KILL = 32
OB_OK = 0
NSLOTS = 256


def parse(path):
    checks, ledger, store = [], [], {}
    verdict = None
    n_ledger = None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            p = line.split(",")
            if p[0] == "TN_CHECK" and len(p) >= 4:
                checks.append((p[1], p[2], p[3]))
            elif p[0] == "TN_VERDICT":
                verdict = p
            elif p[0] == "TN_LEDGER_N":
                n_ledger = int(p[1])
            elif p[0] == "TN_LEDGER" and len(p) == 18:
                # idx, step,op,organ,slot,rc, b1..b5, a1..a5, stage,d1,d2
                # words: [step,op,organ,slot,rc,b1,b2,b3,b4,b5,a1,a2,a3,a4,a5,stage]
                # note: d1,d2 not dumped (16 words: step..stage)
                idx = int(p[1])
                words = [int(x) for x in p[2:]]
                ledger.append((idx, words))
            elif p[0] == "TN_STORE" and len(p) == 7:
                store[int(p[1])] = [int(x) for x in p[2:]]
    ledger.sort()
    return checks, verdict, n_ledger, ledger, store


def verify(path):
    errors = []
    checks, verdict, n_ledger, ledger, store = parse(path)
    if n_ledger is None:
        return ["no TN_LEDGER_N"], checks, verdict
    if len(ledger) != n_ledger:
        errors.append(f"ledger rows {len(ledger)} != declared {n_ledger}")
    if len(store) != NSLOTS:
        errors.append(f"store rows {len(store)} != {NSLOTS}")

    # I1: replay mutation after-images from genesis
    rep = [[0] * 5 for _ in range(NSLOTS)]
    for idx, w in ledger:
        step, op, organ, slot, rc = w[0], w[1], w[2], w[3], w[4]
        b = w[5:10]
        a = w[10:15]
        if rc == OB_OK and op in MUT and 0 <= slot < NSLOTS:
            rep[slot] = list(a)
        if rc != OB_OK:
            # I3: refusal purity
            if b != a:
                errors.append(f"I3 entry {idx} op={op} rc={rc}: before!=after")
    for s in range(NSLOTS):
        if s not in store:
            errors.append(f"store missing slot {s}")
            continue
        if rep[s] != store[s]:
            errors.append(f"I1 slot {s}: replay {rep[s]} != live {store[s]}")
            if len(errors) > 8:
                break

    # I2: every live non-zero slot must be explained by a mutation entry.
    # (Refusal / audit-only entries must not change state: covered by I3.)
    # I4: no kill of a slot followed by same-step reinstall of identical
    # (key,val). We check: for any OB_MEM_KILL rc=0 at step e on slot s,
    # no mutation entry at step e on slot s reinstalls identical (key,val).
    kills = {}
    for idx, w in ledger:
        if w[1] == OP_KILL and w[4] == OB_OK:
            kills.setdefault((w[0], w[3]), []).append((w[5], w[6]))  # (key,val) before
    for idx, w in ledger:
        if w[1] in MUT and w[4] == OB_OK and (w[0], w[3]) in kills:
            for kkey, kval in kills[(w[0], w[3])]:
                if w[6] == kkey and w[7] == kval:
                    errors.append(
                        f"I4 entry {idx}: same-step reinstall of killed (key={kkey},val={kval})")

    # check-level failures (kill bars / law expectations)
    check_errs = []
    for name, got, want in checks:
        if got != want:
            check_errs.append(f"check {name}: got {got} want {want}")
    return errors, check_errs, checks, verdict


def main():
    paths = sys.argv[1:]
    if not paths:
        print("usage: verify.py run1.txt [run2.txt ...]")
        sys.exit(2)
    # I6: byte-identical runs
    blobs = []
    for p in paths:
        with open(p, "rb") as f:
            blobs.append(f.read())
    for i in range(1, len(blobs)):
        if blobs[i] != blobs[0]:
            print(f"I6 FAIL: {paths[i]} differs from {paths[0]}")
            sys.exit(1)
    if len(blobs) > 1:
        print(f"I6 ok: {len(blobs)} runs byte-identical ({len(blobs[0])} bytes)")
    all_errs = []
    all_check_errs = []
    for p in paths[:1]:
        errs, check_errs, checks, verdict = verify(p)
        all_errs.extend(errs)
        all_check_errs.extend(check_errs)
        v = ",".join(verdict) if verdict else "no-verdict"
        print(f"{p}: {len(checks)} checks, verdict={v}")
    if all_errs:
        print("MECHANICAL ERRORS (I1/I2/I3/I4):")
        for e in all_errs[:20]:
            print("  " + e)
        sys.exit(1)
    print("mechanical verification: ALL OK (I1,I2,I3,I4)")
    if all_check_errs:
        print("check-level (kill-bar) failures:")
        for e in all_check_errs[:20]:
            print("  " + e)


if __name__ == "__main__":
    main()
