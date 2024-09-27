# Cross-Origin-Opener-Policy Header

## Purpose

The `Cross-Origin-Opener-Policy` (COOP) header isolates your browsing context from potentially untrusted contexts, preventing attackers from accessing your global object through popups and mitigating cross-origin attacks such as XS-Leaks. By setting this header, you protect against malicious cross-origin interactions that could compromise your application's security.

## Best Practices

- **`same-origin`**: This is the most secure option, isolating your document from other origins.
- **`same-origin-allow-popups`**: Allows popups while maintaining some level of isolation.
- **`unsafe-none`**: Disables COOP, potentially exposing your application to cross-origin risks. Use this only if isolation is not required.

## Configuration in `secure.py`

The `CrossOriginOpenerPolicy` class in `secure.py` allows you to configure the COOP header with options like `same-origin`, `same-origin-allow-popups`, or `unsafe-none` to control the behavior of popups and cross-origin contexts.

### Example Configuration

```python
secure_headers = Secure(
    coop=CrossOriginOpenerPolicy().same_origin()
)
```

### Methods Available

- **`same_origin()`**: Isolates the browsing context to the same origin, preventing cross-origin documents from being loaded.
- **`same_origin_allow_popups()`**: Retains references to popups or tabs that opt out of isolation.
- **`unsafe_none()`**: Disables the COOP protection, allowing the document to be added to its opener’s browsing context group.

## Example Usage

To set up a `Cross-Origin-Opener-Policy` header that isolates your application from cross-origin contexts:

```python
coop = CrossOriginOpenerPolicy().same_origin()
print(coop.header_name)   # Output: 'Cross-Origin-Opener-Policy'
print(coop.header_value)  # Output: 'same-origin'
```

This can then be applied as part of your Secure headers configuration.

```python
secure_headers = Secure(coop=coop)
```

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#cross-origin-opener-policy) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
