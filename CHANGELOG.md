# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Placeholder for upcoming changes.

## [2.0.1] - 2026-04-21

This is the first stable v2 release. Version `2.0.0` was burned and should be skipped when tagging or publishing.

v2 focuses on a cleaner public API, a redesigned preset model, first-class ASGI/WSGI middleware, and stricter, safer header handling.

### Breaking Changes

- `Secure.headers` is now strict and read-only
  - v1: `headers` was a cached `dict[str, str]` and silently collapsed duplicate names
  - v2: duplicate header names (case-insensitive) raise `ValueError`
  - use `header_items()` for multi-valued output or `deduplicate_headers()` to resolve duplicates

- Default headers have changed
  - `Secure.with_default_headers()` now maps to `Preset.BALANCED`
  - v1 default included `Cache-Control: no-store`; v2 does not
  - applications relying on v1 defaults should explicitly configure required headers

- Presets redesigned
  - new `Preset.BALANCED` (recommended default)
  - `Preset.BASIC` updated for Helmet.js parity and no longer matches v1 BASIC
  - `Preset.STRICT` no longer enables HSTS preload by default
  - cache behavior and header composition differ across presets compared to v1

- FastAPI / ASGI integration model changed in practice
  - v1 relied on per-response mutation (`set_headers` / `set_headers_async`)
  - v2 introduces middleware-based integration as the recommended approach

### Added

- Middleware
  - `SecureASGIMiddleware`
  - `SecureWSGIMiddleware`
  - `secure.middleware` module

- Header pipeline helpers
  - `allowlist_headers(...)`
  - `deduplicate_headers(...)`
  - `validate_and_normalize_headers(...)`
  - `header_items()` for ordered `(name, value)` output

- New header builders and constants
  - `CrossOriginResourcePolicy`
  - `XDnsPrefetchControl`
  - `XPermittedCrossDomainPolicies`
  - `MULTI_OK`, `COMMA_JOIN_OK`, `DEFAULT_ALLOWED_HEADERS`
  - policy enums: `OnInvalidPolicy`, `OnUnexpectedPolicy`, `DeduplicateAction`

### Changed

- `Secure.with_default_headers()` now returns the balanced preset
- Header handling is stricter and fails fast on invalid or duplicate configurations
- Header normalization and validation are first-class operations
- Response integration is more robust across sync and async frameworks
- `headers_list` mutations are now reflected correctly (no stale cached state)
- Documentation updated to emphasize middleware usage and preset selection

### Migration Notes

- Do not assume v1 defaults
  - compare emitted headers and explicitly configure any required behavior

- Audit any usage of `Secure.headers`
  - treat as read-only in v2
  - use `header_items()` or `deduplicate_headers()` when duplicates are possible

- Move to middleware for ASGI/WSGI apps
  - replace per-response `set_headers_async()` calls with `SecureASGIMiddleware` or `SecureWSGIMiddleware`

- Explicitly configure behavior that changed
  - add `Cache-Control` if you relied on v1 defaults
  - add HSTS preload manually if required

### Notes

- Neither v1 nor v2 exposes `secure.__version__`; use package metadata for version checks

## [1.0.1] - 2024-10-18

### Fixed

- Improved performance of `Secure.set_headers` by reducing redundant type checks. ([#26](https://github.com/TypeError/secure/issues/26))

## [1.0.0] - 2024-09-27

### Breaking Changes

- Full redesign of the `secure.py` library with modern Python (3.10+) support.
- Major API overhaul for improved usability and Pythonic design.

### Added

- Enhanced support for FastAPI and asynchronous frameworks.
- Added type hints and better type annotations for a smoother developer experience.
- Refined default security headers for improved protection across web frameworks.
- Support for modern Python features such as the union operator (`|`) and `cached_property`.

## [0.3.0] - 2021-04-27

### Breaking Changes

- Full redesign of Secure API.
- Removal of cookie support.

### Added

- Added type hints for better developer experience.
- Added support for FastAPI.

### Changed

- Replaced Feature-Policy with Permissions-Policy (#10).

## [0.2.1] - 2018-12-24

### Added

- Added support for Masonite framework.
- Added docstrings for `SecureHeaders` and `SecureCookie`.

### Changed

- Upper-cased SameSite enum to `SameSite.LAX` / `SameSite.STRICT`.
- Modified hug implementation for SecureHeaders and SecureCookie.
- Renamed `Feature.Values.All` to `Feature.Values.All_` to avoid conflict with the built-in `all`.

### Fixed

- Removed trailing semicolon from Feature Policy.

## [0.2.0] - 2018-12-16

### Added

- Added policy builder `SecurePolicies` in `policies.py`.
- Added `Expires` header for legacy browser support.
- Added `max-age` directive to `Cache-Control` header.

### Changed

- Renamed `XXS` argument to `XXP`.
- Modified `set-cookie` to use Flask's native method.
