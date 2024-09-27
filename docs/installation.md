# Installation Guide

## Overview

`secure.py` is a lightweight and powerful Python library designed to simplify the management of HTTP security headers. It helps you easily add secure headers to web applications, supporting a variety of popular frameworks. This guide will walk you through the installation process, system requirements, and framework compatibility.

---

## Requirements

- **Python Version**: `secure.py` supports Python 3.10 and above.
- **Supported Platforms**: The library is cross-platform, supporting Linux, macOS, and Windows.

To ensure compatibility with `secure.py`, your system should have Python version 3.10 or higher. You can check your Python version by running the following command:

```bash
python --version
```

Most modern systems should meet this requirement.

---

## Installation via pip

To install `secure.py` from the Python Package Index (PyPI), use the following command:

```bash
pip install secure.py
```

This will download and install the latest version of `secure.py`, along with any dependencies required for basic usage.

### Optional Dependencies

If you're using `secure.py` with specific web frameworks, you’ll need to install the respective framework alongside the library. Here are some common optional dependencies:

```bash
pip install aiohttp  # For aiohttp support
pip install flask    # For Flask support
pip install fastapi  # For FastAPI support
```

Make sure to install the framework you're working with to ensure seamless integration with `secure.py`.

For integration with other frameworks, refer to the [framework integration guide](./frameworks.md) for details on the supported frameworks and their setup.

---

## Testing the Installation

After installation, you can verify that `secure.py` is working properly by importing it in a Python shell or script:

```python
>>> from secure import Secure
>>> secure_headers = Secure.with_default_headers()
>>> print(secure_headers)
```

If the headers are printed without any errors, the installation was successful and you're ready to begin securing your web application.

---

## Troubleshooting

If you encounter any issues during installation, ensure the following:

1. **Correct Python Version**: Verify that Python 3.10+ is installed.
2. **pip is Up-to-date**: Make sure you're using the latest version of `pip`. You can upgrade it with:
   ```bash
   pip install --upgrade pip
   ```
3. **Virtual Environments**: Consider using a virtual environment to isolate your dependencies. You can create one with:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

For further issues, consult the [GitHub repository](https://github.com/TypeError/secure) for troubleshooting tips or to open an issue.
