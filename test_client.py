from aura.client import ModelClient, AuraError

client = ModelClient()
try:
    reply = client.chat([{
        "role": "user",
        "content": "Say hello in one sentence."
    }])
    print(reply)
except AuraError as e:
    print("AURA error:", e)