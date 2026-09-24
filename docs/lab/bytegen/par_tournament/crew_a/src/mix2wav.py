#!/usr/bin/env python3
"""mix2wav.py — s32 LE mix dump -> i16 WAV (measurement/harness tooling).

Clipping behavior is DOCUMENTED, not hidden: samples outside i16 range are
hard-clipped and the clip count + peak ratio are printed to stderr.
Usage: mix2wav.py <in.mix> <out.wav>
"""
import struct, sys, wave

def main():
    inp, outp = sys.argv[1], sys.argv[2]
    with open(inp, 'rb') as f:
        raw = f.read()
    n = len(raw) // 4
    vals = struct.unpack('<%di' % n, raw[:n*4])
    clip = 0
    peak = 0
    out = bytearray()
    for v in vals:
        if abs(v) > peak: peak = abs(v)
        # NOTE: render_a's mix dump is i16-scale samples stored in s32 words
        # (max|v| ~ 43337 << 2^31). No >>16 shift — pack the low 16 bits.
        i16 = v
        if i16 > 32767: i16 = 32767; clip += 1
        elif i16 < -32768: i16 = -32768; clip += 1
        out += struct.pack('<h', i16)
    with wave.open(outp, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100)
        w.writeframes(bytes(out))
    print(f"mix2wav: {n} samples, peak={peak/32768.0:.4f} i16FS, clipped={clip} ({100.0*clip/n:.3f}%)",
          file=sys.stderr)

if __name__ == '__main__':
    main()
