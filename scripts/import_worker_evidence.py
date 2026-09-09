"""Import reviewed worker deltas; quarantine chart-label-derived candidate work."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
POLICIES = {
    "5-3": ("d69b11bf", "547f52fd", "supplement_only",
            "Retain newer GitHub OWID 522 package; add missing worker source files and preserve worker narrative separately."),
    "7-3": ("b47ad4f4", "d4682dab", "canonical",
            "Archived FAO workbook recovers named regional series and three-year window midpoints; remains partial, not exact FAO 2014 vintage."),
    "7-4": ("b0ce1e4c", "a0b88a89", "quarantine",
            "Worker canonical values were transcribed from source-chart labels; not accepted reconstruction input under the approved plan. Preserve event-table recovery and candidate evidence."),
    "12-5": ("959d9710", "25c7c29c", "canonical",
             "Recovered processed OWID/ASN passenger-normalized successor replaces less appropriate proxy; exact book vintage remains partial."),
}


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    report = []
    for fid, (base, head, mode, reason) in POLICIES.items():
        base = git("rev-parse", base).decode().strip()
        head = git("rev-parse", head).decode().strip()
        paths = git("diff", "--name-only", base, head, "--", f"figures/{fid}", f"scripts/reconstruct_{fid.replace('-', '_')}.py").decode().splitlines()
        for path in paths:
            data = git("show", f"{head}:{path}")
            target = ROOT / path
            is_source = "/data/raw/" in path or "/data/candidates/" in path
            preserve_only = mode != "canonical" and not (is_source and not target.exists())
            if preserve_only:
                target = ROOT / "reports/consolidation/worker_candidates" / fid / path
            elif target.exists() and any(part in path for part in ["/source_logs/", "/search_iterations/"]):
                data = (target.read_bytes() + f"\n\n## Worker Recovery At {head}\n\n".encode() + data)
            row = {"figure_id": fid, "base_sha": base, "head_sha": head,
                   "source_path": path, "destination": str(target.relative_to(ROOT)),
                   "source_sha256": hashlib.sha256(git("show", f"{head}:{path}")).hexdigest(),
                   "selected_sha256": hashlib.sha256(data).hexdigest(),
                   "policy": mode, "reason": reason}
            report.append(row)
            if args.apply:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
    if args.apply:
        (ROOT / "reports/consolidation/worker_import_manifest.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"apply": args.apply, "files": len(report), "policies": POLICIES}, indent=2))


if __name__ == "__main__":
    main()
