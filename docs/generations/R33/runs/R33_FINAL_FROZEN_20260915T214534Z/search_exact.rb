require 'find';require 'json';require 'digest'
e=File.expand_path(__dir__)
# Extract exact SHA requirements from current registers, without interpreting serialized ML state.
inputs=%w[Research/R33_NATIVE_N17_R27_CONTINUITY/R25_LINEAGE_RECORD.json Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/ROWS.json Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/V91/RECORD.json]
targets=[]
walk=lambda{|x|case x;when Hash;hash=x['known_sha256']||x['sha256'];sz=x['known_byte_length']||x['bytes'];targets << {sha256:hash,bytes:sz,role:x['role']||x['id']||x['required_member']} if hash.to_s.match?(/\A[0-9a-f]{64}\z/) && (x['present']==false||x['known_sha256']||x['minimal_blocker']);x.each_value{|v|walk.call(v)};when Array;x.each{|v|walk.call(v)};end}
inputs.each{|p|walk.call(JSON.parse(File.read(p)))}
JSON.parse(File.read("Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/recovery/SEARCH.json"))["targets"].each{|t|targets<<{sha256:t["sha256"],bytes:t["bytes"],role:t["member"]}}
targets=targets.uniq{|t|t[:sha256]};roots=['/Users/Shared/micah/Documents','/private/tmp'];counts={files:0,size_candidates:0,hashed:0};matches=[];errors=[];inventory=File.open("#{e}/search.inventory.tsv",'w')
roots.each do |root|
 Find.find(root) do |p|
 next if p.start_with?(e+'/')
 begin
 st=File.lstat(p);next unless st.file?;counts[:files]+=1
 names=File.basename(p).match?(/r2[3567]|semantic|dataset|generator|abstraction|speech|robust|release|tnn|znc/i)
 inventory.puts("#{st.size}\t#{p}") if names
 eligible=targets.select{|t| t[:bytes] ? t[:bytes]==st.size : names}
 next if eligible.empty?;counts[:size_candidates]+=1
 # Bound no-size candidates by local artifacts rather than arbitrary multi-GB payloads.
 next if st.size>150_000_000
 sha=Digest::SHA256.file(p).hexdigest;counts[:hashed]+=1
 eligible.each{|t|matches<<t.merge(path:p,actual_bytes:st.size) if sha==t[:sha256]}
 rescue SystemCallError=>ex;errors<<{path:p,error:ex.class.name};end
 end
end
inventory.close
File.write("#{e}/EXACT_INPUT_SEARCH.json",JSON.pretty_generate({roots:roots,targets:targets,counts:counts,matches:matches,errors:errors,exclusions:['No-size targets scanned by relevant basename, size<=150MB; arbitrary renamed payloads not proven absent.','Archives/git objects are covered by pinned lane B native recovery and all-blob records; this scan does not recursively extract archives.','Symlinks are not traversed; remote or other machines not searched.']}))
