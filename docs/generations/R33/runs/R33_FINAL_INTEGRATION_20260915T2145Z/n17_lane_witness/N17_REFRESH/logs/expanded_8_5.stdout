#!/usr/bin/env python3
from pathlib import Path
import re,json,hashlib,sys
p=Path(sys.argv[1]);s=p.read_text(); code='\n'.join(x.split('//')[0] for x in s.splitlines())
checks={
 'balanced_braces':s.count('{')==s.count('}'),
 'graph_runtime_absent':not re.search(r'\b(graph|adjacency)\b',code,re.I),
 'graph_node_edge_absent':not re.search(r'\b(node|edge)\b',code,re.I),
 'aeif_present':'aeif' in s.lower() or 'associative' in s.lower(),
 'episodes_present':'episode' in s.lower(),
 'memory_default_override':'memory_policy_choose' in s and 'default_action' in s,
 'lru_not_authority':'lru_representation_authority' in s,
 'ctc_core_present':'ctc_collapse' in s and 'ctc_forward_score' in s,
 'ctc_no_vad':'no VAD' in s or 'no_vad' in s.lower() or 'without supplied VAD' in s,
 'extreme_gate_present':'suspicious_extreme' in s,
 'trace_parent_links':'t_parent' in s or 'parent_event' in s,
 'foundry_present':'foundry_' in s,
 'newborn_restart_metric':'newborn_restarts' in s,
}
out={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'lines':len(s.splitlines())}
print(json.dumps(out,indent=2));sys.exit(0 if out['status']=='PASS' else 1)
