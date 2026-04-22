# Permissions-Policy

## Purpose

The `Permissions-Policy` HTTP response header lets you enable or disable access to selected browser features and powerful APIs in the current document and in nested browsing contexts (iframes). It replaces the deprecated `Feature-Policy` header.

In this library, `PermissionsPolicy` is a fluent builder for producing a single `Permissions-Policy` header value, suitable for applying via `Secure`.

## Best practices

- Start restrictive: disable features you don’t need to reduce attack surface and protect privacy.
- Enable selectively: allow features only where required, and only for trusted origins.
- Validate in real browsers: support varies by feature and browser; test the behaviors you rely on.

## Configuration with `secure`

```python
from secure import PermissionsPolicy, Secure

secure_headers = Secure(
    permissions=PermissionsPolicy()
        .geolocation()
        .microphone()
        .camera()
)
```
`Preset.BALANCED` and `Preset.STRICT` include `geolocation=(), microphone=(), camera=()` by default; `Preset.BASIC` does not add `Permissions-Policy`.

## Allowlist syntax

`PermissionsPolicy` uses MDN-style allowlist syntax for each directive:

- **No tokens** → `()` (feature disabled)
- **`"*"`** → `*` (feature allowed everywhere; must be used alone)
- **`"self"` / `"src"`** → tokens for same-origin / iframe source origin
- **Origins** → pass a URL (e.g. `"https://a.example.com"`); it is emitted as a double-quoted origin in the header value

Examples:

```python
policy = (
    PermissionsPolicy()
    .geolocation("*")  # geolocation=*
    .camera("self", "https://a.example.com")  # camera=(self "https://a.example.com")
    .microphone()  # microphone=()
)
print(policy.header_value)
```

## Methods

Common methods you’ll use:

- **`geolocation(*allowlist)`**, **`camera(*allowlist)`**, **`microphone(*allowlist)`**, etc.: configure specific directives.
- **`add_directive(directive, *allowlist)`** (alias: **`directive(...)`**): set any directive by name (future-proof when browsers add new ones).
- **`value(raw)`** (alias: **`set(raw)`**): set a complete prebuilt header value (escape hatch; bypasses directive building).
- **`clear()`**: remove all configured directives and any raw override.

## Example usage

```python
from secure import PermissionsPolicy, Secure

permissions_policy = (
    PermissionsPolicy()
    .geolocation()  # disabled
    .camera("self", "https://a.example.com")
    .microphone("self")
)

print(permissions_policy.header_name)   # 'Permissions-Policy'
print(permissions_policy.header_value)  # 'geolocation=(), camera=(self "https://a.example.com"), microphone=(self)'

secure_headers = Secure(permissions=permissions_policy)
```

## Resources

- MDN Web Docs: Permissions-Policy (Reference) — https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy
- OWASP Secure Headers Project: Permissions-Policy — https://owasp.org/www-project-secure-headers/#permissions-policy

## Attribution

This library implements security recommendations from trusted sources:

- MDN Web Docs (licensed under CC-BY-SA 2.5)
- OWASP Secure Headers Project (licensed under CC-BY-SA 4.0)
