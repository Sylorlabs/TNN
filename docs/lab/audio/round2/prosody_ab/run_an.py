import subprocess, sys
for f in sys.argv[1:]:
    r = subprocess.run(['python3', '../shared/analyze.py', f], capture_output=True, text=True, timeout=120)
    out = r.stdout + r.stderr
    # print only the metric lines and gates
    for line in out.splitlines():
        if any(k in line for k in ('prosody:', 'hnr_db', 'peak_dbfs', 'frac_static', 'periodicity', 'hf_rolloff', 'crest_med', 'GATES', 'PASS', 'FAIL')):
            print(f, '|', line.strip())
