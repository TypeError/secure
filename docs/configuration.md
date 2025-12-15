# Configuration Guide

## Overview

This guide provides detailed information on how to configure `secure` beyond the default settings. You can customize security headers, override default behavior, and extend the functionality to meet your application’s unique security requirements.

---

## Default Headers

`Secure.with_default_headers()` uses `Preset.BALANCED`, which configures a consistent, modern baseline. The defaults cover browser isolation, MIME safety, and legacy compatibility guards while keeping the header set lean:

- **Cross-Origin-Opener-Policy:** `same-origin` – isolates the browsing context to prevent exploitation of shared global objects.
- **Cross-Origin-Resource-Policy:** `same-origin` – prevents cross-origin resources from being retrieved unless explicitly permitted.
- **Content-Security-Policy:** `default-src 'self'; base-uri 'self'; font-src 'self' https: data:; form-action 'self'; frame-ancestors 'self'; img-src 'self' data:; object-src 'none'; script-src 'self'; script-src-attr 'none'; style-src 'self' https: 'unsafe-inline'; upgrade-insecure-requests` – a conservative, CSP-first profile with no inline scripts and forced HTTPS upgrades.
- **Strict-Transport-Security (HSTS):** `max-age=31536000; includeSubDomains` – enforces HTTPS for browsers for one year.
- **Permissions-Policy:** `geolocation=(), microphone=(), camera=()` – disables a few sensitive browser features by default.
- **Referrer-Policy:** `strict-origin-when-cross-origin` – balances privacy and analytics by trimming cross-origin referrer data.
- **Server:** empty string – hides the underlying server software.
- **X-Content-Type-Options:** `nosniff` – blocks MIME sniffing attacks.
- **X-Frame-Options:** `SAMEORIGIN` – prevents framing by other origins.

Balanced intentionally skips `Cache-Control` and the older compatibility headers (`X-Permitted-Cross-Domain-Policies`, `X-DNS-Prefetch-Control`, `Origin-Agent-Cluster`, `X-Download-Options`, `X-XSS-Protection`), but you can add them manually when your deployment still depends on them.

### Applying Default Headers

To quickly apply this configuration, use:

```python
secure_headers = Secure.with_default_headers()
```

This is the simplest way to secure your application without manually configuring each individual header. However, for applications with specific security requirements, you can customize headers as needed.

---

## Customizing Headers

Each security header can be customized to meet your application’s unique needs. Below are examples of how to modify some commonly used headers.

### Example: Customizing `X-Frame-Options` to Allow Same-Origin Embedding

If you want to allow your site to be embedded in an iframe, but only by pages from the same origin, use the following configuration:

```python
from secure import Secure, XFrameOptions

secure_headers = Secure(
    xfo=XFrameOptions().sameorigin()
)
```

This protects against clickjacking while maintaining functionality for same-origin embedding, such as internal dashboards.

### Example: Customizing `Strict-Transport-Security`

To ensure that all subdomains of your site are accessed over HTTPS, and to add your domain to the HSTS preload list, you can configure `Strict-Transport-Security` like this:

```python
from secure import Secure, StrictTransportSecurity

secure_headers = Secure(
    hsts=StrictTransportSecurity().max_age(63072000).include_subdomains().preload()
)
```

This configuration enforces HTTPS for 2 years (`max-age=63072000`), applies the rule to all subdomains, and preloads your site into browsers' HSTS lists.

---

## Extending Default Behavior

You can also extend the default behavior by adding custom headers. This is useful when your application requires additional non-standard security headers.

### Example: Adding a Custom Header

```python
from secure import CustomHeader

custom_header = CustomHeader("X-Custom-Header", "CustomValue")

secure_headers = Secure(custom=[custom_header])
```

In this example, a custom HTTP header `X-Custom-Header` is added to the response, allowing you to inject additional security policies or tracking information as required by your application.

---

## Combining Presets with Customization

You can use one of the built-in presets as a starting point and then further customize specific headers to meet your security needs. Every `Secure` instance exposes its configuration as a list of header builders via `headers_list`, so you can replace, reorder, or extend that list to adjust individual headers even after instantiation.

### Example: Customizing a Preset

```python
from secure import Preset, Secure, StrictTransportSecurity

secure_headers = Secure.from_preset(Preset.BASIC)

secure_headers.headers_list = [
    header
    for header in secure_headers.headers_list
    if header.header_name != "Strict-Transport-Security"
]
secure_headers.headers_list.append(
    StrictTransportSecurity()
    .max_age(63072000)
    .include_subdomains()
)
```

This replaces the preset’s `Strict-Transport-Security` builder with a custom one while keeping the remaining headers unchanged.

---

## Summary

`secure` offers flexibility in how you configure your security headers. Whether you’re using the default settings, customizing individual headers, or adding custom headers, the library allows you to secure your application effectively. For more advanced use cases, consider combining presets with custom configurations.

For more details on each supported header, refer to the [Security Headers Documentation](./headers).
