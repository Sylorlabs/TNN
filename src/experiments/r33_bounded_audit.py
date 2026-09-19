"""External bounded execution of the frozen B000 diagnostic; no Python cognition.

Only --run admits its single primary attempt. --preflight runs unrelated sandbox
probes. Output files are exclusive; a failed attempt cannot silently be reused.
All scientific helpers, fixtures and the output parser remain frozen.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import platform
import resource
import selectors
import signal
import subprocess
import sys
import tempfile
import time
from typing import Any

from r33_validate import (
    ROOT, RESEARCH, ContractError, digest, load_json, parse_b000_output,
    require, validate_pins, validate_repository,
)

RUN = RESEARCH / "R33_B000_RUN_PRIMARY_V1"
PREFLIGHT = RESEARCH / "R33_B000_LAUNCH_PREFLIGHT_V5.json"
FREEZE = RESEARCH / "R33_B000_LAUNCH_FREEZE.json"
COMPILER = RESEARCH / "toolchain/znc_macos_arm64_7cacbfc0"
ENV = {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C"}


def utc() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def write_json(path: Path, obj: Any, exclusive: bool = True) -> None:
    """Persist execution outputs, not source edits. Refuse replacing evidence."""
    text = json.dumps(obj, indent=2, allow_nan=False) + "\n"
    if exclusive:
        with path.open("x") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
    else:
        descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
        with os.fdopen(descriptor, "w") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)


def profile(executable: Path, directory: Path, python_probe: bool = False) -> str:
    """Deny write/network/fork; this fixture launcher does not certify read isolation.

    A restricted library read allowlist aborted in macOS dyld before main even
    for /usr/bin/true. Generic system reads are admitted; the separately checked
    native source has no file-read facility and imports no learner state.
    """
    executable = executable.resolve()
    return (
        '(version 1)(deny default)(allow file-read*)'
        '(allow sysctl-read)(allow mach-lookup)'
        '(allow process-exec (literal ' + json.dumps(str(executable)) + '))'
    )


def bounded(command: list[str], directory: Path, label: str, *, wall: float,
            cpu: int, output_limit: int, data_limit: int = 268435456,
            sandboxed: bool = True, python_probe: bool = False) -> dict[str, Any]:
    """Capture exact stdout/stderr with a deadline and wait4 per-child resources.

    This host rejected both RLIMIT_DATA and RLIMIT_RSS in preflight V1.
    Peak RSS is an actual wait4 measurement and a mandatory post-run verdict;
    no unavailable kernel resident-set limit is represented as enforced.
    """
    stdout_path = directory / (label + ".stdout")
    stderr_path = directory / (label + ".stderr")
    actual = command
    if sandboxed:
        actual = ["/usr/bin/sandbox-exec", "-p", profile(Path(command[0]), directory, python_probe), *command]

    def limits() -> None:
        os.setsid()
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
        resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))

    begin = time.monotonic()
    result: dict[str, Any] = {
        "command": actual, "requested_command": command, "started_utc": utc(),
        "environment": ENV, "sandboxed": sandboxed, "termination_reason": None,
        "exit_code": None, "cpu_seconds": None, "peak_rss_bytes": None,
        "stdout_bytes": 0, "stderr_bytes": 0, "native_process_started": False,
        "limits": {"wall_seconds": wall, "cpu_seconds": cpu,
                   "data_bytes": None,
                   "peak_rss_bytes_postrun_ceiling": data_limit if sandboxed else None,
                   "each_output_bytes": output_limit},
        "measurement": "time.monotonic wall; os.wait4 rusage per child; Darwin ru_maxrss bytes",
        "rss_enforcement": "MEASURED_POSTRUN_CEILING_ONLY: host rejects DATA/RSS setrlimit; static allowlisted driver has bounded allocations; not a hard memory sandbox",
    }
    with stdout_path.open("xb") as out, stderr_path.open("xb") as err:
        try:
            child = subprocess.Popen(actual, cwd=directory, env=ENV, stdin=subprocess.DEVNULL,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     preexec_fn=limits, close_fds=True)
        except Exception as error:
            result["termination_reason"] = "SPAWN_FAILURE"
            result["spawn_error"] = repr(error)
            result["wall_seconds"] = time.monotonic() - begin
            return result
        result["native_process_started"] = True
        result["pid"] = child.pid
        selector = selectors.DefaultSelector()
        selector.register(child.stdout, selectors.EVENT_READ, (out, "stdout_bytes"))
        selector.register(child.stderr, selectors.EVENT_READ, (err, "stderr_bytes"))
        usage = None
        reaped = False
        killed = False
        try:
            while not reaped or selector.get_map():
                if not killed and time.monotonic() - begin > wall:
                    result["termination_reason"] = "WALL_LIMIT"
                    try:
                        os.killpg(child.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    killed = True
                for key, _ in selector.select(0.01):
                    block = os.read(key.fileobj.fileno(), 4096)
                    if not block:
                        selector.unregister(key.fileobj)
                        key.fileobj.close()
                        continue
                    stream, counter = key.data
                    available = max(0, output_limit - result[counter])
                    stream.write(block[:available])
                    stream.flush()
                    result[counter] += len(block)
                    if result[counter] > output_limit and not killed:
                        result["termination_reason"] = "OUTPUT_LIMIT"
                        try:
                            os.killpg(child.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        killed = True
                if not reaped:
                    pid, status, observed = os.wait4(child.pid, os.WNOHANG)
                    if pid:
                        child.returncode = os.waitstatus_to_exitcode(status)
                        result["exit_code"] = child.returncode
                        usage, reaped = observed, True
        finally:
            if not reaped:
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                _, status, usage = os.wait4(child.pid, 0)
                child.returncode = os.waitstatus_to_exitcode(status)
                result["exit_code"] = child.returncode
            selector.close()
            for pipe in (child.stdout, child.stderr):
                if not pipe.closed:
                    pipe.close()
            out.flush(); err.flush()
            os.fsync(out.fileno()); os.fsync(err.fileno())
        if usage is not None:
            result["cpu_seconds"] = usage.ru_utime + usage.ru_stime
            result["peak_rss_bytes"] = usage.ru_maxrss
            if sandboxed and usage.ru_maxrss > data_limit:
                result["termination_reason"] = result["termination_reason"] or "RSS_LIMIT_OBSERVED"
    result["wall_seconds"] = time.monotonic() - begin
    result["finished_utc"] = utc()
    result["stdout_sha256"] = digest(stdout_path)
    result["stderr_sha256"] = digest(stderr_path)
    return result


def preflight() -> dict[str, Any]:
    require(platform.system() == "Darwin" and platform.machine() == "arm64", "wrong audit platform")
    require(not PREFLIGHT.exists(), "preflight already recorded; inspect it before a separately named retry")
    directory = Path(tempfile.mkdtemp(prefix="r33-launch-preflight-"))
    python_path = Path(sys.executable).resolve()
    # Homebrew macOS bin/python is a trampoline that execs Python.app. Bind the
    # observed real image directly so the single-executable sandbox stays narrow.
    app_image = python_path.parent.parent / "Resources/Python.app/Contents/MacOS/Python"
    py = str(app_image if app_image.is_file() else python_path)
    code = '''import errno,json,os,socket,resource
r={}
def connect_probe():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as probe:
        probe.settimeout(0.2)
        probe.connect(("127.0.0.1",9))
for name,action in (("write",lambda:open("forbidden","w")),("read",lambda:open("/Users/Shared/micah/Documents/TNN/TNN/README.md")),("network",connect_probe),("fork",os.fork)):
    try:
        value=action()
        if name=="fork":
            if value==0: os._exit(0)
            os.waitpid(value,0)
        elif hasattr(value,"close"): value.close()
        r[name]="ALLOWED"
    except OSError as error:
        r[name]="DENIED" if error.errno in (errno.EPERM,errno.EACCES) else "OTHER_ERROR"
        r[name+"_errno"]=error.errno
r["cpu_limit"]=resource.getrlimit(resource.RLIMIT_CPU)[0]
r["memory_limit_mode"]="MEASURED_POSTRUN_CEILING_ONLY"
print(json.dumps(r,sort_keys=True))
'''
    isolation = bounded([py, "-B", "-c", code], directory, "isolation", wall=10, cpu=3,
                        output_limit=4096, python_probe=True)
    details = {}
    if isolation["exit_code"] == 0:
        details = json.loads((directory / "isolation.stdout").read_text())
    deadline = bounded([py, "-B", "-c", "while True: pass"], directory, "deadline",
                       wall=0.2, cpu=3, output_limit=4096, python_probe=True)
    flood = bounded([py, "-B", "-c", "import os; os.write(1,b'x'*8192)"], directory, "output_limit",
                    wall=5, cpu=3, output_limit=1024, python_probe=True)
    ok = (isolation["exit_code"] == 0 and isolation["termination_reason"] is None
          and all(details.get(x) == "DENIED" for x in ("write", "network", "fork"))
          and details.get("cpu_limit") == 3
          and deadline["termination_reason"] == "WALL_LIMIT"
          and flood["termination_reason"] == "OUTPUT_LIMIT")
    report = {"status": "PASS" if ok else "FAIL", "version": 5, "date": utc(), "probe_directory": str(directory),
              "prior_failed_preflights": ["Research/R33_B000_LAUNCH_PREFLIGHT.json", "Research/R33_B000_LAUNCH_PREFLIGHT_V2.json", "Research/R33_B000_LAUNCH_PREFLIGHT_V3.json", "Research/R33_B000_LAUNCH_PREFLIGHT_V4.json"],
              "isolation": isolation, "observed_denials": details, "deadline": deadline, "output_limit": flood,
              "scope": "External launch controls only; no B000/TNN fixtures executed",
              "limitations": ["macOS hard RSS enforcement not claimed; final wait4 peak checked",
                              "Filesystem read isolation NOT established; audited native helper driver contains no file reads or imports; no M2 shadow qualification",
                              "Probe confirms these operations only, not a complete sandbox security proof",
                              "Compiler runs outside runtime sandbox, bounded to 60 seconds; no cognition"]}
    write_json(PREFLIGHT, report)
    require(ok, "launcher preflight failed; report preserved")
    return report


def update_state(status: str, exposures: int, result: dict[str, Any] | None = None) -> None:
    registry = load_json(RESEARCH / "R33_EXPERIMENT_REGISTRY.json")
    current = load_json(RESEARCH / "R33_CURRENT_STATE.json")
    execution = load_json(RESEARCH / "R33_B000_EXECUTION_STATUS.json")
    consumed = load_json(RESEARCH / "R33_CONSUMED_EVIDENCE_REGISTRY.json")
    active = "R33-B000" if status == "RUNNING" else None
    batch = next(x for x in registry["experiments"] if x["id"] == "R33-B000")
    registry["active_experiment"] = current["active_experiment"] = active
    batch.update(status=status, primary_attempts=1, launch_preflight_status="PASSED_WITH_DECLARED_RSS_LIMITATION",
                 execution_record="Research/R33_B000_RUN_PRIMARY_V1/RESULT.json")
    current.update(status="BOUNDARY_AUDIT_" + status, r33_native_experiments_executed=exposures,
                   next_action="Analyze retained B000 results, then implement and qualify the relevant sensory/state/trace boundary; continue authorized work")
    execution.update(status=status, primary_execution_attempts=1, native_fixture_exposures=exposures,
                     launch_prerequisites_remaining=[], execution_record="Research/R33_B000_RUN_PRIMARY_V1/RESULT.json")
    for fixture in consumed.get("diagnostic_fixtures", []):
        if fixture["batch_id"] == "R33-B000":
            fixture.update(primary_executions=exposures, reserved_primary_attempts=1,
                           status="CONSUMED_DIAGNOSTIC" if exposures else "RESERVED_PRIMARY_ATTEMPT")
    if result is not None:
        execution["observed_witness_results"] = result.get("parsed_output")
        execution["runtime_resources"] = result.get("runtime", {"status": "NOT_EXECUTED"})
        execution["result_reason"] = result["status"]
        execution["errors"] = result.get("errors", [])
    for path, document in (("R33_EXPERIMENT_REGISTRY.json", registry), ("R33_CURRENT_STATE.json", current),
                           ("R33_B000_EXECUTION_STATUS.json", execution), ("R33_CONSUMED_EVIDENCE_REGISTRY.json", consumed)):
        write_json(RESEARCH / path, document, exclusive=False)


def run() -> dict[str, Any]:
    require(load_json(PREFLIGHT)["status"] == "PASS", "preflight not passed")
    freeze = load_json(FREEZE)
    validate_pins(freeze["pins"])
    require(freeze["status"] == "FROZEN_BEFORE_PRIMARY_EXECUTION", "launcher not frozen")
    baseline_check = validate_repository()
    require(not RUN.exists(), "single primary directory exists; do not rerun")
    snapshot = {name: load_json(RESEARCH / name) for name in (
        "R33_CURRENT_STATE.json", "R33_EXPERIMENT_REGISTRY.json", "R33_CONSUMED_EVIDENCE_REGISTRY.json")}
    batch = next(x for x in snapshot["R33_EXPERIMENT_REGISTRY.json"]["experiments"] if x["id"] == "R33-B000")
    require(batch["primary_attempts"] == 0, "primary attempt consumed")
    RUN.mkdir(mode=0o700)
    write_json(RUN / "REGISTRATION_SNAPSHOT.json", snapshot)
    write_json(RUN / "RESERVATION.json", {"batch_id": "R33-B000", "reserved_utc": utc(),
               "attempt": 1, "freeze_sha256": digest(FREEZE), "preflight_sha256": digest(PREFLIGHT),
               "baseline_check": baseline_check, "registration_snapshot_sha256": digest(RUN / "REGISTRATION_SNAPSHOT.json")})
    result: dict[str, Any] = {"batch_id": "R33-B000", "status": "INFRASTRUCTURE_FAILURE",
                             "errors": [], "fixture_exposures": 0, "training_runs": 0,
                             "canonical_mutated": False, "learner_authority_granted": False,
                             "sensory_qualification": False, "promotion": False}
    try:
        update_state("RUNNING", 0)
        source = RESEARCH / "R33_B000_SOURCE.zag"
        config = load_json(RESEARCH / "R33_B000_CONFIG.json")
        binary = RUN / "b000"
        compiler_command = [str(COMPILER), str(source), "--target", "macos-arm64", "--no-zagd",
                            "--no-analyze", "--no-foreground-cache", "-o", str(binary)]
        result["compile"] = bounded(compiler_command, RUN, "compile", wall=60, cpu=55,
                                     output_limit=65536, sandboxed=False)
        require(result["compile"]["exit_code"] == 0 and result["compile"]["termination_reason"] is None,
                "native compilation failed")
        validate_pins(batch["source_pins"])
        validate_pins(freeze["pins"])
        result["binary_sha256"] = digest(binary)
        result["source_sha256"] = digest(source)
        result["config_sha256"] = digest(RESEARCH / "R33_B000_CONFIG.json")
        result["compiler_sha256"] = digest(COMPILER)
        result["system"] = {"platform": platform.platform(), "machine": platform.machine()}
        write_json(RUN / "NATIVE_ADMISSION.json", {"time": utc(), "attempt": 1, "binary_sha256": result["binary_sha256"],
                   "source_sha256": result["source_sha256"], "config_sha256": result["config_sha256"],
                   "compiler_sha256": result["compiler_sha256"], "launch_freeze_sha256": digest(FREEZE)})
        # Once admitted, a crash/incomplete output is a consumed attempted exposure.
        result["fixture_exposures"] = 1
        update_state("RUNNING", 1)
        result["runtime"] = bounded([str(binary)], RUN, "native", wall=30, cpu=20,
                                    output_limit=config["resources"]["stdout_bytes_ceiling"])
        require(result["runtime"]["exit_code"] == 0 and result["runtime"]["termination_reason"] is None,
                "native run failed or resource ceiling exceeded")
        require(result["runtime"]["stderr_bytes"] == 0, "unexpected native stderr")
        result["parsed_output"] = parse_b000_output((RUN / "native.stdout").read_text(), config)
        result["status"] = result["parsed_output"]["status"]
    except Exception as error:
        result["errors"].append(repr(error))
    result["finished_utc"] = utc()
    write_json(RUN / "RESULT.json", result)
    state_status = "COMPLETED" if result["status"] == "EXPECTED_WITNESSES_MATCHED" else "FAILED_REQUIRES_ANALYSIS"
    update_state(state_status, result["fixture_exposures"], result)
    manifest = {"batch_id": "R33-B000", "created_utc": utc(), "files": [
        {"path": str(p.relative_to(ROOT)), "sha256": digest(p), "bytes": p.stat().st_size}
        for p in sorted(RUN.iterdir()) if p.is_file()]}
    write_json(RUN / "MANIFEST.json", manifest)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preflight", action="store_true")
    group.add_argument("--run", action="store_true")
    args = parser.parse_args()
    try:
        report = preflight() if args.preflight else run()
        print(json.dumps(report, indent=2, allow_nan=False))
        return 0 if report["status"] in ("PASS", "EXPECTED_WITNESSES_MATCHED") else 1
    except (ContractError, OSError, ValueError, KeyError) as error:
        print("R33_LAUNCH_FAIL: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
