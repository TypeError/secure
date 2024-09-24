# Cache-Control Header

## Purpose

The `Cache-Control` header is used to define caching mechanisms for both requests and responses. Properly configuring this header can ensure sensitive data isn't inadvertently cached, and resources are served fresh when necessary.

## Best Practices

- **`no-store`**: Prevents any caching of sensitive data.
- **`max-age=0`**: Ensures the content is always fresh.
- **`immutable`**: Helps improve caching efficiency for resources that never change.
- **`no-transform`**: Ensures the intermediaries do not modify the content.

## Configuration in `secure.py`

The `CacheControl` class in `secure.py` allows flexible configuration of this header. It supports adding directives like `no-cache`, `no-store`, `max-age`, and others to ensure appropriate caching behavior.

### Example Configuration

```python
secure_headers = Secure(
    cache=CacheControl()
        .no_store()
        .max_age(0)
)
```

### Methods Available

- **`no_store()`**: Prevents all caching.
- **`no_cache()`**: Requires revalidation before caching.
- **`max_age(seconds)`**: Specifies the maximum time a resource is considered fresh.
- **`must_revalidate()`**: Forces caches to revalidate content before serving it.
- **`immutable()`**: Indicates that the resource is immutable and doesn't need revalidation.

## Example Usage

To set up a `Cache-Control` header with no caching allowed and a max-age of 0:

```python
cache_control = CacheControl().no_cache().no_store().max_age(0)
print(cache_control.header_name)   # Output: 'Cache-Control'
print(cache_control.header_value)  # Output: 'no-cache, no-store, max-age=0'
```

This can then be applied as part of your Secure headers configuration.

```python
secure_headers = Secure(cache=cache_control)
```

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#cache-control) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
