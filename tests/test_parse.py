from poml.prompt import Prompt

with open("chat.poml", "r", encoding="utf-8") as f:
    poml_text = f.read()

prompt = Prompt.parse(poml_text)
filled = prompt.render(user_input="Hello, what is POML?")
print(filled)
