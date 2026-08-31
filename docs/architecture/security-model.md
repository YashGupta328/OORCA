# Security Model

- **Authentication** — OAuth2 password flow with JWT access tokens. Token signing keys loaded from environment.
- **Authorisation** — role-based (`viewer`, `analyst`, `admin`). Permissions enforced in `backend/api/dependencies.py`.
- **Secrets** — never committed; loaded via `.env` and `backend/core/security.py`.
- **Network** — services are reachable only on a private docker network. Public exposure limited to the API gateway.
- **Data access** — RLS in PostgreSQL for investigation-scoped tables.
- **Audit** — every write operation recorded in the `audit` schema with actor, action and entity reference.
- **Supply chain** — pinned dependency versions in `pyproject.toml`; container images scanned in CI.