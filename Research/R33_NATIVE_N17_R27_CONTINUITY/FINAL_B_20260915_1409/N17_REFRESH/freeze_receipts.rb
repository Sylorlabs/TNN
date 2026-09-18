require 'json';require 'fileutils';require 'digest'
e=File.expand_path('Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/N17_REFRESH')
# Preserve the initial journal before assembling the final multi-stage journal.
FileUtils.cp(e+'/commands.tsv',e+'/commands.initial_policy_missing_failure.tsv') unless File.exist?(e+'/commands.initial_policy_missing_failure.tsv')
stages=%w[commands.initial_policy_missing_failure.tsv supplement_commands.tsv final_commands.tsv receipt_commands.tsv pin_commands.tsv deep_commands.tsv complete_commands.tsv]
File.write(e+'/commands.tsv',stages.map{|p|File.read(e+'/'+p)}.join)
closure=[]
Dir[e+'/projected/*.provenance'].each do |p|
 File.readlines(p,chomp:true).each do |line|
 f=line.split("\t");next unless f[0]=='FILE'
 path=f[2];next unless path&&File.file?(path)
 bytes=File.binread(path);if Digest::SHA256.hexdigest(bytes)!=f[1];snapshots=Dir[e+"/sources/*.txt"].select{|x|Digest::SHA256.file(x).hexdigest==f[1]};raise "unfrozen source #{path} #{f[1]}" if snapshots.empty?;bytes=File.binread(snapshots.first);end;target=e+"/import_closure/"+f[1]+"/"+path.sub(/^\//,"");FileUtils.mkdir_p(File.dirname(target));File.binwrite(target,bytes);closure<<target
 end
end
inputs=[]
Dir[e+'/sources/*',e+'/projected/*',e+'/bin/*',e+'/*.rb',e+'/*.zsh',e+'/*.json',e+'/*commands*.tsv',e+'/*commands*.jsonl',e+'/inputs/*.tsv',e+'/inputs/*.txt',e+'/inputs/*.stdin',e+'/inputs/*.stderr',e+'/inputs/r27-policy.json'].each{|p|inputs<<p if File.file?(p)}
inputs.concat(closure.uniq)
repo='/Users/Shared/micah/Documents/TNN/TNN'
inputs.concat(Dir[repo+'/Research/R33_NATIVE_N10_RUN_PRIMARY_V1/parent-map/*'])
inputs<<repo+'/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl'
inputs<<'/Users/Shared/micah/Documents/zag/znc'
inputs<<repo+'/Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/V91_REFRESH/RECORD.json'
File.write(e+'/files.tsv',inputs.uniq.map{|p|"native_source_or_exact_input_or_receipt\t#{p}"}.join("\n")+"\n")
# Archive child commands are separately captured; their exact output bytes get
# native hashes in one inventory rather than being duplicated in this record.
logs=Dir[e+'/logs/*'].select{|p|File.file?(p)}
File.write(e+'/inputs/log_inventory_paths.txt',logs.join("\n")+"\n")
puts "#{inputs.uniq.size} pinned files; #{logs.size} logs to hash"
