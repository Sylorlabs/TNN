"""Red-team live chat harness: drives redteam_bin in chat mode, checks responses."""
import subprocess, sys

def tok(i, saltC):
    n = 2 + (i % 4)
    return "".join(chr(97 + (i * 7 + k * saltC + k * k) % 26) for k in range(n))

def swapfl(s): return s[-1] + s[1:-1] + s[:1] if len(s) > 1 else s
def sortdesc(s): return "".join(sorted(s, reverse=True))
def duplast(s): return s + s[-1:]
def caesar(s): return "".join(chr(97 + (ord(c) - 97 + 1) % 26) for c in s)

class Chat:
    def __init__(self, binary):
        self.p = subprocess.Popen([binary, "chat"], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, text=True, bufsize=1)
        self.p.stdout.readline()  # discard "KB 0 ENT 0" banner
    def ask(self, line):
        self.p.stdin.write(line + "\n"); self.p.stdin.flush()
        return self.p.stdout.readline().rstrip("\n")
    def close(self):
        self.p.stdin.close(); self.p.wait()

def teach(chat, name, fn, idxs, salt):
    for i in idxs:
        x = tok(i, salt)
        chat.ask(f"the {name} of {x} is {fn(x)}.")

def probe_p0(chat, name, x, want):
    r = chat.ask(f"what is the {name} of {x}?")
    exp = f"A the {name} of {x} is {want}."
    ok = (r == exp)
    return ok, r, exp

def main():
    binary = sys.argv[1]
    report = []
    # 1) novel in-family rules with scrambled names, fresh tokens
    for name, fn in [("qzx", swapfl), ("vkb", sortdesc), ("mpl", duplast)]:
        chat = Chat(binary)
        teach(chat, name, fn, list(range(400, 406)) + list(range(900, 906)), 59)
        ok_n = 0; bad = []
        for i in range(406, 414):
            x = tok(i, 61)
            ok, r, exp = probe_p0(chat, name, x, fn(x))
            ok_n += ok
            if not ok: bad.append((x, r, exp))
        chat.close()
        report.append((f"novel-infamily {name}", ok_n, 8, bad[:3]))
    # 2) out-of-family: caesar(+1) should withhold (legacy answer, not engine-shaped)
    chat = Chat(binary)
    teach(chat, "zqw", caesar, list(range(400, 406)) + list(range(900, 906)), 59)
    withheld = 0; leaked = []
    for i in range(406, 414):
        x = tok(i, 61)
        r = chat.ask(f"what is the zqw of {x}?")
        if not r.startswith(f"A the zqw of {x} is "):
            withheld += 1
        else:
            leaked.append(r)
    chat.close()
    report.append(("out-of-family caesar withhold", withheld, 8, leaked[:3]))
    # 3) adversarial: swapfirst2 taught with 2-char examples only -> confident wrong?
    chat = Chat(binary)
    chat.ask("the jkp of ab is ba.")
    chat.ask("the jkp of cd is dc.")
    r = chat.ask("what is the jkp of abc?")
    report.append(("adversarial swapfirst2 2ex", r, "A the jkp of abc is bba. (confident-wrong demo)", []))
    # 4) then a 3rd example that kills all candidates -> withhold
    chat.ask("the jkp of abc is bac.")
    r2 = chat.ask("what is the jkp of def?")
    report.append(("adversarial swapfirst2 3ex", r2, "withhold expected (no consistent program)", []))
    chat.close()
    for name, got, want, bad in report:
        print(f"== {name}\n   got:  {got}\n   want: {want}")
        for b in bad: print(f"   ex: {b}")
    print("DONE")

if __name__ == "__main__":
    main()
