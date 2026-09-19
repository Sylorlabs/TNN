require 'json';require 'digest';require 'fileutils';require 'open3';require 'time'
R='/Users/Shared/micah/Documents/TNN/TNN';D=File.realpath(__dir__);E=R+'/Research/R33_FINAL_INTEGRATION_20260915T2145Z';T='/tmp/r33_final_push_20260915_1409';Dir.chdir(R)
raise 'requalification incomplete' unless JSON.parse(File.read(D+'/REQUAL_RESULT.json'))['unexpected']==[]
s=JSON.parse(File.read(D+'/EXACT_INPUT_SEARCH.json'));raise 'search errors' unless s['errors'].empty?
j=File.open(D+'/final.commands.jsonl','w')
def save(p);dst=D+'/before/'+p.sub(R+'/','').sub(T+'/','task/');FileUtils.mkdir_p(File.dirname(dst));FileUtils.cp(p,dst);end
def edit(p);save(p);File.write(p,yield(File.read(p)));end
# Current documentation only. Frozen/historical packets are immutable witnesses.
p=R+'/Research/R33_NATIVE_N17_R27_CONTINUITY/R26_VERIFIER_CHECK_MATRIX_V1.json'
edit(p){|v|v.gsub('exact receipt bytes are absent','exact 508-byte historical receipt recovered and hash-bound (e845db176e845244cb8127d6e96d424e04a30942f86b9d8061bf03b1851551a1), historical witness custody only')}
p=R+'/Research/R33_NATIVE_N17_R27_CONTINUITY/R25_LINEAGE_REQUIREMENTS.md'
edit(p){|v|v.sub('| R25 accepted policy/receipt | exact member path/bytes not recovered into N17 | absent |',"| R25 accepted policy | selected-release identity recorded; exact admitted bytes unresolved | unqualified within search scope |\n| R25 historical receipt | `e845db176e845244cb8127d6e96d424e04a30942f86b9d8061bf03b1851551a1`, 508 bytes | recovered at `../../R33_FINAL_INTEGRATION_20260915T2145Z/r25_custody/historical_receipt.json`; witness only |")+"\n2026-09-15 remediation: exact receipt custody is closed; complete native 68-check lineage, selected-release/source/input identities and retained-object selectors remain fail-closed. Fresh admission refuses missing inputs66 and wrong hashes1. Deep loose-file, archive-member and reachable/unreachable Git search is frozen in `../../R33_REMEDIATION_FINAL_20260915/EXACT_INPUT_SEARCH.json`; absence is confined to its explicit scope exclusions.\n"}
p=R+'/Research/R33_NATIVE_N17_R27_CONTINUITY/IMPLEMENTATION_DECISION.md'
edit(p){|v|v.sub('The rationale below is retained',"2026-09-15 final remediation supersedes the preceding audit counts: 54 scoped engineering rows (50 static and four inert identity/class equivalents) pass; 26 remain blocked (five R27, 21 R26). The isolated compatibility import/constant gap is repaired. Complete R25 lineage remains blocked by exact input/source/release bindings and unimplemented full lineage semantics. Exact historical receipt custody is closed, with no native lineage credit. V91 generates zero strings. Fresh original qualification and refusals: `../../R33_REMEDIATION_FINAL_20260915/REQUAL_RESULT.json`.\n\nThe rationale below is retained")}
rows=JSON.parse(File.read(T+'/reviewer_evidence/N17_REVIEWED_ROWS.json'))
rows.each do |row|
 if row['fresh_check']
  p=D+'/'+File.basename(row['fresh_log']);raise "missing #{p}" unless File.file?(p);h=Digest::SHA256.file(p).hexdigest;raise "row mismatch #{row['id']}" unless h==row['fresh_sha256'];row['fresh_log']=p
 end
 row['blocker']=row['blocker'].gsub('exact receipt bytes are absent','exact historical receipt bytes recovered and hash-bound; custody only') if row['blocker'].is_a?(String)
end
File.write(D+'/N17_REQUALIFIED_ROWS.json',JSON.pretty_generate(rows))
commands=File.readlines(D+'/commands.jsonl').map{|l|JSON.parse(l)}
commands.each{|c|%w[stdout stderr].each{|v|raise "command hash #{c['label']}" unless Digest::SHA256.file(D+'/'+c['label']+'.'+v).hexdigest==c[v+'_sha256']}}
# Freeze consumed native source trees and original qualification controls without changing their import bindings.
([E+'/n17_fresh',E+'/v91_fresh',E+'/sources',R+'/Research/R33_CONTINUING_LIFE_V1'].flat_map{|q|Dir.glob(q+'/**/*.zag')}+Dir.glob(E+'/*.zag')+Dir.glob(R+'/Research/R33_NATIVE*.zag')).uniq.each do |p|
 dst=D+'/source_witness/'+p.sub(R+'/','');FileUtils.mkdir_p(File.dirname(dst));FileUtils.cp(p,dst)
end
n19=Dir.glob(D+'/n19/logs/*.command').sort.map do |p|
 stem=p.sub(/\.command\z/,''); %w[exit stdout stderr].each{|x|raise "missing N19 #{stem}.#{x}" unless File.file?(stem+'.'+x)}
 {command:File.read(p),exit:File.read(stem+'.exit').strip.to_i,stdout_sha256:Digest::SHA256.file(stem+'.stdout').hexdigest,stderr_sha256:Digest::SHA256.file(stem+'.stderr').hexdigest}
end
raise 'N19 count' unless n19.length==98
Dir.glob(D+'/n19/*results*.txt').each{|p|File.readlines(p).each{|l|m=l.match(/expected=(\d+) actual=(\d+)/);raise "N19 unexpected #{l}" if m&&m[1]!=m[2]}}
File.write(D+'/N19_COMMANDS.json',JSON.pretty_generate(n19))
File.write(D+'/manifest.verify.command',"shasum -a 256 -c #{D}/SHA256SUMS\ncwd=#{R}\n")
File.write(D+'/seal.verify.command',"shasum -a 256 -c #{D}/SEAL.sha256\ncwd=#{R}\n")
record={schema:'R33_FINAL_REMEDIATION_V1',dated_utc:Time.now.utc.iso8601,status:'SAFE_REQUEST_CHANGES_IMPLEMENTED_SCIENTIFIC_GATES_FAIL_CLOSED',r33_complete:false,native_zag_only:true,python_executed:false,foreign_ml_runtime_executed:false,scientific_exposure:0,exposure_scope:'This remediation lane only; historical consumed exposures preserved.',learner_authority_granted:false,learn_opened:false,successor_promoted:false,canonical_r27_mutated:false,canonical_r27:{development_step:60423,newborn_restarts:0},qualification_commands:commands.length,unexpected_exits:0,n17_rows:80,n17_scoped_passes:54,n17_blocked:26,v91_generated:0,search_counts:s['counts'],search_exclusions:s['exclusions'],closed_changes:['Current stale R25 receipt wording corrected; exact receipt remains witness only','Integrator and reviewer current final-text custody seals reconciled; prior seals preserved','Affected original native qualifications rerun and source/output evidence frozen','All 80 row classifications reconciled; original scoped output hashes match'],open_changes:['V91 exact dataset/42-D assembly and sampling/forward semantics; native all16 generation','26 N17 full verifier-equivalence rows','R25 exact selected-release inputs/source/selectors and complete native68-check lineage','Full mutation fixture/freeze/preregistration/reservation/admission/terminal continuity and scientific campaign prerequisites'],scope_exclusions:JSON.parse(File.read(R+'/R33_FINAL_CLOSEOUT.json'))['scope_exclusions'],historical_integrator_manifest:'Verified 6536 entries and SEAL.sha256 exit0; preserved unchanged',historical_final_seal_mismatches:['Integrator final text','Reviewer final text'],no_new_compiler_promotion:true}
File.write(D+'/REMEDIATION_STATUS.json',JSON.pretty_generate(record))
%w[R33_FINAL_CLOSEOUT.json Research/R33_FINAL_CLOSEOUT.json].each do |rel|
 edit(R+'/'+rel){|v|a=JSON.parse(v);a['remediation']={status:record[:status],record:'Research/R33_REMEDIATION_FINAL_20260915/REMEDIATION_STATUS.json',commands:'Research/R33_REMEDIATION_FINAL_20260915/commands.jsonl',search:'Research/R33_REMEDIATION_FINAL_20260915/EXACT_INPUT_SEARCH.json',r33_complete:false,scientific_exposure:0,authority:false};JSON.pretty_generate(a)+"\n"}
end
%w[Research/R33_HANDOFF.md Research/NEXT_AGENT_START_HERE.md].each do |rel|
 edit(R+'/'+rel){|v|v+"\n## Final remediation, 2026-09-15\n\nSafe reviewer changes and affected original native qualifications are complete. Evidence/status: [R33 remediation](R33_REMEDIATION_FINAL_20260915/REMEDIATION_STATUS.json). Current R25 receipt wording and task final-text custody seals are reconciled; old frozen packets remain historical witnesses. Fresh scoped engineering qualification passes, with 54/80 N17 rows and 26 blocked; V91 generates 0/16. Complete R25 lineage and full continuity/fixture/admission/scientific prerequisites remain fail-closed. Exact-input absence is scoped to the new deep search and its exclusions. Stable compiler retained; canonical R27 step60423/restarts0 preserved; this lane exposure0, authority=false, learn refused65, no successor promotion. Earlier consumed exposure counters and registries remain unchanged.\n"}
end
# Preserve text and update current task seals, never silently overwrite the failed prior seals.
%w[integrator reviewer].each do |n|
 p=T+'/'+n+'.seal.sha256';save(p);v=File.read(p).lines.map{|l|sha,path=l.strip.split(/\s+/,2);raise path unless File.file?(path);"#{Digest::SHA256.file(path).hexdigest}  #{path}\n"}.join;File.write(p,v)
end
[[E,'old_manifest_final',['shasum','-a','256','-c','SHA256SUMS']], [E,'old_seal_final',['shasum','-a','256','-c','SEAL.sha256']], [R,'immutable_final',['shasum','-a','256','-c',E+'/immutable.before.sha256']], [R,'integrator_current_seal',['shasum','-a','256','-c',T+'/integrator.seal.sha256']], [R,'reviewer_current_seal',['shasum','-a','256','-c',T+'/reviewer.seal.sha256']]].each do |cwd,n,a|
 o,e,s=Open3.capture3(*a,chdir:cwd);File.binwrite(D+'/'+n+'.stdout',o);File.binwrite(D+'/'+n+'.stderr',e);j.puts(JSON.generate({argv:a,cwd:cwd,exit:s.exitstatus,signal:s.termsig,stdout_sha256:Digest::SHA256.hexdigest(o),stderr_sha256:Digest::SHA256.hexdigest(e)}));raise n unless s.success?
end
j.close
File.write(D+'/FREEZE.json',JSON.pretty_generate({schema:'R33_REMEDIATION_EVIDENCE_FREEZE_V1',dated_utc:Time.now.utc.iso8601,record_sha256:Digest::SHA256.file(D+'/REMEDIATION_STATUS.json').hexdigest,manifest:'SHA256SUMS',exclusions:['SHA256SUMS','SEAL.sha256','manifest.verify.stdout','manifest.verify.stderr','manifest.verify.exit','seal.verify.stdout','seal.verify.stderr','seal.verify.exit'],historical_packets_unchanged:true,authority:false,exposure:0,r33_complete:false}))
final="Safe REQUEST_CHANGES items implemented and freshly verified. Current receipt wording corrected; integrator/reviewer final-text seals reconciled with prior seals preserved. Original native qualifications pass within bounded scope; all80 N17 rows reconciled (54 scoped passes,26 blocked). V91 generates0/16; complete R25 lineage and scientific prerequisites remain fail-closed. Deep exact-input search and exclusions are frozen. Canonical R27 60423/0, stable compiler and consumed registries preserved; lane exposure0, authority=false; no learning or promotion.\n\nEvidence: #{D}/REMEDIATION_STATUS.json; exact argv/exit/output hashes: commands.jsonl and final.commands.jsonl; N19 per-command logs under n19/logs. Hash freeze: SHA256SUMS and SEAL.sha256.\n"
File.write(T+'/remediator.final',final)
exclude=%w[SHA256SUMS SEAL.sha256 manifest.verify.stdout manifest.verify.stderr manifest.verify.exit seal.verify.stdout seal.verify.stderr seal.verify.exit]
File.open(D+'/SHA256SUMS','w'){|f|Dir.glob(D+'/**/*',File::FNM_DOTMATCH).sort.each{|p|next unless File.file?(p);next if exclude.include?(p.sub(D+'/',''));f.puts "#{Digest::SHA256.file(p).hexdigest}  #{p}"};%w[R33_FINAL_CLOSEOUT.json Research/R33_FINAL_CLOSEOUT.json Research/R33_HANDOFF.md Research/NEXT_AGENT_START_HERE.md Research/R33_NATIVE_N17_R27_CONTINUITY/R26_VERIFIER_CHECK_MATRIX_V1.json Research/R33_NATIVE_N17_R27_CONTINUITY/R25_LINEAGE_REQUIREMENTS.md Research/R33_NATIVE_N17_R27_CONTINUITY/IMPLEMENTATION_DECISION.md].each{|p|f.puts "#{Digest::SHA256.file(R+'/'+p).hexdigest}  #{R}/#{p}"};f.puts "#{Digest::SHA256.file(T+'/remediator.final').hexdigest}  #{T}/remediator.final"}
o,e,s=Open3.capture3('shasum','-a','256','-c',D+'/SHA256SUMS');File.write(D+'/manifest.verify.stdout',o);File.write(D+'/manifest.verify.stderr',e);File.write(D+'/manifest.verify.exit',s.exitstatus.to_s+"\n");raise 'freeze verification' unless s.success?
File.open(D+'/SEAL.sha256','w'){|f|%w[SHA256SUMS FREEZE.json REMEDIATION_STATUS.json manifest.verify.stdout manifest.verify.stderr manifest.verify.exit].each{|p|f.puts "#{Digest::SHA256.file(D+'/'+p).hexdigest}  #{D}/#{p}"}}
o,e,s=Open3.capture3('shasum','-a','256','-c',D+'/SEAL.sha256');File.write(D+'/seal.verify.stdout',o);File.write(D+'/seal.verify.stderr',e);File.write(D+'/seal.verify.exit',s.exitstatus.to_s+"\n");raise 'seal' unless s.success?
puts final
