require 'json';require 'digest'
d=File.realpath(__dir__);e='/Users/Shared/micah/Documents/TNN/TNN/Research/R33_FINAL_INTEGRATION_20260915T2145Z';todo=File.readlines(d+'/commands.jsonl').flat_map{|l|JSON.parse(l)['argv'].select{|a|a.end_with?('.zag')}}+Dir.glob(d+'/n19/sources/*.zag');pins={};unresolved=[]
until todo.empty?
 p=File.expand_path(todo.shift);next if pins[p];unless File.file?(p);unresolved<<p;next;end;pins[p]={path:p,bytes:File.size(p),sha256:Digest::SHA256.file(p).hexdigest};File.read(p).scan(/@import\("([^"]+)"\)/).flatten.each{|i|todo<<File.expand_path(i,File.dirname(p))}
end
File.write(d+'/SOURCE_INPUTS.json',JSON.pretty_generate({sources:pins.values,unresolved:unresolved.uniq,compiler:{path:'/Users/Shared/micah/Documents/zag/znc',sha256:Digest::SHA256.file('/Users/Shared/micah/Documents/zag/znc').hexdigest},scope:'Fresh command sources and literal transitive @import closure. Original frozen input and evidence manifest independently reverified.'}));puts "sources=#{pins.size} unresolved=#{unresolved.uniq.size}"
