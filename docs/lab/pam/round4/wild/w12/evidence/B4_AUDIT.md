# B4 construction audit (score_w12.py, pre-battery)

Claim: the driver routes QUARANTINE verdicts to a review log; NOTHING in the driver admits from quarantine.

Every source line mentioning quarantine:
```
                    rows.append((i, 'QUARANTINE', pr, dc)); eq += 1; nquar += 1
    summary = dict(ncand=len(cands), admit=nadmit, quarantine=nquar,
          f"quarantine={got_sum['quarantine']} bar_reject={got_sum['bar_reject']} "
                 if v == 'QUARANTINE' and i not in wrong)
        # kill condition: target quarantined while >=1 junk admitted in an
        tquar = any(v == 'QUARANTINE' for (_, v, _, _) in t)
        print(f'B2: target quarantined={tquar}; '
    # B4: quarantine -> review log; audit: no quarantine->admit path
    qidx = [i for (i, v, pr, dc) in got_rows if v == 'QUARANTINE']
    with open(f'{W12DIR}/evidence/quarantine_review.log', 'w') as f:
            f.write(f'{i}|QUARANTINE|needs deliberative review\n')
    qlines = [ln for ln in src.splitlines() if 'quarantine' in ln.lower()]
    audit.write('Claim: the driver routes QUARANTINE verdicts to a review log; '
                'NOTHING in the driver admits from quarantine.\n\n')
    audit.write('Every source line mentioning quarantine:\n```\n')
    audit.write(f'Structural check: {len(later_admit)} quarantined idx also '
                'assigns ADMIT from quarantine.\n')
    print(f'B4: {len(qidx)} quarantined -> evidence/quarantine_review.log; '
          f'quarantined-then-admitted: {len(later_admit)}; audit -> B4_AUDIT.md')
```

Structural check: 0 quarantined idx also ADMITTED in instrument output (must be 0).
The review-log writer only reads verdicts; no code path assigns ADMIT from quarantine.
