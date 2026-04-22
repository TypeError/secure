# Content-Security-Policy (CSP)

## Purpose

The `Content-Security-Policy` (CSP) response header helps mitigate cross-site scripting (XSS), data injection, and related attacks by restricting where content can be loaded from (scripts, styles, images, fonts, connections, frames, etc.).

CSP is expressed as a list of **directives** separated by semicolons:

```http
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'
```

## Library defaults

If you create a `ContentSecurityPolicy()` and do not configure any directives, it returns the library default:

```text
default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'self'; form-action 'self'
```

This matches `HeaderDefaultValue.CONTENT_SECURITY_POLICY`.
The built-in presets use explicit CSP builders rather than this bare builder default; `Preset.BASIC` and `Preset.BALANCED` add `font-src`, `img-src`, `script-src-attr`, `style-src`, and `upgrade-insecure-requests`.

## Best-practice baseline

A common “safe baseline” CSP includes:

- `default-src 'self'`
- `object-src 'none'`
- `base-uri 'self'`
- `frame-ancestors 'self'` (or `'none'` if you never want to be framed)
- `form-action 'self'`
- optionally `upgrade-insecure-requests`

> CSP is powerful but can break applications if rolled out too aggressively. Start with a report-only policy (see below), review violations, then enforce.

---

## Configuration with `Secure`

### Minimal example

```py
from secure import ContentSecurityPolicy, Secure

csp = (
    ContentSecurityPolicy()
    .default_src(ContentSecurityPolicy.keyword("self"))
    .object_src(ContentSecurityPolicy.keyword("none"))
    .base_uri(ContentSecurityPolicy.keyword("self"))
)

secure_headers = Secure(csp=csp)
```

Then apply headers in your framework integration:

```py
# Flask example
from flask import Flask, Response

app = Flask(__name__)
secure_headers = Secure(csp=csp)

@app.after_request
def add_security_headers(response: Response) -> Response:
    secure_headers.set_headers(response)
    return response
```

### Report-only mode

To observe violations without enforcing (recommended for rollout):

```py
csp_report_only = (
    ContentSecurityPolicy()
    .report_only()
    .default_src(ContentSecurityPolicy.keyword("self"))
    .script_src(ContentSecurityPolicy.keyword("self"))
)

secure_headers = Secure(csp=csp_report_only)
```

Use `.enforce()` to switch back to the enforcing header name.

---

## Fluent directive methods

Common methods include:

- Fetch directives: `default_src`, `script_src`, `style_src`, `img_src`, `font_src`, `connect_src`, `media_src`, `frame_src`, `worker_src`, `manifest_src`, `fenced_frame_src`, `object_src`
- Navigation / embedding: `base_uri`, `form_action`, `frame_ancestors`
- Policy controls: `sandbox`, `upgrade_insecure_requests`
- Reporting: `report_to`, `report_uri` _(deprecated in MDN)_

### Deterministic output and deduplication

- Each directive name appears at most once.
- Tokens passed to a directive are deduplicated (first-seen order preserved).
- Serialization is deterministic and uses `"; "` between directives.

---

## Helper utilities

### Keywords

Use `keyword()` to safely produce quoted CSP keywords like `'self'` and `'none'`:

```py
ContentSecurityPolicy.keyword("self")  # "'self'"
ContentSecurityPolicy.keyword("none")  # "'none'"
```

### Nonces

Use `nonce()` to produce a CSP nonce source expression:

```py
nonce_value = "abc123=="  # base64 / url-safe base64
ContentSecurityPolicy.nonce(nonce_value)  # "'nonce-abc123=='"
```

---

## Escape hatches

### Set an exact policy string

If you need full control (or want to carry over an existing CSP string), use `.value(...)`:

```py
csp = ContentSecurityPolicy().value(
    "default-src 'self'; script-src 'self' https://cdn.example; object-src 'none'"
)
```

`.set(...)` is an alias for `.value(...)`.

### Clear configuration

```py
csp = ContentSecurityPolicy().default_src(ContentSecurityPolicy.keyword("self"))
csp.clear()  # resets back to library default behavior
```

### Custom directives

If you need a directive not covered by a helper method:

```py
csp = (
    ContentSecurityPolicy()
    .custom_directive("default-src", ContentSecurityPolicy.keyword("self"))
    .custom_directive("script-src", ContentSecurityPolicy.keyword("self"))
)

# `.custom(...)` is an alias
```

---

## Nonce + `strict-dynamic` example (recommended pattern)

When you use nonces, the nonce must be generated **per response** and also placed in your HTML script tag(s).
A common pattern is to generate the nonce in request context, then build CSP using it.

### Framework-agnostic CSP construction

```py
import secrets
from secure import ContentSecurityPolicy

nonce = secrets.token_urlsafe(16)

csp = (
    ContentSecurityPolicy()
    .default_src(ContentSecurityPolicy.keyword("self"))
    .script_src(
        ContentSecurityPolicy.nonce(nonce),
        ContentSecurityPolicy.keyword("strict-dynamic"),
    )
    .object_src(ContentSecurityPolicy.keyword("none"))
)

print(csp.header_value)
# default-src 'self'; script-src 'nonce-...' 'strict-dynamic'; object-src 'none'
```

### Flask pattern (nonce shared via `g`)

```py
import secrets
from flask import Flask, Response, g

from secure import ContentSecurityPolicy, Secure

app = Flask(__name__)

@app.before_request
def set_nonce() -> None:
    g.csp_nonce = secrets.token_urlsafe(16)

@app.after_request
def add_security_headers(response: Response) -> Response:
    csp = (
        ContentSecurityPolicy()
        .default_src(ContentSecurityPolicy.keyword("self"))
        .script_src(
            ContentSecurityPolicy.nonce(g.csp_nonce),
            ContentSecurityPolicy.keyword("strict-dynamic"),
        )
        .style_src(ContentSecurityPolicy.keyword("self"))
        .object_src(ContentSecurityPolicy.keyword("none"))
    )
    Secure(csp=csp).set_headers(response)
    return response
```

In your HTML rendering, use the same nonce:

```html
<script nonce="{{ g.csp_nonce }}">
  console.log("Allowed because nonce matches CSP");
</script>
```

---

## Reporting notes (MDN)

- `report-to` is the modern mechanism.
- `report-uri` is deprecated in MDN; some browsers that support `report-to` may ignore `report-uri`.
- If you need broad compatibility during migration, you may specify both.

---

## References

- MDN: Content-Security-Policy
  - [https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy)

- MDN: CSP guide
  - [https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP)

- OWASP Secure Headers Project
  - [https://owasp.org/www-project-secure-headers/#content-security-policy](https://owasp.org/www-project-secure-headers/#content-security-policy)

## Attribution

This library implements security recommendations and reference material from:

- MDN Web Docs (licensed under CC-BY-SA 2.5)
- OWASP Secure Headers Project (licensed under CC-BY-SA 4.0)
