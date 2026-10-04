require 'open3'
require 'json'
require 'digest'
d=File.expand_path(__dir__)
commands=[['canonical_before',['shasum','-a','256','-c','Research/R33_CLOSEOUT_20260915T174458Z/canonical.sha256']],['protected_before',['shasum','-a','256','-c','Research/R33_CLOSEOUT_20260915T174458Z/protected.sha256']]]
%w[review_native memo_negative].each do |name|
commands << ["build_#{name}",['/Users/Shared/micah/Documents/zag/znc',d+"/#{name}.zag",'--target','macos-arm64','--no-zagd','--no-analyze','--no-foreground-cache','-o',d+"/#{name}"]]
commands << ["run_#{name}",[d+"/#{name}"]]
end
commands << ['raw_sha',['shasum','-a','256','Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl','Research/R33_NATIVE_N10_RUN_PRIMARY_V1/parent-map/manifest.bin']]
commands << ['canonical_after',commands[0][1]]
commands << ['protected_after',commands[1][1]]
File.open(d+'/commands.jsonl','wx') do |log|
commands.each do |label,argv|
 out,err,status=Open3.capture3(*argv)
 File.write(d+"/final_#{label}.stdout",out);File.write(d+"/final_#{label}.stderr",err)
 log.puts(JSON.generate({label:label,argv:argv,exit:status.exitstatus,stdout_sha256:Digest::SHA256.hexdigest(out),stderr_sha256:Digest::SHA256.hexdigest(err)}));log.flush
 puts "#{label}: exit #{status.exitstatus}\n#{out}#{err}"
 break unless status.success?
end
end
