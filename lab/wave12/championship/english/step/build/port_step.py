#!/usr/bin/env python3
"""Mechanical port: muse_team English legs -> step team (step-3.7-flash).

Renames files/symbols muse_* -> step_*, MUSE-CLASS -> STEP-CLASS,
MUSEB_/MUSEC_ -> STEPB_/STEPC_, tid 20->51 (direct) / 21->41 (taught teacher),
sealed paths + canaries. Logic/content adaptations (t5_core domain, category
geometry, D2 two-hop) are done by hand after this script runs.
"""
import os
import re

ROOT = "/home/hatch/workspace/tnn-lab/wave12/championship-english/step/legs/tnn"

RENAMES = [
    ("legA/src/muse_trial.zag", "legA/src/step_trial.zag"),
    ("legA/src/muse_corpus.zag", "legA/src/step_corpus.zag"),
    ("legB/src/muse_b7_direct.zag", "legB/src/step_b7_direct.zag"),
    ("legB/src/muse_corpus.zag", "legB/src/step_corpus.zag"),
    ("legB/src/muse_teach.zag", "legB/src/step_teach.zag"),
    ("legC/src/muse_teacher_leg.zag", "legC/src/step_teacher_leg.zag"),
    ("legC/src/muse_corpus.zag", "legC/src/step_corpus.zag"),
    ("legC/src/muse_teach.zag", "legC/src/step_teach.zag"),
    ("shared/muse_teach.zag", "shared/step_teach.zag"),
    ("legA/run_muse.sh", "legA/run_step.sh"),
]

# (pattern, replacement) applied in order; word-boundary safe where needed
SUBS = [
    (r"\bmuse_t_", "step_t_"),
    (r"\bmuse_dump_at\b", "step_dump_at"),
    (r"\bmuse_obs_at\b", "step_obs_at"),
    (r"\bmuse_dis_at\b", "step_dis_at"),
    (r"\bmuse_prb_at\b", "step_prb_at"),
    (r"\bMUSE_DUMP_N\b", "STEP_DUMP_N"),
    (r"\bMUSE_CORPUS_SHA256\b", "STEP_CORPUS_SHA256"),
    (r"\bMUSE_CORPUS\b", "STEP_CORPUS"),
    (r"\bMUSEB_", "STEPB_"),
    (r"\bMUSEC_", "STEPC_"),
    (r"MUSE-CLASS", "STEP-CLASS"),
    (r"\bmuse-native\b", "step-3.7-flash"),
    (r"MUSE-NATIVE", "STEP-3.7-FLASH"),
    (r'"muse_corpus\.zag"', '"step_corpus.zag"'),
    (r'"muse_teach\.zag"', '"step_teach.zag"'),
    # sealed paths (same length: muse->step)
    ("b[0]=109 as u8; b[1]=117 as u8; b[2]=115 as u8; b[3]=101 as u8;",
     "b[0]=115 as u8; b[1]=116 as u8; b[2]=101 as u8; b[3]=112 as u8;"),
    # canaries: "MUB7:direct" -> "STB7:direct"; "MUCT:teacher21" -> "STCT:teacher41"
    # (both share the MU->ST two-byte prefix; B/C/T bytes after are unchanged)
    ("b[0]=77 as u8; b[1]=85 as u8;",
     "b[0]=83 as u8; b[1]=84 as u8;"),
    ("b[12]=50 as u8; b[13]=49 as u8;", "b[12]=52 as u8; b[13]=49 as u8;"),
    ('"MUB7:direct"', '"STB7:direct"'),
    ('"MUCT:teacher21"', '"STCT:teacher41"'),
    ('"muse/b7direct/sealed"', '"step/b7direct/sealed"'),
    ('"muse/teacherleg/sealed"', '"step/teacherleg/sealed"'),
    # tid deltas in comments
    (r"teacher_id=20\b", "teacher_id=51"),
    (r"teacher_id=21\b", "teacher_id=41"),
    (r"\btid=20\b", "tid=51"),
    (r"\btid=21\b", "tid=41"),
    (r"direct\(20\)", "direct(51)"),
    (r"taught-teacher\(21\)", "taught-teacher(41)"),
    (r"\(M2 taught-learner, tid 21\)", "(M2 taught-learner, tid 41)"),
    # TbSess seq fields
    (r"\blast20\b", "last51"),
    (r"\blast21\b", "last41"),
]

TID_CONST_SUBS = [
    ("const TB_TID_DIRECT:i64=20;", "const TB_TID_DIRECT:i64=51;"),
    ("const TB_TID_MUSETAUGHT:i64=21;", "const TB_TID_MUSETAUGHT:i64=41;"),
    ("TB_TID_DIRECT(20)", "TB_TID_DIRECT(51)"),
    ("TB_TID_MUSETAUGHT(21)", "TB_TID_MUSETAUGHT(41)"),
    ("direct(20)/taught-teacher(21)", "direct(51)/taught-teacher(41)"),
]

def main():
    for old, new in RENAMES:
        o, n = os.path.join(ROOT, old), os.path.join(ROOT, new)
        if os.path.exists(o):
            os.rename(o, n)
            print(f"renamed {old} -> {new}")
    n_files = 0
    for dirpath, _, filenames in os.walk(ROOT):
        for fn in filenames:
            if not fn.endswith(".zag") and not fn.endswith(".sh") and not fn.endswith(".py"):
                continue
            p = os.path.join(dirpath, fn)
            with open(p) as f:
                text = f.read()
            orig = text
            for pat, rep in SUBS:
                text = re.sub(pat, rep, text)
            if "q1_types.zag" in fn:
                for pat, rep in TID_CONST_SUBS:
                    text = text.replace(pat, rep)
            if text != orig:
                with open(p, "w") as f:
                    f.write(text)
                n_files += 1
    print(f"rewrote {n_files} files")
    # residual check
    import subprocess
    r = subprocess.run(["grep", "-rn", "muse_t_\\|muse_dump_at\\|muse_obs_at\\|muse_dis_at\\|muse_prb_at\\|MUSE_CORPUS\\|MUSEB_\\|MUSEC_\\|MUSE-CLASS\\|muse-native\\|MUSE-NATIVE",
                        ROOT, "--include=*.zag", "--include=*.sh", "--include=*.py"],
                       capture_output=True, text=True)
    print("residuals:\n" + (r.stdout.strip() or "(none)"))

if __name__ == "__main__":
    main()
