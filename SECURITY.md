# Security Policy

## Supported Versions

Security fixes are provided for the latest patch release in the current major version. Reports about unsupported versions are still useful when the issue can be reproduced in a supported release.

| Version | Supported |
| ------- | --------- |
| 2.x     | Yes       |
| 1.x     | No        |
| < 1.0   | No        |

## Reporting a Vulnerability

Please do not open a public issue or pull request for a suspected security vulnerability.

Report vulnerabilities privately through [GitHub's security advisory form](https://github.com/TypeError/secure/security/advisories/new). If you cannot use GitHub, email [caleb@typeerror.com](mailto:caleb@typeerror.com) with the subject `secure security report`.

Include as much of the following as possible:

- The affected version and installation method
- The relevant Python, operating-system, and web-framework versions
- A description of the vulnerability and its potential impact
- Steps to reproduce or a minimal proof of concept
- Any known mitigations or workarounds
- Whether the vulnerability has been disclosed elsewhere
- A safe way to contact you for follow-up questions

You can expect:

- An acknowledgment within three business days
- An initial assessment or status update within seven business days
- Further updates when the assessment changes or a fix is ready

If the report is accepted, we will coordinate a fix and disclosure timeline with you. When possible, we will publish a security advisory and patched release together, including affected and fixed versions and any available mitigations. Credit will be given if you would like it. If the report is declined, we will explain why—for example, because the behavior is expected, cannot be reproduced, or is outside this project's scope.

Please allow reasonable time to investigate and release a fix before publicly disclosing the vulnerability.

## Scope and Safe Harbor

This policy covers the `secure` package and this repository. It does not authorize testing applications, infrastructure, or data belonging to users of `secure` or any other third party.

We will not pursue legal action against research conducted in good faith under this policy. To qualify, test only systems and data you own or are authorized to use, limit access and exploitation to what is necessary to demonstrate the issue, avoid privacy violations and service disruption, do not retain or disclose sensitive data, and report the vulnerability promptly.

