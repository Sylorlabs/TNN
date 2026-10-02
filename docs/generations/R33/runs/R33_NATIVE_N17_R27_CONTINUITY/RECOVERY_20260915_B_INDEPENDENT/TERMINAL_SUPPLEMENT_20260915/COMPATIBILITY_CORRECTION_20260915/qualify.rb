require 'open3';require 'json';require 'digest';require 'fileutils'
d=File.expand_path(__dir__);log=File.open(d+'/commands.jsonl','wx')
run=lambda do |label,argv,expected,contains=nil|
 o,e,s=Open3.capture3(*argv);File.write(d+'/evidence/'+label+'.stdout',o);File.write(d+'/evidence/'+label+'.stderr',e)
 log.puts(JSON.generate({label:label,argv:argv,exit:s.exitstatus,expected:expected,stdout_sha256:Digest::SHA256.hexdigest(o),stderr_sha256:Digest::SHA256.hexdigest(e)}));log.flush
 puts "#{label}: #{s.exitstatus} expected #{expected}";raise "#{label}: #{o}#{e}" unless s.exitstatus==expected && (!contains||o.include?(contains));o
end
%w[canonical protected].each{|n|run.call(n+'_before',['shasum','-a','256','-c','Research/R33_CLOSEOUT_20260915T174458Z/'+n+'.sha256'],0)}
%w[constant_probe r25_full_digest_exact_parent_v1_runner exact_source_gate independent_admission_tests bounded_allocator_tests].each{|n|run.call('build_'+n,['/Users/Shared/micah/Documents/zag/znc',d+'/sources/N17/'+n+'.zag','--target','macos-arm64','--no-zagd','--no-analyze','--no-foreground-cache','-o',d+'/bin/'+n],0)}
run.call('constant_values',[d+'/bin/constant_probe'],0,"13609471\n7028883\n482409\n499889\n")
run.call('bounded_allocator',[d+'/bin/bounded_allocator_tests'],0)
run.call('admission_preimage_negatives',[d+'/bin/independent_admission_tests'],0,'PASS_NATIVE_R25_HASH_ADMISSION_REJECTS_CORRECT_LENGTH_WRONG_BYTES')
r25=d+'/bin/r25_full_digest_exact_parent_v1_runner';gate=d+'/bin/exact_source_gate';root=d+'/fixtures'
run.call('r25_usage',[r25],64)
leaves=%w[r25.pkl r23.pkl speech.pkl robust.pkl architecture.json sibling.json learning.json]
run.call('r25_missing',[r25,root,*leaves],66)
run.call('gate_missing',[gate,root,'absent.py'],66)
run.call('gate_selftest',[gate,'selftest'],0)
File.binwrite(root+'/malformed.py','abc');File.binwrite(root+'/empty.py','');FileUtils.mkdir_p(root+'/directory.py');File.open(root+'/oversize.py','wb'){|f|f.truncate(33554361)}
File.symlink(root+'/malformed.py',root+'/symlink.py')
[['gate_malformed','malformed.py',71],['gate_empty','empty.py',68],['gate_oversize','oversize.py',68],['gate_nonregular','directory.py',67],['gate_symlink','symlink.py',66],['gate_invalid_leaf','../escape.py',66]].each{|label,leaf,rc|run.call(label,[gate,root,leaf],rc)}
run.call('gate_excerpt',[gate,'/private/tmp/r33_finish_recovery_20260915_b/n17','excerpt.txt'],71)
File.binwrite(root+'/r25.pkl','wrong-size')
run.call('r25_wrong_size',[r25,root,*leaves],66)
[13609471,7028883,482409,499889,6299,371,322].zip(leaves).each{|size,name|File.open(root+'/'+name,'wb'){|f|f.truncate(size)}}
o=run.call('r25_correct_lengths_wrong_hash',[r25,root,*leaves],1,'R25_FULL_EXACT_V1_NUMPY,-25301')
raise o unless o.include?('R25_FULL_EXACT_V1_TORCH,-25401')&&o.include?('R25_FULL_EXACT_V1_DIGEST,-25601')&&o.include?('R25_FULL_EXACT_V1_READY,0')
%w[canonical protected].each{|n|run.call(n+'_after',['shasum','-a','256','-c','Research/R33_CLOSEOUT_20260915T174458Z/'+n+'.sha256'],0)}
log.close
puts 'PASS_COMPATIBILITY_ENGINEERING_CORRECTION; INPUT_LINEAGE_ACCEPTANCE_FAIL_CLOSED'
