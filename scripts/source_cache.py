"""Retain public source downloads once, with URL/date/hash evidence. No secrets."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import requests


def fetch(url: str, output: Path, log: Path) -> Path | None:
    output.parent.mkdir(parents=True, exist_ok=True)
    log.parent.mkdir(parents=True, exist_ok=True)
    entry = {"url": url, "path": str(output), "retrieved_at": datetime.now(timezone.utc).isoformat()}
    if output.exists():
        entry.update(status="retained_existing_no_network", sha256=hashlib.sha256(output.read_bytes()).hexdigest())
    else:
        try:
            response = requests.get(url, timeout=90, headers={"User-Agent": "PinkerChartsResearch/1.0"})
            entry.update(http_status=response.status_code, final_url=response.url, content_type=response.headers.get("Content-Type"))
            response.raise_for_status()
            output.write_bytes(response.content)
            entry.update(status="downloaded", sha256=hashlib.sha256(response.content).hexdigest(), bytes=len(response.content))
        except requests.RequestException as exc:
            entry.update(status="failed", error=str(exc))
    # Downloads may overlap; read the latest log only while holding its lock.
    with log.open("a+") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.seek(0)
        content = handle.read()
        history = json.loads(content) if content else []
        history.append(entry)
        handle.seek(0)
        handle.truncate()
        handle.write(json.dumps(history, indent=2) + "\n")
    print(json.dumps(entry))
    return output if output.exists() else None


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("url")
    p.add_argument("output", type=Path)
    p.add_argument("--log", type=Path, required=True)
    a = p.parse_args()
    raise SystemExit(0 if fetch(a.url, a.output, a.log) else 1)
