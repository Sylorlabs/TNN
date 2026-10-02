require 'json'; require 'open3'
e=File.expand_path('Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/N17_REFRESH')
all=File.readlines(e+'/inputs/git_objects.txt',chomp:true).map(&:split)
objects=all.select{|id,k,n|k=='blob'&&n.to_i<=200000};ids=objects.map(&:first)
out,err,st=Open3.capture3('git','cat-file','--batch',stdin_data:ids.join("\n")+"\n");out=out.b
File.binwrite(e+'/logs/git_behavior.stdout',out);File.binwrite(e+'/logs/git_behavior.stderr',err)
File.write(e+'/logs/git_behavior.exit',st.exitstatus.to_s+"\n");File.write(e+'/logs/git_behavior.argv',"git\ncat-file\n--batch\n");File.write(e+'/inputs/git_behavior.stdin',ids.join("\n")+"\n")
at=0;leads=[]
ids.each do |expected|
 endline=out.index("\n",at);raise 'header' unless endline
 id,k,n=out[at...endline].split;raise 'object' unless id==expected&&k=='blob'
 at=endline+1;bytes=out.byteslice(at,n.to_i);at+=n.to_i+1
 if bytes.match?(/def _build_semantic_dataset|class R23State|class R26State|class R27State|class.*NameMemory|SOCIAL_FAR|def smoke_r26/)
 p=e+'/inputs/git_blobs/'+id;File.binwrite(p,bytes);leads<<{id:id,path:p,bytes:bytes.bytesize}
 end
end
File.write(e+'/GIT_BEHAVIOR_SCAN.json',JSON.pretty_generate({argv:['git','cat-file','--batch'],exit:st.exitstatus,objects_scanned:ids.size,byte_limit:200000,leads:leads,larger_blob_count:all.count{|id,k,n|k=='blob'&&n.to_i>200000},stdin:e+'/inputs/git_behavior.stdin'})+"\n")
puts "#{ids.size} git blobs inspected; #{leads.size} leads"
