# Benchmark protocol

Reproducible procedure and results template for the PostgreSQL-versus-MongoDB
comparison. No measurements are committed here by design: record them from a
controlled run rather than estimating.

## Objective

Compare relational (PostgreSQL) and document (MongoDB) storage under identical
application logic and workload. The Django model, view, form, and URL layers are
byte-identical across `src/postgresql/` and `src/mongodb/`; the substantive
difference between the variants is the database engine configured in
`lcss/settings.py`. Because that application layer is identical, the storage
engine remains the sole independent variable and the comparison stays valid.

## Scenarios

1. **End-to-end HTTP** — [`tests/locustfile.py`](../tests/locustfile.py): an
   `HttpUser` issuing `GET /search_coupons/?search_query=test` (wait 1–3 s).
   Exercises the full request path (routing, ORM/Djongo, template render). Run
   once per backend.
2. **Direct query** — [`tests/locust_postgres_performance.py`](../tests/locust_postgres_performance.py):
   a raw `psycopg2` `SELECT * FROM coupon_coupon` per task (wait 1–2 s),
   isolating database round-trip cost from the Django stack. As shipped this
   covers PostgreSQL only; a `pymongo` analogue is required for a symmetric
   MongoDB direct-query figure. The task subclasses `HttpUser` although it makes
   no HTTP call, so Locust still requires a `--host`.

## Metrics

Locust reports, per endpoint: request count, failure count, throughput
(requests/s), and response-time percentiles (min/mean/p50/p95/p99/max). Record
all; the headline comparison is **throughput and p95 latency at fixed
concurrency**.

## Controlled environment (record for every run)

- **Host** — CPU model/cores, RAM, disk class, OS and kernel.
- **Runtimes** — Python, Django, and `psycopg2`/`djongo`/`pymongo` versions.
- **PostgreSQL** — server version and any non-default `postgresql.conf`.
- **MongoDB** — server/Atlas version, tier, and region. Network RTT to Atlas
  dominates latency and **must** be reported: a local PostgreSQL against a
  remote Atlas cluster is not a like-for-like comparison. Co-locate both engines
  or state the asymmetry explicitly.
- **Dataset** — users and coupons actually seeded in each backend via `scripts/`.
  The shipped defaults are not equal across the two (see Procedure step 1), so
  record both volumes rather than assuming parity.
- **Server** — Django run mode (dev server vs. gunicorn + N workers), `DEBUG=False`.
- **Load** — Locust user count, spawn rate, and run duration.

## Procedure

1. Seed each backend and record what the scripts actually create. PostgreSQL:
   `postgres_create_users.py` (100 users), then
   `postgres_create_coupons_for_users.py` (1000 coupons spread over those users).
   MongoDB: `mongo_create_users.py` (99 users, ids 2–100, id 1 belonging to the
   superuser), then `mongo_create_coupons.py` (1000 coupons, all attributed to
   user id 1). Run `mongo_create_coupons_for_users.py` only alongside an
   equivalent PostgreSQL step: it inserts 5 coupons for every document in
   `auth_user` — 500 after the sequence above — and otherwise breaks volume
   parity. Its inline comment claims 10 per user; the loop is `range(5)`.
2. Start the target app with `DEBUG=False` behind a production-like server.
3. Run each scenario headless and capture CSV:

   ```sh
   mkdir -p results/
   locust -f tests/locustfile.py --host http://<server> \
          -u <users> -r <spawn-rate> -t <duration> \
          --headless --csv results/<backend>_http
   ```

4. Repeat for the direct-query scenario.
5. Run each cell at least three times; discard the first (warm-up) run and report
   the median with spread.

## Results (fill from a real run — do not estimate)

> Environment: `<fill>` · Dataset: `<N users / M coupons>` · Load: `<U users, r/s, t s>` · Date: `<fill>`

### End-to-end HTTP — `/search_coupons/`

| Backend | RPS (median) | p50 (ms) | p95 (ms) | p99 (ms) | failures (%) |
| --- | --- | --- | --- | --- | --- |
| PostgreSQL | — | — | — | — | — |
| MongoDB (Djongo) | — | — | — | — | — |

### Direct query — `SELECT * FROM coupon_coupon` (and `pymongo` equivalent)

| Backend | RPS (median) | p50 (ms) | p95 (ms) | p99 (ms) | failures (%) |
| --- | --- | --- | --- | --- | --- |
| PostgreSQL (`psycopg2`) | — | — | — | — | — |
| MongoDB (`pymongo`) | — | — | — | — | — |

The MongoDB (`pymongo`) direct-query figure is out of scope for this archived
deliverable — no symmetric scenario was implemented — so that row stays
intentionally blank.

## Caveats

- Benchmark the search endpoint, not `home`: the `home` view re-persists every
  coupon on each request, which measures a write storm rather than read
  performance.
- Credentials in the seed and load scripts are placeholders (`<db-password>` and
  `mongodb+srv://<username>:<password>@<cluster-host>/`) read as literals. No
  script consults the environment — only `settings.py` honours a variable, and
  only `DJANGO_SECRET_KEY` — so a run requires a local, uncommitted edit of the
  script constants. Do not commit that edit.
