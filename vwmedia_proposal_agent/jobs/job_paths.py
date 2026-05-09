from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

CANONICAL_ROOT = Path(
    os.environ.get(
        "VWMEDIA_PROPOSAL_SWARM_ROOT",
        "/Volumes/AISharedDrive/family-agents/shared/projects/vwmedia-proposal-swarm/jobs",
    )
)


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "enquiry"


def make_job_id(business_name: str, submitted_at: str | None = None, sequence: str = "001") -> str:
    """Return a stable folder-friendly job id for a website enquiry."""
    if submitted_at:
        try:
            day = datetime.fromisoformat(submitted_at.replace("Z", "+00:00")).strftime("%Y-%m-%d")
        except ValueError:
            day = datetime.now().strftime("%Y-%m-%d")
    else:
        day = datetime.now().strftime("%Y-%m-%d")
    return f"{day}-{slugify(business_name)}-{sequence}"


def job_dir(job_id: str) -> Path:
    return CANONICAL_ROOT / job_id


def final_outputs_dir(job_id: str) -> Path:
    return job_dir(job_id) / "outputs" / "final"


def repo_mnt_alias(repo_root: str | Path, job_id: str) -> Path:
    return Path(repo_root) / "mnt" / slugify(job_id)


def ensure_job_structure(job_id: str, repo_root: str | Path | None = None) -> Path:
    root = job_dir(job_id)
    for rel in ["inputs", "working", "logs", "runs", "outputs/final"]:
        (root / rel).mkdir(parents=True, exist_ok=True)
    if repo_root is not None:
        alias = repo_mnt_alias(repo_root, job_id)
        alias.parent.mkdir(parents=True, exist_ok=True)
        if alias.exists() and not alias.is_symlink():
            archive = alias.with_name(alias.name + ".local-archive")
            counter = 1
            while archive.exists():
                counter += 1
                archive = alias.with_name(alias.name + f".local-archive-{counter}")
            alias.rename(archive)
        if alias.is_symlink() or not alias.exists():
            try:
                alias.unlink()
            except FileNotFoundError:
                pass
            alias.symlink_to(root, target_is_directory=True)
    return root


def write_manifest(job_id: str, status: str, data: dict[str, Any] | None = None) -> Path:
    root = ensure_job_structure(job_id)
    path = root / "manifest.json"
    payload: dict[str, Any] = {}
    if path.exists():
        try:
            payload = json.loads(path.read_text())
        except Exception:
            payload = {}
    payload.update(data or {})
    payload.update(
        {
            "jobId": job_id,
            "status": status,
            "canonicalRoot": str(root),
            "finalOutputs": str(root / "outputs" / "final"),
            "updatedAt": datetime.now().isoformat(timespec="seconds"),
        }
    )
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create/inspect VWMedia Proposal Swarm job folders")
    parser.add_argument("job_id")
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--status", default="created")
    args = parser.parse_args()
    root = ensure_job_structure(args.job_id, args.repo_root)
    manifest = write_manifest(args.job_id, args.status)
    print(root)
    print(manifest)
