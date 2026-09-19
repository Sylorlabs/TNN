require 'json';require 'open3';require 'digest';require 'fileutils'
repo='/Users/Shared/micah/Documents/TNN/TNN';d=File.expand_path(__dir__)+'/additional_verified'
log=File.open(d+'/commands.continuation.jsonl','wx')
run=lambda do |label,args,expected|
 out,err,st=Open3.capture3(*args,chdir:repo);File.binwrite(d+'/logs/'+label+'.stdout',out);File.binwrite(d+'/logs/'+label+'.stderr',err)
 log.puts(JSON.generate({label:label,argv:args,cwd:repo,exit:st.exitstatus,expected:expected,stdout_sha256:Digest::SHA256.hexdigest(out),stderr_sha256:Digest::SHA256.hexdigest(err)}));log.flush
 puts "#{label}: #{st.exitstatus}";raise label unless st.exitstatus==expected
end
# Reviewed journal's same input path had three successive states. Preserve
# copied final wrong-hash fixture; use a separate root for the wrong-size case.
FileUtils.cp_r(d+'/fixtures',d+'/wrong_size_inputs')
File.binwrite(d+'/wrong_size_inputs/r25.pkl',"\0")
leaves=%w[r25.pkl r23.pkl speech.pkl robust.pkl architecture.json sibling.json learning.json]
run.call('r25_wrong_size_isolated',[d+'/bin/r25_full_digest_exact_parent_v1_runner',d+'/wrong_size_inputs',*leaves],66)
run.call('r25_correct_lengths_wrong_hash_isolated',[d+'/bin/r25_full_digest_exact_parent_v1_runner',d+'/fixtures',*leaves],1)
%w[canonical protected].each{|n|run.call(n+'_final',['shasum','-a','256','-c',repo+'/Research/R33_CLOSEOUT_20260915T174458Z/'+n+'.sha256'],0)}
run.call('compiler_final',['shasum','-a','256','/Users/Shared/micah/Documents/zag/znc'],0)
log.close
