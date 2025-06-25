# AutoMailer

## Introduction

This is a library that makes it easy to handle mass-emailing on a large scale.
The main purpose of this library is to streamline and standardize template usage, and to assist in crash recovery by incorporating state management.

## Usage

### Install the Library

```shell
pip install sqlalchemy tabulate pydantic

pip install -i https://test.pypi.org/simple/ automailer==0.0.3
```

### Importing and Using the Library

```python
from automailer import AutoMailer, TemplateModel, TemplateEngine

```

After importing, we need to define a schema for our data model.
This MySchema class inherits from TemplateModel, which is the same as defining a `Pydantic` model from its `BaseModel` class. 

We have four fields for this example. these four fields will be all we need to build the metadata for our email.

```python
class MySchema(TemplateModel):
    name: str
    committee: str
    allotment: str
    email: str
```

Next up, we define the templates for our subject and body.

### Defining Templates

- Template variables can be defined by wrapping the variable name with **Double Curly Braces**
- For example, `{{ name }}` is a variable with key "name".
- This variable name corresponds to the `MySchema` field you defined previously.
- Whitespaces between the variable name and the curly braces are optional, but we recommend them for better readability.

**NOTE**: Variable names must be **lowercase alphanumeric characters, or underscore**. No other character is allowed.


Now, let's define the templates for the subject and body in these two files:

`subject.txt`:
```
MUN Allotment Details
```

`body.txt`:
```
Hi {{name}}

You have been allotted {{ allotment }} in {{  committee  }}.

Congrats.
```

Let's load them into string objects, and initialize our Template Engine with the required data.

```python
with open("body.txt", "r") as f:
    body = f.read()

with open("subject.txt", "r") as f:
    subject = f.read()

template = TemplateEngine(subject=subject, body_text=body)
```

## Loading Data
The list of recipients is expected to be a list of `MySchema` objects, where we defined `MySchema` previously.
From whatever data source you have, convert the data into the schema that you defined.

In this example, my datasource is a list of dictionaries, for convenience.


```python
recipients = [
    {"name": "John", "committee": "ECOSOC", "allotment": "Algeria", "email": "myEmail@gmail.com"},
    {"name": "John", "committee": "ECOSOC", "allotment": "Algeria", "email": "myEmail@outlook.com"},
    {"name": "John", "committee": "ECOSOC", "allotment": "Algeria", "email": "myEmail@snuchennai.edu.in"},
]

obj_recipients = [MySchema(name=recipient['name'], committee=recipient['country'], ... )) for recipient in recipients]
```

### Sending the Emails

Next, we define the AutoMailer instance which handles the email sending for these recipients.
We need to provide the source email credentials, as well as the email provider to be used. 

Currently supported options are: `"gmail"` and `"outlook"`. (case sensitive).

```
automailer = AutoMailer(
    sender_email="myEmail@gmail.com",
    password="myPass",
    provider="gmail",
    session_name="test"
)
```

After that's done, all that's left is to send the emails.

```python
automailer.send_emails(
    recipients=obj_recipients,
    email_field="email",
    template=template
)
```

And we're done!

<hr>

## So why should I use this library?

The beauty of AutoMailer is that if your machine has an outage halfway through sending, there is no need to change the script in any way.
You need **no extra configuration** to prevent an email from sending to the same recipient twice.

Just run the script again, with no changes, and our inbuilt progress management system will take are of the rest.

## Credits

This project was brought to life by a squad in the Tech Team of [SSN-SNUC MUN 2025](https://ssnsnucmun.in)'s Organizing Committee.

- [Nilaa](http://github.com/nil-aa)
- [Kamlesh](http://github.com/Kamlesh-DevOP)
- [Sharon](http://github.com/sharonprabhu11)
- [Mahasvan](http://github.com/Mahasvan)
