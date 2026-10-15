from aura.conversation import Conversation

c = Conversation("You are AURA, a helpful personal assistant")
c.add("user", "hello")
c.add("assistant", "hello there")
c.save()
restored = Conversation.load(c.id)

print(c.for_api())
