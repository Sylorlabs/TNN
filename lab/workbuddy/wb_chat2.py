#!/usr/bin/env python3
"""wb_chat2.py — PURE I/O RELAY for TNN workbuddy chat sessions.

Spawns ./wb_dialogue_bin chat (in BUILD dir) with piped stdin/stdout and
relays: each stdin line -> binary stdin; each "A ..." binary line -> stdout.

This wrapper does NO thinking by design: no prompt engineering, no
preprocessing, no answer shaping, no per-turn logic. One binary process =
one session; when the process exits, the session (history + taught facts)
evaporates -- no persistence.

Usage:
  ./wb_chat2.py < turns.txt        # batch a script of turns
  ./wb_chat2.py                    # interactive (Ctrl-D to end session)
  BINARY=/path/to/bin ./wb_chat2.py

Env:
  BINARY  dialogue binary (default: ~/workspace/workbuddy/build/wb_dialogue_bin)
  KB      kb.txt path visible to the binary's CWD (default: build/kb.txt symlink)
"""
import subprocess, sys, os

BUILD = os.path.expanduser("~/workspace/workbuddy/build")
BINARY = os.environ.get("BINARY",
                         os.path.join(BUILD, "wb_dialogue_bin"))

def main():
    proc = subprocess.Popen([BINARY, "chat"], cwd=BUILD,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            text=True, bufsize=1)
    assert proc.stdin and proc.stdout
    # swallow the "KB ... ENT ..." banner line
    banner = proc.stdout.readline()
    sys.stderr.write("banner: " + banner)
    try:
        for raw in sys.stdin:
            line = raw.rstrip("\n")
            if line == "":
                continue
            proc.stdin.write(line + "\n")
            proc.stdin.flush()
            # read until the "A " response line
            while True:
                out = proc.stdout.readline()
                if out == "":
                    sys.stderr.write("BINARY EOF\n")
                    return
                if out.startswith("A "):
                    sys.stdout.write(out[2:])
                    sys.stdout.flush()
                    break
                # ignore any other binary chatter on stdout
                sys.stderr.write("chatter: " + out)
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        proc.wait()

if __name__ == "__main__":
    main()
