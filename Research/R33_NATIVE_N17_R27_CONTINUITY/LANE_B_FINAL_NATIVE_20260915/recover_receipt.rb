require 'json';require 'open3';require 'digest';require 'fileutils'
repo='/Users/Shared/micah/Documents/TNN/TNN';d=File.expand_path(__dir__);e=d+'/recovered';FileUtils.mkdir_p(e+'/logs');log=File.open(e+'/commands.jsonl','wx')
run=lambda do |label,args,expected=0|
 out,err,st=Open3.capture3(*args,chdir:repo);File.binwrite(e+'/logs/'+label+'.stdout',out);File.binwrite(e+'/logs/'+label+'.stderr',err)
 log.puts(JSON.generate({label:label,argv:args,cwd:repo,exit:st.exitstatus,expected:expected,stdout_sha256:Digest::SHA256.hexdigest(out),stderr_sha256:Digest::SHA256.hexdigest(err)}));log.flush
 raise label unless st.exitstatus==expected;puts "#{label}: #{st.exitstatus}";out
end
archive=repo+'/Research/tnn-pre-v1-r28-aeif-no-graph-shadow.zip';member='tnn-pre-v1-r28-aeif-no-graph-shadow/verification/r25_lineage_rerun.log'
bytes=run.call('exact_receipt_extract',['unzip','-p',archive,member]);File.binwrite(e+'/r25-lineage-historical-exact.json',bytes)
h=run.call('receipt_native_sha256',[d+'/native/project','--hash',e+'/r25-lineage-historical-exact.json']).strip
raise 'receipt admission' unless bytes.bytesize==508 && h=='e845db176e845244cb8127d6e96d424e04a30942f86b9d8061bf03b1851551a1'
tar=repo+'/Research/tnn-pre-v1-r28-aeif-no-graph-shadow.tar.gz'
tarbytes=run.call('tar_receipt_extract',['tar','-xOf',tar,member]);File.binwrite(e+'/r25-lineage-tar-exact.json',tarbytes)
raise 'archive copy mismatch' unless bytes==tarbytes
run.call('tar_receipt_native_sha256',[d+'/native/project','--hash',e+'/r25-lineage-tar-exact.json'])
File.write(e+'/RECEIPT_CUSTODY.json',JSON.pretty_generate({archive:archive,archive_sha256:Digest::SHA256.file(archive).hexdigest,member:member,tar_archive:tar,tar_archive_sha256:Digest::SHA256.file(tar).hexdigest,size:508,sha256:h,role:'HISTORICAL_WITNESS_ONLY',native_lineage_checks_recomputed:0,credit_to_R26_46:0,release_path_equivalence:'Exact bytes recovered through alternate R28 member. Original R27 release-root selector still not recovered; content witness custody only.'})+"\n")
known=JSON.parse(File.read(d+'/search/git_blobs.json'));done=known.map{|r|r['oid']};targets=JSON.parse(File.read(d+'/search/targets.json'))
rows=[]
File.readlines(d+'/search/logs/git_objects.stdout').each_with_index do |line,i|
 oid,type,n=line.split;next unless type=='blob' && !done.include?(oid)
 b=run.call('remaining_blob_'+i.to_s,['git','cat-file','blob',oid]);sha=Digest::SHA256.hexdigest(b)
 rows<<{oid:oid,size:n.to_i,sha256:sha,matches:targets.select{|t|t['sha256']==sha}.map{|t|t['name']}}
end
combined=JSON.parse(JSON.generate(known+rows))
File.write(e+'/ALL_GIT_BLOB_HASHES.json',JSON.pretty_generate(combined)+"\n")
File.write(e+'/SUMMARY.json',JSON.pretty_generate({all_git_blobs:combined.size,all_git_blob_bytes:combined.sum{|r|r['size']},exact_git_matches:combined.select{|r|!r['matches'].empty?},receipt_recovered:true,receipt_historical_only:true})+"\n")
log.close
