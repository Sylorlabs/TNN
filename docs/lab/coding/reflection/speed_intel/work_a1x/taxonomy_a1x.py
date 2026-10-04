#!/usr/bin/env python3
"""A1X failure taxonomy: classify every miss (NEVER item) by family and cause.
Cause model (evidence-backed):
  C1 knowledge-gap: item fires zero predicates at every budget (empty ledger).
     The verdict rule (WITHHOLD iff any non-factual evidence) cannot withhold
     on empty evidence at ANY budget. Sub-causes by family marker gap.
  C2 deliberation-shape failure: ruled out (flat trajectories b2..b32,
     recon outcome-inert, analytic proof).
  C3 verification failure: ruled out (0 vflips; re-derivation provable).
Usage: python3 taxonomy_a1x.py  (run from work_a1x/)
Writes taxonomy_a1x.json + prints tables.
"""
import json
from collections import Counter, defaultdict

FAM_NAMES = ['joke', 'sarcasm', 'hypothetical', 'analogy', 'poetry',
             'counterfactual', 'implicature']

# family id-range mapping per battery: (start, size, name-index)
def fam_of(battery, iid):
    n = int(iid[1:])
    if battery == 'b188':
        return FAM_NAMES[(n - 211) // 20]
    if battery == 'frozen94':
        bounds = [(1, 'joke'), (23, 'sarcasm'), (45, 'hypothetical'),
                  (67, 'analogy'), (89, 'poetry'), (109, 'counterfactual'),
                  (131, 'implicature')]
    else:
        bounds = [(141, 'joke'), (151, 'sarcasm'), (161, 'hypothetical'),
                  (171, 'analogy'), (181, 'poetry'), (191, 'counterfactual'),
                  (201, 'implicature')]
    for start, name in bounds:
        if start <= n < start + 10:
            return name
    return '?'

# what the inventory covers per family vs what the misses use
MARKER_GAP = {
    'joke': 'inventory: 8 fixed absurdity patterns (goldfish filed, toaster+chess, ...). '
            'misses: absurd-but-unlisted situations (router filed for overtime, ...).',
    'sarcasm': 'inventory: POS-word + NEG-situation co-occurrence. '
               'misses: sarcasm without that pairing ("Oh sure, the dog ate my homework").',
    'hypothetical': 'inventory: 5 openers (suppose, hypothetically, what if, imagine if, if dogs could talk). '
                    'misses: other framings (pretend, say, picture, consider, let us say).',
    'analogy': 'inventory: 4 fixed simile phrases (is a drill sergeant, voice is honey, ...). '
               'misses: metaphors outside the four ("The lecture was a slow leak").',
    'poetry': 'inventory: 10 fixed images (moon poured, autumn writes, ...). '
              'misses: lyric language outside the ten ("Rain tattoos the pavement").',
    'counterfactual': 'inventory: 4 frames (if i had, would have, could have, if i were). '
                      'misses: counterfactuals outside the four (inverted "Had they called sooner" IS covered; '
                      'misses use other forms).',
    'implicature': 'inventory: 5 fixed hints (cold in here, trash is getting full, ...). '
                   'misses: indirect requests outside the five ("Your headlights are still on").',
}

def load_items(path):
    raw = json.load(open(path))
    items = raw['items'] if isinstance(raw, dict) else raw
    return {it['id']: it['utterance'] for it in items}

def main():
    batteries = {
        'b188': ('epi/sweep_b188/sweep_b188.json', 'epi/battery_a1x_items.json'),
        'frozen94': ('epi/sweep_frozen94/sweep_frozen94.json', 'epi/items_frozen94.json'),
        'a1r94': ('epi/sweep_a1r94/sweep_a1r94.json', 'epi/items_a1r94.json'),
    }
    taxonomy = {}
    for bname, (sweep_p, items_p) in batteries.items():
        sweep = json.load(open(sweep_p))
        utts = load_items(items_p)
        mecha = json.load(open('mechanism_a1x.json')) if bname == 'b188' else None
        # recompute classes from trajectories for this battery
        trajs = sweep['trajectories']
        def correct(iid, ver):
            if iid.startswith('F'):
                return ver == 'WITHHOLD'
            if iid.startswith('BC'):
                return ver == 'ENDORSE'
            return ver == 'WITHHOLD'
        budgets = sorted(trajs[next(iter(trajs))].keys(), key=lambda b: int(b[1:]))
        misses = [iid for iid, tj in trajs.items()
                  if not any(correct(iid, tj[b]) for b in budgets)]
        # every miss must be a W item (F/BC are 100%)
        assert all(i.startswith('W') for i in misses), misses
        fam_counts = Counter(fam_of(bname, i) for i in misses)
        # cause assignment: C1 for all (empty ledger proven by predictor);
        # C2/C3 cleared with 0
        taxonomy[bname] = {
            'n_misses': len(misses),
            'by_family': dict(fam_counts),
            'cause_counts': {'C1_knowledge_gap': len(misses),
                             'C2_deliberation_shape': 0,
                             'C3_verification': 0},
            'examples': {fam: [ (i, utts[i]) for i in misses if fam_of(bname, i) == fam][:2]
                         for fam in FAM_NAMES},
        }
        print('=== %s: %d misses ===' % (bname, len(misses)))
        for fam in FAM_NAMES:
            ex = taxonomy[bname]['examples'][fam]
            print('  %-14s %2d  e.g. %s: "%s"' %
                  (fam, fam_counts[fam], ex[0][0] if ex else '-', (ex[0][1][:64] if ex else '-')))
    # cross-battery stability of the family profile
    print('\nmiss profile stability (share of misses by family):')
    for fam in FAM_NAMES:
        shares = ['%s %.2f' % (b, taxonomy[b]['by_family'].get(fam, 0) / taxonomy[b]['n_misses'])
                  for b in batteries]
        print('  %-14s %s' % (fam, '  '.join(shares)))
    json.dump({'taxonomy': taxonomy, 'marker_gap': MARKER_GAP},
              open('taxonomy_a1x.json', 'w'), indent=1, sort_keys=True)
    print('\nwrote taxonomy_a1x.json')

if __name__ == '__main__':
    main()
