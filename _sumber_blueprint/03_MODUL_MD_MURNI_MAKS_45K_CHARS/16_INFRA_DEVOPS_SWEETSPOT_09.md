
<!-- [ID:16_INFRA_DEVOPS_S130] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: INTERNAL, ALL, NO-NEW-PRIVILEGES:TRUE, ORCHESTRATOR, SCANNER_NET -->
# Sandbox: no privileged mode, no docker socket, no host network
EXPOSE 8002
CMD ["uvicorn", "services.scanner.main:app", "--host", "0.0.0.0", "--port", "8002"]

version: "3.9"

x-common: &common
  restart: unless-stopped
  env_file: [../../.env]
  networks: [internal]

x-secure: &secure
  <<: *common
  read_only: true
  tmpfs: [/tmp]
  cap_drop: [ALL]
  security_opt: [no-new-privileges:true]

services:
  orchestrator:
    <<: *secure
    build:
      context: ../..
      dockerfile: infra/docker/Dockerfile.orchestrator
    ports: ["8000:8000"]
    volumes:
      - ../../office/logs:/app/office/logs
      - ../../office/brain:/app/office/brain:ro
      - ../../office/config:/app/office/config:ro
    depends_on: [redis, postgres]

  payment:
    <<: *secure
    build:
      context: ../..
      dockerfile: infra/docker/Dockerfile.payment
    ports: ["8001:8001"]
    volumes:
      - ../../services/payment/store:/app/services/payment/store
      - ../../office/logs:/app/office/logs
    depends_on: [orchestrator]

  scanner:
    <<: *secure
    build:
      context: ../..
      dockerfile: infra/docker/Dockerfile.scanner
    ports: ["8002:8002"]
    # Sandbox: tanpa host network, tanpa akses .env sensitif (gunakan .env.scanner)
    env_file: [../../.env.scanner]
    networks: [scanner_net]     # network terpisah
    volumes:
      - ../../services/scanner/reports:/app/services/scanner/reports
    depends_on: [orchestrator]

  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-devpass}
      POSTGRES_DB: office
    volumes: [pg_data:/var/lib/postgresql/data]
    networks: [internal]

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    networks: [internal]

networks:
  internal:
  scanner_net:      # scanner isolated dari internal
    internal: true

volumes:
  pg_data:


<!-- [ID:16_INFRA_DEVOPS_S131] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# Cloudflare WAF — Rules Wajib


<!-- [ID:16_INFRA_DEVOPS_S132] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## 4. Managed Rules
- OWASP Core Ruleset: ON.
- Cloudflare Managed: ON.
- Anomaly score: block > 50, challenge > 20.


<!-- [ID:16_INFRA_DEVOPS_S133] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## 5. Origin Protection
- Cloudflare Tunnel (cloudflared) — origin TIDAK terbuka ke internet.
- mTLS antara CF dan origin.
- Header wajib di origin: `CF-Access-Jwt-Assertion` valid.


<!-- [ID:16_INFRA_DEVOPS_S134] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## 6. Kill switch integration
- Cloudflare Worker subscribe ke KV "kill_switch" → bila L0/L2 aktif,
  worker return 503 untuk semua request non-owner.

// Cloudflare Worker: cek KV kill_switch, block bila aktif.
export default {
  async fetch(req, env) {
    const state = await env.KILL_SWITCH.get("state"); // "OFF" | "L0" | "L1" | ...
    if (state && state !== "OFF" && state !== "null") {
      const isOwner = req.headers.get("X-Owner-Token") === env.OWNER_TOKEN;
      if (!isOwner) {
        return new Response(JSON.stringify({
          ok: false, reason: `kill_switch:${state}`
        }), { status: 503, headers: { "content-type": "application/json" }});
      }
    }
    return fetch(req);
  }
}

terraform {
  required_version = ">= 1.6"
  required_providers {
    cloudflare = { source = "cloudflare/cloudflare", version = "~> 4.0" }
  }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

resource "cloudflare_record" "app" {
  zone_id = var.zone_id
  name    = var.domain
  value   = var.tunnel_cname
  type    = "CNAME"
  proxied = true
}

resource "cloudflare_ruleset" "waf_custom" {
  zone_id = var.zone_id
  name    = "custom-waf"
  kind    = "zone"
  phase   = "http_request_firewall_custom"

  rules {
    action      = "block"
    expression  = "(http.request.uri.path contains \"/payment\" and http.request.method eq \"POST\" and not cf.bot_management.verified_bot)"
    description = "block unverified bot on payment"
  }

  rules {
    action      = "challenge"
    expression  = "(http.request.uri.path contains \"/scan\")"
    description = "challenge scanner endpoints"
  }

  rules {
    action      = "block"
    expression  = "(ip.geoip.country in {\"T1\"})"   # TOR
    description = "block TOR"
  }
}

resource "cloudflare_ruleset" "ratelimit" {
  zone_id = var.zone_id
  name    = "ratelimit"
  kind    = "zone"
  phase   = "http_ratelimit"

  rules {
    action      = "block"
    expression  = "(http.request.uri.path contains \"/payment\")"
    description = "payment 10/min"
    ratelimit {
      characteristics     = ["ip.src"]
      period              = 60
      requests_per_period = 10
      mitigation_timeout  = 900
    }
  }

  rules {
    action      = "block"
    expression  = "(http.request.uri.path contains \"/scan\")"
    description = "scan 20/min"
    ratelimit {
      characteristics     = ["ip.src"]
      period              = 60
      requests_per_period = 20
      mitigation_timeout  = 600
    }
  }
}

resource "cloudflare_tunnel" "origin" {
  account_id = var.account_id
  name       = "office-origin"
  secret     = var.tunnel_secret
}

variable "cloudflare_api_token" { type = string, sensitive = true }
variable "account_id"           { type = string }
variable "zone_id"              { type = string }
variable "domain"               { type = string, default = "app" }
variable "tunnel_cname"         { type = string }
variable "tunnel_secret"        { type = string, sensitive = true }


<!-- [ID:16_INFRA_DEVOPS_S135] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# PRIVATE_KEY, SEED_PHRASE, OPENAI_API_KEY, BANK_API_SECRET, dsb.

.PHONY: bootstrap agents security up down health

bootstrap:
	python scripts/bootstrap.py

agents:
	python scripts/gen_agents.py

security:
	bash scripts/security-check.sh

up:
	docker compose -f infra/docker/docker-compose.dev.yml up --build -d

down:
	docker compose -f infra/docker/docker-compose.dev.yml down

health:
	python scripts/healthcheck.py

Paket Isi Fungsi
5 services/payment/* Semua uang keluar lewat gate FIN, risk scoring, tidak ada jalur lain
6 services/scanner/* Airdrop / bansos / program finder / NVIDIA Spectrum — sandbox read-only ketat
7 infra/* Docker non-root+read-only, compose dengan network terisolasi, Cloudflare WAF + Worker kill switch, Terraform ruleset
8 scripts/* + Makefile + requirements.txt + api.py Tinggal make bootstrap && make agents && make up && make health

make bootstrap           # buat struktur
python scripts/gen_agents.py

<!-- [ID:16_INFRA_DEVOPS_S136] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ── Embedded Username & Credential Seed Pools ───────────────────────
ADJ = [
    "swift", "quiet", "brave", "lucky", "cosmic", "rapid", "clever", "mellow",
    "crimson", "golden", "amber", "bright", "calm", "coral", "daring", "eager",
    "fierce", "gentle", "icy", "jolly", "kind", "lunar", "misty", "noble",
    "polar", "proud", "rusty", "silver", "solar", "tidy", "vivid", "wild",
    "bold", "cozy", "keen", "nimble"
]
NOUN = [
    "eagle", "otter", "falcon", "panda", "comet", "signal", "raven", "tiger",
    "nebula", "lynx", "badger", "birch", "bison", "cedar", "cloud", "crane",
    "dove", "ember", "fern", "finch", "fox", "heron", "maple", "mink",
    "moose", "orca", "owl", "pebble", "pine", "robin", "seal", "spruce",
    "stork", "whale", "wren", "brook"
]

