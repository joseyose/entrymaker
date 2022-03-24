from pathlib import Path
from datetime import date
# import pprint

# temporary info
# DATA = {"source": r"E:\test\notes",
#         "note": "python",
#         "tags": ["python", "programming", "vfx"],
#         "grok": 4,
#         "resources": ["path1", "path2"],
#         "title": "How to do that thing I've been meaning to learn",
#         "contents":
# """**core.editor**
# By default, Git uses whatever you’ve set as your default text editor via one of the shell environment variables VISUAL or EDITOR, or else falls back to the vi editor to create and edit your commit and tag messages. To change that default to something else, you can use the core.editor setting:
# """}


# class DataStore():
#     def __init__(self):
#         self.data = {"source": r"E:\test\notes",
#                      "note": "python",
#                      "tags": ["python", "programming", "vfx"],
#                      "grok": 4,
#                      "resources": ["path1", "path2"],
#                      "title": "How do I that thing I've been meaning",
#                      "contents":
# """It really is incredible how long it took me to appreciate this feature of not only python but programming in general. It's also so easy to setup with python. 
# Anyways, all you have to do is: 
# `python -m venv /path/to/new/virtual/environment`

# You can have a directory full of environments that you might you know share across different projects or you could simply have one at the root of any project you are working on."
#                      """}


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

    # def validate_path(self, path):
    #     if Path(path):
    #         return True
    #     else:
    #         return False

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
            row += f"#{i} "
        row += f"| [[{note}#{title}]]\n"

        return row

    def parse_note(self):
        title = self.data["title"]
        note = self.data["contents"]

        return title, note

    # def get_original_data(self, path):
    #     # Check if the provide file exists
    #     original_note_path = Path(path)

    #     if Path(path).is_file():
    #         # original_note_name = Path(path).name
    #         # new_note = Path(path).parent.joinpath(f"tmp_{original_note_name}")

    #         # Read the original note
    #         with open(original_note_path, "r") as f:
    #             data = f.read()

    #         # # Make a copy of the original note
    #         # with open(str(new_note), "w") as f:
    #         #     f.write(data)

    #         return data

# ExportMD().export()
# what do I need?
"""
- know where my learning status note is          --- [x]
- know which note I want append to               --- [x]
- know which tags the user provided              --- [x]
- know which grok score they gave                --- [x]
- know the resources they gave                   --- [x]
- know the title description                     --- [x]
- know the contents of their new note            --- [x]
- finally export that to the note the gave us    --- [x]

We need a data structure --- likely a dictionary that contains all of
those things

data = {"source": "/path/,
        "note": "note_to_use",
        "tags": [list of tags],
        "grok": "grok_score",
        "resource": [list_of_resources],
        "title": "title_description",
        "contents": "full string of content"
        }
"""
