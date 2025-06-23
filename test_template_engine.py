from automailer.core.template import TemplateEngine, TemplateModel

class MyFields(TemplateModel):
    name: str
    committee: str
    allotment: str

with open("body.txt", "r") as f:
    body = f.read()

with open("subject.txt", "r") as f:
    subject = f.read()

fields = MyFields(name="John Doe", committee="ECOSOC", allotment="Algeria")


t = TemplateEngine(body_text=body, subject=subject)

res = t.render(fields)

print(res)
