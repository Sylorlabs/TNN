#!/usr/bin/env python3
"""Bootloader verification ladder B1-B5 (frozen 2026-09-22).
Reads the emitted image path from argv[1]. Prints disassembly + verdict.
Exit 0 = PASS (B1-B5), 1 = FAIL.
"""
import sys

IMG = sys.argv[1]
data = open(IMG, "rb").read()
fails = []
notes = []

# B1 size
if len(data) != 512:
    fails.append(f"B1 size: got {len(data)}, want 512")
else:
    notes.append("B1 size=512 OK")

# B2 signature
if len(data) == 512 and data[510] == 0x55 and data[511] == 0xAA:
    notes.append("B2 signature 55 AA OK")
else:
    fails.append("B2 signature: bytes[510..512] != 55 AA")

# --- frozen 16-bit decoder ---
# returns list of (addr, text, kind, detail)
def decode(buf):
    ins = []
    pc = 0
    n = len(buf)
    while pc < n:
        b = buf[pc]
        if 0xB8 <= b <= 0xBF:
            if pc + 2 >= n: return None, f"truncated imm16 at {pc}"
            imm = buf[pc+1] | (buf[pc+2] << 8)
            rn = ["ax","cx","dx","bx","sp","bp","si","di"][b & 7]
            ins.append((pc, f"mov {rn},0x{imm:04x}", "mov_imm16", (rn, imm)))
            pc += 3
        elif b == 0x8E:
            if pc + 1 >= n or buf[pc+1] != 0xD8:
                return None, f"unsupported 8E modrm at {pc}"
            ins.append((pc, "mov ds,ax", "mov_ds_ax", ()))
            pc += 2
        elif b == 0xAC:
            ins.append((pc, "lodsb", "lodsb", ()))
            pc += 1
        elif b == 0x84:
            if pc + 1 >= n or buf[pc+1] != 0xC0:
                return None, f"unsupported 84 modrm at {pc}"
            ins.append((pc, "test al,al", "test_al", ()))
            pc += 2
        elif b == 0x74 or b == 0x75:
            if pc + 1 >= n: return None, f"truncated rel8 at {pc}"
            rel = buf[pc+1] if buf[pc+1] < 128 else buf[pc+1] - 256
            tgt = pc + 2 + rel
            m = "jz" if b == 0x74 else "jnz"
            ins.append((pc, f"{m} {tgt}", "jcc", (m, tgt)))
            pc += 2
        elif b == 0xB4:
            if pc + 1 >= n: return None, f"truncated imm8 at {pc}"
            ins.append((pc, f"mov ah,0x{buf[pc+1]:02x}", "mov_ah", (buf[pc+1],)))
            pc += 2
        elif b == 0xCD:
            if pc + 1 >= n: return None, f"truncated int# at {pc}"
            ins.append((pc, f"int 0x{buf[pc+1]:02x}", "int", (buf[pc+1],)))
            pc += 2
        elif b == 0xEB:
            if pc + 1 >= n: return None, f"truncated jmp rel8 at {pc}"
            rel = buf[pc+1] if buf[pc+1] < 128 else buf[pc+1] - 256
            tgt = pc + 2 + rel
            ins.append((pc, f"jmp {tgt}", "jmp", (tgt,)))
            pc += 2
        elif b == 0xFA:
            ins.append((pc, "cli", "cli", ()))
            pc += 1
        elif b == 0xF4:
            ins.append((pc, "hlt", "hlt", ()))
            pc += 1
        else:
            return None, f"INVALID opcode 0x{b:02x} at {pc}"
        # halt-pattern stop: cli; hlt; jmp rel8 -> cli addr
        if len(ins) >= 3 and ins[-3][2] == "cli" and ins[-2][2] == "hlt" \
           and ins[-1][2] == "jmp" and ins[-1][3][0] == ins[-3][0]:
            return ins, None
    return None, "halt pattern (cli;hlt;jmp $) never found"

code_end = None
if not fails:
    ins, derr = decode(data[:510])
    if derr:
        fails.append(f"B3 decode: {derr}")
    else:
        code_end = ins[-1][0] + 2
        notes.append(f"B3 decode OK: {len(ins)} insns, code_end={code_end}")
        print("--- disassembly ---")
        for a, t, k, d in ins:
            print(f"{a:3d}: {t}")

# B4 semantics
if code_end is not None:
    kinds = [k for _, _, k, _ in ins]
    # mov ax,0x07c0 then mov ds,ax
    ax_ok = any(k == "mov_imm16" and d == ("ax", 0x07C0) for _, _, k, d in ins)
    ds_ok = "mov_ds_ax" in kinds
    if ax_ok and ds_ok:
        notes.append("B4a DS=0x07C0 setup OK")
    else:
        fails.append(f"B4a DS setup: ax07c0={ax_ok} ds_ax={ds_ok}")
    # mov si,imm16 == code_end
    si = [d for _, _, k, d in ins if k == "mov_imm16" and d[0] == "si"]
    if si and si[0][1] == code_end:
        notes.append(f"B4b mov si,{code_end} (SI->message) OK")
    else:
        fails.append(f"B4b mov si: got {si}, want imm16=={code_end}")
    # backward jmp = print loop (exclude the halt-closing jmp -> cli)
    halt_cli = next(a for a, _, k, _ in ins if k == "cli")
    jmps = [(a, d[0]) for a, _, k, d in ins if k == "jmp"]
    back = [(a, t) for a, t in jmps if t < a and t != halt_cli]
    if back:
        la, lt = back[-1]
        loop_top, loop_end = lt, la + 2
        body = [(a, t, k, d) for a, t, k, d in ins if loop_top <= a < loop_end]
        bks = [k for _, _, k, _ in body]
        ah_pos = next((i for i, k in enumerate(bks) if k == "mov_ah" and body[i][3][0] == 0x0E), None)
        int_pos = next((i for i, k in enumerate(bks) if k == "int" and body[i][3][0] == 0x10), None)
        if ah_pos is not None and int_pos is not None and ah_pos < int_pos:
            notes.append(f"B4c print loop OK: mov ah,0x0E then int 0x10 in [{loop_top},{loop_end})")
        else:
            fails.append(f"B4c loop body lacks mov ah,0x0E before int 0x10 (ah={ah_pos} int={int_pos})")
    else:
        fails.append("B4c no backward jmp (print loop) found")
    # forward conditional jump into halt region
    jccs = [(a, d) for a, _, k, d in ins if k == "jcc"]
    exits = [(a, m, t) for a, (m, t) in jccs if t >= halt_cli and t < code_end and a < halt_cli]
    if exits:
        notes.append(f"B4d loop-exit jcc OK: {exits[0]}")
    else:
        fails.append("B4d no forward jz/jnz into halt region")

# B5 layout: ASCIIZ then zeros
if code_end is not None:
    reg = data[code_end:510]
    i = 0
    while i < len(reg) and 0x20 <= reg[i] <= 0x7E:
        i += 1
    msg = reg[:i]
    rest_ok = (i < len(reg) and reg[i] == 0 and all(c == 0 for c in reg[i+1:]) and i >= 1)
    if rest_ok:
        notes.append(f"B5 layout OK: msg={msg!r} then 00 then zeros to 510")
    else:
        fails.append(f"B5 layout: msg={msg!r}, region not ASCIIZ+zeros")

print("--- verdict ---")
for x in notes:
    print("ok:", x)
if fails:
    for x in fails:
        print("FAIL:", x)
    print("RESULT: FAIL")
    sys.exit(1)
print("RESULT: PASS (B1-B5)")
