# SmartMailer Documentation

## Overview

SmartMailer is a Python library for bulk email delivery with:

- Jinja2-powered subject, text, and HTML templates
- Pydantic-backed recipient models
- Session tracking to avoid duplicate sends across reruns
- Concurrent SMTP delivery using an async connection pool
- Optional per-recipient or global CC, BCC, and attachments

The current package version is `1.0.0`.

## Installation

### Requirements

- Python `3.9+`
- An SMTP account supported by SmartMailer's provider settings

### Install from the project

```bash
pip install .
```

For local development:

```bash
pip install -e .
```

### Runtime dependencies

SmartMailer currently depends on:

- `sqlalchemy`
- `tabulate`
- `pydantic>=2.0`
- `aiosmtplib`
- `jinja2`
- `threading`

## Supported Providers

SmartMailer reads SMTP settings from `src/smartmailer/core/settings.json`.

At the moment, the bundled providers are:

- `gmail`
- `outlook`

The `provider` argument must match one of those keys exactly.

## Gmail Setup

If you use Gmail, use a Google App Password instead of your normal account password.

1. Enable 2-Step Verification in your Google account.
2. Open <https://myaccount.google.com/apppasswords>.
3. Create an app password for mail usage.
4. Pass that 16-character password to SmartMailer.

## Quick Start

```python
from jinja2 import Environment

from smartmailer import SmartMailer, TemplateEngine, TemplateModel
from smartmailer.core.template import (
    JinjaTemplateParser,
    JinjaTemplateRenderer,
    TemplateValidator,
)


class Recipient(TemplateModel):
    name: str
    committee: str
    allotment: str
    email: str


subject = "MUN Allotment Details"
text_body = """Dear {{ name }},

Congratulations.
You are assigned to the {{ committee }} committee with the allotment of {{ allotment }}.

Regards,
The Organizing Committee
"""

html_body = """
<html>
  <body>
    <p>Dear {{ name }},</p>
    <p>
      You are assigned to the <strong>{{ committee }}</strong> committee
      with the allotment of <strong>{{ allotment }}</strong>.
    </p>
  </body>
</html>
"""

env = Environment()

template = TemplateEngine(
    parser=JinjaTemplateParser(env),
    validator=TemplateValidator(),
    renderer=JinjaTemplateRenderer(env),
    subject=subject,
    text=text_body,
    html=html_body,
)

recipients = [
    Recipient(
        name="John",
        committee="UNDP",
        allotment="India",
        email="john@gmail.com",
    ),
    Recipient(
        name="John",
        committee="UNDP",
        allotment="USA",
        email="john@outlook.com",
    ),
]

mailer = SmartMailer(
    sender_email="your_email@gmail.com",
    password="your-app-password",
    provider="gmail",
    session_name="mun-allotments",
    log_to_file=False,
    log_level="WARNING",
)

mailer.send_emails(
    recipients=recipients,
    email_field="email",
    template=template,
    show_preview=True,
    preview_count=5,
)
```

## Core Concepts

### `TemplateModel`

Recipients should be defined using `TemplateModel`, which is built on top of Pydantic.

```python
class Recipient(TemplateModel):
    name: str
    email: str
```

Important behavior:

- Field names must be lowercase Python identifiers.
- Template validation uses your model fields as the allowed variable set.
- Each recipient gets a computed `hash_string`, which SmartMailer uses for session tracking.

### `TemplateEngine`

`TemplateEngine` coordinates three responsibilities:

- parsing variables from templates
- validating them against the model schema
- rendering the final subject/body

You can provide any combination of:

- `subject`
- `text`
- `html`

At least one of `text` or `html` should render to non-empty content before sending.

### Jinja components

The standard setup is:

```python
env = Environment()

parser = JinjaTemplateParser(env)
renderer = JinjaTemplateRenderer(env)
validator = TemplateValidator()
```

## Template Rules

SmartMailer uses Jinja2 syntax:

- variables: `{{ name }}`
- conditionals: `{% if allotment %}...{% endif %}`
- loops: `{% for item in items %}...{% endfor %}`
- filters: `{{ email | lower }}`

Validation is fail-fast:

- if a template references a field not present on your `TemplateModel`, rendering raises an error
- SmartMailer logs that recipient's rendering failure and skips that recipient

Example:

```text
Dear {{ name }},
{% if allotment %}
You have been assigned: {{ allotment }}
{% else %}
Your allotment is pending.
{% endif %}
```

## Loading Template Files

You can load templates from files before building the engine:

```python
with open("subject.txt", "r", encoding="utf-8") as f:
    subject = f.read()

with open("body.txt", "r", encoding="utf-8") as f:
    body = f.read()
```

Then pass those strings into `TemplateEngine`.

## Sending Emails

### Basic send

```python
mailer.send_emails(
    recipients=recipients,
    email_field="email",
    template=template,
)
```

### Method signature

```python
send_emails(
    recipients,
    email_field,
    template,
    attachment_paths=None,
    cc=None,
    bcc=None,
    cc_field="cc",
    bcc_field="bcc",
    attachment_field="attachments",
    show_preview=True,
    preview_count=5,
)
```

### What the arguments do

- `recipients`: list of `TemplateModel` instances
- `email_field`: model field containing the destination email address
- `template`: configured `TemplateEngine`
- `attachment_paths`: global attachments added to all outgoing emails unless overridden per recipient
- `cc`: global CC recipients
- `bcc`: global BCC recipients
- `cc_field`: recipient model field used for per-recipient CC values
- `bcc_field`: recipient model field used for per-recipient BCC values
- `attachment_field`: recipient model field used for per-recipient attachments
- `show_preview`: prints the first rendered email before sending starts
- `preview_count`: wait time in seconds before sending begins after preview

## Concurrency Model

SmartMailer sends bulk mail concurrently.

Current behavior in `MailSender`:

- an async SMTP connection pool is created
- the pool size is fixed at `10`
- each recipient is sent by a worker coroutine
- failed connections are recreated and returned to the pool

This means SmartMailer is designed to process multiple emails in parallel instead of sending strictly one-by-one.

Practical notes:

- if your SMTP provider has rate limits, send carefully
- the preview delay happens before the concurrent send phase starts
- session tracking still records recipients individually as sends succeed

## Session Tracking and Crash Recovery

SmartMailer stores session data in:

```text
mail_sessions/
```

How it works:

- each `session_name` gets its own database file
- sent recipients are tracked using the recipient model's `hash_string`
- rerunning the same session skips recipients already marked as sent

This is what makes crash recovery simple: rerun the script with the same `session_name`, and SmartMailer avoids resending recipients already completed in that session.

You can inspect sent entries with:

```python
mailer.show_sent()
```

## CC, BCC, and Attachments

You can define these per recipient by adding optional fields to your model.

```python
from typing import Optional


class Recipient(TemplateModel):
    name: str
    email: str
    cc: Optional[list[str]] = None
    bcc: Optional[list[str]] = None
    attachments: Optional[list[str]] = None
```

Example usage:

```python
recipients = [
    Recipient(
        name="Arjun",
        email="arjun@example.com",
        cc=["mentor@example.com"],
        bcc=["audit@example.com"],
        attachments=[r"C:\files\invite.pdf"],
    )
]

mailer.send_emails(
    recipients=recipients,
    email_field="email",
    template=template,
    cc_field="cc",
    bcc_field="bcc",
    attachment_field="attachments",
)
```

Notes:

- per-recipient attachment fields are read from each model instance
- global `cc`, `bcc`, and `attachment_paths` can still be passed directly to `send_emails`
- BCC recipients are used during delivery, but SmartMailer does not place a `Bcc` header into the message in the async bulk path

## HTML Emails

If both `text` and `html` are provided, SmartMailer builds a multipart email with both representations.

If only one is provided, that one is sent.

```python
template = TemplateEngine(
    parser=parser,
    validator=validator,
    renderer=renderer,
    subject="Welcome {{ name }}",
    text="Hello {{ name }}",
    html="<p>Hello <strong>{{ name }}</strong></p>",
)
```

## Logging

`SmartMailer` accepts:

- `log_to_file`
- `log_level`

Example:

```python
mailer = SmartMailer(
    sender_email="your_email@gmail.com",
    password="your-app-password",
    provider="gmail",
    session_name="batch-01",
    log_to_file=True,
    log_level="INFO",
)
```
