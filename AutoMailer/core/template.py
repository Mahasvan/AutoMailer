from typing import Optional

class Template:
    def __init__(self, subject: str, text: Optional[str] = None, html: Optional[str] = None):
        self.subject = subject
        self.text = text
        self.html = html

    def _fill(self, template: Optional[str], row: dict[str, str]) -> Optional[str]:
        if not template:
            return None
        for key, value in row.items():
            template = template.replace(f"{{{{{key}}}}}", value)
        return template

    def render_subject(self, row: dict[str, str]) -> str:
        return self._fill(self.subject, row) or ""

    def render_text(self, row: dict[str, str]) -> str:
        return self._fill(self.text, row) or ""

    def render_html(self, row: dict[str, str]) -> str:
        return self._fill(self.html, row) or ""
