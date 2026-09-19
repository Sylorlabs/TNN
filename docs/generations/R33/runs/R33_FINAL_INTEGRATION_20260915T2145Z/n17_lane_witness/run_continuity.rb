require 'json';require 'open3';require 'digest';require 'fileutils'
repo='/Users/Shared/micah/Documents/TNN/TNN';dest=File.expand_path(__dir__);base=File.dirname(dest)
correction=base+'/RECOVERY_20260915_B_INDEPENDENT/TERMINAL_SUPPLEMENT_20260915/COMPATIBILITY_CORRECTION_20260915'
review=base+'/V91_SEMANTIC_KAT/reviews/RECOVERY_B_INDEPENDENT'
log=File.open(dest+'/native/continuity_commands.jsonl','wx')
run=lambda do |label,argv,expected|
 out,err,st=Open3.capture3(*argv,chdir:repo)
 File.binwrite(dest+'/native/logs/'+label+'.stdout',out);File.binwrite(dest+'/native/logs/'+label+'.stderr',err)
 log.puts(JSON.generate({label:label,argv:argv,cwd:repo,exit:st.exitstatus,expected:expected,stdout_sha256:Digest::SHA256.hexdigest(out),stderr_sha256:Digest::SHA256.hexdigest(err)}));log.flush;puts "#{label}: #{st.exitstatus}";raise label unless st.exitstatus==expected
 out
end
sources={'r25_constants'=>correction+'/sources/N17/constant_probe.zag','r25_admission'=>correction+'/sources/N17/independent_admission_tests.zag','r25_runner'=>correction+'/sources/N17/r25_full_digest_exact_parent_v1_runner.zag','source_gate'=>correction+'/sources/N17/repaired_exact_source_gate.zag','tokens'=>correction+'/sources/N17/forbidden_selector_tests.zag','v91_independent'=>review+'/independent_review.zag','v91_lineage'=>review+'/lineage_review.zag','v91_targets'=>review+'/targets_review.zag'}
sources.each do |n,source|
 run.call('project_'+n,[dest+'/native/project',source,dest+'/native/'+n+'.zag',dest+'/native/'+n+'.provenance'],0)
 run.call('build_'+n,['/Users/Shared/micah/Documents/zag/znc',dest+'/native/'+n+'.zag','--target','macos-arm64','--no-zagd','--no-analyze','--no-foreground-cache','-o',dest+'/native/'+n],0)
end
%w[r25_constants r25_admission tokens].each{|n|run.call(n,[dest+'/native/'+n],0)}
run.call('source_gate_selftest',[dest+'/native/source_gate','selftest'],0)
run.call('source_missing',[dest+'/native/source_gate',dest+'/native','absent-r26.py'],66)
run.call('r25_usage',[dest+'/native/r25_runner'],64)
leaves=%w[r25.pkl r23.pkl speech.pkl robust.pkl architecture.json sibling.json learning.json]
root=dest+'/native/r25_negative';FileUtils.mkdir_p(root)
run.call('r25_missing',[dest+'/native/r25_runner',root,*leaves],66)
[13609471,7028883,482409,499889,6299,371,322].zip(leaves).each{|size,name|File.open(root+'/'+name,'wb'){|f|f.truncate(size)}}
run.call('r25_wrong_hashes',[dest+'/native/r25_runner',root,*leaves],1)
run.call('v91_independent',[dest+'/native/v91_independent',dest+'/V91/inputs'],0)
run.call('v91_lineage',[dest+'/native/v91_lineage',dest+'/V91/nested_r23',dest+'/V91/inputs'],0)
run.call('v91_targets',[dest+'/native/v91_targets',dest+'/native/intended.framed.bin'],0)
log.close
