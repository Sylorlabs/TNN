from pathlib import Path
import json,re,hashlib
src=Path('/mnt/data/tnn-r31-endogenous-chunking/tnn_r31_endogenous_chunking.zag').read_text()
low=src.lower()
checks={
 'graph_free': not any(x in low for x in ['graph','adjacency']),
 'no_transformer_language_model': not any(x in low for x in ['transformer','tokenizer','next-token','bpe']),
 'repeated_span_recruitment':'r31_proposal_observe' in src and 'r31_observe_stream' in src,
 'reversible_segmentation':'r31_segment' in src and 'r31_reconstruct' in src,
 'literal_fallback':'out_id[nout]=-1-seq[pos]' in src,
 'grounded_utility':'r31_grounded_consistency' in src,
 'delayed_regret':'r31_chunk_regret_update' in src,
 'hierarchical_recurrence':'r31_pair_observe' in src,
 'alignment_after_chunks':'r31_alignment_cost' in src,
 'structured_chunk_evidence':'r31_chunk_signature' in src and 'r31_signature_distance' in src,
 'support_gap_recruitment':'r31_largest_support_gap' in src and 'r31_support_gap_choose' in src,
 'regime_consequence_memory':'r31_regime_predict' in src and 'r31_regime_choose' in src,
 'learned_reinspection_value':'r31_reinspection_value' in src and 'r31_reinspection_regret_update' in src,
 'extreme_score_gate':'r31_extreme_score_gate' in src,
 'episodic_core':'episod' in low,
 'memory_authority':'memory_policy_choose' in src,
 'causal_trace':'trace_emit' in src,
}
out={'pass':all(checks.values()),'checks':checks,'source_sha256':hashlib.sha256(src.encode()).hexdigest(),'lines':len(src.splitlines())}
Path('/mnt/data/tnn-r31-endogenous-chunking/results/source_contract.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
