from .client import ModelClient, AuraError
from .conversation import Conversation
system_message = ("You are AURA, a helpful personal assistant, "
                  "keep conversation concise by default and stay under a few "
                  "hundred words, and give more details only when asked")

def choose_conversation():
    saved = Conversation.list_saved()
    if saved:
        for index,conv in enumerate(saved, start=1):
            print(f"{index}. {conv[0]}")
        while True:
            text = input("Enter the conversation number to continue from "
                            "or click enter for new conversation: ").strip()
            if not text:
                return Conversation(system_message)

            try:
                use = int(text)
            except ValueError:
                print("Invalid input! Enter an integer")
                continue
            else:
                if use > len(saved) or use < 1:
                    print("That conversation number isn't listed")
                    continue
                else:
                    break

        resume_conv = Conversation.load(saved[use-1][0])
        return resume_conv
    else:
        return Conversation(system_message)



def main():
    # c = Conversation(system_message)
    c = choose_conversation()
    client = ModelClient()
    while True:
        try:
            q = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("Goodbye.")
            break
        if not q:
            continue
        if q.lower() == 'exit':
            c.title = client.chat(c.gen_title())
            c.save()
            break
        elif q == "/clear":
            c.reset()
            print("Conversation reset successful")
            continue
        elif q == "/new":
            c = Conversation(system_message)
            print("Started a new Conversation")
        else:
            c.add("user", q)
            try:
                reply = client.chat(c.for_api())
                if len(c.history) == 3 or (len(c.history) - 1) % 20 == 0:
                    c.title = client.chat(c.gen_title())
                    c.save()
            except AuraError as e:
                c.pop()
                print("[error]", e)
                continue
            print(f"AURA:", reply)
            msg = c.for_api()
            print(len(msg), "messages,", sum(len(m["content"])for m in msg), "characters")
            c.add("assistant", reply)
            c.save()
