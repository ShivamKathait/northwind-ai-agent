# Northwind Group consolidation (FY2024, GBP)

Take-home submission for Plainflow, bundle ID **NWG-D0BC**.

## Setup

Requires Python 3.10+. There are no runtime dependencies; pytest is needed only for the tests.

```bash
python3 -m pip install pytest   # only for `make test`
```

## Run

```bash
make run        # = PYTHONPATH=src python3 -m consol.run --data data --out output
make test
```

Outputs are written to `output/`. `data/` holds the input bundle exactly as received. `data/MANIFEST.sha256`
records its hashes; each run writes `output/run_provenance.json`, which says whether the inputs still match the bundle.

Status: Phase 0 skeleton. The consolidation stages are not implemented yet.
