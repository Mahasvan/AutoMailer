class Template:
    def __init__(self, subject: str, text: str = None, html: str = None):
        self.subject = subject
        self.text = text
        self.html = html

    def _fill(self, template: str, row: dict[str, str]) -> str:
        if not template:
            return None
        for key, value in row.items():
            template = template.replace(f"{{{{{key}}}}}", value)
        return template

    def render_subject(self, row: dict[str, str]) -> str:
        return self._fill(self.subject, row)

    def render_text(self, row: dict[str, str]) -> str:
        return self._fill(self.text, row)

    def render_html(self, row: dict[str, str]) -> str:
        return self._fill(self.html, row)
