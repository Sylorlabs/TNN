require 'json';require 'open3';require 'fileutils'
e=File.expand_path('Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/N17_REFRESH');scope=JSON.parse(File.read(e+'/SEARCH_SCOPE.json'));paths=File.readlines(e+'/inputs/candidates_expanded.txt',chomp:true)
paths.concat(scope['archives'].map{|r|r['path']})
queue=JSON.parse(File.read(e+'/EXPANDED_ARCHIVE_RECOVERY.json')).select{|r|r['member'].match?(/\.(?:zip|tar|tgz|tar\.gz)$/)}.map{|r|[r['path'],1,r['member']]}
FileUtils.mkdir_p(e+'/inputs/nested_members');journal=File.open(e+'/nested_commands.jsonl','w');records=[];serial=0
run=lambda do |label,argv|
 out,err,st=Open3.capture3(*argv);File.binwrite(e+'/logs/'+label+'.stdout',out);File.binwrite(e+'/logs/'+label+'.stderr',err);File.write(e+'/logs/'+label+'.argv',argv.join("\n")+"\n");File.write(e+'/logs/'+label+'.exit',st.exitstatus.to_s+"\n");journal.puts(JSON.generate({label:label,argv:argv,exit:st.exitstatus,role:'operational_nested_archive_recovery'}));journal.flush;[out.b,st.exitstatus]
end
until queue.empty?
 path,depth,origin=queue.shift;serial+=1
 list,rc=run.call('nested_list_'+serial.to_s,['tar','-tf',path]);recovered=[]
 if rc==0
 list.lines.map(&:chomp).each_with_index do |m,k|
 next unless m.match?(/\.(?:py|pkl|json|zip|tar|tgz|tar\.gz)$|MANIFEST\.sha256$/)&&!m.end_with?('/')
 data,exitcode=run.call('nested_member_'+serial.to_s+'_'+k.to_s,['tar','-xOf',path,m]);next unless exitcode==0
 p=e+'/inputs/nested_members/'+serial.to_s+'_'+k.to_s;File.binwrite(p,data);paths<<p;recovered<<{member:m,path:p,bytes:data.bytesize,behavior_lead:data.match?(/def _build_semantic_dataset|class R23State|class R26State|class R27State|SOCIAL_FAR|def smoke_r26/)}
 queue<<[p,depth+1,m] if depth<3&&m.match?(/\.(?:zip|tar|tgz|tar\.gz)$/)
 end
 end
 records<<{path:path,depth:depth,origin:origin,listing_exit:rc,recovered:recovered}
end
journal.close;File.write(e+'/NESTED_ARCHIVE_RECOVERY.json',JSON.pretty_generate(records)+"\n");File.write(e+'/inputs/candidates_deep.txt',paths.uniq.join("\n")+"\n");puts "#{serial} nested inventories; #{paths.uniq.size} deep candidates"
