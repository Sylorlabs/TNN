require 'json'
require 'open3'
require 'digest'
repo='/Users/Shared/micah/Documents/TNN/TNN'
dest=File.expand_path(__dir__)+'/recovery'
search=JSON.parse(File.read(dest+'/SEARCH.json'))
metadata=File.readlines(dest+'/logs/all_git_objects.stdout')
ids=metadata.map{|line|id,type,size=line.split; id if type=='blob'}.compact
rows=[]; stderr=''; code=nil
argv=['git','cat-file','--batch']
Open3.popen3(*argv,chdir:repo) do |input,output,errors,wait|
  writer=Thread.new{ids.each{|id|input.puts(id)};input.close}
  error_reader=Thread.new{stderr=errors.read}
  ids.each do |id|
    header=output.gets; oid,type,size=header.split
    raise header unless oid==id&&type=='blob'
    data=output.read(size.to_i); raise id unless data.bytesize==size.to_i&&output.read(1)=="\n"
    h=Digest::SHA256.hexdigest(data)
    matches=search['targets'].select{|r|r['sha256']==h}.map{|r|r['member']}
    definitions=[]
    if data.bytesize<200000&&!data.include?("\0")
      text=data.dup.force_encoding('UTF-8').scrub
      definitions=text.lines.select{|s|s.match?(/def _build_semantic_dataset|class MotifGenerator|class R26State|class R27State|SOCIAL_FAR|def smoke_r26/)}.map(&:strip)
    end
    rows<<{oid:id,bytes:data.bytesize,sha256:h,exact_matches:matches,behavior_definition_lines:definitions}
  end
  writer.join;error_reader.join;code=wait.value.exitstatus
end
raise code.to_s unless code==0
File.write(dest+'/GIT_ALL_BLOB_HASHES.json',JSON.pretty_generate({scope:'Every repository Git blob, reachable or unreachable, independently SHA256 hashed without executing contents.',blob_count:rows.size,total_bytes:rows.sum{|r|r[:bytes]},rows:rows})+"\n")
File.write(dest+'/git_deep_command.json',JSON.pretty_generate({argv:argv,cwd:repo,stdin_source:'logs/all_git_objects.stdout filtered to blob OIDs, in metadata order, newline terminated',stdin_sha256:Digest::SHA256.hexdigest(ids.join("\n")+"\n"),exit:code,stderr_sha256:Digest::SHA256.hexdigest(stderr),output_inventory_sha256:Digest::SHA256.file(dest+'/GIT_ALL_BLOB_HASHES.json').hexdigest})+"\n")
puts "all blobs=#{rows.size} bytes=#{rows.sum{|r|r[:bytes]}} exact matches=#{rows.count{|r|!r[:exact_matches].empty?}} behavior hits=#{rows.count{|r|!r[:behavior_definition_lines].empty?}}"
