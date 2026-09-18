"""One bounded Linux native invocation with partial-evidence preservation."""
from pathlib import Path
import json
import os
import resource
import signal
import subprocess
import time

root = Path(".scratch/e51aj")
if (root/"RAW.log").exists():
    raise SystemExit("scientific log already exists; refusing a duplicate invocation")
limit = 5400


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (2*1024**3, 2*1024**3))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024**3, 1024**3))


started = time.monotonic()
timed_out = False
with (root/"RAW.log").open("xb") as log:
    process = subprocess.Popen([str(root/"NATIVE_BUILD_1")], stdout=log, stderr=subprocess.STDOUT,
                               preexec_fn=limits, start_new_session=True)
    try:
        code = process.wait(timeout=limit)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()
        code = 124
elapsed = time.monotonic()-started
stats = resource.getrusage(resource.RUSAGE_CHILDREN)
result = {"exit_code":code, "timed_out":timed_out, "wall_seconds":elapsed,
          "native_timeout_seconds":limit, "max_address_space_bytes":2*1024**3,
          "max_output_file_bytes":1024**3, "peak_rss_kib":stats.ru_maxrss,
          "user_cpu_seconds":stats.ru_utime, "system_cpu_seconds":stats.ru_stime}
(root/"RUN_EXECUTION.json").write_text(json.dumps(result,indent=2)+"\n")
(root/"EXIT_CODE.txt").write_text(str(code)+"\n")
with (root/"RAW.log").open() as stream, (root/"SUMMARY.log").open("w") as summary:
    for line in stream:
        if line.startswith(("e51aj_metrics,", "e51aj_replica_complete,", "e51aj_outcome,", "e51aj_integrity_gate,", "TNN_R32_E51AJ_")):
            summary.write(line)
print(json.dumps(result,indent=2))
raise SystemExit(0 if code == 0 and not timed_out else 1)
