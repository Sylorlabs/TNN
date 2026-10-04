require 'json'
require 'digest'
require 'open3'
require 'fileutils'
# Byte inventory only; no historical code or serialized object execution.
repo='/Users/Shared/micah/Documents/TNN/TNN'
base=repo+'/Research/R33_NATIVE_N17_R27_CONTINUITY'
dest=File.expand_path(__dir__)+'/search'
FileUtils.mkdir_p(dest+'/logs')
journal=File.open(dest+'/commands.jsonl','wx')
run=lambda do |label,args|
 out,err,st=Open3.capture3(*args,chdir:repo)
 File.binwrite(dest+'/logs/'+label+'.stdout',out)
 File.binwrite(dest+'/logs/'+label+'.stderr',err)
 journal.puts(JSON.generate({label:label,argv:args,cwd:repo,exit:st.exitstatus,stdout_sha256:Digest::SHA256.hexdigest(out),stderr_sha256:Digest::SHA256.hexdigest(err)}));journal.flush
 puts "#{label}: #{st.exitstatus}"
 [out,st.exitstatus]
end
refs=JSON.parse(File.read(base+'/SOURCE_REFERENCE_INDEX.json'))
targets=refs['original_members'].map{|r|{name:r['path'],sha256:r['sha256'],size:r['size_bytes']}}
targets += JSON.parse(File.read(base+'/R25_LINEAGE_RECORD.json'))['required_artifacts'].map{|r|{name:r['id'],sha256:r['sha256'],size:r['size_bytes']}}
targets += [
 {name:'r23_source',size:63069,sha256:'517eb325096d5ae71ebb3bf659da77eac4266129136b888b469a99e366d4b642'},
 {name:'r23_state',size:7028883,sha256:'fc24881f104052c09a4cb6e596b01ae5c107d9ae0356c8799ec97eff3edf440b'},
 {name:'r23_summary',size:29242,sha256:'74cdb944e1037e92100d0dee2eca6ffaebcabe53346bb114c4bd09b035e3a495'},
 {name:'r26_state',sha256:refs['expected_semantic_identity']['r26_accepted_state_raw_sha256']},
 {name:'r27_release',size:refs['original_release']['size_bytes'],sha256:refs['original_release']['sha256']}
]
File.write(dest+'/targets.json',JSON.pretty_generate(targets)+"\n")
hashes=targets.map{|r|r[:sha256]}.compact
sizes=targets.map{|r|r[:size]}.compact
roots=['/Users/Shared/micah','/Users/bypass/Downloads','/private/tmp']
paths,status=run.call('files',['rg','--files','--hidden','--no-ignore',*roots])
files=paths.lines.map(&:chomp).uniq
rows=[];errors=[];admissions=[];archives=[]
files.each do |p|
 begin
  next unless File.file?(p)
  n=File.size(p)
  archives<<p if p.match?(/\.(zip|tar|tgz|tar\.gz|tar\.xz)$/i)
  # Includes renamed small source/summary/policy/manifests, exact-size large inputs,
  # and arbitrary named serialized states, without loading historical objects.
  next unless (n>0 && n<=110000) || sizes.include?(n) || p.match?(/(?:r2[3567]|accepted|speech|robust).*(?:pkl|zip|bin)$/i)
  h=Digest::SHA256.file(p).hexdigest
  matches=targets.select{|r|r[:sha256]==h}.map{|r|r[:name]}
  rows<<{path:p,size:n,sha256:h,matches:matches}
  admissions<<rows[-1] unless matches.empty?
 rescue SystemCallError=>e
  errors<<{path:p,error:e.message}
 end
end
File.write(dest+'/candidate_hashes.json',JSON.pretty_generate(rows)+"\n")
File.write(dest+'/admissions.json',JSON.pretty_generate(admissions)+"\n")
File.write(dest+'/errors.json',JSON.pretty_generate(errors)+"\n")
puts "files #{files.size}, hashes #{rows.size}, admitted copies #{admissions.size}, archives #{archives.size}"
archive_rows=[]
archives.uniq.each_with_index do |p,i|
 out,ec=run.call('archive_'+i.to_s,p.end_with?('.zip') ? ['unzip','-Z1',p] : ['tar','-tf',p])
 members=out.lines.map(&:strip)
 selected=members.select{|m|m.match?(/(?:r2[3567]|verify_r2[567]|smoke_r26|MANIFEST\.sha256|speech|robust|general.learning|\.(mp4|avi|mov|mkv)$)/i)}
 row={path:p,size:File.size(p),sha256:Digest::SHA256.file(p).hexdigest,exit:ec,members:members.size,selected:selected,member_hashes:[]}
 if ec==0 && p.end_with?('.zip')
  selected.each_with_index do |m,k|
   next if m.end_with?('/')
   bytes,me=run.call("member_#{i}_#{k}",['unzip','-p',p,m])
   h=Digest::SHA256.hexdigest(bytes)
   found=targets.select{|t|t[:sha256]==h}.map{|t|t[:name]}
   row[:member_hashes]<<{member:m,size:bytes.bytesize,sha256:h,exit:me,matches:found}
  end
 end
 archive_rows<<row
end
File.write(dest+'/archives.json',JSON.pretty_generate(archive_rows)+"\n")
objects,ec=run.call('git_objects',['git','cat-file','--batch-all-objects','--batch-check=%(objectname) %(objecttype) %(objectsize)'])
gitrows=[]
objects.lines.each_with_index do |line,i|
 oid,type,n=line.split;next unless type=='blob' && (n.to_i<=110000 || sizes.include?(n.to_i))
 bytes,st=run.call('blob_'+i.to_s,['git','cat-file','blob',oid])
 h=Digest::SHA256.hexdigest(bytes)
 found=targets.select{|r|r[:sha256]==h}.map{|r|r[:name]}
 leads=bytes.include?('_build_semantic_dataset') || bytes.include?('SOCIAL_FAR') || bytes.include?('class NameMemory')
 gitrows<<{oid:oid,size:n.to_i,sha256:h,exit:st,matches:found,behavior_lead:leads}
end
File.write(dest+'/git_blobs.json',JSON.pretty_generate(gitrows)+"\n")
run.call('behavior_search',['rg','--hidden','--no-ignore','-l','def _build_semantic_dataset|def smoke_r26|SOCIAL_FAR|class.*NameMemory',*roots,'-g','*.py','-g','*.txt','-g','*.zag'])
summary={roots:roots,inventory_exit:status,returned_paths:files.size,hashed_files:rows.size,exact_admitted_copies:admissions.size,archives:archive_rows.size,git_blobs:gitrows.size,git_exact_matches:gitrows.select{|r|!r[:matches].empty?},archive_exact_matches:archive_rows.flat_map{|r|r[:member_hashes].select{|m|!m[:matches].empty?}},scope_exclusions:['Denied/unreturned paths excluded; errors retained','Not exhaustive arbitrary embedded or renamed archive recovery','No external/network recovery','No historical code, pickle, reducers or ML runtime executed']}
File.write(dest+'/SUMMARY.json',JSON.pretty_generate(summary)+"\n")
journal.close
puts JSON.generate(summary)
