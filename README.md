# SmartMailer

SmartMailer is a Python library for sending bulk emails with support for templates, attachments, session management, and logging. It is designed for easy integration into your own projects.
SmartMailer is a Python library for sending bulk emails with support for templates, attachments, session management, and logging. It is designed for easy integration into your own projects.

## Features

- Send individual or bulk emails
- Templated subjects, plain text, and HTML content
- Attachments support
- CC and BCC support
- Session management to avoid duplicate sends
- Logging for all actions

## Quickstart

Visit [The Documentation Page](https://github.com/Mahasvan/SmartMailer/blob/main/DOCS.md)

<!-- 
## Installation

Install via pip (after building your package):

```
pip install .
```

Or add to your `requirements.txt` if published to PyPI:

```
SmartMailer
```

## Requirements

- Python 3.10+
- `sqlalchemy`
- `tabulate`
- `pydantic` -->
<!-- 
## Quick Start


### 1. Prepare your settings

Edit `SmartMailer/core/settings.json` to include your SMTP provider details:

```json
{
    "gmail": ["smtp.gmail.com", 587],
    "outlook": ["smtp.office365.com", 587]
}
```

### 2. Example Usage

```python
from SmartMailer.smartmailer import SmartMailer

# Define your sender credentials and session name
sender_email = "your_email@gmail.com"
password = "your_password"
provider = "gmail"
session_name = "june_campaign"

# Create a SmartMailer instance
mailer = SmartMailer(sender_email, password, provider, session_name)

# Prepare your recipient list (must include 'email' key)
recipients = [
    {"email": "recipient1@example.com", "name": "Alice"},
    {"email": "recipient2@example.com", "name": "Bob"}
]

# Define your templates
subject_template = "Hello, {name}!"
text_template = "Dear {name},\nThis is a plain text email."
html_template = "<p>Dear {name},</p><p>This is an <b>HTML</b> email.</p>"

# Optional: Attachments, CC, BCC
attachments = ["path/to/file.pdf"]
cc = ["cc@example.com"]
bcc = ["bcc@example.com"]

# Send emails
mailer.send_emails(
    recipients=recipients,
    subject_template=subject_template,
    text_template=text_template,
    html_template=html_template,
    attachment_paths=attachments,
    cc=cc,
    bcc=bcc
)

# Show sent recipients
mailer.show_sent()
```

### 3. Template Placeholders

You can use any key from your recipient dictionary as a placeholder in your templates, e.g. `{name}`.

### 4. Session Management

SmartMailer tracks which recipients have already been emailed in a session. If you run the script again with the same session name, only new recipients will be emailed.

## Logging

Logs are handled via the built-in logger and will output to the console. -->


## So why should I use this library?

The beauty of SmartMailer is that if your machine has an outage halfway through sending, there is no need to change the script in any way.
You need **no extra configuration** to prevent an email from sending to the same recipient twice.

Just run the script again, with no changes, and our inbuilt progress management system will take care of the rest.

## License

[MIT License](https://github.com/Mahasvan/SmartMailer/blob/main/LICENSE)


## Credits

This project was brought to life by a squad in the Tech Team of [SSN-SNUC MUN 2025](https://ssnsnucmun.in)'s Organizing Committee.

- [Nilaa](http://github.com/nil-aa)
- [Kamlesh](http://github.com/Kamlesh-DevOP)
- [Sharon](http://github.com/sharonprabhu11)
- [Nitin Karthick](https://github.com/yukii1004)
- [Mahasvan](http://github.com/Mahasvan)

**Note:** Never hardcode your email password in production code. Use environment variables or secure vaults.
