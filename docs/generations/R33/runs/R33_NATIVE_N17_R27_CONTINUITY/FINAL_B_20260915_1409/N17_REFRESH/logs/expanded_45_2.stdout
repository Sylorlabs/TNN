from pathlib import Path
import json,hashlib
p=Path('/mnt/data/r32_epistemic/tnn_r32_epistemic_chunking.zag');s=p.read_text();low=s.lower()
checks={
 'no_transformer':all(x not in low for x in ['transformer','tokenizer','next-token',' bpe']),
 'no_vad_mechanism':all(x not in low for x in ['fn vad_', 'voice_activity_detector', 'vad_boundary_input']),
 'endogenous_chunks':'r31_observe_stream' in s and 'r31_segment' in s,
 'raw_dual_route':'r31_dual_evidence_score' in s and 'r31_should_retrieve_raw' in s,
 'epistemic_population':'r32_hyp_observe' in s and 'r32_unresolved_index' in s,
 'source_dependence':'r32_evidence_dependence' in s and 'r32_group_evidence_score' in s,
 'elastic_temporal':'r32_elastic_temporal_accumulate' in s and 'r32_relative_time_bin' in s,
 'surprise_segments':'r32_transition_surprise' in s and 'r32_surprise_boundary_candidate' in s,
 'observational_equivalence':'r32_best_affordable_separation' in s and 'r32_equivalence_decide' in s,
 'delayed_regret':'r32_equivalence_regret_update' in s and 'r32_commit_regret_update' in s,
 'causal_trace':'trace_emit' in s,
 'memory_authority':'memory_policy_choose' in s,
}
out={'pass':all(checks.values()),'checks':checks,'sha256':hashlib.sha256(s.encode()).hexdigest(),'lines':len(s.splitlines())}
Path('/mnt/data/r32_epistemic/R32_SOURCE_CONTRACT_V7.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
