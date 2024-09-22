# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Placeholder for upcoming changes.

## [1.0.0] - YYYY-MM-DD

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
