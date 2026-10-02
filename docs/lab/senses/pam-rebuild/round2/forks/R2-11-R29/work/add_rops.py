#!/usr/bin/env python3
p = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-11-R29/src/forkB/r2-11b.zag"
s = open(p).read()

# 1. reset render-ops counter per trial (mode-independent -> B4 safe)
a = "    p64(S,0,0);p64(S,8,0);p64(S,16,0);p64(S,24,0);p64(S,32,0);\n"
assert s.count(a) == 1
s = s.replace(a, a + "    p64(S,70128,0);\n", 1)

# 2. open render_ops.tsv next to failed.tsv
b = '        nio_write_all(ffd,"trial\\ttask\\tfixture\\trc\\n");\n'
assert s.count(b) == 1, s.count(b)
c = (b + '        let qline:[]u8=path2(outdir,"render_ops.tsv");\n'
        '        let qcs:[]u8=nio_cstr(qline);\n'
        '        let qfd:i64=_zag_raw_syscall(2,_zag_slice_ptr(qcs) as i64,577,420,0,0,0);\n'
        '        nio_free(qcs);\n'
        '        if(qfd<0){_zag_println("ERR render_ops.tsv");return 1;}\n'
        '        nio_write_all(qfd,"trial\\trops\\n");\n')
s = s.replace(b, c, 1)

# 3. after the emit loop, record this trial's render ops (B4-safe: percepts.tsv untouched)
d = "            let nh:[]u8=ledger_step(S,prev,task,trial,do_emit);\n"
assert s.count(d) == 1
e = ('            // R2-11B B3: renderer ops for this trial (separate file; the\n'
     '            // percepts.tsv row stays mode-independent for B4)\n'
     '            let rops:i64=g64(S,70128);\n'
     '            let qb:[]u8=nio_alloc(512);\n'
     '            let qa:i32=0;\n'
     '            qa=b_put(qb,qa,trial);qa=b_put8(qb,qa,9);\n'
     '            qa=b_put_i64(qb,qa,rops);qa=b_put8(qb,qa,10);\n'
     '            nio_write_all(qfd,qb[0..qa]);\n' + d)
s = s.replace(d, e, 1)

# 4. close qfd with the others
f = "        _zag_raw_syscall(3,ffd,0,0,0,0,0);\n"
assert s.count(f) == 1
s = s.replace(f, f + "        _zag_raw_syscall(3,qfd,0,0,0,0,0);\n", 1)

open(p, "w").write(s)
print("rops accounting added")
