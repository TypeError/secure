# Releasing `secure`

Publishing a GitHub Release triggers `.github/workflows/publish.yml`. Do not publish the release until CI has passed and the tag matches the version in `pyproject.toml` (for example, version `2.0.2` requires tag `v2.0.2`). Prereleases are intentionally blocked from production PyPI.

## One-time trusted publishing setup

1. In the GitHub repository, create an environment named exactly `pypi`.
2. Add a deployment branch/tag rule that permits only release tags (recommended pattern: `v*`). Add required reviewers where the repository plan supports them, and prevent administrators from bypassing the rule when appropriate.
3. Open <https://pypi.org/manage/project/secure/settings/publishing/> and add a GitHub Actions trusted publisher with these exact values:
   - PyPI project: `secure`
   - Owner: `TypeError`
   - Repository: `secure`
   - Workflow name: `publish.yml`
   - Environment name: `pypi`

Do not create or store a PyPI API token. The publish job obtains a short-lived OIDC credential and keeps the publishing action's default package attestations enabled.

## Local release checks

Run these commands from an activated development environment before publishing the GitHub Release:

```bash
python3 -m pytest -q
ruff check secure tests
ruff format --check secure tests
python3 -m build
python3 -m twine check dist/*
git diff --check
```

## Release process

1. Merge reviewed changes into `main`.
2. Update the package version in `pyproject.toml` and refresh `uv.lock`.
3. Run the local checks and confirm CI succeeds on `main`.
4. Create and publish a GitHub Release from the matching tag (for example, `v2.0.2`). Publishing the GitHub Release starts the PyPI workflow.
5. Approve the `pypi` environment deployment if required.
6. Let GitHub Actions build, validate, and publish the artifacts.
7. Verify the version appears at <https://pypi.org/project/secure/>.
8. Install the released version in a clean environment and verify its metadata and import.
9. For a security release, publish the corresponding advisory only after the patched package is available.

The workflow fails if the release tag does not exactly match the package version or if the tagged commit is not on `main`. PyPI rejects attempts to overwrite an existing release.
