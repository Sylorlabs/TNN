require 'json';require 'open3'
e=File.expand_path('Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/N17_REFRESH')
lines=File.readlines(e+'/logs/deep_candidate_hashes.stdout',chomp:true)
errors=lines.select{|s|s.start_with?("ERROR\t")}.map{|s|s.split("\t",2)[1]}
complete=lines.select{|s|s.start_with?("FILE\t")};log=File.open(e+'/large_archive_commands.jsonl','w')
errors.each_with_index do |path,i|
 argv=['shasum','-a','256',path];out,err,st=Open3.capture3(*argv);label='large_archive_'+i.to_s
 File.binwrite(e+'/logs/'+label+'.stdout',out);File.binwrite(e+'/logs/'+label+'.stderr',err);File.write(e+'/logs/'+label+'.argv',argv.join("\n")+"\n");File.write(e+'/logs/'+label+'.exit',st.exitstatus.to_s+"\n")
 log.puts(JSON.generate({label:label,argv:argv,exit:st.exitstatus,role:'local_operational_hash_large_archive_exceeds_native_32MiB_primitive_bound',bytes:File.size(path)}));log.flush
 raise 'hash failed' unless st.exitstatus==0&&out.match?(/\A[0-9a-f]{64} /)
 complete<<['FILE',path,File.size(path),out.split.first].join("\t")
end
log.close;File.write(e+'/inputs/deep_complete_hashes.tsv',complete.join("\n")+"\n")
File.write(e+'/HASH_SCOPE.json',JSON.pretty_generate({native_candidate_hashes:lines.size-errors.size,local_operational_large_archive_hashes:errors.size,native_candidate_process_exit:1,native_size_bound:33554360,complete_hash_count:complete.size,excluded_hashes:0,qualification_boundary:'Local large-file integrity hashing is operational tooling. Native row/digest/inference qualification uses Zag only. No archive listing/hash counts as native generation or lineage closure.'})+"\n")
puts "#{errors.size} large archive hashes recovered; #{complete.size} total"
