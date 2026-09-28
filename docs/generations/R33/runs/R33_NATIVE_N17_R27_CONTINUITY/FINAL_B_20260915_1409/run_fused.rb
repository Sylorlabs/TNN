require 'open3';require 'json';require 'digest'
repo='/Users/Shared/micah/Documents/TNN/TNN';dest=File.expand_path(__dir__)
log=File.open(dest+'/native/fused_commands.jsonl','wx')
run=lambda do |label,argv,expected|
 out,err,st=Open3.capture3(*argv,chdir:repo)
 File.binwrite(dest+'/native/logs/'+label+'.stdout',out);File.binwrite(dest+'/native/logs/'+label+'.stderr',err)
 log.puts(JSON.generate({label:label,argv:argv,cwd:repo,exit:st.exitstatus,expected:expected,stdout_sha256:Digest::SHA256.hexdigest(out),stderr_sha256:Digest::SHA256.hexdigest(err)}));log.flush;puts "#{label}: #{st.exitstatus}";raise label unless st.exitstatus==expected
 out
end
%w[r27_fused fused_negative].each do |n|
 run.call('project_'+n,[dest+'/native/project',dest+'/'+n+'.zag',dest+'/native/'+n+'.zag',dest+'/native/'+n+'.provenance'],0)
 run.call('build_'+n,['/Users/Shared/micah/Documents/zag/znc',dest+'/native/'+n+'.zag','--target','macos-arm64','--no-zagd','--no-analyze','--no-foreground-cache','-o',dest+'/native/'+n],0)
end
run.call('fused_negative',[dest+'/native/fused_negative'],0)
out=run.call('r27_fused',[dest+'/native/r27_fused','digest'],0)
raise 'digest mismatch' unless out.include?('R27_NATIVE_DIGEST,562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04')&&out.include?('R26_NATIVE_DIGEST,44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649')
log.close
