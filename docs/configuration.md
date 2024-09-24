# Configuration Guide

## Overview

This guide provides detailed information on how to configure `secure.py` beyond the default settings. You can customize security headers, override default behavior, and extend the functionality to meet your application’s unique security requirements.

---

## Default Headers

By default, `secure.py` applies a set of widely-used security headers that provide a strong baseline of protection. These include:

- **Strict-Transport-Security (HSTS)**: Ensures that browsers only connect to your site over HTTPS.
- **X-Frame-Options**: Protects against clickjacking attacks by controlling whether your site can be embedded in an iframe.
- **X-Content-Type-Options**: Prevents browsers from MIME-sniffing a response away from the declared `Content-Type`.
- **Content-Security-Policy (CSP)**: Mitigates Cross-Site Scripting (XSS) and data injection attacks by defining allowed content sources.

### Applying Default Headers

To quickly apply these default headers, use the following command:

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
secure_headers = Secure(
    xfo=Secure.XFrameOptions().sameorigin()
)
```

This protects against clickjacking while maintaining functionality for same-origin embedding, such as internal dashboards.

### Example: Customizing `Strict-Transport-Security`

To ensure that all subdomains of your site are accessed over HTTPS, and to add your domain to the HSTS preload list, you can configure `Strict-Transport-Security` like this:

```python
secure_headers = Secure(
    hsts=Secure.StrictTransportSecurity().max_age(63072000).include_subdomains().preload()
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

You can use one of the built-in presets as a starting point and then further customize specific headers to meet your security needs.

### Example: Customizing a Preset

```python
from secure import Secure, Preset

secure_headers = Secure.from_preset(Preset.BASIC)
secure_headers.hsts.max_age(63072000)  # Override the default max-age value
```

This approach allows you to quickly set up basic security headers while customizing certain parameters to fit your application’s security posture.

---

## Summary

`secure.py` offers flexibility in how you configure your security headers. Whether you’re using the default settings, customizing individual headers, or adding custom headers, the library allows you to secure your application effectively. For more advanced use cases, consider combining presets with custom configurations.

For more details on each supported header, refer to the [Security Headers Documentation](./headers).
