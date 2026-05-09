# VWMedia Proposal Swarm Job Output Contract

## Canonical Root

All durable job outputs must be written under the AI Shared Drive:

```text
/Volumes/AISharedDrive/family-agents/shared/projects/vwmedia-proposal-swarm/jobs/{jobId}/
```

The repository-local `mnt/{jobId}` path is allowed only as a compatibility alias for OpenSwarm tools. It should be a symlink to the canonical shared folder, not a separate copy.

## Required Job Structure

```text
jobs/{jobId}/
  input.json or inputs/input.json
  manifest.json
  working/
  logs/
  runs/
  outputs/
    final/
      proposal-deck.pptx    # if generated
      proposal-deck.pdf
      proposal.pdf
      quote.pdf
      internal-scoping-document.pdf
```

## Rules

1. Generate a unique job ID for every enquiry.
2. Do not reuse another client's folder.
3. Do not write final artifacts only to the repo-local `mnt/` directory.
4. If a tool requires `mnt/{jobId}`, create it as a symlink to the shared job folder.
5. Put temporary files in `working/`, logs in `logs/`, and review-ready files in `outputs/final/`.
6. Update `manifest.json` whenever status changes.
7. Never overwrite previous runs silently; use `runs/001`, `runs/002`, or archive/timestamped folders for reruns.

## Status Values

Use these status values in `manifest.json`:

- `created`
- `queued`
- `researching`
- `drafting`
- `rendering`
- `review-ready`
- `approved`
- `blocked`
- `failed`
