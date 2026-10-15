from datetime import datetime
import json
from json import JSONDecodeError
from pathlib import Path
class Conversation:
    def __init__(self, system_message, title="New conversation"):
        self.system_message = {"role":"system", "content": system_message}
        self.title = title
        self.id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.history = []


    def add(self, role, content):
        self.history.append({"role":role, "content":content, "timestamp":datetime.now().isoformat(timespec="seconds")})


    def reset(self):
        self.history = []


    def pop(self):
        try:
            self.history.pop()
        except IndexError:
            pass


    def for_api(self):
        copy =  [
            {
                "role": x["role"],
                "content": x["content"]
            }
            for x in self.history
        ]
        reversed(copy)
        max_char = 12000
        total = 0
        history = []
        no = 0
        total += len(copy[no]['content'])
        try:
            history.append(copy[no])
            while total <= max_char:
                no += 1
                history.append(copy[no])
                total += len(copy[no]['content'])
            reversed(history)
        except IndexError:
            pass
        history.insert(0, self.system_message)
        return history


    def gen_title(self):
        hist = self.for_api()
        try:
            hist = hist[:3] + hist[-3:]
        except IndexError:
            pass
        hist.append({
            "role": "assistant",
            "content": "Read through all our message history and generate a short suitable title for it"
        })
        return hist


    def to_dict(self):
        hist = {
            "title": self.title,
            "id": self.id,
            "system_message": self.system_message["content"],
            "history": self.history
        }
        data = json.dumps(hist, indent=2)
        return data


    def save(self):
        folder = Path("conversations")
        folder.mkdir(exist_ok=True)
        path = folder / f"{self.id}.json"
        data = self.to_dict()
        with open(f"{path}", 'w') as f:
            f.write(data)

    @classmethod
    def load(cls, file_id:str):
        folder = Path("conversations")
        path = folder / f"{file_id}.json"
        with open(path, 'r') as file:
            data = json.load(file)
        conv = cls(data["system_message"], data["title"])
        conv.id = data["id"]
        conv.history = data["history"]
        return conv

    @classmethod
    def list_saved(cls):
        conv_hist = []
        folder = Path("conversations")
        exists = folder.exists()
        if exists:
            for file in folder.glob("*.json"):
                with open(file, 'r') as f:
                    data = json.load(f)
                try:
                    conv_hist.append((data["id"], data["title"]))
                except JSONDecodeError:
                    continue
            sorted(conv_hist, reverse=True)
            return conv_hist
        else:
            return []