require 'json';require 'open3';require 'digest';require 'fileutils'
R='/Users/Shared/micah/Documents/TNN/TNN';E=R+'/Research/R33_FINAL_INTEGRATION_20260915T2145Z';D=File.realpath(__dir__);C='/Users/Shared/micah/Documents/zag/znc';F=%w[--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache]
Dir.chdir(R);J=File.open(D+'/commands.jsonl','w');FAIL=[]
def run(n,a,x=0)
 o,e,s=Open3.capture3(*a);File.binwrite(D+'/'+n+'.stdout',o);File.binwrite(D+'/'+n+'.stderr',e);v={label:n,argv:a,cwd:Dir.pwd,exit:s.exitstatus,signal:s.termsig,expected:x,stdout_sha256:Digest::SHA256.hexdigest(o),stderr_sha256:Digest::SHA256.hexdigest(e)};J.puts(JSON.generate(v));J.flush;FAIL<<v if s.exitstatus!=x;puts "#{n}: #{s.exitstatus} expected=#{x}";STDOUT.flush;o
end
def build(n,s);run('build_'+n,[C,s,*F,'-o',D+'/'+n]);end
run('git_before',%w[git diff --binary]);run('immutable_before',['shasum','-a','256','-c',E+'/immutable.before.sha256']);run('stable_identity',['cmp',C,E+'/compiler.stable.znc']);run('old_integrator_seal',['shasum','-a','256','-c','/tmp/r33_final_push_20260915_1409/integrator.seal.sha256'],1)
{'v68'=>'outer_learner_packet_bridge_v68_tests','v73'=>'zag_checkpoint_sliceparam_repro_v73','v71'=>'zag_checkpoint_module_repro_v71','integration'=>'lane_d_packet_integration'}.each{|n,s|build(n,R+'/Research/R33_CONTINUING_LIFE_V1/'+s+'.zag');run(n,[D+'/'+n]) unless n=='integration'}
%w[original_v68 original_v73 minimal_v68 minimal_v73].each{|n|build(n,E+'/'+n+'.zag');run(n,[D+'/'+n],n.start_with?('original') ? 1 : 0)}
build('v92',E+'/sources/Research/R33_NATIVE_N17_R27_CONTINUITY/V92_STATE_IMAGE_QUAL/state_image_qual_v92.zag');FileUtils.mkdir_p(D+'/packet')
%w[selftest write read write-corrupt read-corrupt write-truncated read-truncated write-packet read-packet write-packet-corrupt read-packet-corrupt write-packet-truncated read-packet-truncated].each{|m|run('v92_'+m,[D+'/v92',m,D+'/packet'])}
%w[good corrupt inner torn].each{|s|FileUtils.mkdir_p(D+'/outer_'+s)}
%w[write:good reload:good corrupt:corrupt refuse:corrupt inner:inner refuse:inner torn:torn refuse:torn reload:good learn:good].each_with_index{|s,i|m,shape=s.split(':');run("transport_#{i}_#{m}",[D+'/integration',m,D+'/outer_'+shape,D+'/packet'],m=='learn' ? 65 : 0)}
s=File.binread(E+'/continuing.zag').gsub(E+'/runtime_continuing',D+'/runtime_continuing').gsub(E+'/continuing',D+'/continuing');File.binwrite(D+'/continuing.zag',s);build('continuing',D+'/continuing.zag');run('baseline',[D+'/continuing','supervise']);run('baseline_learn',[D+'/continuing','learn'],65)
%w[rows structure primitives identity memo policy fused fused_negative admission tokens r25 r26 r27 source_gate].each{|n|build('n17_'+n,E+'/n17_fresh/'+n+'.zag')}
%w[rows structure primitives identity memo fused_negative admission tokens].each{|n|run('n17_'+n,[D+'/n17_'+n])}
%w[r26 r27 fused].each{|n|run('n17_'+n+'_digest',[D+'/n17_'+n,'digest'])}
run('policy_selftest',[D+'/n17_policy','selftest']);run('policy',[D+'/n17_policy',R+'/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-policy.json']);run('policy_bad',[D+'/n17_policy',E+'/n17_fresh/bad_policy.json'],71)
root=D+'/r25_missing';FileUtils.mkdir_p(root);a=%w[r25.pkl r23.pkl speech.pkl robust.pkl architecture.json sibling.json learning.json];run('r25_missing',[D+'/n17_r25',root,*a],66);[13609471,7028883,482409,499889,6299,371,322].zip(a).each{|sz,n|File.open(root+'/'+n,'wb'){|f|f.truncate(sz)}};run('r25_wrong_hash',[D+'/n17_r25',root,*a],1);run('source_gate_selftest',[D+'/n17_source_gate','selftest']);run('source_gate_missing',[D+'/n17_source_gate',root,'absent-r26.py'],66)
%w[oracle numeric bpe rows_test rows_emit gate].each{|n|build('v91_'+n,E+'/v91_fresh/projected/'+n+'.zag')}
%w[oracle numeric].each{|n|run('v91_'+n,[D+'/v91_'+n,E+'/v91_fresh/inputs'])};run('v91_bpe',[D+'/v91_bpe',E+'/v91_fresh/inputs/bpe.framed.bin']);%w[rows_test rows_emit].each{|n|run('v91_'+n,[D+'/v91_'+n],1)};run('v91_gate',[D+'/v91_gate',E+'/v91_fresh/inputs'],91);run('v91_no_input',[D+'/v91_gate'],91);run('v91_fake',[D+'/v91_gate','--generated',E+'/v91_fresh/inputs/oracle.framed.bin'],91)
n=D+'/n19';FileUtils.mkdir_p([n+'/bin',n+'/logs',n+'/roots']);FileUtils.cp_r(E+'/n19/sources',n+'/sources')
%w[run supplement reap].each{|v|File.binwrite(n+'/'+v+'.zsh',File.binread(E+'/n19/'+v+'.zsh').gsub(E+'/n19',n));run('n19_'+v,['zsh',n+'/'+v+'.zsh'])}
run('immutable_after',['shasum','-a','256','-c',E+'/immutable.before.sha256']);run('git_after',%w[git diff --binary]);run('git_preserved',['cmp',D+'/git_before.stdout',D+'/git_after.stdout']);J.close;File.write(D+'/REQUAL_RESULT.json',JSON.pretty_generate({unexpected:FAIL,native_only:true,scientific_exposure:0,authority:false}));exit(FAIL.empty? ? 0 : 1)
