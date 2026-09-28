require 'json';require 'digest';require 'open3';require 'fileutils'
repo='/Users/Shared/micah/Documents/TNN/TNN';d=File.expand_path(__dir__)+'/chained_final';log=File.open(d+'/commands.negative.jsonl','wx')
run=lambda do |label,args|
 out,err,st=Open3.capture3(*args,chdir:repo);File.binwrite(d+'/logs/'+label+'.stdout',out);File.binwrite(d+'/logs/'+label+'.stderr',err)
 log.puts(JSON.generate({label:label,argv:args,cwd:repo,exit:st.exitstatus,expected:0,stdout_sha256:Digest::SHA256.hexdigest(out),stderr_sha256:Digest::SHA256.hexdigest(err)}));log.flush
 puts "#{label}: #{st.exitstatus}";raise label unless st.success?
end
run.call('project_negative',[d+'/project',d+'/sources/dependency_negative.zag',d+'/negative.zag',d+'/negative.provenance'])
run.call('build_negative',['/Users/Shared/micah/Documents/zag/znc',d+'/negative.zag','--target','macos-arm64','--no-zagd','--no-analyze','--no-foreground-cache','-o',d+'/negative'])
run.call('dependency_negative',[d+'/negative']);log.close
