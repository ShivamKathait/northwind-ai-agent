"""Entry point: python -m consol.run --data data --out output"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

MANIFEST = "MANIFEST.sha256"


def verify_manifest(data_dir: Path) -> list[dict]:
    """Compare input files with the bundle manifest.

    A mismatch is reported, not fatal: inputs are expected to change (new data, what-if runs),
    but every run must say whether it consolidated the original bundle or something else.
    """
    findings: list[dict] = []
    manifest_path = data_dir / MANIFEST
    if not manifest_path.exists():
        return [{"file": MANIFEST, "status": "missing", "detail": "no manifest; input provenance unknown"}]
    expected = {}
    for line in manifest_path.read_text().splitlines():
        if line.strip():
            digest, name = line.split(maxsplit=1)
            expected[name.strip()] = digest
    for name, digest in sorted(expected.items()):
        path = data_dir / name
        if not path.exists():
            findings.append({"file": name, "status": "missing", "detail": "listed in manifest but absent"})
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            findings.append({"file": name, "status": "changed", "expected": digest, "actual": actual})
    for path in sorted(data_dir.iterdir()):
        if path.is_file() and path.name != MANIFEST and path.name not in expected:
            findings.append({"file": path.name, "status": "unlisted", "detail": "not in manifest"})
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Consolidate Northwind Group FY2024 in GBP")
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--out", type=Path, default=Path("output"))
    parser.add_argument("--llm", action="store_true",
                        help="also run the optional LLM mapping reviewer (proposals only, never feeds figures)")
    args = parser.parse_args(argv)

    if not args.data.is_dir():
        print(f"data directory not found: {args.data}", file=sys.stderr)
        return 2
    args.out.mkdir(parents=True, exist_ok=True)

    provenance = verify_manifest(args.data)
    for f in provenance:
        print(f"WARNING input provenance: {f['file']} {f['status']}", file=sys.stderr)
    (args.out / "run_provenance.json").write_text(
        json.dumps({"inputs_match_manifest": not provenance, "findings": provenance}, indent=2) + "\n")

    # Pipeline stages are added in later phases.
    return 0


if __name__ == "__main__":
    sys.exit(main())
