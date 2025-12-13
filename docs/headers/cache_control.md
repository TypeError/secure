# Cache-Control

## Purpose

`Cache-Control` is a comma-separated list of **directives** that control caching behavior for both **requests** and **responses**. Used correctly, it helps prevent sensitive data from being cached and improves performance for cacheable assets. :contentReference[oaicite:1]{index=1}

## Default behavior

If you create `CacheControl()` and do not add directives, it returns the library default value:

- **Default header value:** `no-store, max-age=0` :contentReference[oaicite:2]{index=2}

This is a secure baseline intended to prevent storage of sensitive responses.

## Using with `Secure`

```python
from secure.secure import Secure
from secure.headers.cache_control import CacheControl

secure = Secure(
    cache=CacheControl().no_store().max_age(0)
)
```

If you don’t configure any directives, the default value is emitted.

## Common recipes

### 1) Prevent storing (recommended for sensitive responses)

```python
from secure.headers.cache_control import CacheControl

cc = CacheControl()  # default: no-store, max-age=0
print(cc.header_name)   # Cache-Control
print(cc.header_value)  # no-store, max-age=0
```

### 2) Always revalidate (useful for dynamic HTML)

```python
cc = CacheControl().no_cache()
print(cc.header_value)  # no-cache
```

> Note: `no-cache` does **not** mean “do not store.” It means “store, but revalidate before reuse.”

### 3) Cache-busted static assets (long-lived)

If your assets are fingerprinted (e.g., `/app.4f3c1.js`), you can cache them aggressively:

```python
cc = CacheControl().public().max_age(31536000).immutable()
print(cc.header_value)  # public, max-age=31536000, immutable
```

### 4) Shared caches (CDNs/proxies) vs browser caches

```python
cc = CacheControl().s_maxage(604800).max_age(60)
print(cc.header_value)  # s-maxage=604800, max-age=60
```

`s-maxage` applies to shared caches and overrides `max-age` for them.

### 5) Stale content during revalidation / on error

```python
cc = (
    CacheControl()
    .max_age(604800)
    .stale_while_revalidate(86400)
    .stale_if_error(86400)
)
print(cc.header_value)  # max-age=604800, stale-while-revalidate=86400, stale-if-error=86400
```

## Builder API

### Boolean directives (no value)

- `.no_store()`, `.no_cache()`, `.no_transform()`
- `.public()`, `.private()`
- `.must_revalidate()`, `.proxy_revalidate()`
- `.immutable()`
- `.must_understand()` (recommended to pair with `.no_store()` for safe fallback)

### Parameterized directives (integer seconds)

- `.max_age(seconds)`
- `.s_maxage(seconds)`
- `.min_fresh(seconds)` (request)
- `.stale_while_revalidate(seconds)`
- `.stale_if_error(seconds)`

### Request directives

- `.only_if_cached()`
- `.max_stale(seconds=None)` (if omitted, accepts staleness of any age)

## Escape hatches

### `.value("...")`

Set an explicit header value (replaces all configured directives):

```python
cc = CacheControl().value("no-store, max-age=0")
print(cc.header_value)  # no-store, max-age=0
```

### `.custom("token")`

Add a **non-standard / non-MDN** directive token (for niche proxies/CDNs):

```python
cc = CacheControl().custom("x-cache-mode=aggressive")
print(cc.header_value)  # x-cache-mode=aggressive
```

### `.clear()`

Reset to the default (no directives configured; default value will be returned).

## Deterministic output & overwrites

- Directives are rendered as a **stable**, comma-separated list.
- Repeating a parameterized directive overwrites the previous value (e.g., calling `.max_age(60)` then `.max_age(0)` results in `max-age=0`).
- The builder rejects obvious header-splitting primitives (CR/LF) in `.value(...)` and `.custom(...)`.

## Attribution

This library implements security recommendations and behavior described by:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#cache-control) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
