# Deploying the Agent-DID control plane

This runbook deploys the control plane to a single Linux VPS (e.g. your own server) and serves it over HTTPS at `https://<your-domain>`.

The stack is three containers, defined in [`deploy/docker-compose.prod.yml`](../deploy/docker-compose.prod.yml):

| Service | Role |
| ------- | ---- |
| `app`   | FastAPI control plane — gunicorn + uvicorn workers (`ENV=production`) |
| `db`    | PostgreSQL 16 — durable storage, safe for multiple workers |
| `caddy` | Reverse proxy — terminates TLS for `<your-domain>` with automatic Let's Encrypt |

Only Caddy is exposed to the internet (ports 80/443). The app and database stay
on the internal Docker network.

---

## 1. Point DNS at the server

In the Hostinger DNS panel for `<your-domain>` (DNS / Nameservers → Manage DNS records),
add these `A` records pointing at the VPS:

| Type | Name | Value          | TTL  |
| ---- | ---- | -------------- | ---- |
| A    | `@`  | `<SERVER_IP>` | 300  |
| A    | `www`| `<SERVER_IP>` | 300  |

> The nameservers shown are `ns1/ns2.dns-parking.com` (Hostinger's). As long as
> the domain uses Hostinger nameservers, these records take effect without any
> nameserver change. Allow a few minutes (up to the TTL) for propagation.

Verify propagation before continuing:

```bash
dig +short <your-domain>        # should print <SERVER_IP>
```

TLS issuance will fail until the A record resolves to this server and ports
80/443 are reachable, so don't skip this check.

## 2. Prepare the server

SSH into the VPS and install Docker Engine + the Compose plugin:

```bash
ssh root@<SERVER_IP>

# Docker (official convenience script)
curl -fsSL https://get.docker.com | sh
docker --version && docker compose version
```

Open the web ports (if a firewall is enabled):

```bash
# ufw example — adjust for your firewall
ufw allow 80/tcp
ufw allow 443/tcp
```

## 3. Get the code

```bash
git clone https://github.com/didoneworld/Agent-DID.git
cd Agent-DID
git checkout claude/magical-tesla-P8Xdp   # until this is merged to main
```

## 4. Configure secrets

```bash
cp deploy/.env.prod.example deploy/.env.prod
```

Edit `deploy/.env.prod` and set, at minimum:

- `ACME_EMAIL` — your email for Let's Encrypt notices.
- `SESSION_SIGNING_SECRET` — `openssl rand -hex 32`
- `POSTGRES_PASSWORD` — `openssl rand -hex 24`

`DOMAIN` is already `<your-domain>`. The app refuses to start in production without
`SESSION_SIGNING_SECRET`, so this step is mandatory.

`deploy/.env.prod` is git-ignored — keep it on the server only.

## 5. Launch

```bash
docker compose --env-file deploy/.env.prod \
  -f deploy/docker-compose.prod.yml up -d --build
```

Watch the logs while Caddy obtains the certificate (first boot only):

```bash
docker compose --env-file deploy/.env.prod \
  -f deploy/docker-compose.prod.yml logs -f caddy
```

## 6. Verify

```bash
# From the server or anywhere once DNS has propagated:
curl -fsS https://<your-domain>/health                       # -> {"status":"ok", ...}
curl -fsS https://<your-domain>/.well-known/openid-configuration | head
```

The OpenAPI docs are served at `https://<your-domain>/docs`.

---

## Operations

**View logs**

```bash
docker compose --env-file deploy/.env.prod -f deploy/docker-compose.prod.yml logs -f app
```

**Update to a new version**

```bash
git pull
docker compose --env-file deploy/.env.prod \
  -f deploy/docker-compose.prod.yml up -d --build
```

**Back up the database**

```bash
docker compose --env-file deploy/.env.prod -f deploy/docker-compose.prod.yml \
  exec db pg_dump -U agentid agentid > backup-$(date +%F).sql
```

**Restore a backup**

```bash
cat backup-YYYY-MM-DD.sql | docker compose --env-file deploy/.env.prod \
  -f deploy/docker-compose.prod.yml exec -T db psql -U agentid -d agentid
```

**Stop / start**

```bash
docker compose --env-file deploy/.env.prod -f deploy/docker-compose.prod.yml down   # stop (data volumes persist)
docker compose --env-file deploy/.env.prod -f deploy/docker-compose.prod.yml up -d   # start
```

---

## Troubleshooting

| Symptom | Likely cause / fix |
| ------- | ------------------ |
| TLS cert never issues | `<your-domain>` doesn't resolve to this server yet, or ports 80/443 are blocked. Re-check `dig +short <your-domain>` and the firewall. |
| `502 Bad Gateway` from Caddy | The `app` container isn't healthy yet. `... logs app` — most often a missing `SESSION_SIGNING_SECRET` (app exits on boot in production). |
| `app` restarts on boot | `SESSION_SIGNING_SECRET` unset, or `DATABASE_URL` can't reach `db`. Confirm `deploy/.env.prod` is passed via `--env-file`. |
| Want to run without Postgres | The app falls back to SQLite when `DATABASE_URL` is unset. Drop the `db` service and the `DATABASE_URL`/`depends_on` lines from the app service, and mount a volume at `/app/data` to persist the SQLite file. Postgres is recommended for multi-worker durability. |
