# Matt's OpenSwarm Setup

Local setup created by Pauline on 2026-05-09.

## Paths

- Repo clone: `~/Documents/OpenSwarm/OpenSwarm`
- Test deck: `~/Documents/OpenSwarm/open_swarm.pptx`

## Local tools

- Node.js: user-local under `~/opt/node-current`
- npm global prefix: `~/.npm-global`
- uv/Python manager: `~/.local/bin/uv`
- Python 3.12: installed via `uv python install 3.12`
- OpenSwarm CLI: `~/.npm-global/bin/openswarm`

## Shell setup

`~/.zshrc` now adds:

```bash
export PATH="$HOME/opt/node-current/bin:$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"
```

## Next setup items

- Create or connect Matt's GitHub fork, then update `origin` to the fork and add upstream as `VRSEN/OpenSwarm`.
- Add provider credentials through `openswarm providers` or a local `.env` copied from `.env.example`.
- Use the test deck with the slides/docs workflow once provider auth is configured.
