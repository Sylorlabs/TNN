require 'open3'; require 'digest'; require 'json'
r='/Users/Shared/micah/Documents/TNN/TNN';d=File.realpath(__dir__);e=r+'/Research/R33_FINAL_INTEGRATION_20260915T2145Z'
File.open(d+'/custody.commands.jsonl','w') do |j|
 [[e,'old_manifest',['shasum','-a','256','-c','SHA256SUMS']], [e,'old_seal',['shasum','-a','256','-c','SEAL.sha256']], [r,'reviewer_seal',['shasum','-a','256','-c','/tmp/r33_final_push_20260915_1409/reviewer.seal.sha256']]].each do |cwd,n,a|
 o,err,s=Open3.capture3(*a,chdir:cwd);File.binwrite(d+'/'+n+'.stdout',o);File.binwrite(d+'/'+n+'.stderr',err);j.puts(JSON.generate({argv:a,cwd:cwd,exit:s.exitstatus,signal:s.termsig,stdout_sha256:Digest::SHA256.hexdigest(o),stderr_sha256:Digest::SHA256.hexdigest(err)}));puts "#{n}:#{s.exitstatus}";raise n unless s.success?
 end
end
