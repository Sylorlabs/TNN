require 'json';require 'open3';require 'digest'
e=File.expand_path('Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/N17_REFRESH')
j=JSON.parse(File.read(e+'/EVIDENCE.json'));r=JSON.parse(File.read(e+'/ROW_CLASSIFICATIONS.json'));v=JSON.parse(File.read(File.dirname(e)+'/V91_REFRESH/RECORD.json'))
raise 'row scope' unless r['rows'].size==80&&r['direct_static_passes']==50&&r['reviewed_inert_equivalent_passes']==4&&r['blocked_source_rows']==26
raise 'generation scope' unless v['generated_outputs']==0&&v['oracle_matches']==16&&v['generator_parity']==false
File.write(e+'/FINAL_PINS.sha256',j['files'].map{|f|"#{f['sha256']}  #{f['path']}"}.join("\n")+"\n")
log=File.open(e+'/final_verification_commands.jsonl','w')
run=lambda do |label,argv|
 out,err,st=Open3.capture3(*argv);File.write(e+'/logs/'+label+'.stdout',out);File.write(e+'/logs/'+label+'.stderr',err);File.write(e+'/logs/'+label+'.argv',argv.join("\n")+"\n");File.write(e+'/logs/'+label+'.exit',st.exitstatus.to_s+"\n")
 log.puts(JSON.generate({label:label,argv:argv,exit:st.exitstatus,stdout_sha256:Digest::SHA256.hexdigest(out),stderr_sha256:Digest::SHA256.hexdigest(err),role:'operational_final_receipt_and_preservation_validation'}));log.flush
 puts "#{label}: #{st.exitstatus}";raise label unless st.exitstatus==0
end
run.call('final_pins',['shasum','-a','256','-c',e+'/FINAL_PINS.sha256'])
repo='/Users/Shared/micah/Documents/TNN/TNN'
run.call('preserve_final_canonical',['shasum','-a','256','-c',repo+'/Research/R33_CLOSEOUT_20260915T174458Z/canonical.sha256'])
run.call('preserve_final_protected',['shasum','-a','256','-c',repo+'/Research/R33_CLOSEOUT_20260915T174458Z/protected.sha256'])
run.call('owned_diff_check',['git','-C',repo,'diff','--check','--','Research/R33_NATIVE_N17_R27_CONTINUITY'])
log.close
receipt={status:'LOCAL_EVIDENCE_AUDIT_FINISHED_FULL_CONTINUITY_AND_V91_FAIL_CLOSED',native_commands:j['commands'].size,native_pinned_files:j['files'].size,native_log_hashes:File.readlines(e+'/logs/log_hash_inventory.stdout').size,source_rows:80,direct_static_passes:50,reviewed_inert_equivalent_passes:4,blocked_source_rows:26,terminal_blockers:27,generator_outputs:0,oracle_strings:16,canonical_step:60423,newborn_restarts:0,exposure:0,authority:false,promotion:false,record:e+'/EVIDENCE.json',rows:e+'/ROW_CLASSIFICATIONS.json',input_pins:e+'/INPUT_ADMISSIONS_DEEP.json',v91:File.dirname(e)+'/V91_REFRESH/RECORD.json',sha256:{}}
[receipt[:record],receipt[:rows],receipt[:input_pins],receipt[:v91],e+'/FINAL_PINS.sha256',e+'/final_verification_commands.jsonl',File.dirname(e)+'/FINAL_REPORT.md'].each{|p|receipt[:sha256][p]=Digest::SHA256.file(p).hexdigest}
File.write(e+'/FINAL_RECEIPT.json',JSON.pretty_generate(receipt)+"\n")
puts JSON.generate(receipt.reject{|k,v|k==:sha256})
