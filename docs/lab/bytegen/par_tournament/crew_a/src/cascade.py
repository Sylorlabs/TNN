import struct
def read_mix(p):
    d = open(p,'rb').read()
    n = len(d)//4
    return struct.unpack('<%di'%n, d), n
clean, n = read_mix('runs/a_clean.mix')
SR = 44100
cases = {
  'single-bit': ('runs/a_f1.mix', 3*SR, 1),
  'burst':      ('runs/a_fb.mix', 10*SR, SR),
  'dropout':    ('runs/a_fd.mix', 10*SR, SR),
  'dc-shift':   ('runs/a_fdc.mix', 10*SR, SR),
}
for name,(p,fat,flen) in cases.items():
    f, nf = read_mix(p)
    assert nf == n, (name, nf, n)
    pre  = sum(1 for i in range(0,fat) if f[i]!=clean[i])
    win  = sum(1 for i in range(fat,fat+flen) if f[i]!=clean[i])
    post = sum(1 for i in range(fat+flen,n) if f[i]!=clean[i])
    print(f"{name:10s} pre={pre}/{fat} win={win}/{flen} post={post}/{n-fat-flen}")
