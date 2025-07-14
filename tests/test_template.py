import pytest
import json
from pydantic import ValidationError
from automailer.core.template import TemplateModel, TemplateEngine, get_placeholder_regex

def test_template_model_valid_keys():
    class MyTemplate(TemplateModel):
        name: str
        email_123: str
        user_id: int
    
    model = MyTemplate(name="John", email_123="test@example.com", user_id=42)
    assert model.name == "John"
    assert isinstance(model.hash_string, str)
    assert json.loads(model.hash_string) == {
        "name": "John",
        "email_123": "test@example.com",
        "user_id": 42
    }

def test_template_model_invalid_key_raises():
    with pytest.raises(ValidationError) as e:
        class BadTemplate(TemplateModel):
            Name: str

        BadTemplate(Name="Invalid")

    assert "must be lowercase alphanumeric characters or underscore" in str(e.value)

def test_get_placeholder_regex():
    pattern = get_placeholder_regex("username")
    assert pattern.pattern == r"\{\{ *username *\}\}"
    assert pattern.fullmatch("{{ username }}")
    assert pattern.fullmatch("{{username}}")
    assert pattern.fullmatch("{{  username }}")
    assert not pattern.fullmatch("{{ username }")

def test_template_engine_render_basic():
    class MyTemplate(TemplateModel):
        username: str
        email: str

    fields = MyTemplate(username="nitin", email="user@example.com")

    engine = TemplateEngine(
        subject="Welcome, {{ username }}",
        body_text="Hello {{ username }}, your email is {{ email }}.",
        body_html="<b>{{ username }}</b> - {{ email }}"
    )

    result = engine.render(fields)
    
    assert result["subject"] == "Welcome, nitin"
    assert result["text"] == "Hello nitin, your email is user@example.com."
    assert result["html"] == "<b>nitin</b> - user@example.com"

def test_template_engine_partial_template():
    class MyTemplate(TemplateModel):
        product: str

    fields = MyTemplate(product="Pen")
    engine = TemplateEngine(
        subject="Product: {{ product }}",
        body_text=None,
        body_html=None
    )

    result = engine.render(fields)
    assert result["subject"] == "Product: Pen"
    assert result["text"] is None
    assert result["html"] is None

def test_template_engine_unmatched_placeholder_remains():
    class MyTemplate(TemplateModel):
        foo: str

    fields = MyTemplate(foo="Bar")
    engine = TemplateEngine(
        subject="Missing: {{ unknown }}",
        body_text="Only {{ foo }}",
        body_html="Also {{ foo }}"
    )

    result = engine.render(fields)
    assert result["subject"] == "Missing: {{ unknown }}"
    assert result["text"] == "Only Bar"
    assert result["html"] == "Also Bar"
