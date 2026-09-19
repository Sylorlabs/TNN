require 'json';require 'open3';require 'digest';require 'fileutils'
repo='/Users/Shared/micah/Documents/TNN/TNN';d=File.expand_path(__dir__);e=d+'/verification';FileUtils.mkdir_p(e);log=File.open(e+'/commands.jsonl','wx')
run=lambda do |label,args|
 out,err,st=Open3.capture3(*args,chdir:repo);File.binwrite(e+'/'+label+'.stdout',out);File.binwrite(e+'/'+label+'.stderr',err)
 log.puts(JSON.generate({label:label,argv:args,cwd:repo,exit:st.exitstatus,expected:0,stdout_sha256:Digest::SHA256.hexdigest(out),stderr_sha256:Digest::SHA256.hexdigest(err)}));log.flush
 raise label unless st.success?;puts "#{label}: 0";out
end
run.call('frozen_packet',['shasum','-a','256','-c',d+'/SHA256SUMS'])
%w[canonical protected].each{|n|run.call(n,['shasum','-a','256','-c',repo+'/Research/R33_CLOSEOUT_20260915T174458Z/'+n+'.sha256'])}
c=run.call('compiler',['shasum','-a','256','/Users/Shared/micah/Documents/zag/znc']);raise 'compiler pin' unless c.start_with?('3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956 ')
run.call('owned_whitespace',['git','diff','--check','--','Research/R33_NATIVE_N17_R27_CONTINUITY'])
run.call('git_status',['git','status','--short'])
v=JSON.parse(File.read(d+'/v91/RECORD.json'))
table=v['files'];raise 'native file manifest absent' unless table.is_a?(Array)
table.each{|f|raise 'native record pin '+f['path'] unless Digest::SHA256.file(f['path']).hexdigest==f['sha256']}
r=JSON.parse(File.read(d+'/ROWS.json'));raise 'row counts' unless r['rows'].size==80 && r['counts']['blocked_source_rows']==26
raise 'V91 row scope' unless JSON.parse(File.read(d+'/V91_ROWS.json'))['rows'].size==16 && v['generated_outputs']==0
raise 'canonical scalar observations' unless File.read(d+'/native/logs/rows.stdout').include?('B_ROW,R27-04,PASS,375762,3') && File.read(d+'/native/logs/rows.stdout').include?('B_ROW,R27-03,PASS,375763,3')
log.close
receipt={status:'FROZEN_NATIVE_PACKET_HASHES_ACCOUNTING_AND_CANONICAL_PINS_PASS',full_verifier_equivalent_continuity:'FAIL_CLOSED',native_record_file_pins:table.size,manifest_sha256:Digest::SHA256.file(d+'/SHA256SUMS').hexdigest,final_json_sha256:Digest::SHA256.file(d+'/FINAL.json').hexdigest,verification_journal_sha256:Digest::SHA256.file(e+'/commands.jsonl').hexdigest}
File.write(e+'/RESULT.json',JSON.pretty_generate(receipt)+"\n")
puts JSON.generate(receipt)
