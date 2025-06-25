from typing import Optional, Dict
from pydantic import BaseModel, model_validator, computed_field
import re
import json


def get_placeholder_regex(key) -> re.Pattern:
    pattern = r"\{\{ *KEY *\}\}".replace("KEY", key)
    return re.compile(pattern)

class TemplateModel(BaseModel):
    @model_validator(mode='after')
    def check_lowercase_alphanumeric(self):
        # we are validating the field names themselves, not the value.
        # this is because we are replacing them in the template string.
        for name, _ in self.__dict__.items():
            if not re.fullmatch(r'[a-z0-9_]+', name):
                raise ValueError(f"Field '{name}' must be lowercase alphanumeric characters or underscore.")
        return self

    @computed_field
    @property
    def hash_string(self) -> str:
        """
        Returns a hash of the model's fields.
        This is used to uniquely identify the template model.
        """
        # we cant do model_dump because it keeps recursively calling this computed field
        dump = self.model_json_schema()
        res = {}
        for key in dump["properties"].keys():
            res[key] = self.__dict__.get(key, None)
        return json.dumps(res)

class TemplateEngine:
    subject: Optional[str] = None
    text: Optional[str] = None
    html: Optional[str] = None

    def __init__(self, subject: Optional[str] = None, body_text: Optional[str] = None, body_html: Optional[str] = None):
        self.subject = subject
        self.text = body_text
        self.html = body_html

    def render(self, fields: TemplateModel) -> Dict[str, str]:
        res: dict = {
            "subject": self.subject,
            "text": self.text,
            "html": self.html
        }

        for key, value in fields.model_dump().items():
            regex = get_placeholder_regex(key)

            if self.subject:
                res["subject"] = regex.sub(str(value), res["subject"])
            if self.text:
                res["text"] = regex.sub(str(value), res["text"])
            if self.html:
                res["html"] = regex.sub(str(value), res["html"])

        return res
