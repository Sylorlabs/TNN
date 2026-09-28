require 'open3';require 'json';require 'digest';require 'fileutils'
repo='/Users/Shared/micah/Documents/TNN/TNN';dest=File.expand_path(__dir__)
log=File.open(dest+'/native/policy_commands.jsonl','wx')
run=lambda do |label,argv,expected|
 out,err,st=Open3.capture3(*argv,chdir:repo)
 File.binwrite(dest+'/native/logs/'+label+'.stdout',out);File.binwrite(dest+'/native/logs/'+label+'.stderr',err)
 log.puts(JSON.generate({label:label,argv:argv,cwd:repo,exit:st.exitstatus,expected:expected,stdout_sha256:Digest::SHA256.hexdigest(out),stderr_sha256:Digest::SHA256.hexdigest(err)}));log.flush;puts "#{label}: #{st.exitstatus}";raise label unless st.exitstatus==expected
end
source=dest+'/policy.zag';expanded=dest+'/native/policy.zag'
run.call('project_policy',[dest+'/native/project',source,expanded,dest+'/native/policy.provenance'],0)
run.call('build_policy',['/Users/Shared/micah/Documents/zag/znc',expanded,'--target','macos-arm64','--no-zagd','--no-analyze','--no-foreground-cache','-o',dest+'/native/policy'],0)
run.call('policy_selftest',[dest+'/native/policy','selftest'],0)
policy=repo+'/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-policy.json'
FileUtils.cp(policy,dest+'/native/frozen-r27-policy.json')
run.call('policy',[dest+'/native/policy',dest+'/native/frozen-r27-policy.json'],0)
File.binwrite(dest+'/native/policy_changed.json',File.binread(policy).sub('TEENAGER_ENGLISH','TEENAGER_ENGXISH'))
run.call('policy_changed_refused',[dest+'/native/policy',dest+'/native/policy_changed.json'],71)
log.close
