from automailer.core.template import TemplateEngine, TemplateModel

class MyFields(TemplateModel):
    name: str
    committee: str
    allotment: str

with open("body.txt", "r") as f:
    body = f.read()

print("Body text loaded successfully.")
print(body)

with open("subject.txt", "r") as f:
    subject = f.read()

fields = MyFields(name="John Doe", committee="ECOSOC", allotment="Algeria")


t = TemplateEngine(body_text=body)

res = t.render(fields)

# 1. name
    # 1. key, value -> "name", "John Doe"
    # 2. regex = re.compile(r"\{\{ *name *\}\}")
    # 3. replace pattern matches with John Doe
# 2. committee
    # 1. key, value -> "committee", "ECOSOC"
    # 2. regex = re.compile(r"\{\{ *committee *\}\}")
    # 3. replace pattern matches with ECOSOC
# 3. allotment
    # 1. key, value -> "allotment", "Algeria"
    # 2. regex = re.compile(r"\{\{ *allotment *\}\}")
    # 3. replace pattern matches with Algeria


print("+"*10)
print(res["text"])
