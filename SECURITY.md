# Security Policy

## Status

This repository is an archived academic project (TH Köln, Large and Cloud-based
Software Systems, Summer 2023), retained for reference and portfolio purposes.
It is **not under active development** and receives no functional or security
updates.

## Not for production use

The application runs with Django's development configuration and was written as a
student exercise for comparative database benchmarking, not as a hardened
deployment. Both `settings.py` files ship with `DEBUG = True`, an empty
`ALLOWED_HOSTS`, and a placeholder `SECRET_KEY` (`<your-secret-key>`); the
database credentials are likewise placeholders (`<db-password>` and
`mongodb+srv://<username>:<password>@<cluster-host>/`), not live secrets. It must
not be deployed on an untrusted network or operated against real data.

## Known Limitations

The source carries the posture of a development-grade Django project. These notes
are recorded for transparency, not as a maintenance backlog:

- **Development settings.** `DEBUG = True` exposes stack traces and configuration
  to any client on error, `ALLOWED_HOSTS` is empty, and `SECRET_KEY` falls back
  to a committed placeholder when `DJANGO_SECRET_KEY` is unset. None of these are
  suitable outside local development.
- **Unauthenticated views.** The site root (`home`) and the hashtag listing and
  search views (`coupon_by_hashtag`, `search_coupons`) are reachable without a
  session, as are `signup` and `loginUser`; every other view is gated with
  Django's `@login_required`. `home` is additionally a write path — it re-saves
  every `Coupon` row on each request, so an unauthenticated client amplifies a
  page view into a full-table write.
- **Broken password-change view.** `changepassword` constructs
  `PasswordChangeForm(request.user.request.POST)`; `User` has no `request`
  attribute, so both the GET and the POST branch raise `AttributeError` before
  anything is rendered. The screen is linked from the profile page and has never
  worked in this code.
- **Unhandled search input.** `search_coupons` reads `search_query` outside the
  branch that binds it, so a query longer than the form's 100-character limit
  raises `NameError` and returns HTTP 500 to an unauthenticated client.
- **Third-party front-end assets.** The templates load jQuery 2.1.3 from
  `ajax.googleapis.com`, Materialize CSS from `cdnjs.cloudflare.com`, and
  Material Icons from `fonts.googleapis.com` at render time, none of them with a
  subresource-integrity attribute. Every page load therefore executes
  third-party script and reaches third-party hosts, and the UI is not
  reproducible offline.
- **No transport security or rate limiting.** The project provides no TLS,
  throttling, or abuse protection; these are left to a deployment environment
  that is absent here.
- **Benchmark seed data.** The seed scripts under `scripts/` create fixed test
  accounts for load testing only and must never be run against a real database.
  Their credential handling differs by backend: the PostgreSQL seed
  (`postgres_create_users.py`) assigns every account the same publicly known
  PBKDF2 hash, whereas the MongoDB seed (`mongo_create_users.py`) writes a
  random plaintext string per account. Neither is a live secret.

The application does inherit Django's built-in protections — the ORM
parameterizes queries, CSRF middleware is enabled, and passwords are stored with
Django's PBKDF2 hasher — but these do not substitute for the hardening a
production deployment requires.

## Reporting

To report a substantive issue worth recording, contact <info@mtorun0x7cd.com>.
Given the archived status of the project, a fix or response is not guaranteed.
