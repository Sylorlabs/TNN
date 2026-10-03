# NAMECHECK: Learner-State Dynamics Analyst

## Step 0: Toolchain guard (mandatory, recorded)

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 27 allowed tools
  (git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum
  git-receive-pack git-upload-pack find sort head tail od xxd stat touch diff).
- `export PATH="$HOME/safebin"`.
- `which python3 python` returned NOTHING. Zero forbidden executables invoked
  in this wave. All computation in Zag (pinned
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`); shell used only to invoke
  znc, run binaries, git ops, move/copy files.

## Scope

Read-only dynamics analysis of frozen TNN-2 learner state. One verbatim copy
of frozen `tnn2.zag` (SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
verified identical before and after) with the original test `main` removed and
a measurement driver appended. Cognition code untouched. Frozen
`tnn2_build/tnn2.zag` and `tnn2_build/tnn2_bin` verified unmodified at end of
wave (same hashes, clean `git status` on `tnn2_build/`).

## Input provenance

- Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
- Interface semantics cross-checked against in-source tests (`t_t2_inquire`,
  `t_t2_revise`, `t_c13`) in the same frozen file.
- Unsealed practice subjects ONLY: synthetic integer subjects
  (1000s, 2000s, 3000s, 7000s, 9000s). No sealed H2/FW/H2 world files opened,
  listed, or hashed beyond the pre-existing directory names. No sealed content
  inspected at any point.

## Constraints honored

- Frozen binary/source read-only; all experiments on the clearly marked copy
  in this directory (`sd_base.zag`, `sd_full.zag`, `sd_dyn_bin`).
- Determinism: 3/3 byte-identical runs
  (`fbc52cfb3b6d2b771c44738931accd400d1dd04147933c091a25eec8a42968ea`).
- Zero em dashes in deliverables (byte-verified before commit).
- Paper untouched. Nothing pushed. Local commit only, explicit pathspecs.
