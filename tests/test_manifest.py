import shutil
from pathlib import Path

from consol.run import verify_manifest

DATA = Path(__file__).resolve().parents[1] / "data"


def test_bundle_matches_manifest():
    assert verify_manifest(DATA) == []


def test_changed_input_is_reported(tmp_path):
    copy = tmp_path / "data"
    shutil.copytree(DATA, copy)
    with open(copy / "fx_rates.csv", "ab") as f:
        f.write(b"GBP,SGD,closing,1.7000,2024-12-31,SGD per 1 GBP\r\n")
    findings = verify_manifest(copy)
    assert [(f["file"], f["status"]) for f in findings] == [("fx_rates.csv", "changed")]


def test_unlisted_and_missing_files_are_reported(tmp_path):
    copy = tmp_path / "data"
    shutil.copytree(DATA, copy)
    (copy / "tb_in.csv").unlink()
    (copy / "extra.csv").write_text("x\n")
    statuses = {(f["file"], f["status"]) for f in verify_manifest(copy)}
    assert statuses == {("tb_in.csv", "missing"), ("extra.csv", "unlisted")}
