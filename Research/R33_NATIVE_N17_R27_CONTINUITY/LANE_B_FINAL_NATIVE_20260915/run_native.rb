require 'json'
require 'open3'
require 'digest'
require 'fileutils'
# Local orchestration only. All parent parsing, predicates and digests run Zag.
repo = '/Users/Shared/micah/Documents/TNN/TNN'
base = repo + '/Research/R33_NATIVE_N17_R27_CONTINUITY'
dest = File.expand_path(__dir__)
FileUtils.mkdir_p(dest + '/native/logs')
journal = File.open(dest + '/native/commands.jsonl', 'wx')
run = lambda do |label, argv, expected = 0|
  out, err, status = Open3.capture3(*argv, chdir: repo)
  %w[stdout stderr].zip([out, err]).each { |ext, bytes| File.binwrite(dest + '/native/logs/' + label + '.' + ext, bytes) }
  journal.puts(JSON.generate({label: label, argv: argv, cwd: repo, exit: status.exitstatus, expected: expected, stdout_sha256: Digest::SHA256.hexdigest(out), stderr_sha256: Digest::SHA256.hexdigest(err)})); journal.flush
  puts "#{label}: #{status.exitstatus}"
  raise label unless status.exitstatus == expected
  out
end
%w[canonical protected].each { |x| run.call(x + '_before', ['shasum', '-a', '256', '-c', repo + '/Research/R33_CLOSEOUT_20260915T174458Z/' + x + '.sha256']) }
compiler = '/Users/Shared/micah/Documents/zag/znc'
run.call('compiler_before', ['shasum', '-a', '256', compiler])
flags = ['--target', 'macos-arm64', '--no-zagd', '--no-analyze', '--no-foreground-cache']
project = dest + '/native/project'
run.call('build_project', [compiler, base + '/V91_SEMANTIC_KAT/v91_project_native.zag', *flags, '-o', project])
sources = {'rows'=>'LANE_B_AUDIT_20260915/rows.zag', 'structure'=>'LANE_B_AUDIT_20260915/structure.zag', 'primitives'=>'LANE_B_AUDIT_20260915/primitives.zag', 'r26'=>'r26_digest.zag', 'r27'=>'r27_digest.zag', 'identity'=>'RECOVERY_20260915_B_INDEPENDENT/review_native.zag', 'memo'=>'RECOVERY_20260915_B_INDEPENDENT/memo_negative.zag'}
sources.each do |label, relative|
  expanded = dest + '/native/' + label + '.zag'
  provenance = dest + '/native/' + label + '.provenance'
  run.call('project_' + label, [project, base + '/' + relative, expanded, provenance])
  File.readlines(provenance, chomp: true).each do |line|
    words = line.split("\t")
    next unless words[0] == 'FILE'
    path = words[2]
    target = dest + '/native/import_closure/' + path
    FileUtils.mkdir_p(File.dirname(target)); FileUtils.cp(path, target)
  end
  run.call('build_' + label, [compiler, expanded, *flags, '-o', dest + '/native/' + label])
end
%w[rows structure primitives identity memo].each { |x| run.call(x, [dest + '/native/' + x]) }
run.call('r26_selftest', [dest + '/native/r26', 'selftest'])
r26 = run.call('r26_digest', [dest + '/native/r26', 'digest'])
raise 'r26 comparison' unless r26.include?('44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649')
r27 = run.call('r27_digest', [dest + '/native/r27', 'digest'])
raise 'r27 comparison' unless r27.include?('562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04')
%w[canonical protected].each { |x| run.call(x + '_after', ['shasum', '-a', '256', '-c', repo + '/Research/R33_CLOSEOUT_20260915T174458Z/' + x + '.sha256']) }
run.call('compiler_after', ['shasum', '-a', '256', compiler])
journal.close
