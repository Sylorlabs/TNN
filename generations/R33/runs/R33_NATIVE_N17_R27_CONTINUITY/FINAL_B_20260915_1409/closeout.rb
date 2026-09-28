require 'json';require 'open3';require 'digest';require 'fileutils'
repo='/Users/Shared/micah/Documents/TNN/TNN';dest=File.expand_path(__dir__);base=File.dirname(dest)
FileUtils.mkdir_p(dest+'/verification')
log=File.open(dest+'/verification/commands.jsonl','wx')
run=lambda do |label,argv|
 out,err,st=Open3.capture3(*argv,chdir:repo)
 File.binwrite(dest+'/verification/'+label+'.stdout',out);File.binwrite(dest+'/verification/'+label+'.stderr',err)
 log.puts(JSON.generate({label:label,argv:argv,cwd:repo,exit:st.exitstatus,stdout_sha256:Digest::SHA256.hexdigest(out),stderr_sha256:Digest::SHA256.hexdigest(err)}));log.flush;raise label unless st.exitstatus==0;puts label+': 0'
end
%w[canonical protected].each{|n|run.call(n,['shasum','-a','256','-c',repo+'/Research/R33_CLOSEOUT_20260915T174458Z/'+n+'.sha256'])}
run.call('diff_check',['git','diff','--check','--','Research/R33_NATIVE_N17_R27_CONTINUITY'])
summary=JSON.parse(File.read(dest+'/FINAL.json'))
raise 'authority' unless summary['authority'].values.all?{|v|v==false||v==0}&&summary['canonical']['mutated']==false&&summary['full_verifier_equivalent_continuity']=='FAIL_CLOSED'
owned=Dir.glob(dest+'/**/*',File::FNM_DOTMATCH).select{|p|File.file?(p)&&!p.start_with?(dest+'/verification/')&&p!=dest+'/SHA256SUMS'}
current=%w[STATUS.json EVIDENCE_REGISTER.json VERIFIER_CHECK_MATRIX_V3.json R26_VERIFIER_CHECK_MATRIX_V1.json VERIFIER_CHECK_MATRIX_V2.json R25_LINEAGE_RECORD.json PARENT_TYPE_INVENTORY.json VERIFY_CONTRACT.md PARENT_RUNTIME_BOUNDARY.md V91_SEMANTIC_KAT/V91_STATUS.md].map{|n|base+'/'+n}
immutable=['/Users/Shared/micah/Documents/zag/znc',repo+'/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl',repo+'/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-policy.json']+Dir[repo+'/Research/R33_NATIVE_N10_RUN_PRIMARY_V1/parent-map/*'].select{|p|File.file?(p)}
paths=(owned+current+immutable).uniq.sort
File.open(dest+'/SHA256SUMS','wx'){|f|paths.each{|p|f.puts(Digest::SHA256.file(p).hexdigest+'  '+p)}}
run.call('sealed_artifacts',['shasum','-a','256','-c',dest+'/SHA256SUMS'])
log.close
final_hash=Digest::SHA256.file(dest+'/FINAL.json').hexdigest
manifest_hash=Digest::SHA256.file(dest+'/SHA256SUMS').hexdigest
handoff='/tmp/r33_final_push_20260915_1409/b.final'
File.open(handoff,'wx') do |f|
 f.puts "Lane B local native engineering audit finished; V91 generation and full N17 continuity FAIL_CLOSED."
 f.puts "All 80 source rows classified: 50 fresh direct native static passes + 4 independently reviewed native engineering equivalents = 54 bounded passes; 26 reviewed blocked rows (R27 5, R26 21). Exact blockers: #{dest}/ROWS.json."
 f.puts "V91: 16/16 oracle custody and intended four-field binding; authored dataset/order 0/16 (exit 1); actual generated strings 0; admission exit 91. Exact R23 methods/source and complete 42-D conditions unavailable in searched scope; no expected-output shortcut used. #{dest}/V91_BOUND_ROWS.json."
 f.puts "Fresh native R26/R27 digest recomputation PASS, including additive fused native dependency (no cached R26 preimage literal). Native R27 policy rows and negatives PASS. New fused/policy adapters remain author-verified, pending independent review. Corrected R25 compatibility rebuild/negative admission PASS; actual R25 digest/lineage and exact input bundle remain blocked."
 f.puts "Search: 31,136 local paths, 27 archives, all 1,610 Git blobs/744,029,506 bytes; no exact missing input matches. Scope exclusions are explicit in FINAL.json; early-release media is unbound to R26."
 f.puts "Stable compiler preserved. Canonical raw/map and protected hashes pass; R27 step 60423/restarts 0. No learn, learner authority, scientific exposure, promotion, foreign runtime or forbidden Git mutation."
 f.puts "FINAL.json #{final_hash}\nSHA256SUMS #{manifest_hash}\nSealed #{paths.size} files; checksum command exit 0. Evidence/argv/exits/hashes: #{dest}/FINAL.json and native/*commands.jsonl, V91/commands.tsv, verification/commands.jsonl. Current N17 STATUS/matrices/register/lineage/runtime notes updated; replaced status preserved under prior_status."
end
File.write('/tmp/r33_final_push_20260915_1409/b.seal.sha256',Digest::SHA256.file(handoff).hexdigest+'  '+handoff+"\n"+manifest_hash+'  '+dest+'/SHA256SUMS'+"\n")
puts handoff
