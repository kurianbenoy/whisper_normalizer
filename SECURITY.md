# Security Policy

## Supported Versions

This project follows semantic versioning. Security updates are provided for the latest 1.0.x release, including pre-releases such as `1.0.0a1`, and for the latest 0.1.x release until 1.0.0 is published.

| Version                                      | Supported                                   |
| -------------------------------------------- | ------------------------------------------- |
| 1.0.x (including pre-releases, e.g. 1.0.0a1) | :white_check_mark:                          |
| 0.1.x                                        | :warning: security fixes until 1.0.0 final  |
| < 0.1.0                                      | :x:                                         |

Fixes are released against the latest version in a supported line; upgrade to receive them.

## Reporting a Vulnerability

Please report security vulnerabilities **privately** via email to **kurian.bkk@gmail.com**.

Include the following details:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes

The maintainer will:
- Acknowledge receipt within 7 days
- Provide a preliminary assessment within 14 days
- Release a fix as soon as practical, typically within 30 days for critical issues

Do **not** file public issues for security vulnerabilities.

## Scope

This policy covers the `whisper_normalizer` package and its direct dependencies. Vulnerabilities in transitive dependencies should be reported to their respective maintainers.