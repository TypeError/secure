# Documentation

`secure` is a small, focused library for adding modern security headers to Python web applications. The public API centers on `Secure`, with typed builder classes for individual headers when you need to customize a policy.

## Start here

- [README quick start](../README.md#quick-start)
- [Installation](./installation.md)
- [Usage](./usage.md)
- [Configuration](./configuration.md)

## Framework integration

See [Framework Integration](./frameworks.md) for WSGI and ASGI examples. The guide keeps the same `Secure` configuration across frameworks and only changes how you attach it.

## Header builders

- [Cache-Control](./headers/cache_control.md)
- [Content-Security-Policy](./headers/content_security_policy.md)
- [Cross-Origin-Embedder-Policy](./headers/cross_origin_embedder_policy.md)
- [Cross-Origin-Opener-Policy](./headers/cross_origin_opener_policy.md)
- [Cross-Origin-Resource-Policy](./headers/cross_origin_resource_policy.md)
- [Custom Header](./headers/custom_header.md)
- [Permissions-Policy](./headers/permissions_policy.md)
- [Referrer-Policy](./headers/referrer_policy.md)
- [Server](./headers/server.md)
- [Strict-Transport-Security](./headers/strict_transport_security.md)
- [X-Content-Type-Options](./headers/x_content_type_options.md)
- [X-DNS-Prefetch-Control](./headers/dns_prefetch_control.md)
- [X-Frame-Options](./headers/x_frame_options.md)
- [X-Permitted-Cross-Domain-Policies](./headers/x-permitted-cross-domain-policies.md)

## Migration notes

See [Migration Notes](./migration.md) for the v2-facing changes around presets, async response support, and package-level imports.
