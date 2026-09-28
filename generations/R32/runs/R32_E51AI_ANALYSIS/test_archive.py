"""Synthetic archive rejection tests; never experimental evidence."""
import json
from pathlib import Path
import runpy
import tempfile
import unittest
import warnings
import zipfile

AUDIT = runpy.run_path(str(Path(__file__).with_name("verify_archive.py")))


class ArchiveTests(unittest.TestCase):
    def fixture(self, base):
        run = {"id": AUDIT["RUN"], "run_attempt": 1, "workflow_id": 350732604,
               "repository": {"full_name": "Sylorlabs/TNN"}, "head_sha": AUDIT["SOURCE"],
               "head_commit": {"tree_id": AUDIT["TREE"]}, "status": "completed"}
        jobs = {"jobs": [{"id": AUDIT["JOB"], "run_id": AUDIT["RUN"], "head_sha": AUDIT["SOURCE"]}]}
        (base / "RUN.json").write_text(json.dumps(run))
        (base / "JOBS.json").write_text(json.dumps(jobs))
        with zipfile.ZipFile(base / "artifact.zip", "w") as archive:
            archive.writestr("SYNTHETIC_ONLY.txt", "NOT AN EXPERIMENT")
        self.metadata(base)
        return run

    def metadata(self, base):
        data = (base / "artifact.zip").read_bytes()
        artifact = {"name": "r32-e51ai-native-" + AUDIT["SOURCE"],
                    "workflow_run": {"id": AUDIT["RUN"], "head_sha": AUDIT["SOURCE"]},
                    "size_in_bytes": len(data), "digest": "sha256:" + AUDIT["digest"](data)}
        (base / "ARTIFACTS.json").write_text(json.dumps({"artifacts": [artifact]}))

    def reject(self, change, message):
        with tempfile.TemporaryDirectory(prefix="e51ai-synthetic-audit-") as directory:
            base = Path(directory)
            run = self.fixture(base)
            change(base, run)
            with self.assertRaisesRegex(ValueError, message):
                AUDIT["audit"](base, base)
            self.assertFalse((base / "extracted").exists())

    def test_wrong_run(self):
        def change(base, run):
            run["id"] = -1
            (base / "RUN.json").write_text(json.dumps(run))
        self.reject(change, "run/attempt/workflow mismatch")

    def test_running_is_not_complete(self):
        def change(base, run):
            run["status"] = "in_progress"
            (base / "RUN.json").write_text(json.dumps(run))
        self.reject(change, "run not terminal")

    def test_wrong_digest(self):
        def change(base, run):
            meta = json.loads((base / "ARTIFACTS.json").read_text())
            meta["artifacts"][0]["digest"] = "sha256:" + "0" * 64
            (base / "ARTIFACTS.json").write_text(json.dumps(meta))
        self.reject(change, "digest mismatch")

    def test_path_traversal(self):
        def change(base, run):
            with zipfile.ZipFile(base / "artifact.zip", "a") as archive:
                archive.writestr("../outside", "unsafe")
            self.metadata(base)
        self.reject(change, "unsafe member")

    def test_duplicate_member(self):
        def change(base, run):
            with warnings.catch_warnings(), zipfile.ZipFile(base / "artifact.zip", "a") as archive:
                warnings.simplefilter("ignore", UserWarning)
                archive.writestr("SYNTHETIC_ONLY.txt", "duplicate")
            self.metadata(base)
        self.reject(change, "duplicate archive members")

    def test_symlink(self):
        def change(base, run):
            entry = zipfile.ZipInfo("link")
            entry.create_system = 3
            entry.external_attr = 0o120777 << 16
            with zipfile.ZipFile(base / "artifact.zip", "a") as archive:
                archive.writestr(entry, "/outside")
            self.metadata(base)
        self.reject(change, "unsafe member or symlink")


if __name__ == "__main__":
    unittest.main()
