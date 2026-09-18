require 'json';require 'open3';require 'digest'
d=File.expand_path(__dir__);log=File.open(d+'/commands.jsonl','wx')
run=lambda do |label,args,expected|
 out,err,st=Open3.capture3(*args);File.write(d+'/evidence/'+label+'.stdout',out);File.write(d+'/evidence/'+label+'.stderr',err)
 row={label:label,argv:args,exit:st.exitstatus,expected:expected,stdout_sha256:Digest::SHA256.hexdigest(out),stderr_sha256:Digest::SHA256.hexdigest(err)};log.puts(JSON.generate(row));log.flush;puts "#{label}: exit #{st.exitstatus} expected #{expected}";raise "failed #{label}: #{err}" unless [expected].flatten.include?(st.exitstatus);out
end
%w[canonical protected].each{|n|run.call(n+'_before',['shasum','-a','256','-c','Research/R33_CLOSEOUT_20260915T174458Z/'+n+'.sha256'],0)}
%w[r25_full_digest_exact_parent_v1_runner exact_source_gate independent_admission_tests].each do |n|
 run.call('build_'+n,['/Users/Shared/micah/Documents/zag/znc',d+'/sources/N17/'+n+'.zag','--target','macos-arm64','--no-zagd','--no-analyze','--no-foreground-cache','-o',d+'/bin/'+n],0)
end
run.call('r25_usage',[d+'/bin/r25_full_digest_exact_parent_v1_runner'],64)
run.call('r25_missing',[d+'/bin/r25_full_digest_exact_parent_v1_runner',d+'/evidence','missing_r25.pkl','missing_r23.pkl','missing_speech.pkl','missing_robust.pkl','missing_arch.json','missing_sibling.json','missing_learning.json'],66)
run.call('source_selftest',[d+'/bin/exact_source_gate','selftest'],0)
run.call('source_missing',[d+'/bin/exact_source_gate',d+'/evidence','missing_r26.py'],66)
run.call('source_excerpt_reject',[d+'/bin/exact_source_gate','/private/tmp/r33_finish_recovery_20260915_b/n17','excerpt.txt'],71)
run.call('admission_tests',[d+'/bin/independent_admission_tests'],[0,1])
archives=File.readlines(d+'/evidence/archives.txt',chomp:true).uniq
inventory=archives.each_with_index.map do |path,i|
 args=path.end_with?('.zip') ? ['unzip','-Z1',path] : ['tar','-tf',path]
 out=run.call('archive_'+(i+1).to_s,args,0)
 {ordinal:i+1,path:path,bytes:File.size(path),sha256:Digest::SHA256.file(path).hexdigest,members:out.lines.size,prior_listing_sha256:Digest::SHA256.file('/tmp/r33_finish_recovery_20260915_b/n17/archive_'+(i+1).to_s+'.stdout').hexdigest,listing_sha256:Digest::SHA256.hexdigest(out),candidate_members:out.lines.map(&:strip).select{|x|x.match?(/(?:r2[3567].*(?:accepted|experiments|verify)|verify_r2[567]|smoke_r26|MANIFEST\.sha256|\.(?:mp4|avi)$)/i)}}
end
File.write(d+'/ARCHIVE_REVIEW.json',JSON.pretty_generate(inventory)+"\n")
roots=['/Users/Shared/micah/Documents','/Users/Shared/micah/Downloads','/Users/bypass/Downloads','/private/tmp']
run.call('local_files',['rg','--files','--hidden','--no-ignore',*roots],[0,2])
run.call('behavior_search',['rg','--hidden','--no-ignore','-l','SOCIAL_FAR|def smoke_r26|class R26State|class R27State|class.*NameMemory',*roots,'-g','*.py','-g','*.txt','-g','*.zag'],[0,1,2])
%w[canonical protected].each{|n|run.call(n+'_after',['shasum','-a','256','-c','Research/R33_CLOSEOUT_20260915T174458Z/'+n+'.sha256'],0)}
log.close
