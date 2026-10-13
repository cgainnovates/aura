from aura.client import ModelClient, AuraError

client = ModelClient()
try:
    reply = client.chat([{
        "role": "user",
        "content": "Say Hello in a sentence."
    }])
    print(reply)
except AuraError as e:
    print("AURA error:", e)