"""Synthetic ZIP boundary tests, never scientific observations."""
import io
from pathlib import Path
import runpy
import unittest
import warnings
import zipfile

V = runpy.run_path(str(Path(__file__).with_name("verify_archive.py")))


class ArchiveTests(unittest.TestCase):
    def fixture(self,names):
        blob = io.BytesIO()
        with warnings.catch_warnings(), zipfile.ZipFile(blob,"w") as archive:
            warnings.simplefilter("ignore",UserWarning)
            for name in names:
                archive.writestr(name,"SYNTHETIC_ONLY")
        blob.seek(0)
        return zipfile.ZipFile(blob)

    def test_normal_paths(self):
        with self.fixture(["RAW.log","inputs/Research/example.txt"]) as archive:
            self.assertEqual(len(V["inspect_zip"](archive)),2)

    def test_parent_traversal(self):
        with self.fixture(["../outside"]) as archive, self.assertRaisesRegex(ValueError,"unsafe"):
            V["inspect_zip"](archive)

    def test_absolute(self):
        with self.fixture(["/outside"]) as archive, self.assertRaisesRegex(ValueError,"unsafe"):
            V["inspect_zip"](archive)

    def test_backslash(self):
        with self.fixture(["..\\outside"]) as archive, self.assertRaisesRegex(ValueError,"unsafe"):
            V["inspect_zip"](archive)

    def test_duplicate(self):
        with self.fixture(["RAW.log","RAW.log"]) as archive, self.assertRaisesRegex(ValueError,"duplicate"):
            V["inspect_zip"](archive)

    def test_symlink(self):
        entry = zipfile.ZipInfo("link")
        entry.create_system = 3
        entry.external_attr = 0o120777 << 16
        with self.fixture([entry]) as archive, self.assertRaisesRegex(ValueError,"unsafe"):
            V["inspect_zip"](archive)


if __name__ == "__main__":
    unittest.main()
