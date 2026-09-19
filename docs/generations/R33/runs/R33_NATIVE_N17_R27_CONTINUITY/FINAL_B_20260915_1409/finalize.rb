require 'json';require 'digest';require 'fileutils'
repo='/Users/Shared/micah/Documents/TNN/TNN';dest=File.expand_path(__dir__);base=File.dirname(dest)
rel='FINAL_B_20260915_1409'
json=lambda{|p|JSON.parse(File.read(p))}
hash=lambda{|p|Digest::SHA256.file(p).hexdigest}
write=lambda{|p,j|File.write(p,JSON.pretty_generate(j)+"\n")}
%w[commands policy_commands fused_commands continuity_commands].each do |name|
 rows=File.readlines(dest+'/native/'+name+'.jsonl').map{|l|JSON.parse(l)}
 raise name unless rows.all?{|r|r['exit']==r['expected']}
end
raise 'fused incomplete' unless File.exist?(dest+'/native/logs/r27_fused.stdout')
raise 'continuity incomplete' unless File.exist?(dest+'/native/logs/v91_targets.stdout')
raise 'V91 incomplete' unless File.exist?(dest+'/V91/structured_record.json') || File.readlines(dest+'/V91/commands.tsv').last.start_with?('serialize_record')
prior=dest+'/prior_status';FileUtils.mkdir_p(prior)
editable=%w[STATUS.json EVIDENCE_REGISTER.json VERIFIER_CHECK_MATRIX_V3.json R26_VERIFIER_CHECK_MATRIX_V1.json VERIFIER_CHECK_MATRIX_V2.json R25_LINEAGE_RECORD.json PARENT_TYPE_INVENTORY.json VERIFY_CONTRACT.md PARENT_RUNTIME_BOUNDARY.md]
editable.each{|n|FileUtils.cp(base+'/'+n,prior+'/'+n)}
FileUtils.cp(base+'/V91_SEMANTIC_KAT/V91_STATUS.md',prior+'/V91_STATUS.md')
provenance=[]
Dir[dest+'/native/*.provenance'].each do |file|
 File.readlines(file,chomp:true).each do |line|
  kind,h,path=line.split("\t");next unless kind=='FILE'
  raise 'source changed '+path unless hash.call(path)==h
  target=dest+'/native/import_closure/'+path
  FileUtils.mkdir_p(File.dirname(target));FileUtils.cp(path,target)
  provenance<<{source:path,sha256:h,frozen_copy:target}
 end
end
write.call(dest+'/native/IMPORT_CLOSURE.json',provenance.uniq)
required_documents=(Dir[base+'/*.json']+Dir[base+'/*.md']+Dir[base+'/SOURCE_REFERENCES/*']+Dir[base+'/RECOVERY_20260915_B_INDEPENDENT/*.{json,txt,zag}']+Dir[base+'/V91_SEMANTIC_KAT/*.{zag,md,zsh}']+Dir[base+'/RECOVERY_20260915_B_INDEPENDENT/TERMINAL_SUPPLEMENT_20260915/*.{json,txt}']).select{|p|File.file?(p)}
write.call(dest+'/READ_INPUT_REGISTER.json',required_documents.map{|p|{path:p,sha256:hash.call(p),bytes:File.size(p),role:'Read-only specification/provenance input at final audit; retained metrics are witnesses.'}})
terminal=base+'/RECOVERY_20260915_B_INDEPENDENT/TERMINAL_SUPPLEMENT_20260915/COMPATIBILITY_CORRECTION_20260915/FINAL_TERMINAL_REVIEW.json'
blocked=json.call(terminal)['reviewed_rows'].map{|r|[r['id'],r]}.to_h
review=base+'/RECOVERY_20260915_B_INDEPENDENT/REVIEW.json'
static={}
%w[rows structure policy].each do |n|
 File.readlines(dest+'/native/logs/'+n+'.stdout',chomp:true).each do |line|
  fields=line.split(',');next unless fields[0]=='B_ROW'
  raise line unless fields[2]=='PASS'
  static[fields[1]]={log:rel+'/native/logs/'+n+'.stdout',stdout_sha256:hash.call(dest+'/native/logs/'+n+'.stdout'),native_record:fields}
 end
end
raise static.size.to_s unless static.size==47
%w[R27-05 R27-07 R26-03].zip(%w[r27_digest r26_digest r26_digest]).each{|id,n|static[id]={log:rel+'/native/logs/'+n+'.stdout',stdout_sha256:hash.call(dest+'/native/logs/'+n+'.stdout'),scope:'Native preimage reconstruction and comparison to recorded digest witness; no scientific rerun or standalone release-summary admission.'}}
accepted=%w[R27-01 R27-18 R26-01 R26-34]
rows=[]
%w[VERIFIER_CHECK_MATRIX_V3.json R26_VERIFIER_CHECK_MATRIX_V1.json].each do |n|
 matrix=json.call(base+'/'+n)
 matrix['rows'].each do |row|
  id=row['id'];entry={id:id,source_line:row['line'],condition:row['condition'],name:row['name'],required:true}
  if static.key?(id)
   entry.merge!({classification:'DIRECT_NATIVE_RECOMPUTATION',disposition:'PASS_FRESH_NATIVE_STATIC_SCOPE',evidence:static[id],review_status:'Existing native static scope retained; new native policy parser is author-verified, independent adapter review pending.'})
   row['class']=entry[:classification];row['status']=entry[:disposition];row.delete('minimal_blocker')
  elsif accepted.include?(id)
   entry.merge!({classification:'NATIVE_EQUIVALENT_REQUIRES_REVIEW',disposition:'PASS_REVIEWED_NATIVE_ENGINEERING_EQUIVALENT',evidence:{log:rel+'/native/logs/identity.stdout',stdout_sha256:hash.call(dest+'/native/logs/identity.stdout'),accepted_independent_review:review,review_sha256:hash.call(review)},review_status:'Independent review accepted the stipulated inert identity/exact-class equivalent; implementation freshly reexecuted. No live historical object behavior claimed.'})
   row['class']=entry[:classification];row['status']=entry[:disposition];row.delete('minimal_blocker')
  else
   b=blocked.fetch(id)
   entry.merge!({classification:id=='R26-46' ? 'HISTORICAL_WITNESS_ONLY' : 'DEFERRED_BLOCKER',disposition:'FAIL_CLOSED_REVIEW_COMPLETED_INPUT_OR_IMPLEMENTATION_BLOCKED',blocker:b['blocker'],reason:b['reason'],closure_requires:b['closure_requires'],required_member:b['required_member'],known_sha256:b['known_sha256'],known_byte_length:b['known_byte_length'],review_status:'COMPLETED_WITH_FAIL_CLOSED_ACCEPTANCE',review_record:terminal,review_sha256:hash.call(terminal)})
   row['class']=entry[:classification];row['status']=entry[:disposition];row['minimal_blocker']=entry[:blocker]
  end
  row['final_b_evidence']=rel+'/ROWS.json';rows<<entry
 end
 matrix['native_pass_count']=matrix['rows'].count{|r|r['status'].start_with?('PASS')}
 matrix['unresolved_required_row_count']=matrix['rows'].size-matrix['native_pass_count']
 matrix['status']='FRESH_NATIVE_STATIC_AND_REVIEWED_ENGINEERING_EQUIVALENTS_FULL_VERIFIER_FAIL_CLOSED'
 matrix['final_b_audit']={record:rel+'/FINAL.json',source_row_accounting_only:true,full_runtime_qualified:false}
 write.call(base+'/'+n,matrix)
end
raise 'accounting' unless rows.size==80&&rows.count{|r|r[:disposition].start_with?('PASS')}==54&&rows.count{|r|r[:disposition].start_with?('FAIL')}==26
write.call(dest+'/ROWS.json',{schema:'R33_N17_80_SOURCE_ROWS_FINAL_B_V1',source_basis:'Historical matrices are specification witnesses. New disposition comes from fresh native output or accepted independent native-equivalent review plus fresh replay.',rows:rows,counts:{required:80,direct_native_static:50,reviewed_native_engineering_equivalents:4,blocked:26,r27_pass:28,r27_blocked:5,r26_pass:26,r26_blocked:21,full_runtime_qualified:false}})
v2=json.call(base+'/VERIFIER_CHECK_MATRIX_V2.json');v2['rows'].each do |r|
 refs=r['exact_v3_source_rows']||[];next if refs.empty?
 matches=rows.select{|x|refs.include?(x[:id])}
 r['final_b_disposition']=matches.map{|x|{id:x[:id],disposition:x[:disposition]}}
 if matches.all?{|x|x[:disposition].start_with?('PASS')}
  r['status']='SUPERSEDED_COARSE_ROW_ALL_REFERENCED_EXACT_ROWS_HAVE_NATIVE_ENGINEERING_PASS';r.delete('minimal_blocker')
 end
end
v2['status']='SUPERSEDED_COARSE_SCOPE_SEE_FINAL_B_80_SOURCE_ROWS';v2['final_b_audit']=rel+'/ROWS.json';write.call(base+'/VERIFIER_CHECK_MATRIX_V2.json',v2)
search=json.call(dest+'/recovery/SEARCH.json');git=json.call(dest+'/recovery/GIT_ALL_BLOB_HASHES.json')
summary={identity:'R33_N17_LANE_B_FINAL_LOCAL_EVIDENCE_CLOSEOUT',status:'LOCAL_ENGINEERING_AUDIT_FINISHED_V91_GENERATION_AND_FULL_CONTINUITY_BLOCKED',full_verifier_equivalent_continuity:'FAIL_CLOSED',r25_lineage:'FAIL_CLOSED_EXACT_INPUTS_SOURCE_BINDINGS_AND_NATIVE_LINEAGE_SUITE_MISSING',rows_record:rel+'/ROWS.json',counts:{direct_native_static_pass:50,reviewed_native_equivalent_pass:4,source_row_deficits:26,r27_deficits:5,r26_deficits:21,v91_generator_parity_deficits:1,audited_row_plus_v91_deficits:27},v91:{actual_native_generated_strings:0,oracle_custody_matches:16,intended_four_field_bindings:16,full_42_dimensional_condition_vectors:'UNADMITTED',authored_dataset_order_matches:0,author_reconstruction_exit:1,gate_exit:91,oracle_frame_sha256:hash.call(dest+'/V91/inputs/oracle.framed.bin'),bpe_frame_sha256:hash.call(dest+'/V91/inputs/bpe.framed.bin'),evidence:rel+'/V91',why_not_implemented:'Exact dataset/BPE special-token/input assembly/forward/dtype/temperature/stopping/seeded sampler definitions absent from searched local evidence; no oracle lookup or fitted reconstruction substitutes for inference.'},digests:{r26:'44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649',r27:'562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04',r26_preimage_bytes:391221,r27_preimage_bytes:17764,original_tools_freshly_rebuilt:true,fused_native_dependency_pass:true,fused_adapter_review:'AUTHOR_VERIFIED_NOT_INDEPENDENTLY_REVIEWED',fused_adaptation:rel+'/FUSED_SOURCE_ADAPTATION.json'},search:{local_paths:search['file_count'],archives:search['archives'].size,all_git_blobs:git['blob_count'],all_git_blob_bytes:git['total_bytes'],exact_missing_input_matches:0,records:[rel+'/recovery/SEARCH.json',rel+'/recovery/GIT_ALL_BLOB_HASHES.json'],scope_exclusions:['Other machine directories retain prior terminal-review search scope; not newly exhaustively searched.','Arbitrary renamed payloads or recursively embedded archives are not proven absent.','Media from early releases exists; exact original R26 artifact selector/hash/decode semantics are unbound.']},independent_review:{four_equivalents_accepted:true,remaining_26_blockers_review_completed:true,new_adapters_review_pending:true,full_closure_acceptance:false},scope_exclusions:['Stored experimental metrics/decisions were inspected, not regenerated.','Historical receipts and prior source/hash records are witnesses only.','No full 20-fixture mutation suite, complete R25 lineage suite, historical forward/smoke/video/name-memory/abstraction behavior qualification.','Native inert graph predicates do not execute historical objects.','Row+V91 deficit count excludes separate fixture/freeze/preregistration/admission requirements and adapter review; it is not an authorization ladder count.','Existing bounded source-specific scalar lexemes/accepted-parent selectors remain; no universal JSON or historical numeric runtime certification.'],canonical:{raw_sha256:'31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a',map_manifest_sha256:'b7c083364e98d9e5cd674a47b0136de157fedd538b06c743f0c672652984327f',development_step:60423,newborn_restarts:0,mutated:false},authority:{learn_opened:false,learner_authority:false,scientific_exposure:0,promotion:false},execution:{native_zag_engineering_only:true,compiler_replaced:false,python:false,pytorch:false,numpy_runtime:false,pickle_or_reducer:false,foreign_ml:false,forbidden_git_mutations:false},remaining_source_rows:rows.select{|r|r[:disposition].start_with?('FAIL')}.map{|r|r[:id]}}
write.call(dest+'/FINAL.json',summary)
status=json.call(base+'/STATUS.json');status['status']='FRESH_NATIVE_54_ENGINEERING_ROWS_PASS_26_SOURCE_ROWS_AND_V91_GENERATION_FAIL_CLOSED'
status['remaining_blockers']=['5 R27 source rows: 06,08,09,32,33','21 R26 source rows: 06-09,16-22,38-47','V91 native generation: exact method/source/42-D condition inputs absent; zero generated outputs']
status['next_action']='Recover/admit exact source/input bundles and implement reviewed behavior/lineage equivalents for the 26 blocked rows and V91 generation. New fused/policy adapters still require independent review; fixture/freeze/admission gates remain closed.'
status['r25_lineage_status']='FAIL_CLOSED_EXACT_INPUTS_BINDINGS_AND_NATIVE_LINEAGE_SUITE_MISSING_COMPATIBILITY_IMPORT_FIXED'
status['latest_review_record']='RECOVERY_20260915_B_INDEPENDENT/TERMINAL_SUPPLEMENT_20260915/COMPATIBILITY_CORRECTION_20260915/FINAL_TERMINAL_REVIEW.json'
status['final_b_closeout']={record:rel+'/FINAL.json',row_classifications:rel+'/ROWS.json',direct_native_static_passes:50,reviewed_native_equivalent_passes:4,unresolved_source_rows:26,v91_generated_outputs:0,row_plus_v91_deficits:27,full_closure_acceptance:false}
status['lane_b_audit']['role']='HISTORICAL_PRIOR_AUDIT_COUNTS_SUPERSEDED_BY_FINAL_B';status['integrated_closeout']['role']='HISTORICAL_PRIOR_INTEGRATED_RECEIPT_NOT_CURRENT_ACCOUNTING'
write.call(base+'/STATUS.json',status)
lineage=json.call(base+'/R25_LINEAGE_RECORD.json');lineage['status']='FAIL_CLOSED_EXACT_EXECUTION_INPUTS_BINDINGS_AND_COMPLETE_NATIVE_LINEAGE_MISSING'
lineage['final_b_audit']={record:rel+'/FINAL.json',compatibility_import_and_numeric_constant_gap:'CLOSED_FOR_REVIEWED_ISOLATED_COMPATIBILITY_SOURCES_FRESH_REBUILD_PASS',native_r25_digest_closed:false,native_r25_lineage_closed:false,actual_input_bundle_absent_in_search_scope:true,source_bundle_identities:rel+'/recovery/SEARCH.json'}
lineage['lane_b_audit']['minimal_compile_blocker']='HISTORICAL_SUPERSEDED: isolated reviewed compatibility correction fixes import/constant gap; fresh corrected runner rebuild passes. Original runner source preserved.'
write.call(base+'/R25_LINEAGE_RECORD.json',lineage)
inventory=json.call(base+'/PARENT_TYPE_INVENTORY.json');inventory['entries'].each do |e|
 if e['id']=='R27.semantic-generator'
  e['status']='REVIEWED_NATIVE_MEMO_IDENTITY_PASS_V91_INFERENCE_PARITY_BLOCKED'
 elsif e['id']=='R25.lineage'
  e['status']='FAIL_CLOSED_EXACT_INPUTS_BINDINGS_AND_NATIVE_LINEAGE_SUITE_MISSING_COMPATIBILITY_IMPORT_FIXED'
 end
end
inventory['final_b_audit']={record:rel+'/FINAL.json',inert_identity_and_exact_class_equivalents_reviewed:true,historical_runtime_behavior_qualified:false};write.call(base+'/PARENT_TYPE_INVENTORY.json',inventory)
register=json.call(base+'/EVIDENCE_REGISTER.json');register['status']='FRESH_NATIVE_54_ENGINEERING_ROW_PASSES_FULL_CONTINUITY_FAIL_CLOSED'
register['final_b_evidence']={record:rel+'/FINAL.json',rows:rel+'/ROWS.json',commands:Dir[dest+'/native/*commands.jsonl'].map{|p|p.delete_prefix(base+'/')},direct_native_static_pass_count:50,reviewed_native_equivalent_pass_count:4,blocked_source_rows:26,generated_strings:0}
register['missing_or_unqualified_inputs'].each{|e|e['status']='EXACT_80_ROWS_ACCOUNTED_54_ENGINEERING_PASSES_26_REVIEWED_BLOCKED' if e['id']=='exact-verifier-accounting'}
register['implementation_decision']['reason']='Fresh native digest/static checks and four reviewed inert identity/class equivalents pass; exact behavioral/source/policy/manifest/R25 lineage/V91 generation deficits remain. New fused digest/policy adapters are author-verified only.'
write.call(base+'/EVIDENCE_REGISTER.json',register)
%w[VERIFY_CONTRACT.md PARENT_RUNTIME_BOUNDARY.md].each do |n|
 File.open(base+'/'+n,'a'){|f|f.puts "\n2026-09-15 final Lane B correction: `#{rel}/ROWS.json` now accounts for all 80 source rows: 50 fresh native static passes, four independently reviewed native inert identity/exact-class equivalents freshly replayed, and 26 reviewed fail-closed source rows (R27 5; R26 21). V91 custody matches all 16 oracle strings but native inference generated zero strings; exact method/input bindings remain absent. Stable compiler rebuilds pass. Reviewed isolated R25 compatibility import/constant/allocator correction passes fresh native tests, while actual exact inputs and complete lineage remain blocked. New native policy parser and fused digest adapter are author-verified; independent adapter review pending. Earlier counts/import/compiler blockers above are historical and superseded for this narrow scope. No full continuity, learn, authority, exposure or promotion. See `#{rel}/FINAL.json`."}
end
File.open(base+'/V91_SEMANTIC_KAT/V91_STATUS.md','a'){|f|f.puts "\nFresh final Lane B native replay: `../#{rel}/V91/commands.tsv` and `../#{rel}/native/continuity_commands.jsonl`. All stable compiler builds pass. Oracle custody 16/16, retained tensor/BPE/interpreter equality and intended four-field bindings pass; 42-D vectors remain unadmitted. Authored dataset/order still matches 0/16 (exit 1); native generated strings remain zero and gate exit 91/CLOSED. Repository/Zag search: 31,136 paths, 27 archives, and all 1,610 Git blobs (744,029,506 bytes) hashed; no exact missing R23 source/state/summary found within recorded scope. Actual seeded generation was not implemented because exact methods/inputs are absent. No extracted oracle or expected-output shortcut is claimed as generation. See `../#{rel}/FINAL.json` for exact blockers and exclusions."}
write.call(dest+'/INITIAL_HARNESS_FAILURE.json',{argv:['ruby',rel+'/git_deep.rb'],exit:1,error:'Ruby installed version lacks Array#filter_map; replaced metadata helper with map.compact.',scope:'Orchestration error before Git blob streaming; not a native qualifier failure or scientific execution.'})
puts JSON.generate(summary[:counts])
