# Installation

`secure` requires Python 3.10 or newer and has no external dependencies.

Install it with `uv` or `pip`:

```bash
uv add secure
```

```bash
pip install secure
```

If you are following a framework example, install that framework separately.

```bash
pip install fastapi
```

After installation, import the public API from the package root:

```python
from secure import Secure
```

Most public builders are also re-exported from the package root, so you can usually keep imports in the form `from secure import Secure, Preset, ContentSecurityPolicy`.
