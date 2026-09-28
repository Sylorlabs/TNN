require 'find';require 'json';require 'digest';require 'open3'
d=File.realpath(__dir__);r='/Users/Shared/micah/Documents/TNN/TNN';Dir.chdir(r)
t=JSON.parse(File.read('/tmp/r33_final_push_20260915_1409/reviewer_evidence/EXACT_INPUT_SEARCH.json'))['targets']
v=JSON.parse(File.read(r+'/Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/V91/RECORD.json'));t+=v['missing_exact_inputs'].map{|x|{'sha256'=>x['sha256'],'bytes'=>x['bytes'],'role'=>x['role']}}
# Include every explicit exact-input digest in the current native R25 admission source.
File.read(r+'/Research/R33_FINAL_INTEGRATION_20260915T2145Z/n17_fresh/r25.zag').scan(/[0-9a-f]{64}/).uniq.each{|sha|t<<{'sha256'=>sha,'bytes'=>nil,'role'=>'native_r25_source_digest'}}
t=t.uniq{|x|x['sha256']};File.write(d+'/SEARCH_TARGETS.json',JSON.pretty_generate(t));matches=[];errors=[];counts={files:0,hashed:0,bytes_hashed:0,archives:0,archive_members:0,git_blobs:0};archives=[];inv=File.open(d+'/search.inventory.tsv','w');roots=['/Users/Shared/micah/Documents','/private/tmp'];j=File.open(d+'/search.commands.jsonl','w')
check=lambda{|p,sz,sha|t.select{|x|x['sha256']==sha}.each{|x|matches<<x.merge('path'=>p,'actual_bytes'=>sz)}}
roots.each{|root|Find.find(root){|p|next if p.start_with?(d+'/');begin;s=File.lstat(p);next unless s.file?;counts[:files]+=1;inv.puts("#{s.size}\t#{p}");archives<<p if p.start_with?(r+'/')&&p.match?(/\.(zip|tar\.gz|tgz)\z/i);eligible=t.any?{|x|x['bytes']==s.size}||s.size<=1_000_000||p.match?(/r2[3567]|semantic|dataset|speech|robust|release|tnn/i);next unless eligible&&s.size<=150_000_000;sha=Digest::SHA256.file(p).hexdigest;counts[:hashed]+=1;counts[:bytes_hashed]+=s.size;check.call(p,s.size,sha);rescue SystemCallError=>ex;errors<<{path:p,error:ex.class.name};end}}
inv.close;puts "files=#{counts[:files]} hashed=#{counts[:hashed]}";STDOUT.flush
run=lambda{|a|o,e,s=Open3.capture3(*a);j.puts(JSON.generate({argv:a,cwd:r,exit:s.exitstatus,signal:s.termsig,stdout_sha256:Digest::SHA256.hexdigest(o),stderr_sha256:Digest::SHA256.hexdigest(e)}));j.flush;errors<<{argv:a,exit:s.exitstatus,stderr:e} unless s.success?;o}
archives.uniq.each do |p|
 counts[:archives]+=1;zip=p.end_with?('.zip');names=run.call(zip ? ['unzip','-Z1',p] : ['tar','-tf',p]).lines.map(&:strip)
 names.each do |n|
 next if n.end_with?('/');next unless n.match?(/r2[3567]|semantic|dataset|speech|robust|MANIFEST|\.pkl\z|\.py\z|\.json\z|\.zip\z|\.tar\.gz\z/i)
 a=zip ? ['unzip','-p',p,n] : ['tar','-xOf',p,n];o=run.call(a);counts[:archive_members]+=1;check.call(p+'::'+n,o.bytesize,Digest::SHA256.hexdigest(o))
 end
end
# Fresh inventory of reachable and unreachable blobs, with no Git mutation.
objects=run.call(['git','cat-file','--batch-all-objects','--batch-check=%(objectname) %(objecttype) %(objectsize)'])
objects.lines.each{|l|oid,type,sz=l.split;next unless type=='blob';size=sz.to_i;next unless size<=1_000_000||t.any?{|x|x['bytes']==size};o=run.call(['git','cat-file','blob',oid]);counts[:git_blobs]+=1;check.call('git:blob:'+oid,o.bytesize,Digest::SHA256.hexdigest(o))}
j.close;File.write(d+'/EXACT_INPUT_SEARCH.json',JSON.pretty_generate({roots:roots,targets:t,counts:counts,matches:matches,errors:errors,exclusions:['Symlinks not traversed; inaccessible roots reported; remote machines not searched.','Loose files hashed regardless of basename up to 1MB, exact known sizes and relevant basenames up to 150MB; arbitrary larger renamed unknown-size files excluded.','All local TNN zip/tar.gz/tgz inventories inspected; source/JSON/state/normative member names selected. Renamed binary and recursive nested archive contents excluded.','All reachable/unreachable Git blobs up to 1MB or exact known required sizes hashed; other large unknown-size blobs excluded.']}));puts JSON.generate(counts)
