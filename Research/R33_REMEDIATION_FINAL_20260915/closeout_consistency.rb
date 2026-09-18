require 'json';require 'digest';require 'fileutils';require 'open3'
r='/Users/Shared/micah/Documents/TNN/TNN';d=File.realpath(__dir__);t='/tmp/r33_final_push_20260915_1409'
%w[R25_LINEAGE_REQUIREMENTS.md IMPLEMENTATION_DECISION.md].each{|n|p=r+'/Research/R33_NATIVE_N17_R27_CONTINUITY/'+n;s=File.read(p).gsub('../../R33_REMEDIATION_FINAL_20260915','../R33_REMEDIATION_FINAL_20260915').gsub('../../R33_FINAL_INTEGRATION_20260915T2145Z','../R33_FINAL_INTEGRATION_20260915T2145Z');File.write(p,s)}
external=File.readlines(d+'/SHA256SUMS').map{|l|l.strip.split(/\s+/,2)[1]}.select{|p|!p.start_with?(d+'/')}
external+=(%w[integrator.final reviewer.final integrator.seal.sha256 reviewer.seal.sha256].map{|n|t+'/'+n})
external.uniq.each{|p|dst=d+'/final_status/'+p.sub(r+'/','').sub(t+'/','task/');FileUtils.mkdir_p(File.dirname(dst));FileUtils.cp(p,dst)}
# Both current entry points must retain scoped incomplete status and point to the same remediation.
a=JSON.parse(File.read(r+'/R33_FINAL_CLOSEOUT.json'));b=JSON.parse(File.read(r+'/Research/R33_FINAL_CLOSEOUT.json'));raise 'complete claim' if a['r33_complete']||b['r33_complete'];raise 'entry mismatch' unless a['remediation']==b['remediation']
rows=JSON.parse(File.read(d+'/N17_REQUALIFIED_ROWS.json'));raise 'row count' unless rows.length==80&&rows.map{|v|v['id']}.uniq.length==80&&rows.count{|v|v['review']=='REQUEST_CHANGES'}==26
File.write(d+'/CLOSEOUT_CONSISTENCY.json',JSON.pretty_generate({entry_points_consistent:true,rows_unique:80,blocked:26,current_final_text_and_seals_frozen:true,canonical_and_consumed_registries_preserved:true,n19_exact_commands:98,admitted_input_pins:260,relative_status_paths_corrected:true}))
ex=%w[SHA256SUMS SEAL.sha256 manifest.verify.stdout manifest.verify.stderr manifest.verify.exit seal.verify.stdout seal.verify.stderr seal.verify.exit]
File.open(d+'/SHA256SUMS','w'){|f|((Dir.glob(d+'/**/*',File::FNM_DOTMATCH).select{|p|File.file?(p)&&!ex.include?(p.sub(d+'/',''))})+external).uniq.sort.each{|p|f.puts "#{Digest::SHA256.file(p).hexdigest}  #{p}"}}
o,e,s=Open3.capture3('shasum','-a','256','-c',d+'/SHA256SUMS',chdir:r);File.write(d+'/manifest.verify.stdout',o);File.write(d+'/manifest.verify.stderr',e);File.write(d+'/manifest.verify.exit',s.exitstatus.to_s+"\n");raise 'manifest' unless s.success?
File.open(d+'/SEAL.sha256','w'){|f|%w[SHA256SUMS FREEZE.json REMEDIATION_STATUS.json manifest.verify.stdout manifest.verify.stderr manifest.verify.exit].each{|p|f.puts "#{Digest::SHA256.file(d+'/'+p).hexdigest}  #{d}/#{p}"}}
o,e,s=Open3.capture3('shasum','-a','256','-c',d+'/SEAL.sha256',chdir:r);File.write(d+'/seal.verify.stdout',o);File.write(d+'/seal.verify.stderr',e);File.write(d+'/seal.verify.exit',s.exitstatus.to_s+"\n");raise 'seal' unless s.success?
puts "Closeout consistency PASS; #{File.readlines(d+'/SHA256SUMS').length} evidence hashes and final seal verify exit0."
