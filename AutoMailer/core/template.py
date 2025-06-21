from typing import Optional, Dict
from pydantic import BaseModel

class Template(BaseModel):
    subject: str
    text: Optional[str] = None
    html: Optional[str] = None

    def _fill(self, template: Optional[str], row: Dict[str, str]) -> Optional[str]:
        if not template:
            return None
        for key, value in row.items():
            template = template.replace(f"{{{{{key}}}}}", value)
        return template

    def render_subject(self, row: Dict[str, str]) -> str:
        return self._fill(self.subject, row) or ""

    def render_text(self, row: Dict[str, str]) -> str:
        return self._fill(self.text, row) or ""

    def render_html(self, row: Dict[str, str]) -> str:
        return self._fill(self.html, row) or ""
