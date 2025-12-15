# Contributing

Thanks for helping make `secure` better. The following guidance keeps contributions aligned with the project’s release-quality standards.

## Development environment

1. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install the package in editable mode so local changes are picked up automatically:
   ```bash
   pip install -e .
   ```
3. Install the tooling used by the project:
   ```bash
   pip install ruff
   ```
   _Optional:_ `uv` is the package manager used by the project for releases; you can use `uv add ...` to manage dependencies, but it is not required for local development.

## Running tests, linting, and formatting

- **Run unit tests:** `python -m unittest tests/*/*.py`
- **Run the linter:** `ruff check`
- **Apply formatting / fix issues:** `ruff format`

Run these commands before opening a pull request. If you rely on a different Python version, keep it within the supported range (Python 3.10+).

## Adding a header document

1. Add a new guide under `docs/headers/` named after the header (for example, `docs/headers/example_header.md`).
2. Mirror the structure of the existing header docs:
   - Start with a **Purpose** section that explains the header’s intent.
   - Describe the **Default behavior** and mention how the builder models that default.
   - Show a **Using with `Secure`** example and describe the builder API with method names.
   - Include **Resources** / **Attribution** and any security caveats.
3. Link the new document from `docs/README.md` (under the Security Headers list) so readers can discover it easily.
4. Ensure code snippets use the public API (`from secure import ...`), reference the appropriate response types, and avoid framework-specific terminology unless a callout is necessary.

## Adding a framework example

1. Update `docs/frameworks.md`:
   - Add the framework to the table of contents.
   - Include a short intro describing the framework’s model (WSGI vs ASGI, sync vs async).
   - Provide at least one working example showing how to wire `Secure` (middleware, hooks, or response-level helpers).
   - Mention the correct response type (`Response`, `JSONResponse`, etc.) or highlight that you are working with the framework’s default response object.
2. If the framework needs extra instructions (e.g., disabling Uvicorn’s `Server` header), document them in the same section.
3. Keep the tone focused on security headers rather than broader framework guidance.

## Commit conventions

- Keep commit messages short (<72 characters) and in the imperative (e.g., `docs: clarify defaults`).
- Prefix doc-only changes with `docs:` so reviewers immediately know the scope.
- Reference any related issue or PR in the description when applicable.
- Run linting/tests before committing to minimize follow-up work.

## Pull request checklist

- [ ] I have run `python -m unittest tests/*/*.py` locally (or a representative suite) and addressed any failures.
- [ ] I have run `ruff check` and `ruff format` (when formatting attr).
- [ ] Documentation updates describe the new behavior (new header docs, framework guidance, etc.).
- [ ] If applicable, I have updated the release notes/CHANGELOG entry for new user-visible behavior.
- [ ] My changes follow the project’s security and contribution guidelines (this document).
