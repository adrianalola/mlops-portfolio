# Cloud Security Capstone — Secure DB Access + Docker/TShark + IaC

This repository shows a defense-in-depth DB access pattern:
- Humans: **SSH tunnel** → PgBouncer loopback (127.0.0.1:6432)
- Services: **mTLS** to a scoped PgBouncer listener
- Evidence: **tshark (Wireshark CLI)** packet capture proving TLS
- Infra as Code: **Terraform + Ansible** samples

Quick start demo: `part1-db-secure-access/docker-demo/README.md`
