from pathlib import Path
from datetime import date

class ExportMD():
    def __init__(self, data):
        self.data = data
        super(ExportMD, self).__init__()

    def export(self):
        learningstatus = Path(self.data["source"]).joinpath(
            "learningstatus.md")
        note = Path(self.data["source"]).joinpath(f"{self.data['note']}.md")

        self.write_summary(path=learningstatus)
        self.write_note(path=note)

    def write_summary(self, path):
        summary = self.parse_summary()
        with open(path, "a") as f:
            f.write(summary)

    def write_note(self, path):
        title, note = self.parse_note()

        with open(path, "a") as f:
            f.write("\n")
            f.write(f"## {title}\n")

            for i in self.data["resources"]:
                f.write(f"[Resource]({i})\n")

            f.write(note)
            f.write("\n")

    def parse_summary(self):
        today = date.today()
        title = self.data["title"]
        grok = "+ " * self.data["grok"]
        tags = self.data["tags"]
        note = self.data["note"]

        row = f"{today} | {title} | {grok}| "
        for i in tags:
            if i:
                clean_tag = i.split()[0]
                row += f"#{clean_tag} "
                
        row += f"| [[{note}#{title}]]\n"

        return row

    def parse_note(self):
        title = self.data["title"]
        note = self.data["contents"]

        return title, note
