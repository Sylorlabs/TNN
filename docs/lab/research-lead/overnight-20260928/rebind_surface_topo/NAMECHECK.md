# NAMECHECK.md -- Rebinding Surface & Topology Worker

## Step 0: Toolchain Guard
- Date: 2026-10-01
- Safebin setup: `mkdir -p $HOME/safebin`, symlinked 36 allowed tools
- PATH exported: `$HOME/safebin`
- `which python3 python`: (empty, no output) -- GUARD PASS
- No forbidden executables invoked.

## Step 1: Provenance
- Worker: Rebinding Surface & Topology Worker (Micah Q2A, Q2E)
- Parent: main agent (subagent session 517cd7bb-597e-483d-ae6a-c4d221bf7263)
- Base: frozen TNN-2 (SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd)
- Rebind mechanism: from 91585087c (rb_patch.zag, verbatim)

## Step 2: Unfrozen-Variant-Only
- All experiments use UNFROZEN variants.
- Frozen base (st_base.zag) is read-only reference, never modified.
- Patch (st_patch.zag) is verbatim from 91585087c.

## Constraints
- Pure Zag via pinned znc.
- Zero em/en dashes in documentation (byte-verified before commit).
- Paper untouched.
- Nothing pushed (local commits only).
- Explicit pathspecs on git add and git commit.
