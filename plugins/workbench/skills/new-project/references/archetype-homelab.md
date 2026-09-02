# Archetype: homelab service

Layout: `compose.yml` at the root as the source of truth for the host, `config/` for
mounted configuration, `backup/` for backup artefacts (gitignored except `.gitkeep`),
`docs/runbook.md` for operations.

## What SPEC.md needs

- **§2 Decisions** — which host, which image and why that one over the alternatives,
  reverse proxy and hostname, whether it is exposed outside the LAN (and if so, what
  fronts it).
- **§5 Dependencies and access** — what it talks to: a database container, an NFS mount,
  another service on the LAN, an external API. Ports it claims on the host — a port
  registry in the spec is unglamorous and saves a genuinely annoying afternoon.
- **§6 Verification** — how you know it is up and actually working, not just running:

  ```bash
  docker compose ps            # expected: state Up, health healthy
  docker compose logs --tail=50 <svc>
  curl -fsS http://<host>:<port>/healthz
  ```

  A container in state `Up` proves the process started, not that the service works. The
  health check is the real test.

## Traps worth a hard rule

- **Drift between the box and the file.** Changes made by hand on the host and never
  written back are how a service becomes unreproducible. `compose.yml` wins; if they have
  diverged, re-apply from the file.
- **`:latest`.** Pin the tag. With `:latest`, rollback becomes archaeology and "it broke
  overnight and nothing changed" becomes a sentence you say out loud.
- **Untested restores.** `docs/runbook.md` has a `Last tested:` line. Keep it honest —
  a backup nobody has restored from is a hypothesis, not a backup.
- **Volumes without a stated home.** Say where persistent data lives on the host and
  whether it is in the backup set. Bind mount vs named volume is a decision; record it.
- **`.env` on the host.** It holds real values, it is gitignored, and it is generated
  from `.env.example` via the password manager (`op inject`). It never gets committed and
  never gets pasted anywhere.
