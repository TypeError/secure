# X-Content-Type-Options

## Purpose

The `X-Content-Type-Options` header tells browsers to **respect the MIME type declared in `Content-Type`** instead of trying to guess ("sniff") a different type.

In practice, setting `X-Content-Type-Options: nosniff` can cause browsers to **block**:

- `style` requests not served as `text/css`
- `script` requests not served with a JavaScript MIME type

This helps reduce the risk of content being interpreted as executable when it should not be.

## Best Practices

- **Set to `nosniff`** (recommended): This is the standard and widely supported directive.
- **Use correct `Content-Type` values**: `nosniff` is most effective when your server sends accurate MIME types.

## Configuration with `Secure`

The `XContentTypeOptions` class configures `X-Content-Type-Options`.

**Default header value:** `nosniff`
All built-in presets include it.

### Minimal configuration

```python
from secure import Secure, XContentTypeOptions

secure_headers = Secure(
    xcto=XContentTypeOptions().nosniff(),
)
```

### Methods available

- **`nosniff()`**: Sets the header to `nosniff`, which blocks certain `script`/`style` requests when MIME types are incorrect.
- **`set(value)` / `value(value)`**: Sets a raw/custom header value (escape hatch). `value` is an alias for `set`.
- **`clear()`**: Resets the header to the library default (`nosniff`).

> Note: `set/value` are escape hatches. If you use `Secure.validate_and_normalize_headers(...)`, that layer is responsible for sanitization and safety checks.

## Example usage

```python
from secure import XContentTypeOptions

xcto = XContentTypeOptions().nosniff()
print(xcto.header_name)   # 'X-Content-Type-Options'
print(xcto.header_value)  # 'nosniff'
```

Apply via `Secure`:

```python
from secure import Secure, XContentTypeOptions

secure_headers = Secure(xcto=XContentTypeOptions().nosniff())
```

## Resources

- MDN Web Docs: X-Content-Type-Options
  [https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options)
- OWASP Secure Headers Project: X-Content-Type-Options
  [https://owasp.org/www-project-secure-headers/#x-content-type-options](https://owasp.org/www-project-secure-headers/#x-content-type-options)

## Attribution

This library implements security recommendations from trusted sources:

- MDN Web Docs (CC-BY-SA 2.5)
  [https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor](https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor)
  [https://creativecommons.org/licenses/by-sa/2.5/](https://creativecommons.org/licenses/by-sa/2.5/)
- OWASP Secure Headers Project (CC-BY-SA 4.0)
  [https://creativecommons.org/licenses/by-sa/4.0/](https://creativecommons.org/licenses/by-sa/4.0/)
