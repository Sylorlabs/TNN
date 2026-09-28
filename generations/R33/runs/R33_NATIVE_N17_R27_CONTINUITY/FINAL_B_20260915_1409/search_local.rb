require 'json'
require 'open3'
require 'digest'
require 'fileutils'
repo = '/Users/Shared/micah/Documents/TNN/TNN'
base = repo + '/Research/R33_NATIVE_N17_R27_CONTINUITY'
dest = File.expand_path(__dir__) + '/recovery'
FileUtils.mkdir_p(dest + '/logs')
journal = File.open(dest + '/commands.jsonl', 'wx')
run = lambda do |label, args, allowed = [0]|
  out, err, st = Open3.capture3(*args, chdir: repo)
  File.binwrite(dest + '/logs/' + label + '.stdout', out); File.binwrite(dest + '/logs/' + label + '.stderr', err)
  journal.puts(JSON.generate({label: label, argv: args, cwd: repo, exit: st.exitstatus, allowed: allowed, stdout_sha256: Digest::SHA256.hexdigest(out), stderr_sha256: Digest::SHA256.hexdigest(err)})); journal.flush
  raise label unless allowed.include?(st.exitstatus)
  out
end
index = JSON.parse(File.read(base + '/SOURCE_REFERENCE_INDEX.json'))
targets = index['original_members'].map { |r| {member: r['path'], bytes: r['size_bytes'], sha256: r['sha256']} }
targets += [
  {member:'r23_experiments.py',bytes:63069,sha256:'517eb325096d5ae71ebb3bf659da77eac4266129136b888b469a99e366d4b642'},
  {member:'r23-accepted-state.pkl',bytes:7028883,sha256:'fc24881f104052c09a4cb6e596b01ae5c107d9ae0356c8799ec97eff3edf440b'},
  {member:'r23_summary.json',bytes:29242,sha256:'74cdb944e1037e92100d0dee2eca6ffaebcabe53346bb114c4bd09b035e3a495'},
  {member:'r26-accepted-state.pkl',bytes:nil,sha256:'df3acde273aa682642d13763a24208ff1dbb42968313cbe2a4256f7ccbc1f839'}]
rows = []
check = lambda do |locator, bytes|
  digest = Digest::SHA256.hexdigest(bytes)
  matched = targets.select { |r| r[:sha256] == digest }.map { |r| r[:member] }
  rows << {locator: locator, bytes: bytes.bytesize, sha256: digest, exact_matches: matched}
end
paths = run.call('all_local_paths', ['rg','--files','--hidden','--no-ignore',repo,'/Users/Shared/micah/Documents/zag'],[0,2]).lines.map(&:chomp)
paths.each do |path|
  next if path.start_with?(File.expand_path(__dir__) + '/') || path.include?('/.git/') || !File.file?(path)
  size = File.size(path)
  if targets.any? { |r| r[:bytes] == size } || path.match?(/(?:r2[3567].*(?:\.py|\.pkl|\.json)|MANIFEST\.sha256|verify_r2[3567]|smoke_r26)/i)
    check.call(path, File.binread(path)) if size <= 80000000
  end
end
archives = paths.select { |p| p.match?(/\.(?:zip|tar|tar\.gz|tgz|tar\.xz)\z/i) && !p.include?('/node_modules/') && !p.include?('/.git/') }.uniq
archive_rows = []
archives.each_with_index do |path, i|
  zip = path.end_with?('.zip')
  listing = run.call("archive_#{i}_list", zip ? ['unzip','-Z1',path] : ['tar','-tf',path],[0,1])
  members = listing.lines.map(&:chomp)
  selected = members.select { |m| m.match?(/(?:r2[3567].*(?:\.py|\.pkl|\.json)|MANIFEST\.sha256|verify_r2[3567]|smoke_r26|\.(?:mp4|avi|mov|wav|flac)\z)/i) && !m.end_with?('/') }
  selected.each_with_index do |member, k|
    bytes = run.call("archive_#{i}_member_#{k}", zip ? ['unzip','-p',path,member] : ['tar','-xOf',path,member],[0])
    check.call(path + '::' + member, bytes)
  end
  archive_rows << {path: path, bytes: File.size(path), sha256: Digest::SHA256.file(path).hexdigest, member_count: members.size, selected_members: selected}
  puts "archive #{i+1}/#{archives.size}"
end
metadata = run.call('all_git_objects', ['git','cat-file','--batch-all-objects','--batch-check=%(objectname) %(objecttype) %(objectsize)'])
metadata.lines.each do |line|
  oid, type, size = line.split
  next unless type == 'blob' && targets.any? { |r| r[:bytes] == size.to_i }
  bytes = run.call('git_blob_' + oid, ['git','cat-file','blob',oid])
  check.call('git:blob:' + oid, bytes)
end
behavior_paths = run.call('full_behavior_definitions', ['rg','--hidden','--no-ignore','-l','def _build_semantic_dataset|class MotifGenerator|def smoke_r26|def resolve|SOCIAL_FAR',repo,'-g','*.py','-g','*.txt','-g','!**/*diff*'],[0,1,2])
result = {scope:'All rg-enumerated repository and local Zag paths including ignored/hidden files; selected inert archive members; all reachable/unreachable Git blobs at known exact target sizes. No historical code or serialized reducers executed.', file_count: paths.size, git_object_count: metadata.lines.size, targets: targets.map { |r| r.merge(exact_locations: rows.select { |x| x[:exact_matches].include?(r[:member]) }.map { |x| x[:locator] }) }, archives: archive_rows, checked_candidates: rows, behavior_definition_candidates: behavior_paths.lines.map(&:chomp), exclusions:['Other user directories not newly enumerated; prior terminal supplement covers those roots.','Git blobs with unknown required byte length and unrecognized file names are not exhaustively content-hashed.','Archive selection is by original member names and media extensions; arbitrary renamed nested payloads are not proven absent.']}
File.write(dest + '/SEARCH.json',JSON.pretty_generate(result)+"\n")
journal.close
puts "files=#{paths.size}; objects=#{metadata.lines.size}; candidates=#{rows.size}; matches=#{rows.count{|r|!r[:exact_matches].empty?}}"
