require 'json';require 'digest'
dest=File.expand_path(__dir__);base=File.dirname(dest);rel='FINAL_B_20260915_1409'
edit=lambda do |p,&block|
 j=JSON.parse(File.read(p));block.call(j);File.write(p,JSON.pretty_generate(j)+"\n")
end
%w[VERIFIER_CHECK_MATRIX_V3.json R26_VERIFIER_CHECK_MATRIX_V1.json].each do |n|
 edit.call(base+'/'+n) do |j|
  j['native_pass_count_rule']='Engineering row count includes fresh direct static native checks/digests and four independently accepted inert identity/exact-class equivalents freshly reexecuted. No experimental metric rerun, live historical runtime, receipt replay or full continuity qualification is inferred.'
  j['lane_b_audit']['role']='HISTORICAL_PRIOR_AUDIT_SUPERSEDED_FOR_CURRENT_ROW_ACCOUNTING'
  j['final_b_audit']['reviewed_native_equivalent_pass_count']=2
  j['final_b_audit']['independent_review_acceptance']='Existing four-row native engineering review; new policy/fused adapters still await independent review.'
 end
end
edit.call(base+'/VERIFIER_CHECK_MATRIX_V2.json') do |j|
 j['rows'].each do |r|
  next unless r['status'].start_with?('SUPERSEDED_COARSE_ROW_ALL_')
  r['class']=r['final_b_disposition'].any?{|x|x['disposition']=='PASS_REVIEWED_NATIVE_ENGINEERING_EQUIVALENT'} ? 'NATIVE_EQUIVALENT_REQUIRES_REVIEW' : 'DIRECT_NATIVE_RECOMPUTATION'
 end
 j['native_count_rule']='Superseded coarse scope has no independent qualification count. See exact 80-row FINAL_B ROWS.json accounting.'
end
edit.call(base+'/EVIDENCE_REGISTER.json') do |j|
 j['fresh_evidence']['role']='HISTORICAL_PRIOR_AUDIT_SEE_FINAL_B_EVIDENCE'
end
bound=[]
File.readlines(dest+'/V91/logs/oracle.stdout',chomp:true).each do |line|
 m=line.match(/^V91_ORACLE,(\d+),node=(\d+),opcode_offset=(\d+),opcode=(\d+),text_offset=(\d+),bytes=(\d+),sha256=([0-9a-f]{64}),bound_equal=1,text=(.*)$/)
 next unless m
 bound<<{index:m[1].to_i,classification:'DEFERRED_BLOCKER_NATIVE_GENERATION_NOT_IMPLEMENTED',generated:false,oracle:{node:m[2].to_i,opcode_offset:m[3].to_i,opcode:m[4].to_i,text_offset:m[5].to_i,bytes:m[6].to_i,native_sha256:m[7],expected_text:m[8],custody_only:true},input_binding:{meaningful_fields_native_verified:4,full_condition_42_dimensional:'UNADMITTED'},blocker:'Exact frozen generation dataset/BPE special-token/forward/numeric/sampling method and complete condition construction unavailable in recorded local search scope.'}
end
raise 'bound rows' unless bound.size==16&&bound.map{|r|r[:index]}==(0...16).to_a
File.write(dest+'/V91_BOUND_ROWS.json',JSON.pretty_generate({schema:'R33_V91_BOUND_STRING_NATIVE_GENERATION_DEFICITS_V1',oracle_parent:'root.base_state.base_state.r24_state.r23_state.evidence.semantic_generation.examples',raw_parent_sha256:'31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a',oracle_receipt_sha256:Digest::SHA256.file(dest+'/V91/inputs/oracle.framed.bin').hexdigest,actual_native_generated:0,rows:bound})+"\n")
edit.call(dest+'/FINAL.json'){|j|j['v91']['bound_row_classifications']=rel+'/V91_BOUND_ROWS.json'}
