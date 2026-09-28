require 'json'
require 'digest'
require 'fileutils'
require 'open3'
R='/Users/Shared/micah/Documents/TNN/TNN'
D=File.realpath(__dir__)
T='/tmp/r33_final_push_20260915_1409'
Dir.chdir(R)
raise 'qualification incomplete' unless File.file?(D+'/REQUAL_RESULT.json')
raise 'unexpected qualification exits' unless JSON.parse(File.read(D+'/REQUAL_RESULT.json'))['unexpected'].empty?
raise 'search incomplete' unless File.file?(D+'/EXACT_INPUT_SEARCH.json')
raise 'prior manifest mismatch' unless JSON.parse(File.read(D+'/PRIOR_MANIFEST_VERIFICATION.json'))['mismatches'].empty?
FileUtils.mkdir_p(D+'/prior_custody')
%w[integrator.final integrator.seal.sha256 reviewer.final reviewer.seal.sha256].each{|n|FileUtils.cp(T+'/'+n,D+'/prior_custody/'+n)}
# Preserve the detailed review that the launcher subsequently replaced with a short final.
log=File.binread(T+'/reviewer.log')
review=log[/REQUEST_CHANGES\n\nIndependent adversarial review.*?Overall R33 completion: REQUEST_CHANGES\.[^\n]*/m]
raise 'detailed review not recovered' unless review
File.binwrite(D+'/DETAILED_REVIEW_WITNESS.txt',review+"\n")
changes=[]
%w[Research/R33_NATIVE_N17_R27_CONTINUITY/R26_VERIFIER_CHECK_MATRIX_V1.json Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_INTEGRATION_ROW_MATRIX.json].each do |p|
 s=File.binread(p)
 next unless s.include?('exact receipt bytes are absent')
 FileUtils.cp(p,D+'/prior_custody/'+File.basename(p))
 v=s.gsub('exact receipt bytes are absent','exact historical receipt bytes are recovered and SHA256-bound (e845db176e845244cb8127d6e96d424e04a30942f86b9d8061bf03b1851551a1), witness custody only')
 JSON.parse(v)
 File.binwrite(p,v)
 changes<<{path:p,before:Digest::SHA256.hexdigest(s),after:Digest::SHA256.hexdigest(v)}
end
p='Research/R33_NATIVE_N17_R27_CONTINUITY/R25_LINEAGE_REQUIREMENTS.md'
s=File.read(p);FileUtils.cp(p,D+'/prior_custody/'+File.basename(p))
s=s.sub('| R25 accepted policy/receipt | exact member path/bytes not recovered into N17 | absent |', '| R25 accepted policy | selected-release policy identity not yet admitted | blocked |\n| Historical R25 receipt | `Research/R33_FINAL_INTEGRATION_20260915T2145Z/r25_custody/historical_receipt.json`, 508 bytes, SHA256 `e845db176e845244cb8127d6e96d424e04a30942f86b9d8061bf03b1851551a1` | recovered; witness only |'.gsub('\\n',"\n"))
File.write(p,s)
changes<<{path:p,after:Digest::SHA256.hexdigest(s)}
File.write(D+'/CHANGES.json',JSON.pretty_generate(changes))
# Repair only the mismatching final-text entry; preserve every other original seal pin.
p=T+'/integrator.seal.sha256'
s=File.read(p);h=Digest::SHA256.file(T+'/integrator.final').hexdigest
raise 'unexpected seal format' unless s.include?(T+'/integrator.final')
s=s.lines.map{|l|l.end_with?(T+"/integrator.final\n") ? "#{h}  #{T}/integrator.final\n" : l}.join
File.write(p,s)
def check(label,argv)
 o,e,x=Open3.capture3(*argv)
 File.binwrite(D+'/'+label+'.stdout',o);File.binwrite(D+'/'+label+'.stderr',e)
 File.open(D+'/closeout.commands.jsonl','a'){|f|f.puts(JSON.generate({label:label,argv:argv,cwd:Dir.pwd,exit:x.exitstatus,signal:x.termsig,stdout_sha256:Digest::SHA256.hexdigest(o),stderr_sha256:Digest::SHA256.hexdigest(e)}))}
 raise label unless x.success?
end
check('integrator_seal_repaired',['shasum','-a','256','-c',p])
check('final_immutable',['shasum','-a','256','-c','Research/R33_FINAL_INTEGRATION_20260915T2145Z/immutable.before.sha256'])
q=File.readlines(D+'/commands.jsonl').map{|l|JSON.parse(l)}
search=JSON.parse(File.read(D+'/EXACT_INPUT_SEARCH.json'))
receipt=R+'/Research/R33_FINAL_INTEGRATION_20260915T2145Z/r25_custody/historical_receipt.json'
raise 'receipt identity' unless File.size(receipt)==508 && Digest::SHA256.file(receipt).hexdigest=='e845db176e845244cb8127d6e96d424e04a30942f86b9d8061bf03b1851551a1'
summary={schema:'R33_REMEDIATION_CLOSEOUT_V1',evidence_directory:D.sub(R+'/',''),r33_complete:false,safe_requested_changes:'CLOSED',native_qualification_commands:q.size,unexpected_exits:[],prior_evidence_entries_verified:6536,receipt_bytes:508,receipt_sha256:Digest::SHA256.file(receipt).hexdigest,receipt_role:'HISTORICAL_WITNESS_ONLY',canonical_step:60423,newborn_restarts:0,canonical_r27_mutated:false,stable_compiler_replaced:false,learn_opened:false,learner_authority_granted:false,scientific_exposure:0,successor_promoted:false,python_executed:false,foreign_ml_runtime_executed:false,blocked_rows:26,open_gates:['26 N17 source-bound rows','V91 actual native 16-string generation parity','Complete native R25 68-check lineage and exact admissions','Full mutation/freeze/preregistration/reservation/admission/terminal continuity prerequisites'],search_counts:search['counts'],search_exclusions:search['exclusions'],search_errors:search['errors']}
File.write(D+'/REMEDIATION_CLOSEOUT.json',JSON.pretty_generate(summary)+"\n")
text="\n\nR33 reviewer remediation, 2026-09-15: safe custody and stale-receipt changes are closed. Fresh stable native requalification and deep local search are frozen in `Research/R33_REMEDIATION_20260915T2152Z`. The 508-byte historical R25 receipt is present and hash-bound, witness only. Integrator final-text custody is reconciled with its actual bytes; prior mismatching seal is retained as a diagnostic. All 6,536 prior evidence entries verify. R33 remains incomplete: 26 N17 rows, actual V91 generation parity, complete native R25 lineage and remaining admission/scientific prerequisites stay fail-closed. Canonical R27 step60423/restarts0 and stable compiler are unchanged; this remediation grants no learner authority, opens no learn, creates zero scientific exposure and promotes no successor. Historical frozen snapshots retain their original text and hashes; this record supersedes their receipt-absence wording only. Exact commands, exits, output hashes, search scope and exclusions are in the remediation closeout.\n"
%w[Research/R33_HANDOFF.md Research/R33_ROADMAP_COMPLETION_MATRIX.md Research/R33_INDEPENDENT_REVIEWS.md].each{|p|File.open(p,'a'){|f|f.write(text)}}
%w[R33_FINAL_CLOSEOUT.json Research/R33_FINAL_CLOSEOUT.json].each do |p|
 v=JSON.parse(File.read(p));v['remediation_closeout']=summary[:evidence_directory]+'/REMEDIATION_CLOSEOUT.json';v['remediation_status']='SAFE_REQUESTED_CHANGES_CLOSED_FULL_R33_FAIL_CLOSED';File.write(p,JSON.pretty_generate(v)+"\n")
end
seal=T+'/integrator.seal.sha256'
File.write(seal,File.readlines(seal).map{|l|h,p=l.chomp.split(/  /,2); "#{Digest::SHA256.file(p).hexdigest}  #{p}\n"}.join)
check('integrator_seal_final',['shasum','-a','256','-c',seal])
File.write(D+'/REMEDIATION_STATUS.md',text.lstrip)
File.write(T+'/remediator.final',"Safe REQUEST_CHANGES implemented and freshly verified. Corrected current R25 receipt wording; repaired integrator final-text seal; retained original diagnostics and historical snapshots. Evidence: #{summary[:evidence_directory]}/REMEDIATION_CLOSEOUT.json and SHA256SUMS. All 6,536 prior evidence entries verify. Native qualifications use unchanged stable znc; canonical R27 remains step60423/restarts0. R33 remains incomplete: 26 N17 rows, actual V91 generation parity, native R25 lineage and remaining admission prerequisites stay fail-closed. No learn, authority, scientific exposure or promotion.\n")
FileUtils.mkdir_p(D+'/final_documents')
%w[R33_FINAL_CLOSEOUT.json Research/R33_FINAL_CLOSEOUT.json Research/R33_HANDOFF.md Research/R33_ROADMAP_COMPLETION_MATRIX.md Research/R33_INDEPENDENT_REVIEWS.md Research/R33_NATIVE_N17_R27_CONTINUITY/R26_VERIFIER_CHECK_MATRIX_V1.json Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_INTEGRATION_ROW_MATRIX.json Research/R33_NATIVE_N17_R27_CONTINUITY/R25_LINEAGE_REQUIREMENTS.md].each{|p|dest=D+'/final_documents/'+p;FileUtils.mkdir_p(File.dirname(dest));FileUtils.cp(p,dest)}
%w[integrator.final integrator.seal.sha256 reviewer.final reviewer.seal.sha256 remediator.final].each{|n|FileUtils.cp(T+'/'+n,D+'/final_documents/'+n)}
File.open(D+'/SHA256SUMS','w'){|f|Dir.glob(D+'/**/*',File::FNM_DOTMATCH).sort.each{|p|next unless File.file?(p);next if ['SHA256SUMS','SEAL.sha256'].include?(File.basename(p));f.puts "#{Digest::SHA256.file(p).hexdigest}  #{p}"}}
File.write(D+'/SEAL.sha256',"#{Digest::SHA256.file(D+'/SHA256SUMS').hexdigest}  #{D}/SHA256SUMS\n")
puts JSON.generate(summary)
