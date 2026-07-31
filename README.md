<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/social_preview_dark.png" />
    <source media="(prefers-color-scheme: light)" srcset="docs/social_preview_light.png" />
    <img src="docs/social_preview_light.png" alt="Coupon Management Platform" width="880" />
  </picture>
</p>

# Coupon Management Platform

> A Django web application implemented against two database backends — PostgreSQL and MongoDB — for community-driven coupon sharing, built to compare relational and document storage under identical workloads using Locust load tests.

[![CI](https://img.shields.io/github/actions/workflow/status/mtorun0x7cd/coupon-management/ci.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=CI)](https://github.com/mtorun0x7cd/coupon-management/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python_3-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django_4.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Locust](https://img.shields.io/badge/Locust-006600?style=for-the-badge&logo=locust&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

> **Archived.** A frozen record of completed work, preserved for reference and not actively maintained. See [`SECURITY.md`](SECURITY.md) for scope and disclosures.

---

## Overview

This platform lets users create, share, and discover discount coupons within a community. Registered users post coupons with discount metadata, upvote or downvote submissions, comment on deals, and find coupons through a hashtag-based taxonomy and search.

The technical focus is a **comparative storage-engine study**: the same Django application is run against two distinct database backends — PostgreSQL (relational, via `psycopg2`) and MongoDB (document-oriented, via Djongo). Both deployments share the same domain model, view, form, and URL layer, differing in the `settings.py` database configuration. This isolates storage-engine behaviour from application logic and makes the two engines directly comparable under identical workloads.

Load is generated with **Locust**, and seed scripts populate each backend with stated volumes of synthetic test data; record content is drawn from an unseeded RNG, so two seeding runs are comparable by volume rather than byte-identical. This is an archived academic team deliverable, retained for reference; it is not maintained and is not suitable for production use (see [Security](#security)).

## Context

| Dimension | Detail |
| :--- | :--- |
| **Institution** | TH Köln (University of Applied Sciences) |
| **Program** | Computer Science & Engineering (Technische Informatik), M.Sc. |
| **Course** | Large and Cloud-based Software Systems (LCSS) |
| **Semester** | Summer 2023 |
| **Type** | Team |

## Features

- **User management** — registration, authentication, a password-change screen (non-functional in the archived code — see [`SECURITY.md`](SECURITY.md)), and a per-user coupon history via Django's built-in auth system
- **Coupon creation** — coupons with name, discount amount, expiration date, and an auto-generated coupon code derived from the name and discount
- **Voting** — upvote/downvote with an aggregate score tracked per coupon
- **Comments** — user comments on individual coupons, with a recomputed comment count
- **Hashtag taxonomy** — tag coupons with hashtags (auto-prefixed with `#`), then browse and search by hashtag through a global search form
- **Admin console** — Django admin registration for the `Coupon`, `Comment`, and `Hashtag` models
- **Dual database backends** — identical application logic running on PostgreSQL and on MongoDB via Djongo
- **Performance benchmarking** — Locust scenarios for HTTP-level and direct-query comparison of the two backends
- **Database seeding** — scripts that populate either backend with synthetic users and coupons at the volumes fixed in the scripts

The actor-level scope of the application is summarised below (PlantUML source: [`assets/use_case.puml`](assets/use_case.puml)).

![Use Case Diagram](assets/use_case.png)

## Architecture

The project ships two parallel Django deployments under `src/`, each targeting a different storage engine:

```text
src/
├── postgresql/lcss/     # Django project backed by PostgreSQL (psycopg2)
│   ├── coupon/          # App: models, views, forms, templates
│   └── lcss/            # Project settings, URLs, WSGI/ASGI
└── mongodb/lcss/        # Django project backed by MongoDB (Djongo)
    ├── coupon/          # App: identical model/view layer
    └── lcss/            # Project settings (Djongo engine)
```

The model, view, form, and URL layers are the same across the two variants; the substantive difference between them is the `settings.py` database engine. This isolates storage-engine performance from application logic.

```text
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Browser   │────▶│  Django App  │────▶│  PostgreSQL     │
│   (Client)  │     │  (Views,     │     │  OR             │
│             │◀────│   Forms,     │◀────│  MongoDB (Atlas)│
└─────────────┘     │   Templates) │     └─────────────────┘
                    └──────────────┘
                           ▲
                           │
                    ┌──────────────┐
                    │  Locust      │
                    │  (Load Test) │
                    └──────────────┘
```

The domain model consists of three entities:

- **Coupon** — linked to `auth.User` via `ForeignKey`; stores name, expiration, discount amount, score, code, comment count, and a many-to-many relation to Hashtag
- **Comment** — linked to both Coupon and User; stores text and an auto-timestamped creation date
- **Hashtag** — unique name field, auto-prepended with a `#` prefix on save

### Data Model

Both backends use the same Django model layer, shown below. On PostgreSQL it maps to normalized tables with a `coupon_coupon_hashtags` junction table; on MongoDB, Djongo (`ENFORCE_SCHEMA = True`) maps the same models onto collections with reference fields and a junction collection. The two deployments therefore exercise the same logical schema on different storage engines — the variable under study.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#EFF6FF', 'edgeColor': '#2563EB', 'primaryBorderColor': '#2563EB', 'lineColor': '#2563EB', 'textColor': '#0F172A' }}}%%
erDiagram
    auth_user |o--o{ Coupon : owns
    auth_user |o--o{ Comment : writes
    Coupon ||--o{ Comment : receives
    Coupon }o--o{ Hashtag : "tagged with"
    Coupon {
        int id PK
        int user_id FK
        varchar name
        datetime expiring_date
        float discount_amt
        int score
        varchar code
        int comments_amt
    }
    Comment {
        int id PK
        int coupon_id FK
        int user_id FK
        text text
        datetime created_date
    }
    Hashtag {
        int id PK
        varchar name UK
    }
```

### Performance Benchmarking

Two Locust scenarios under `tests/` drive load against the system:

- [`locustfile.py`](tests/locustfile.py) — an `HttpUser` that repeatedly requests the hashtag search endpoint (`/search_coupons/`) on a running Django server, measuring end-to-end HTTP throughput and latency.
- [`locust_postgres_performance.py`](tests/locust_postgres_performance.py) — a scenario that opens a direct `psycopg2` connection per task and issues `SELECT * FROM coupon_coupon`, isolating database round-trip cost from the Django request stack.

The seed scripts under `scripts/` populate each backend with users and coupons, but the shipped defaults are not equal across the two — 100 users on PostgreSQL against 99 on MongoDB (ids 2–100, id 1 belonging to the superuser) — so volume parity has to be established deliberately. Measured results depend on host hardware and database tuning and are not reproduced here; [`docs/BENCHMARK.md`](docs/BENCHMARK.md) gives the protocol, the per-script seeding volumes, and a results template to record them.

## Tech Stack

| Category | Technologies |
| --- | --- |
| Language | Python 3 |
| Framework | Django 4.2.1 (PostgreSQL variant); Django 3.1.x via Djongo (MongoDB variant) |
| SQL database | PostgreSQL (via `psycopg2`) |
| NoSQL database | MongoDB Atlas (via Djongo) |
| Load testing | Locust |
| Diagrams | PlantUML |

## Project Structure

```text
coupon-management/
├── src/
│   ├── postgresql/lcss/               # Django project — PostgreSQL backend
│   │   ├── coupon/                    # App (models, views, forms, templates)
│   │   └── lcss/                      # Settings, URLs, WSGI/ASGI
│   └── mongodb/lcss/                  # Django project — MongoDB backend (Djongo)
│       ├── coupon/                    # App (identical logic)
│       └── lcss/                      # Settings (Djongo engine)
├── tests/
│   ├── locustfile.py                  # HTTP load test (hashtag search endpoint)
│   └── locust_postgres_performance.py # Direct PostgreSQL query load test
├── scripts/                           # Database seeding and cleanup utilities
├── assets/                            # PlantUML use-case diagram (source + PNG)
├── docs/
│   ├── social_preview.svg             # Repository header graphic (source)
│   ├── social_preview_light.png       # Header graphic — light theme
│   ├── social_preview_dark.png        # Header graphic — dark theme
│   ├── social_card.png                # Social sharing card
│   ├── render.sh                      # SVG-to-PNG rendering script
│   └── BENCHMARK.md                   # Benchmark protocol and results template
├── requirements.txt                   # Python dependencies — PostgreSQL variant and Locust
├── requirements-mongodb.txt           # Python dependencies — MongoDB/Djongo variant
├── .github/                           # CI workflows, funding, dependabot
├── CONTRIBUTING.md
├── CITATION.cff
├── SECURITY.md
├── LICENSE
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+ for the PostgreSQL variant (Locust 2.45 requires 3.10+); Python 3.9 or older for the MongoDB/Djongo variant, whose pinned Django 3.1.12 and PyMongo 3.11.4 support Python 3.6–3.9
- PostgreSQL 14+ (for the SQL variant)
- MongoDB Atlas, or a local MongoDB, for the NoSQL variant. The deliverable was run against Atlas as pinned; note the support envelope, since Djongo 1.3.7 pins `pymongo<=3.11.4`, whose documented server support ends at MongoDB 4.4, while current Atlas clusters run 6.0 and later

### Installation

```bash
# Clone the repository
git clone https://github.com/mtorun0x7cd/coupon-management.git
cd coupon-management

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# PostgreSQL backend (Django 4.2.1 + psycopg2 + Locust):
pip install -r requirements.txt

# MongoDB backend — Djongo pins an older Django/pymongo,
# so install it in a separate virtual environment on Python 3.9 or older:
pip install -r requirements-mongodb.txt
```

### Configuration

Set database credentials in the appropriate `settings.py`:

- **PostgreSQL**: `src/postgresql/lcss/lcss/settings.py`
- **MongoDB**: `src/mongodb/lcss/lcss/settings.py`

Provide a `DJANGO_SECRET_KEY` environment variable, or replace the placeholder in `settings.py`. The committed credentials are placeholders, not live secrets.

### Run (PostgreSQL variant)

```bash
cd src/postgresql/lcss
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Run (MongoDB variant)

```bash
cd src/mongodb/lcss
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Database Seeding

Seed scripts under `scripts/` populate test data for benchmarking:

```bash
# PostgreSQL seeding
python scripts/postgres_create_users.py
python scripts/postgres_create_coupons_for_users.py

# MongoDB seeding
python scripts/mongo_create_users.py
python scripts/mongo_create_coupons.py
python scripts/mongo_create_coupons_for_users.py
```

### Load Testing

```bash
# HTTP-level load test against the running Django server
locust -f tests/locustfile.py --host=http://localhost:8000

# Direct PostgreSQL query load test (bypasses Django)
locust -f tests/locust_postgres_performance.py
```

## Documentation

| Document | Description |
| :--- | :--- |
| [BENCHMARK.md](docs/BENCHMARK.md) | Reproducible PostgreSQL-vs-MongoDB benchmark protocol and results template |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Archive policy and the route for reporting a factual correction |

## References

[1] Django Software Foundation, "Django Documentation (v4.2)," 2023. [Online]. Available: <https://docs.djangoproject.com/en/4.2/>

[2] Locust Contributors, "Locust — A Modern Load Testing Framework." [Online]. Available: <https://locust.io/>

[3] The PostgreSQL Global Development Group, "PostgreSQL Documentation." [Online]. Available: <https://www.postgresql.org/docs/>

[4] MongoDB, Inc., "MongoDB Documentation." [Online]. Available: <https://www.mongodb.com/docs/>

[5] Doableware, "Djongo — Django and MongoDB Connector." [Online]. Available: <https://www.djongomapper.com/>

## Citation

Citation metadata is provided in [`CITATION.cff`](CITATION.cff); GitHub renders a *Cite this repository* action from it.

## Security

This is an archived academic project and is not actively maintained. It runs with Django's development settings — `DEBUG = True`, an empty `ALLOWED_HOSTS`, and a placeholder `SECRET_KEY` — and the database credentials in both `settings.py` files are placeholders, not live secrets. It has not undergone a security review and must not be deployed on an untrusted network or against real data. See [`SECURITY.md`](SECURITY.md) for details.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Contact

**Mert Torun, M.Sc.** — IT Security Architect · Systems Engineer  
mtorun0x7cd · Research & Development

His work spans the verification and validation of safety-critical systems, infrastructure hardening, and cryptographic integrity, grounded in an M.Sc. in Computer Science & Engineering from TH Köln. This repository is preserved as a record of a completed project rather than maintained as a living tool.

- **Email**: [info@mtorun0x7cd.com](mailto:info@mtorun0x7cd.com)
- **Website**: [mtorun0x7cd.com](https://mtorun0x7cd.com)
- **LinkedIn**: [linkedin.com/in/mtorun0x7cd](https://www.linkedin.com/in/mtorun0x7cd)
- **GitHub**: [github.com/mtorun0x7cd](https://github.com/mtorun0x7cd)
