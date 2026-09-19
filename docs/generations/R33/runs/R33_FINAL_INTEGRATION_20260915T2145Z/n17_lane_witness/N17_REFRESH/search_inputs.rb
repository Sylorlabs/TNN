require 'json'
require 'open3'
require 'fileutils'
e=File.expand_path('Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/N17_REFRESH')
sizes=[63069,7028883,29242,13609471,569,8864,8881,4206,74856,25160,13019,83905,508,482409,499889,56777645]
files=File.readlines(e+'/inputs/local_files.txt',chomp:true).uniq
candidates=[];archives=[];errors=[];magic_checked=0
files.each do |p|
 begin
 next unless File.file?(p)
 n=File.size(p)
 candidates<<p if sizes.include?(n)||p.match?(/(?:r2[3567].*(?:accepted|experiments|summary|release)|verify_r2[567]|smoke_r26|MANIFEST\.sha256|\.(?:mp4|avi|mov|mkv|webm)$)/i)
 # Inspect file headers even for renamed archives; exclude raw native map pages.
 next if p.include?('/parent-map/')||p.include?('/torch-pages/')
 magic=File.binread(p,4);magic_checked+=1
 archives<<p if magic.start_with?("PK\x03\x04".b,"\x1f\x8b".b,"BZh".b,"\xfd7zX".b)||p.match?(/\.(?:tar|tgz|zip|tar\.gz|tar\.xz)$/i)
 rescue => ex
 errors<<{path:p,error:ex.message}
 end
end
journal=File.open(e+'/search_commands.jsonl','w')
run=lambda do |label,argv|
 out,err,st=Open3.capture3(*argv)
 File.binwrite(e+'/logs/'+label+'.stdout',out);File.binwrite(e+'/logs/'+label+'.stderr',err)
 File.write(e+'/logs/'+label+'.argv',argv.join("\n")+"\n");File.write(e+'/logs/'+label+'.exit',st.exitstatus.to_s+"\n")
 journal.puts(JSON.generate({label:label,argv:argv,exit:st.exitstatus,role:'operational_archive_or_git_byte_recovery'}));journal.flush
 [out,st.exitstatus]
end
FileUtils.mkdir_p(e+'/inputs/archive_members');FileUtils.mkdir_p(e+'/inputs/git_blobs')
objects=File.readlines(e+'/inputs/git_objects.txt',chomp:true)
objects.each do |line|
 id,kind,n=line.split
 next unless kind=='blob'&&sizes.include?(n.to_i)
 out,rc=run.call('git_blob_'+id,['git','cat-file','blob',id])
 if rc==0
 p=e+'/inputs/git_blobs/'+id;File.binwrite(p,out);candidates<<p
 end
end
inventory=[]
archives.uniq.each_with_index do |path,i|
 out,rc=run.call('archive_'+i.to_s,['tar','-tf',path])
 members=rc==0 ? out.lines.map(&:chomp) : []
 selected=members.select{|m|m.match?(/(?:r2[3567].*(?:accepted|experiments|summary|release)|verify_r2[567]|smoke_r26|MANIFEST\.sha256|\.(?:mp4|avi|mov|mkv|webm|zip|tar|tgz)$)/i)}
 recovered=[]
 selected.each_with_index do |m,k|
 next if m.end_with?('/')
 bytes,exitcode=run.call('member_'+i.to_s+'_'+k.to_s,['tar','-xOf',path,m])
 next unless exitcode==0
 p=e+'/inputs/archive_members/'+i.to_s+'_'+k.to_s;File.binwrite(p,bytes);candidates<<p
 recovered<<{member:m,path:p,bytes:bytes.bytesize}
 end
 inventory<<{path:path,bytes:File.size(path),listing_exit:rc,member_count:members.size,recovered:recovered}
end
journal.close
File.write(e+'/inputs/candidates.txt',candidates.uniq.join("\n")+"\n")
File.write(e+'/SEARCH_SCOPE.json',JSON.pretty_generate({returned_paths:files.size,magic_headers_inspected:magic_checked,inspection_errors:errors,git_objects:objects.size,selection_sizes:sizes,candidates:candidates.uniq.size,archives:inventory,exclusions:['rg denied RustDesk directories','no global absence asserted','compressed git blobs admitted only by exact-size export','nested compressed member contents not recursively searched in this pass','standalone byte identity is never inferred from embedded objects']})+"\n")
puts "#{files.size} paths; #{magic_checked} headers; #{archives.uniq.size} archives; #{candidates.uniq.size} candidates"
