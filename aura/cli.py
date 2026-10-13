from .client import ModelClient, AuraError

def main():
    client = ModelClient()
    history = [{"role": "system", "content": "You are AURA, a helpful personal assistant"}]
    while True:
        try:
            q = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("Goodbye.")
            break
        if not q:
            continue
        if q.lower() == 'exit':
            break
        else:
            history.append({"role": "user", "content": f"{q}"})
            try:
                reply = client.chat(history)
            except AuraError as e:
                history.pop()
                print("[error]", e)
                continue
            print(f"AURA:", reply)
            history.append({"role": "assistant", "content": reply})