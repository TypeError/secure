# Secure Headers Documentation

Welcome to the documentation for **Secure Headers**, a flexible Python library for managing HTTP security headers. This guide will help you get started with configuring headers, integrating with various web frameworks, and understanding how each security header works.

---

## 📖 Table of Contents

- [Getting Started](#getting-started)
- [Supported Frameworks](#supported-frameworks)
- [Security Headers](#security-headers)
- [Additional Resources](#additional-resources)
- [Contributing](#contributing)

---

## 🚀 Getting Started

To quickly get started using Secure Headers, check out the basic configuration guide in the main README:

- [Quick Start Guide](../README.md#basic-usage)

For installation instructions, see the [Installation section](./installation.md).

For usage examples, see the [Usage Guide](./usage.md).

For detailed configuration options, see the [Configuration Guide](./configuration.md).

---

## 🔧 Supported Frameworks

Secure Headers is compatible with many popular Python web frameworks. Below are the integration guides for each supported framework, consolidated in the [Frameworks Integration Guide](./frameworks.md):

| Framework                                   | Documentation                                   |
| ------------------------------------------- | ----------------------------------------------- |
| [aiohttp](https://docs.aiohttp.org)         | [Integration Guide](./frameworks.md#aiohttp)    |
| [Bottle](https://bottlepy.org)              | [Integration Guide](./frameworks.md#bottle)     |
| [Django](https://www.djangoproject.com)     | [Integration Guide](./frameworks.md#django)     |
| [Falcon](https://falconframework.org)       | [Integration Guide](./frameworks.md#falcon)     |
| [FastAPI](https://fastapi.tiangolo.com)     | [Integration Guide](./frameworks.md#fastapi)    |
| [Flask](https://flask.palletsprojects.com/) | [Integration Guide](./frameworks.md#flask)      |
| [Pyramid](https://trypyramid.com)           | [Integration Guide](./frameworks.md#pyramid)    |
| [Quart](https://pgjones.gitlab.io/quart/)   | [Integration Guide](./frameworks.md#quart)      |
| [Sanic](https://sanicframework.org)         | [Integration Guide](./frameworks.md#sanic)      |
| [Starlette](https://www.starlette.io/)      | [Integration Guide](./frameworks.md#starlette)  |
| [Tornado](https://www.tornadoweb.org/)      | [Integration Guide](./frameworks.md#tornado)    |
| [TurboGears](https://turbogears.org/)       | [Integration Guide](./frameworks.md#turbogears) |
| [Web2py](http://www.web2py.com/)            | [Integration Guide](./frameworks.md#web2py)     |
| [Morepath](https://morepath.readthedocs.io) | [Integration Guide](./frameworks.md#morepath)   |

If your framework is not listed here, Secure Headers can likely still be integrated. Refer to the [Custom Framework Integration Guide](./frameworks.md#custom-frameworks) for general integration tips.

---

## 🛡️ Security Headers

Secure Headers supports many critical HTTP security headers. Below is a list of headers you can configure, along with detailed documentation for each:

- [Cache-Control](./headers/cache_control.md)  
  Configure caching behavior to protect sensitive content.

- [Content-Security-Policy](./headers/content_security_policy.md)  
  Prevent XSS and data injection attacks by controlling allowed content sources.

- [Cross-Origin-Embedder-Policy](./headers/cross_origin_embedder_policy.md)  
  Enhance cross-origin security by specifying cross-origin resource policies.

- [Cross-Origin-Opener-Policy](./headers/cross_origin_opener_policy.md)  
  Prevent attackers from accessing your global objects via cross-origin documents.

- [Custom Headers](./headers/custom_header.md)  
  Define and manage custom HTTP headers for advanced configurations.

- [Permissions-Policy](./headers/permissions_policy.md)  
  Control access to browser features such as geolocation, camera, and microphone.

- [Referrer-Policy](./headers/referrer_policy.md)  
  Manage how much referrer information is shared during navigation.

- [Server](./headers/server.md)  
  Hide or customize the `Server` header to prevent exposing your server details.

- [Strict-Transport-Security (HSTS)](./headers/strict_transport_security.md)  
  Ensure that communication is only over HTTPS by enforcing strict transport security.

- [X-Content-Type-Options](./headers/x_content_type_options.md)  
  Prevent MIME-sniffing attacks by ensuring the browser follows the declared `Content-Type`.

- [X-Frame-Options](./headers/x_frame_options.md)  
  Protect against clickjacking by controlling whether your content can be framed.

---

## 📚 Additional Resources

- [MDN Web Docs - HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)  
  Explore more about HTTP headers and their use cases.

- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)  
  Learn about security best practices for HTTP headers from OWASP.

- [Hardenize - HTTP Security Headers](https://www.hardenize.com/blog/https-security-headers)  
  A guide on the importance of HTTP security headers and how to use them effectively.

- [Mozilla Observatory](https://observatory.mozilla.org/)  
  A security tool to check the implementation of security headers on your site.

- [Security Headers by Scott Helme](https://securityheaders.com/)  
  A free tool to test your site for missing security headers.

- [HSTS Preload List](https://hstspreload.org/)  
  Learn about adding your domain to the HTTP Strict Transport Security (HSTS) preload list.

- [CSP Evaluator by Google](https://csp-evaluator.withgoogle.com/)  
  A tool for analyzing Content Security Policies to ensure strong security practices.

---

## 💬 Contributing

We welcome contributions! If you'd like to contribute or have any feedback, feel free to:

- **Open an Issue**: Report bugs or request features.
- **Submit a Pull Request**: Contribute code or documentation improvements.
- **Contact Us**: Reach out via [GitHub](https://github.com/TypeError/secure).
