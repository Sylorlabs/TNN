#!/usr/bin/env python3
"""vocab_extract.py — build VOCAB.md from planner journals.
Reads DELIBERATED lines (growth winners, extensions, init, caps) and writes
the grown vocabulary table with each action's measured evidence and reason.
Usage: vocab_extract.py <journal> [journal2 ...] > VOCAB.md  (deep run journal first)
"""
import sys, re

FORM = {0: 'vib1 single sine FM', 1: 'vib2 dual sine FM',
        2: 'jitter per-period fmix32', 3: 'contour 16-pt guarded'}

def main():
    actions = {}   # id -> dict
    events = []    # ordered (depth, text)
    for jp in sys.argv[1:]:
        depth = 0
        for line in open(jp):
            line = line.rstrip('\n')
            m = re.match(r'^TARGET (\d+)', line)
            if m: depth = int(m.group(1))
            if 'DELIBERATED vocab_init' in line:
                p = dict(k.split('=', 1) for k in line.split()[2:])
                actions[1] = {'form': FORM[0], 'how': 'init',
                              'reason': p.get('reason', ''),
                              'gain_pm': p.get('gain_pm', ''),
                              'maxcv_pm': p.get('maxcv_pm', ''),
                              'note': 'inherited null hypothesis'}
                events.append((depth, 'init A1'))
            m = re.search(r'DELIBERATED grown action_id=(\d+) winner=H(\d+) amode=(\d+) reason=([^\s]+) pred_err_pm=(\d+) need_pm=(\d+) yield_pm=(\d+)', line)
            if m:
                aid, h, am = int(m.group(1)), int(m.group(2)), int(m.group(3))
                actions[aid] = {'form': FORM.get(am, '?'), 'how': 'grown',
                                'reason': 'winner=H%d argmin-predicted-ERR' % h,
                                'pred_err_pm': m.group(5), 'need_pm': m.group(6),
                                'yield_pm': m.group(7), 'note': m.group(4)}
                events.append((depth, 'grew A%d' % aid))
            m = re.search(r'DELIBERATED extended action_id=(\d+) form=([^\s]+) new_maxcv_pm=(\d+) reason=([^\s]+)', line)
            if m:
                aid = int(m.group(1))
                if aid in actions:
                    actions[aid]['maxcv_pm'] = m.group(3)
                    actions[aid]['note'] = (actions[aid].get('note', '') +
                                            '; extended: ' + m.group(4))
                events.append((depth, 'extended A%d' % aid))
            if 'UNEXPRESSIBLE' in line:
                m2 = re.search(r'need_cv_pm=(\d+) best_yield_pm=(\d+) finding=([^\s]+)', line)
                if m2:
                    events.append((depth, 'UNEXPRESSIBLE need=%s yield=%s %s' %
                                   (m2.group(1), m2.group(2), m2.group(3))))
            if 'VOCAB_FULL' in line:
                events.append((depth, 'VOCAB_FULL'))
            if 'correction-beyond-tracking-frontier' in line:
                events.append((depth, 'R6 correction held (beyond frontier)'))
            if 'depth_capped_at_tracking_frontier' in line:
                events.append((depth, 'R6 plan depth capped at frontier'))
    out = []
    out.append('# VOCAB.md — the grown vocabulary (B-F1 unified planner)')
    out.append('')
    out.append('Actions below are 100% from the planner\'s own measurements.')
    out.append('Each row: the form, how it entered, the DELIBERATED reason,')
    out.append('and the measured numbers that justified it.')
    out.append('')
    out.append('| ID | Form | Entered | Reason | Measured evidence |')
    out.append('|----|------|---------|--------|-------------------|')
    for aid in sorted(actions):
        a = actions[aid]
        ev = '; '.join('%s=%s' % (k, v) for k, v in a.items()
                       if k not in ('form', 'how', 'reason') and v != '')
        out.append('| A%d | %s | %s | %s | %s |' %
                   (aid, a['form'], a['how'], a['reason'], ev))
    out.append('')
    out.append('## Growth timeline (deep run)')
    out.append('')
    for depth, ev in events:
        out.append('- depth %d: %s' % (depth, ev))
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    main()
