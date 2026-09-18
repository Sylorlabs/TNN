"""External byte fixtures/oracles and bounded native C02 execution; no cognition.

Encoded packet builders are evaluator fixtures. Native Zag alone reads, validates,
owns, serializes, restores and decodes records. Retained output files are compared
against independent Python struct/zlib/math oracles and hash-pinned.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path
import re
import struct
import sys
import time
import zlib

from r33_validate import ROOT, RESEARCH, ContractError, digest, load_json, require, validate_pins
from r33_bounded_audit import COMPILER, bounded, utc, write_json
from r33_c01 import verify_saved as verify_c01

SOURCES = ["R33_B001_RAW_RECORD.zag", "R33_B001_C02_DRIVER.zag", "R33_B001_COMPONENTS.zag"]
CONFIG = RESEARCH / "R33_B001_C02_CONFIG.json"
FREEZE = RESEARCH / "R33_B001_C02_FREEZE.json"
RUN = RESEARCH / "R33_B001_C02_RUN_PRIMARY_V1"
FIELDS = ["encoding", "channels", "rate", "width", "height", "items", "payload", "clock", "ordinal", "tick", "timebase", "source"]


def sandbox_policy(directory: Path, executable: Path) -> str:
    return ('(version 1)(deny default)(allow file-read*)(allow sysctl-read)(allow mach-lookup)'
            '(allow file-write* (subpath '+json.dumps(str(directory.resolve()))+'))'
            '(allow process-exec (literal '+json.dumps(str(executable.resolve()))+'))')


def preflight() -> dict:
    directory=RESEARCH/"R33_B001_C02_LAUNCH_PROBE"
    require(not directory.exists(),"C02 preflight exists; preserve it before a versioned change")
    directory.mkdir(mode=0o700);inside=directory/"writable";inside.mkdir()
    py=Path(sys.executable).resolve()
    app=py.parent.parent/"Resources/Python.app/Contents/MacOS/Python"
    if app.is_file():py=app
    code='''import errno,json,os,socket
r={}
def local_write():
    with open("allowed","w") as f:f.write("scoped test")
def outside_write():
    with open("../forbidden","w") as f:f.write("should not exist")
def connect():
    with socket.socket() as s:s.connect(("127.0.0.1",9))
for name,fn in (("inside",local_write),("outside",outside_write),("network",connect),("fork",os.fork)):
    try:
        v=fn()
        if name=="fork":
            if v==0:os._exit(0)
            os.waitpid(v,0)
        r[name]="ALLOWED"
    except OSError as e:r[name]="DENIED" if e.errno in (errno.EPERM,errno.EACCES) else "OTHER_ERROR"
print(json.dumps(r,sort_keys=True))
'''
    command=["/usr/bin/sandbox-exec","-p",sandbox_policy(inside,py),str(py),"-B","-c",code]
    run_record=bounded(command,inside,"probe",wall=10,cpu=5,output_limit=4096,sandboxed=False)
    observed=json.loads((inside/"probe.stdout").read_text()) if run_record["exit_code"]==0 else {}
    passed=(run_record["exit_code"]==0 and run_record["termination_reason"] is None
            and observed=={"inside":"ALLOWED","outside":"DENIED","network":"DENIED","fork":"DENIED"}
            and not (directory/"forbidden").exists())
    report={"status":"PASS" if passed else "FAIL","runtime":run_record,"observed":observed,
            "scope":"Engineering launcher test, no C02 raw-record or learner execution",
            "read_isolation_qualified":False,"hard_rss_enforcement_qualified":False}
    write_json(directory/"RESULT.json",report);require(passed,"C02 scoped write preflight failed")
    return report


def checksummed(content: bytes, skip: int) -> bytes:
    check = zlib.adler32(content[:skip] + content[skip + 8:])
    return content[:skip] + struct.pack("<II", check & 65535, check >> 16) + content[skip + 8:]


def packet(config: dict, case: dict) -> tuple[bytes, dict, bytes]:
    meta = dict(config["default_metadata"])
    if case["kind"] in ("rgb", "rgb_maximum"):
        maximum = case["kind"] == "rgb_maximum"
        values = [i % 256 for i in range(64*64*3)] if maximum else list(config["rgb_bytes"])
        if case.get("reverse_pixels"):
            values = values[3:] + values[:3]
        payload = bytes(values)
        meta.update(encoding=2, channels=3, rate=0, width=64 if maximum else 2,
                    height=64 if maximum else 1, items=4096 if maximum else 2)
    else:
        values = list(config["audio_samples"])
        if "sample_one" in case:
            values[1] = case["sample_one"]
        if case["kind"] == "empty":
            values = []
        if case["kind"] in ("maximum", "overmaximum"):
            values = [0] * (65537 if case["kind"] == "overmaximum" else 65536)
            values[-1] = 1
        payload = struct.pack("<" + "h" * len(values), *values)
        meta["items"] = len(values) // meta["channels"]
    meta["payload"] = len(payload)
    meta.update(case.get("metadata", {}))
    raw = checksummed(b"TNNRAW01" + struct.pack("<12I", *(meta[k] for k in FIELDS)) + b"\0" * 8 + payload, 56)
    mutation = case.get("mutation")
    if mutation == "magic": raw = b"X" + raw[1:]
    elif mutation == "truncate": raw = raw[:-1]
    elif mutation == "append": raw += b"\0"
    elif mutation == "payload_bit": raw = raw[:64] + bytes([raw[64] ^ 1]) + raw[65:]
    elif mutation is not None: raise ContractError("unknown packet mutation")
    return raw, meta, payload


def snapshot(raw: bytes, meta: dict) -> bytes:
    cursor = [meta["clock"], meta["ordinal"] + 1, meta["tick"], meta["timebase"]]
    return checksummed(b"TNNSNP01" + struct.pack("<6I", *cursor, len(raw), 1) + b"\0" * 8 + raw, 32)


def expected_success(meta: dict, payload: bytes, detached: int) -> tuple[dict, dict]:
    decoded = list(struct.unpack("<" + "h" * (len(payload) // 2), payload)) if meta["encoding"] == 1 else list(payload)
    return ({"status": 0, "used": 64 + len(payload), "detached": detached, "decoded_status": 0,
             "retrieval_status": 0, "retrieval_detached": 1, "unused_tail_changes": 0},
            {"cursor": [meta["clock"], meta["ordinal"] + 1, meta["tick"], meta["timebase"]],
             "metadata": [meta[k] for k in FIELDS], "decoded": decoded})


def expected_output(status: int, meta: dict | None, payload: bytes, mode: str,
                    retained: tuple[bytes, dict] | None = None) -> tuple[dict, dict]:
    if status == 0:
        require(meta is not None, "missing success metadata")
        metrics, vectors = expected_success(meta, payload, 1 if mode == "capture" and payload else -1)
        if not payload: vectors.pop("decoded")
        return metrics, vectors
    raw, previous = retained if retained is not None else (b"", None)
    vectors = {"cursor": [previous["clock"], previous["ordinal"]+1, previous["tick"], previous["timebase"]]
               if previous else [7, 0, -1, 1000000]}
    if raw: vectors["retained_bytes"] = list(raw)
    return ({"status": status, "used": len(raw), "detached": -1,
             "changed_destination_bytes": sum(value != 211 for value in raw)}, vectors)


def schedule_count(config: dict) -> int:
    return (len(config["cases"]) + len(config["reload_cases"]) + 1 +
            len(config["continuation_controls"]) + len(config["snapshot_alias_cases"]) +
            len(config["snapshot_negatives"]))


def parse_output(text: str) -> tuple[dict, dict]:
    metrics = {}
    vectors = {}
    for row in csv.reader(io.StringIO(text)):
        require(len(row) in (3, 4) and row[0] in ("M", "V"), "invalid C02 record")
        require(len(row) == (3 if row[0] == "M" else 4), "wrong C02 record arity")
        for value in row[2:]:
            require(re.fullmatch(r"-?(0|[1-9][0-9]*)", value) is not None, "invalid integer")
            require(-(2**31) <= int(value) < 2**31, "out-of-range integer")
        if row[0] == "M":
            require(row[1] not in metrics, "duplicate C02 metric")
            metrics[row[1]] = int(row[2])
        else:
            index, value = int(row[2]), int(row[3])
            require(0 <= index <= 65536, "C02 vector index outside envelope")
            current = vectors.setdefault(row[1], {})
            require(index not in current, "duplicate C02 vector item")
            current[index] = value
    ordered = {}
    for key, values in vectors.items():
        require(set(values) == set(range(len(values))), "C02 vector gap")
        ordered[key] = [values[i] for i in range(len(values))]
    return metrics, ordered


def compile_only(attempt: int) -> dict:
    require(1 <= attempt <= 99, "invalid build attempt")
    directory = RESEARCH / ("R33_B001_C02_BUILD_" + str(attempt).zfill(2))
    require(not directory.exists(), "build already recorded")
    directory.mkdir(mode=0o700)
    for name in SOURCES:
        with (directory / name).open("xb") as out: out.write((RESEARCH / name).read_bytes())
    command = [str(COMPILER), str(directory / SOURCES[1]), "--target", "macos-arm64", "--no-zagd", "--no-analyze", "--no-foreground-cache", "-o", str(directory / "c02")]
    result = bounded(command, directory, "compile", wall=60, cpu=55, output_limit=65536, sandboxed=False)
    report = {"status": "COMPILE_PASS_NOT_EXECUTED" if result["exit_code"] == 0 and result["termination_reason"] is None else "COMPILE_FAILURE",
              "date": utc(), "native_case_executions": 0, "compile": result,
              "compiler_sha256": digest(COMPILER), "source_pins": [{"path": str((directory / n).relative_to(ROOT)), "sha256": digest(directory / n)} for n in SOURCES]}
    if (directory / "c02").exists(): report["binary_sha256"] = digest(directory / "c02")
    write_json(directory / "BUILD_RECORD.json", report)
    return report


def change_state(status: str, case_count: int, result: dict | None = None) -> None:
    registry = load_json(RESEARCH / "R33_EXPERIMENT_REGISTRY.json")
    state = load_json(RESEARCH / "R33_CURRENT_STATE.json")
    consumed = load_json(RESEARCH / "R33_CONSUMED_EVIDENCE_REGISTRY.json")
    batch = next(x for x in registry["experiments"] if x["id"] == "R33-B001-C02")
    fixture = next(x for x in consumed["diagnostic_fixtures"] if x["batch_id"] == "R33-B001-C02")
    batch.update(status=status, primary_attempts=1, native_case_executions=case_count)
    registry["active_experiment"] = state["active_experiment"] = "R33-B001-C02" if status == "RUNNING" else None
    fixture.update(primary_executions=int(case_count > 0), native_case_executions=case_count,
                   status="CONSUMED_FILE_TRANSPORT_CASES" if case_count else "RESERVED")
    state.update(status="ENCODED_FILE_TRANSPORT_" + status, r33_native_experiments_executed=2+int(case_count>0),
                 next_action="Analyze actual encoded-file and snapshot evidence; continue relevant information-availability, durable telemetry and parent-state qualification")
    if result is not None: batch["result_status"] = result["status"]
    for name, value in (("R33_EXPERIMENT_REGISTRY.json", registry), ("R33_CURRENT_STATE.json", state), ("R33_CONSUMED_EVIDENCE_REGISTRY.json", consumed)):
        write_json(RESEARCH / name, value, exclusive=False)


def run() -> dict:
    verify_c01()
    require(load_json(RESEARCH/"R33_B001_C02_LAUNCH_PROBE/RESULT.json")["status"]=="PASS","C02 preflight incomplete")
    freeze = load_json(FREEZE)
    require(freeze["status"] == "PREREGISTERED_BEFORE_PRIMARY_EXECUTION", "C02 not frozen")
    validate_pins(freeze["pins"])
    registry = load_json(RESEARCH / "R33_EXPERIMENT_REGISTRY.json")
    batch = next(x for x in registry["experiments"] if x["id"] == "R33-B001-C02")
    require(registry["active_experiment"] is None and batch["primary_attempts"] == 0, "C02 unadmitted or active work")
    require(not RUN.exists(), "C02 primary already reserved")
    build_path = ROOT / freeze["build_record"]
    build = load_json(build_path)
    require(build["status"] == "COMPILE_PASS_NOT_EXECUTED", "no successful C02 build")
    validate_pins(build["source_pins"])
    require(digest(COMPILER) == build["compiler_sha256"], "compiler drift")
    for name in SOURCES: require(digest(RESEARCH/name) == digest(build_path.parent/name), "compiled-source drift")
    RUN.mkdir(mode=0o700)
    write_json(RUN / "RESERVATION.json", {"date":utc(), "batch":batch, "freeze_sha256":digest(FREEZE), "build_record_sha256":digest(build_path)})
    binary = RUN / "c02"
    with binary.open("xb") as out: out.write((build_path.parent / "c02").read_bytes())
    binary.chmod(0o700)
    require(digest(binary) == build["binary_sha256"], "binary copy mismatch")
    config = load_json(CONFIG)
    require(schedule_count(config) == config["expected_native_cases"], "C02 configuration schedule mismatch")
    result = {"batch_id":"R33-B001-C02", "status":"INCOMPLETE", "cases":[], "errors":[], "training_runs":0,
              "canonical_mutated":False, "learner_authority_granted":False, "promotion":False,
              "natural_perception_qualified":False, "crash_atomicity_qualified":False, "binary_sha256":digest(binary)}
    started = time.monotonic()
    captures = {}
    change_state("RUNNING", 0)

    def one(case_id: str, mode: str, source: Path, expected_packet: bytes | None,
            meta: dict | None, payload: bytes, status: int, capacity: int,
            following: Path | None = None, retained: tuple[bytes, dict] | None = None) -> Path:
        require(time.monotonic()-started < config["resources"]["batch_wall_seconds"], "C02 total budget exhausted")
        directory = RUN / case_id;directory.mkdir(mode=0o700)
        output = directory / "record.rrs"
        policy = sandbox_policy(directory,binary)
        command = ["/usr/bin/sandbox-exec","-p",policy,str(binary),mode,str(source),str(output),str(capacity)]
        if following is not None: command.append(str(following))
        admitted = {"id":case_id,"mode":mode,"input_path":str(source.relative_to(ROOT)),
                    "input_sha256":digest(source),"expected_status":status,
                    "date":utc(),"binary_sha256":digest(binary),"output_write_scope":str(directory)}
        if following is not None:
            admitted.update(following_sha256=digest(following), following_path=str(following.relative_to(ROOT)))
        write_json(directory / "ADMISSION.json", admitted)
        # Record the attempted case before launch; infrastructure failures stay consumed.
        case = {**admitted,"status":"ADMITTED_NOT_VALIDATED"};result["cases"].append(case)
        change_state("RUNNING", len(result["cases"]))
        remaining = config["resources"]["batch_wall_seconds"] - (time.monotonic()-started)
        observed = bounded(command,directory,"native",wall=min(config["resources"]["case_wall_seconds"],remaining),
                           cpu=config["resources"]["case_cpu_seconds"],output_limit=config["resources"]["case_output_bytes"],sandboxed=False)
        case["runtime"] = observed
        case["sandbox_scope_note"] = "Inner explicit sandbox profile permits only this fresh case directory writes; outer bounded runner flag describes its own wrapper"
        require(observed["exit_code"] == 0 and observed["termination_reason"] is None and observed["stderr_bytes"] == 0, "C02 native failure: "+case_id)
        require(observed["peak_rss_bytes"] <= config["resources"]["case_peak_rss_bytes"], "C02 measured RSS exceeded")
        metrics, vectors = parse_output((directory / "native.stdout").read_text())
        expected_m, expected_v = expected_output(status,meta,payload,mode,retained)
        require(metrics == expected_m and vectors == expected_v, "C02 state/metadata/value mismatch: "+case_id)
        if status == 0:
            require(meta is not None and expected_packet is not None,"missing success oracle")
            require(output.is_file() and output.read_bytes() == snapshot(expected_packet,meta), "C02 snapshot byte mismatch: "+case_id)
            case["snapshot_sha256"] = digest(output)
        else:
            require(not output.exists(), "C02 rejection wrote snapshot: "+case_id)
        require(digest(source)==admitted["input_sha256"], "native modified source file")
        if following is not None: require(digest(following)==admitted["following_sha256"], "native modified following file")
        case.update(status="MATCHED",observed_metrics=metrics,vector_elements_checked=sum(len(v) for v in vectors.values()))
        write_json(directory / "CASE_RESULT.json",case)
        return output

    try:
        for spec in config["cases"]:
            raw,meta,payload = packet(config,spec)
            source = RUN / (spec["id"]+".raw")
            with source.open("xb") as out: out.write(raw)
            capacity = max(0,len(raw)-1) if spec.get("capacity_short") else 131136
            if "capacity_delta" in spec: capacity = len(raw)+spec["capacity_delta"]
            if "capacity" in spec: capacity = spec["capacity"]
            saved = one(spec["id"],spec.get("mode","capture"),source,raw,meta,payload,spec["status"],capacity)
            if spec["status"] == 0: captures[spec["id"]] = (saved,raw,meta,payload)
        for name in config["reload_cases"]:
            saved,raw,meta,payload = captures[name]
            one(name+"_reload","reload",saved,raw,meta,payload,0,131136)
        follow = config["continuation"]
        saved,_,_,_ = captures[follow["parent"]]
        raw,meta,payload = packet(config,{"kind":"audio",**follow})
        source = RUN / "following.raw"
        with source.open("xb") as out: out.write(raw)
        one("continued_after_reload","continue",saved,raw,meta,payload,0,131136,source)
        parent_saved,parent_raw,parent_meta,_ = captures["audio_base"]
        for spec in config["continuation_controls"]:
            raw,meta,payload=packet(config,{"kind":"audio",**spec})
            source=RUN/(spec["id"]+".raw")
            with source.open("xb") as out: out.write(raw)
            one(spec["id"],"continue",parent_saved,raw,meta,payload,spec["status"],131136,source,
                (parent_raw,parent_meta) if spec["status"] else None)
        for mode in config["snapshot_alias_cases"]:
            saved,raw,meta,payload=captures["audio_base"]
            one(mode,mode,saved,raw,meta,payload,0,len(raw))
        for spec in config["snapshot_negatives"]:
            corrupt = bytearray(captures["audio_base"][0].read_bytes());corrupt[spec["offset"]] ^= 1
            raw = checksummed(bytes(corrupt),32) if spec["recompute_checksum"] else bytes(corrupt)
            source = RUN / (spec["id"]+".rrs")
            with source.open("xb") as out: out.write(raw)
            one(spec["id"],"reload",source,None,None,b"",spec["status"],131136)
        require(len(result["cases"])==config["expected_native_cases"],"C02 schedule incomplete")
        result["status"] = "ENCODED_FILE_AND_RELOAD_CASES_MATCHED"
    except Exception as error:
        result["errors"].append(repr(error));result["status"]="FAILED_REQUIRES_ANALYSIS"
    result["finished_utc"]=utc();result["batch_wall_seconds"]=time.monotonic()-started
    write_json(RUN / "RESULT.json",result)
    change_state("COMPLETED" if not result["errors"] else "FAILED_REQUIRES_ANALYSIS",len(result["cases"]),result)
    write_json(RUN / "MANIFEST.json",{"files":[{"path":str(p.relative_to(ROOT)),"sha256":digest(p),"bytes":p.stat().st_size}
               for p in sorted(RUN.rglob("*")) if p.is_file()]})
    return {"status":result["status"],"cases_attempted":len(result["cases"]),"errors":result["errors"],"result_path":str(RUN/"RESULT.json")}


def verify_saved() -> dict:
    freeze = load_json(FREEZE);validate_pins(freeze["pins"])
    result = load_json(RUN/"RESULT.json");manifest=load_json(RUN/"MANIFEST.json")
    validate_pins(manifest["files"])
    require(len(manifest["files"])==len({x["path"] for x in manifest["files"]}),"duplicate C02 artifact")
    for entry in manifest["files"]:
        path=ROOT/entry["path"]
        require(path.resolve().is_relative_to(RUN.resolve()) and path.stat().st_size==entry["bytes"],"C02 artifact scope/size drift")
    require(digest(FREEZE)==load_json(RUN/"RESERVATION.json")["freeze_sha256"],"C02 freeze changed")
    require(digest(RUN/"c02")==result["binary_sha256"],"C02 binary drift")
    require(result["training_runs"]==0 and not result["canonical_mutated"] and not result["promotion"]
            and not result["learner_authority_granted"] and not result["natural_perception_qualified"]
            and not result["crash_atomicity_qualified"],"C02 scope expanded")
    require({str(p.relative_to(ROOT)) for p in RUN.rglob("*") if p.is_file()}==
            {x["path"] for x in manifest["files"]}|{str((RUN/"MANIFEST.json").relative_to(ROOT))},"unmanifested C02 output")
    if result["status"]=="ENCODED_FILE_AND_RELOAD_CASES_MATCHED":
        config=load_json(CONFIG);expected={}
        require(len(result["cases"])==schedule_count(config)==config["expected_native_cases"] and not result["errors"],"false C02 completion")
        for spec in config["cases"]:
            raw,meta,payload=packet(config,spec)
            expected[spec["id"]]=(spec["status"],raw,meta,payload,spec.get("mode","capture"),None)
        for name in config["reload_cases"]:
            _,raw,meta,payload,_,_=expected[name];expected[name+"_reload"]=(0,raw,meta,payload,"reload",None)
        raw,meta,payload=packet(config,{"kind":"audio",**config["continuation"]})
        expected["continued_after_reload"]=(0,raw,meta,payload,"continue",None)
        _,parent_raw,parent_meta,parent_payload,_,_=expected["audio_base"]
        for spec in config["continuation_controls"]:
            raw,meta,payload=packet(config,{"kind":"audio",**spec})
            expected[spec["id"]]=(spec["status"],raw,meta,payload,"continue",(parent_raw,parent_meta) if spec["status"] else None)
        for mode in config["snapshot_alias_cases"]:expected[mode]=(0,parent_raw,parent_meta,parent_payload,mode,None)
        for spec in config["snapshot_negatives"]:expected[spec["id"]]=(spec["status"],None,None,b"","reload",None)
        require({c["id"] for c in result["cases"]}==set(expected),"C02 case identity mismatch")
        for case in result["cases"]:
            require(case["status"]=="MATCHED","unmatched C02 case")
            runtime=case["runtime"]
            require(runtime["exit_code"]==0 and runtime["termination_reason"] is None and runtime["stderr_bytes"]==0,"failed C02 runtime")
            for key,limit in (("wall_seconds",30),("cpu_seconds",20),("peak_rss_bytes",268435456),("stdout_bytes",8388608)):
                require(0<=runtime[key]<=limit,"C02 resource violation")
            for stream in ("stdout","stderr"):
                require(digest(RUN/case["id"]/("native."+stream))==runtime[stream+"_sha256"],"C02 stream drift")
            status,raw,meta,payload,mode,retained=expected[case["id"]]
            for prefix in ("input","following"):
                if prefix+"_path" in case:
                    path=ROOT/case[prefix+"_path"]
                    require(path.resolve().is_relative_to(RUN.resolve()) and digest(path)==case[prefix+"_sha256"],"C02 input drift")
            metrics,vectors=parse_output((RUN/case["id"]/"native.stdout").read_text())
            em,ev=expected_output(status,meta,payload,mode,retained)
            if status==0:
                require((RUN/case["id"]/"record.rrs").read_bytes()==snapshot(raw,meta),"C02 independent snapshot replay mismatch")
            else:
                require(not (RUN/case["id"]/"record.rrs").exists(),"rejection wrote record")
            require(metrics==em and vectors==ev,"C02 independent output replay mismatch")
    registry=load_json(RESEARCH/"R33_EXPERIMENT_REGISTRY.json")
    batch=next(x for x in registry["experiments"] if x["id"]=="R33-B001-C02")
    require(batch["primary_attempts"]==1 and batch["native_case_executions"]==len(result["cases"]),"C02 registry mismatch")
    return {"status":"PASS","result_status":result["status"],"native_cases":len(result["cases"]),"artifact_hashes":len(manifest["files"]),"natural_perception_qualified":False,"all_r33_complete":False}


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__);group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--compile",type=int);group.add_argument("--run",action="store_true");group.add_argument("--verify",action="store_true");group.add_argument("--preflight",action="store_true")
    args=parser.parse_args()
    try:
        report=compile_only(args.compile) if args.compile else preflight() if args.preflight else run() if args.run else verify_saved()
        print(json.dumps(report,indent=2));raise SystemExit(1 if report["status"] in ("COMPILE_FAILURE","FAILED_REQUIRES_ANALYSIS") else 0)
    except (ContractError,OSError,ValueError,KeyError,StopIteration) as error:
        print("R33_C02_FAIL: "+str(error),file=sys.stderr);raise SystemExit(1)
