from aura.client import ModelClient

client = ModelClient()
first = client.chat([{"role": "user", "content": "My name is Goodluck."}])
print("1:", first)

history = [
    {"role": "user", "content": "My name is Goodluck."},
    {"role": "assistant", "content": first},
    {"role": "user","content": "What is my name"},
]
second = client.chat(history)
print("2:", second)