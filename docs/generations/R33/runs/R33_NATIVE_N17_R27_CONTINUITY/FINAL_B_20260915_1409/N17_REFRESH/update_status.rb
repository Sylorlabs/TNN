require 'json'
n='Research/R33_NATIVE_N17_R27_CONTINUITY';e=n+'/FINAL_B_20260915_1409/N17_REFRESH';r=JSON.parse(File.read(e+'/ROW_CLASSIFICATIONS.json'));index=r['rows'].to_h{|x|[x['id'],x]}
write=lambda{|p,j|File.write(p,JSON.pretty_generate(j)+"\n")}
%w[VERIFIER_CHECK_MATRIX_V3.json R26_VERIFIER_CHECK_MATRIX_V1.json].each do |f|
 j=JSON.parse(File.read(n+'/'+f))
 j['rows'].each do |row|
 fresh=index.fetch(row['id']);row['pre_final_b_status']||=row['status'];row['pre_final_b_class']||=row['class']
 row['class']=fresh['class'];row['status']=fresh['status'];row['audit_evidence']=e+'/ROW_CLASSIFICATIONS.json';row['independent_review_absent']=false
 row['fresh_native_evidence']=fresh['fresh_evidence'];row['fresh_native_evidence_sha256']=fresh['fresh_evidence_sha256']
 if fresh['status'].start_with?('FAIL')
 row['minimal_blocker']=fresh['blocker'];row['closure_requires']=fresh['closure_requires']
 else
 row.delete('minimal_blocker');row['claim_boundary']='Fresh native static source-row engineering or independently reviewed inert equivalent only; no whole historical runtime, regenerated metric, scientific qualification or admission.'
 end
 end
 j['status']='FINAL_B_FRESH_NATIVE_ROW_AUDIT_FULL_CONTINUITY_FAIL_CLOSED';j['final_b_evidence']=e+'/ROW_CLASSIFICATIONS.json'
 j['native_count_rule']='Static and reviewed inert-equivalent engineering credit only. Full runtime qualification count remains zero.'
 write.call(n+'/'+f,j)
end
j=JSON.parse(File.read(n+'/VERIFIER_CHECK_MATRIX_V2.json'))
j['status']='SUPERSEDED_COARSE_ACCOUNTING_USE_V3_AND_FINAL_B_NATIVE_ROWS';j['final_b_evidence']=e+'/ROW_CLASSIFICATIONS.json'
j['rows'].each do |row|
 ids=row['exact_v3_source_rows']||[];fresh=ids.map{|id|index[id]}.compact
 next if fresh.empty?
 if fresh.all?{|x|x['status'].start_with?('PASS')}
 row['status']='SUPERSEDED_GROUP_FRESH_ENGINEERING_ONLY';row.delete('minimal_blocker')
 else
 row['status']='SUPERSEDED_GROUP_FAIL_CLOSED';row['minimal_blocker']=fresh.select{|x|x['status'].start_with?('FAIL')}.map{|x|x['blocker']}.join(' | ')
 end
end
write.call(n+'/VERIFIER_CHECK_MATRIX_V2.json',j)
j=JSON.parse(File.read(n+'/STATUS.json'));j['status']='FINAL_B_NATIVE_STATIC_AND_REVIEWED_INERT_EQUIVALENTS_PASS_FULL_VERIFIER_AND_V91_FAIL_CLOSED'
j['next_action']='Recover and admit exact selected release/source/runtime inputs listed in FINAL_B_20260915_1409/N17_REFRESH/ROW_CLASSIFICATIONS.json and V91_REFRESH/RECORD.json; implement only source-bound native behavior/lineage/generation. No learn, learner authority, scientific exposure or promotion.'
j['remaining_blockers']=['5 R27 source rows: 06,08,09,32,33','21 R26 source rows: 06,07,08,09,16,17,18,19,20,21,22,38,39,40,41,42,43,44,45,46,47','V91: zero native generated strings; exact R23 dataset/BPE/forward/generate and precision/sampling semantics remain source-unbound; standalone R23 state and summary identities unavailable']
j['verifier_check_matrix_status']='ALL_33_R27_AND_47_R26_ROWS_FRESH_NATIVE_CLASSIFIED_54_ENGINEERING_PASSES_26_BLOCKED'
j['r25_lineage_status']='FAIL_CLOSED_EXACT_INPUTS_BINDING_AND_FULL_NATIVE_LINEAGE_NOT_QUALIFIED_ISOLATED_COMPATIBILITY_GAPS_REPAIRED'
j['latest_review_record']='RECOVERY_20260915_B_INDEPENDENT/TERMINAL_SUPPLEMENT_20260915/COMPATIBILITY_CORRECTION_20260915/FINAL_TERMINAL_REVIEW.json'
j['independent_terminal_row_review']='COMPLETED_FAIL_CLOSED_NOT_REVIEW_ABSENT'
j['lane_b_final']={'row_record'=>e+'/ROW_CLASSIFICATIONS.json','native_command_and_file_record'=>e+'/EVIDENCE.json','input_admission_record'=>e+'/INPUT_ADMISSIONS_DEEP.json','v91_record'=>n+'/FINAL_B_20260915_1409/V91_REFRESH/RECORD.json','direct_static_passes'=>50,'reviewed_inert_equivalent_passes'=>4,'r27_engineering_passes'=>28,'r26_engineering_passes'=>26,'blocked_source_rows'=>26,'terminal_blocker_count'=>27,'accounting'=>'5 R27 + 21 R26 required source-row deficits + V91 generation parity; independent terminal review is complete. Full runtime/fixture/admission exclusions remain explicit.','full_runtime_qualified_passes'=>0,'canonical_step'=>60423,'newborn_restarts'=>0,'scientific_exposure'=>0,'native_generator_constructed'=>false,'native_generated_strings'=>0,'oracle_strings_custodied'=>16}
write.call(n+'/STATUS.json',j)
j=JSON.parse(File.read(n+'/R25_LINEAGE_RECORD.json'));j['status']='FAIL_CLOSED_EXACT_BUNDLE_SOURCE_BINDINGS_AND_FULL_NATIVE_LINEAGE_UNQUALIFIED'
j['lane_b_audit']['minimal_compile_blocker']='Historical main import issue repaired only in isolated reviewed compatibility sources; final native rebuild/probes pass. No exact-bundle positive digest or lineage pass.'
j['lane_b_audit']['minimal_input_blocker']='Fresh native input-pin comparison over recovered files/archive members finds no exact R25/R23/speech/noise/canonical input bundle; complete source/extraction/retained-object and 68-check lineage bindings remain unqualified.'
j['final_b_evidence']=e+'/EVIDENCE.json';j['final_b_input_admissions']=e+'/INPUT_ADMISSIONS_DEEP.json';write.call(n+'/R25_LINEAGE_RECORD.json',j)
%w[R26_DIGEST_CLOSURE_MATRIX.json R27_DIGEST_CLOSURE_MATRIX.json].each do |f|
 j=JSON.parse(File.read(n+'/'+f));j['final_b_fresh_evidence']=e+'/EVIDENCE.json';j['final_b_scope']='Exact fresh native semantic digest comparison only; release summary bytes, whole verifier, fused dependency service and behavior/admission not qualified.';write.call(n+'/'+f,j)
end
j=JSON.parse(File.read(n+'/EVIDENCE_REGISTER.json'));j['status']='FINAL_B_FRESH_NATIVE_ENGINEERING_54_ROWS_26_BLOCKED_V91_PARITY_FAIL_CLOSED';j['scope']='Native Zag engineering qualification; shell/Ruby/archive/local hashing only orchestrates and inventories bytes, never inference/training or a scientific evaluator.'
j['fresh_evidence']['final_b_record']=e+'/EVIDENCE.json';j['fresh_evidence']['final_b_row_record']=e+'/ROW_CLASSIFICATIONS.json';j['fresh_evidence']['final_b_direct_static_passes']=50;j['fresh_evidence']['final_b_reviewed_inert_equivalent_passes']=4;j['fresh_evidence']['final_b_full_runtime_passes']=0;j['fresh_evidence']['final_b_unresolved_rows']=26
j['missing_or_unqualified_inputs'].each{|x|x['status']='EXACT_80_ROWS_FRESH_CLASSIFIED_26_BLOCKED_TERMINAL_REVIEW_COMPLETE' if x['id']=='exact-verifier-accounting'}
j['implementation_decision']['reason']='Fresh native digests/static rows and four previously independently reviewed inert equivalents pass; exact behavior/source/release/lineage inputs still block full continuity. Nine policy rows now recomputed by hash-bound native parser.'
j['final_b_v91_record']=n+'/FINAL_B_20260915_1409/V91_REFRESH/RECORD.json';write.call(n+'/EVIDENCE_REGISTER.json',j)
puts 'N17 status and matrices updated with explicit narrow scope.'
