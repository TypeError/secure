# Content-Security-Policy Header

## Purpose

The `Content-Security-Policy` (CSP) header helps mitigate cross-site scripting (XSS), data injection, and other attacks by specifying the sources from which content can be loaded. By restricting the sources for different types of content (scripts, styles, images, etc.), CSP provides an additional layer of security.

## Best Practices

- **`default-src 'self'`**: Restricts content to the same origin by default.
- **`object-src 'none'`**: Disables plugins such as Flash and Java applets.
- **`script-src 'self'`**: Allows JavaScript execution only from your domain.
- **`upgrade-insecure-requests`**: Ensures that any HTTP URLs are upgraded to HTTPS.

## Configuration in `secure.py`

The `ContentSecurityPolicy` class in `secure.py` allows flexible configuration of CSP. You can add various directives for specific content types like `script-src`, `style-src`, `img-src`, etc., to enhance security.

### Example Configuration

```python
secure_headers = Secure(
    csp=ContentSecurityPolicy()
        .default_src("'self'")
        .script_src("'self'")
        .style_src("'self'")
        .object_src("'none'")
)
```

### Methods Available

- **`default_src(*sources)`**: Specifies default content sources.
- **`script_src(*sources)`**: Specifies valid JavaScript sources.
- **`style_src(*sources)`**: Specifies valid CSS sources.
- **`object_src(*sources)`**: Specifies valid plugin sources (e.g., `<object>`, `<embed>`, `<applet>`).
- **`upgrade_insecure_requests()`**: Automatically upgrades HTTP URLs to HTTPS.

## Example Usage

To set up a `Content-Security-Policy` header that only allows content from the same origin and restricts the use of plugins:

```python
csp = ContentSecurityPolicy()
    .default_src("'self'")
    .script_src("'self'")
    .object_src("'none'")
print(csp.header_name)   # Output: 'Content-Security-Policy'
print(csp.header_value)  # Output: "default-src 'self'; script-src 'self'; object-src 'none'"
```

This can then be applied as part of your Secure headers configuration.

```python
secure_headers = Secure(csp=csp)
```

## Using Nonce and `strict-dynamic` in Content-Security-Policy

Content Security Policy (CSP) allows you to enhance the security of your web application by specifying the allowed sources of content. Using a nonce with the `strict-dynamic` directive improves protection against Cross-Site Scripting (XSS) attacks by dynamically allowing only scripts that are explicitly marked with a nonce. This is especially useful when you want to allow some inline scripts while ensuring only those scripts and their dynamically loaded dependencies are executed.

### Example: Using Nonce with `strict-dynamic`

Here’s how to set a CSP with a nonce and `strict-dynamic` using `secure.py`:

```python
import uuid

from flask import Flask, Response

from secure import ContentSecurityPolicy, Secure

app = Flask(__name__)


def generate_nonce():
    # Create a unique nonce for each request
    return uuid.uuid4().hex


secure_headers = Secure(
    csp=ContentSecurityPolicy()
    .default_src("'self'")
    .script_src(ContentSecurityPolicy().nonce(generate_nonce()), "'strict-dynamic'")
    .style_src("'self'")
    .object_src("'none'")
)


@app.after_request
def add_security_headers(response: Response):
    # Apply the security headers with a new nonce for each response
    nonce = generate_nonce()
    secure_headers.set_headers(response)
    # Ensure the nonce is passed in the CSP for inline scripts
    response.headers["Content-Security-Policy"] = response.headers[
        "Content-Security-Policy"
    ].replace("'nonce-'", f"'nonce-{nonce}'")
    return response


@app.route("/")
def home():
    # Example HTML with an inline script using the nonce
    nonce = generate_nonce()
    html = f"""
    <html>
    <head>
      <title>Secure.py with CSP</title>
      <script nonce='{nonce}'>
        console.log('This script is allowed because it has a nonce!');
      </script>
    </head>
    <body>
      Hello, world!
    </body>
    </html>
    """
    return Response(html, content_type="text/html")


if __name__ == "__main__":
    app.run()
```

### Example Output Headers

This example sets the following HTTP headers on the response:

```http
Content-Security-Policy: default-src 'self'; script-src 'nonce-<generated-nonce>' 'strict-dynamic'; style-src 'self'; object-src 'none'
```

```html
<html>
  <head>
    <title>Secure.py with CSP</title>
    <script nonce="<generated-nonce>">
      console.log("This script is allowed because it has a nonce!");
    </script>
  </head>
  <body>
    Hello, world!
  </body>
</html>
```

- **`default-src 'self'`**: Only content from the same origin is allowed by default.
- **`script-src 'nonce-<generated-nonce>' 'strict-dynamic'`**: Only scripts with the nonce or dynamically loaded by trusted scripts are allowed.
- **`style-src 'self'`**: Only CSS from the same origin is allowed.
- **`object-src 'none'`**: The `<object>` element is disabled for additional security.

### Why Use `strict-dynamic`?

The `strict-dynamic` directive allows the CSP to trust dynamically created scripts as long as they are loaded by scripts with a nonce or from a trusted source. This reduces the need to explicitly list external sources in the CSP, improving security by ensuring only scripts with a nonce or trusted dynamic scripts are executed.

For more details on `Content-Security-Policy` and the `nonce` attribute, refer to the following resources:

- [MDN Web Docs: Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy)
- [OWASP Secure Headers Project: Content-Security-Policy](https://owasp.org/www-project-secure-headers/#content-security-policy)

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#content-security-policy) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
