# Security Policy

## Supported Versions

We take security seriously and are committed to providing timely updates for supported versions.

| Version | Supported          |
| ------- | ------------------ |
| 7.0.1   | :white_check_mark: |
| 6.0.0   | :white_check_mark: |
| < 6.0   | :x:                |

---

## Reporting a Vulnerability

**Please DO NOT report security vulnerabilities through public GitHub issues.**

We use GitHub's private vulnerability reporting feature to securely receive and manage security reports.

### How to Report

1. Go to the repository's **Security** tab.
2. Click **"Report a vulnerability"**.
3. Fill out the form with as much detail as possible.

If you are unable to use GitHub's private reporting, you may send an email to:

**kouroshhamidi92@gmail.com**

Please include the following information in your report:

- Type of vulnerability (e.g., XSS, CSRF, RCE, SQL injection)
- Affected file(s) and line(s) of code
- Step-by-step instructions to reproduce the issue
- Proof-of-concept (if available)
- Potential impact of the vulnerability

---

## Response Timeline

We strive to address all security issues as quickly as possible.

| Step | Timeframe |
| ---- | --------- |
| Initial response | Within 48 hours |
| Investigation & confirmation | Within 7 days |
| Fix development & testing | 7–30 days (depending on severity) |
| Patch release & public disclosure | Coordinated with reporter |

---

## Responsible Disclosure Policy

We kindly ask that you:

- **Do not** publicly disclose the vulnerability until we have released a fix.
- **Do not** exploit the vulnerability for malicious purposes.
- **Do not** perform attacks that could harm our users or infrastructure.

We will:

- Acknowledge your report within 48 hours.
- Keep you updated on our progress.
- Give you credit for the discovery (if you wish).
- Work with you to coordinate public disclosure.

---

## Security Updates

Security patches are released as part of regular version updates. We recommend all users to keep their installations up to date.

---

## Scope

This security policy applies to all code and dependencies within the **NumberGuessBot** project, including:

- Core bot code (`bot.py`, `game_core.py`)
- Desktop application (`desktop_app.py`, `HiddenNumber.exe`)
- Web interface (`index.html`)

---

## Exclusions

The following are **out of scope**:

- Third-party services or APIs used by the bot (e.g., Telegram, Bale)
- Vulnerabilities in outdated versions that are no longer supported
- Social engineering attacks
- Physical attacks

---

## Recognition

We appreciate the efforts of security researchers who help make this project safer. With your permission, we will publicly thank you in the project's release notes or README.

---

**Thank you for helping keep NumberGuessBot secure!**
