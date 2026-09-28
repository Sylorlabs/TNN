require 'json'; require 'open3'; require 'fileutils'
e=File.expand_path('Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/N17_REFRESH')
j=JSON.parse(File.read(e+'/SEARCH_SCOPE.json'));paths=File.readlines(e+'/inputs/candidates.txt',chomp:true)
FileUtils.mkdir_p(e+'/inputs/expanded_members');log=File.open(e+'/expanded_commands.jsonl','w');records=[]
j['archives'].each_with_index do |a,i|
 next unless a['listing_exit']==0
 list=File.readlines(e+'/logs/archive_'+i.to_s+'.stdout',chomp:true)
 list.each_with_index do |m,k|
 next unless m.match?(/\.(?:py|zip|tar|tgz|tar\.gz)$/i)&&!m.end_with?('/')
 out,err,st=Open3.capture3('tar','-xOf',a['path'],m)
 label='expanded_'+i.to_s+'_'+k.to_s
 File.binwrite(e+'/logs/'+label+'.stdout',out);File.binwrite(e+'/logs/'+label+'.stderr',err)
 argv=['tar','-xOf',a['path'],m];File.write(e+'/logs/'+label+'.argv',argv.join("\n")+"\n");File.write(e+'/logs/'+label+'.exit',st.exitstatus.to_s+"\n")
 log.puts(JSON.generate({label:label,argv:argv,exit:st.exitstatus,role:'operational_member_byte_recovery'}));log.flush
 next unless st.exitstatus==0
 p=e+'/inputs/expanded_members/'+i.to_s+'_'+k.to_s;File.binwrite(p,out);paths<<p
 records<<{archive:a['path'],member:m,path:p,bytes:out.bytesize,behavior_lead:out.b.match?(/def _build_semantic_dataset|class R23State|class R26State|class R27State|class.*NameMemory|SOCIAL_FAR|def smoke_r26/)}
 end
end
log.close;File.write(e+'/inputs/candidates_expanded.txt',paths.uniq.join("\n")+"\n");File.write(e+'/EXPANDED_ARCHIVE_RECOVERY.json',JSON.pretty_generate(records)+"\n");puts "#{records.size} additional members; #{records.count{|r|r[:behavior_lead]}} behavior leads"
