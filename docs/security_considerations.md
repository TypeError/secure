# Security Considerations

## Overview

Security headers are one part of a web application's security posture. They help browsers enforce transport, embedding, content loading, and privacy rules, but they do not replace application-layer controls such as output encoding, CSRF protection, authentication, or input validation.

This guide keeps the advice tied to what `secure` actually emits and where the tradeoffs are operational rather than theoretical.

## Importance of Security Headers

### **Strict-Transport-Security (HSTS)**

The `Strict-Transport-Security` header ensures that browsers only connect to your site over HTTPS, preventing MITM attacks by forcing a secure connection. It tells the browser to remember to always access the site via HTTPS, even if the user tries to access it over HTTP.

- [MDN Docs - Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)
- **Best Practice**: Use a long `max-age` and include subdomains only when every subdomain is HTTPS-ready.
- **Pitfall**: Be cautious when setting the `preload` directive, as it’s difficult to remove once added to the HSTS preload list.

---

### **Content-Security-Policy (CSP)**

The `Content-Security-Policy` header limits which sources the browser will trust for scripts, styles, images, frames, and other resource types. A well-tuned CSP reduces the impact of XSS and unsafe third-party content, but the policy still has to match how your frontend actually loads code and assets.

- [MDN Docs - Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy)
- **Best Practice**: Start with a restrictive baseline and expand only where the application requires it. Use nonces or hashes for inline scripts when possible.
- **Pitfall**: Overly permissive CSP rules (e.g., using `unsafe-inline`, `unsafe-eval`, or `*`) can leave your application vulnerable to XSS attacks.

---

### **X-Frame-Options**

The `X-Frame-Options` header prevents clickjacking by controlling whether a page can be framed. In modern deployments, treat it as a compatibility header alongside CSP `frame-ancestors`.

- [MDN Docs - X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)
- **Best Practice**: Set to `DENY` to completely block framing, or `SAMEORIGIN` if you only want to allow framing from your own domain.
- **Pitfall**: Be careful when setting `SAMEORIGIN` if you allow content embedding. Incorrect settings can break legitimate functionality, such as embedded dashboards or widgets.

---

### **X-Content-Type-Options**

The `X-Content-Type-Options` header prevents MIME-sniffing by telling browsers to respect the declared `Content-Type`. In practice, it is most relevant for blocking incorrectly typed script and stylesheet responses.

- [MDN Docs - X-Content-Type-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options)
- **Best Practice**: Always set this header to `nosniff`.
- **Pitfall**: This header can surface incorrect `Content-Type` handling in your app or asset pipeline.

---

### **Referrer-Policy**

The `Referrer-Policy` header controls how much referrer information is included with requests. By limiting referrer data, you can prevent sensitive URL data from being exposed to third-party sites.

- [MDN Docs - Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy)
- **Best Practice**: Use `strict-origin-when-cross-origin` to protect sensitive referrer information while preserving analytics functionality.
- **Pitfall**: Using `unsafe-url` can expose full URLs, which may leak sensitive data.

---

### **Permissions-Policy**

The `Permissions-Policy` header allows you to disable or scope browser features such as geolocation, camera access, and microphone access.

- [MDN Docs - Permissions-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy)
- **Best Practice**: Disable unnecessary features (e.g., `camera`, `microphone`, `geolocation`) to reduce attack surface.
- **Pitfall**: Incorrectly blocking required features may break functionality like video conferencing or map-based services.

---

### **Cross-Origin-Embedder-Policy (COEP)**

The `Cross-Origin-Embedder-Policy` header controls whether a document can load cross-origin resources that do not explicitly opt in via CORP or CORS.

- [MDN Docs - Cross-Origin-Embedder-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy)
- **Best Practice**: Use COEP when you need cross-origin isolation and can verify that your own and third-party resources are compatible.
- **Pitfall**: Misconfiguration often breaks legitimate cross-origin assets before it improves anything.

---

### **Cross-Origin-Opener-Policy (COOP)**

The `Cross-Origin-Opener-Policy` header isolates a document's browsing context group, which helps reduce XS-Leaks and is typically paired with COEP when you need cross-origin isolation.

- [MDN Docs - Cross-Origin-Opener-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy)
- **Best Practice**: Set this to `same-origin` to protect against XS-Leaks and ensure that only same-origin documents can access the browsing context.
- **Pitfall**: Popups, payment flows, or OAuth-style integrations may need a less strict value than `same-origin`.

---

### **Cache-Control**

The `Cache-Control` header controls how responses are cached. For security-sensitive responses, it helps prevent browsers and intermediaries from storing content that should not persist.

- [MDN Docs - Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)
- **Best Practice**: Use `no-store` for sensitive pages like login or payment forms to ensure that they are not cached.
- **Pitfall**: Improper caching of sensitive data can lead to exposure of private information.

---

### **Server**

The `Server` header can disclose software details, but changing or clearing it should be treated as passive information reduction, not as a primary defense.

- [MDN Docs - Server](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server)
- **Best Practice**: Set a generic or empty value when your stack allows it, and disable framework or proxy defaults that would re-add a value upstream.
- **Pitfall**: Do not assume hiding `Server` materially hardens a vulnerable application.

---

### **Custom Headers**

`CustomHeader` is an escape hatch for application-specific response headers. Use it when you need to emit a header that does not have a dedicated builder, but keep the semantics and deployment expectations documented elsewhere in your application.

---

## Common Pitfalls

- **Improper CSP configurations**: Using `unsafe-inline`, `unsafe-eval`, or broad source allowlists weakens CSP quickly.
- **Weak HSTS rollout discipline**: Sending HSTS before all routes and subdomains are HTTPS-ready can break access just as easily as it improves transport security.

## OWASP Guidelines

For further recommendations on security headers, refer to the [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/).

---

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
