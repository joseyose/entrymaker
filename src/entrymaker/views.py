from ui.widget import Ui_Form
from PyQt5 import QtWidgets, QtGui  # , QtCore, QtGui
from pathlib import Path
from exportmd import ExportMD
from sys import platform

WORDWRAP = 80


class Window(QtWidgets.QDialog, Ui_Form):
    def __init__(self):
        super(Window, self).__init__()

        self._setupUI()
        self.setWindowTitle("entry_maker::1.0")
        self.configure_ui()

    def enable_fields(self):
        self.lineedit_description.setEnabled(True)
        self.textedit_edit.setEnabled(True)
        self.textedit_preview.setEnabled(True)
        self.lineedit_tags.setEnabled(True)
        self.button_add.setEnabled(True)
        self.button_remove.setEnabled(True)
        self.lineedit_resource1.setEnabled(True)
        self.slider_grokscore.setEnabled(True)
        self.button_reset.setEnabled(True)

    def activate_export(self):
        count = len(self.lineedit_description.text())
        if count == 0:
            self.button_export.setEnabled(False)
        else:
            self.button_export.setEnabled(True)

    def _setupUI(self):
        self.setupUi(self)
        self.resources = [self.lineedit_resource1]
        self.update_resourcescount()

    def configure_ui(self):
        # BUTTONS CLICKED
        self.button_filedialog.clicked.connect(self.load_filedialog)
        self.button_add.clicked.connect(self.add_resource)
        self.button_remove.clicked.connect(self.remove_resource)
        self.button_export.clicked.connect(self.export)
        self.button_reset.clicked.connect(self.reset_ui)

        # Enable buttons
        self.button_export.setEnabled(False)
        self.button_reset.setEnabled(False)
        self.combobox_note.setEnabled(False)
        self.lineedit_description.setEnabled(False)
        self.textedit_edit.setEnabled(False)
        self.textedit_preview.setEnabled(False)
        self.lineedit_tags.setEnabled(False)
        self.lineedit_resource1.setEnabled(False)
        self.button_add.setEnabled(False)
        self.button_remove.setEnabled(False)
        self.slider_grokscore.setEnabled(False)
        self.lineedit_description.textChanged.connect(self.changecolorpastlimit)
        self.textedit_edit.textChanged.connect(self.set_markdown)

        # Setup line wraps for the preview
        self.textedit_edit.clear()
        self.textedit_edit.setLineWrapMode(
            QtWidgets.QTextEdit.FixedColumnWidth)
        self.textedit_edit.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.textedit_edit.setLineWrapColumnOrWidth(WORDWRAP)

        self.textedit_preview.clear()
        self.textedit_preview.setLineWrapMode(
            QtWidgets.QTextEdit.FixedColumnWidth)
        self.textedit_preview.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.textedit_preview.setLineWrapColumnOrWidth(WORDWRAP)
        # self.textEdit_2.setTextColor(QtGui.QColor(255, 0, 0))

        self.textedit_edit.setTabStopDistance(
            QtGui.QFontMetricsF(
                self.textedit_edit.font()).horizontalAdvance(' ') * 4)
        self.textedit_preview.setTabStopDistance(
            QtGui.QFontMetricsF(
                self.textedit_preview.font()).horizontalAdvance(' ') * 4)
        # self.plainTextEdit.setTabStopDistance(
        # QtGui.QFontMetricsF(
        # self.plainTextEdit.font()).horizontalAdvance(' ') * 4)

        # This was in the constructor prior to this
        self.textedit_preview.setReadOnly(True)
        self.lineedit_description.textChanged.connect(self.activate_export)
        self.combobox_note.activated.connect(self.enable_fields)

        # check for existing config file
        self.check_init_dir()

    def check_init_dir(self):
        dirfile = Path("./bin/init.txt")

        if dirfile.exists():
            with open(dirfile, "r") as f:
                notes_path = f.read().splitlines()[0]
                print(notes_path)
                self.lineedit_source.setText(notes_path)
                self.populate_combobox()
        else:
            print("Init file does not exist")
                    
    def load_filedialog(self):
        if self.lineedit_source.text():
            initDir = self.lineedit_source.text()
        else:
            initDir = str(Path.home())

        # Load file dialog
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Notes Directory", initDir)

        if path:
            self.lineedit_source.setText(path)
            # Populate qcombobox
            self.populate_combobox()

    def populate_combobox(self):
        # Clear it first
        self.combobox_note.clear()
        # Good god this is a much shorter version of this, but it's basically
        # doing the same thing :)
        # md = Path(self.lineedit_source.text()).rglob("*.md")
        notes = [""]

        for path in Path(self.lineedit_source.text()).rglob("*.md"):
            # make sure to check which os I'm launching from 
            if platform == "win32":
                path = str(path).split("\\")[-1].split(".")[0]
            else:
                path = str(path).split("/")[-1].split(".")[0]

            notes.append(path)

        # Only modify this if we actually find markdown files
        if len(notes) >= 2:
            notes.sort()
            self.combobox_note.setEnabled(True)
            self.combobox_note.addItems(notes)

    def add_resource(self):
        count = self.grid_resources.count()

        if count >= 2:
            edit = QtWidgets.QLineEdit()
            label = QtWidgets.QLabel()

            self.grid_resources.addWidget(label, count, 0)
            self.grid_resources.addWidget(edit, count, 1)
        
            self.resources.append(edit)
            label.setText(f"Resource #{len(self.resources)}")

            self.update_resourcescount()

    def changecolorpastlimit(self):
        count = len(self.lineedit_description.text())
        if count > 50:
            self.lineedit_description.setStyleSheet("color: #F2C12E;")
        else:
            self.lineedit_description.setStyleSheet("color: black;")

    def set_markdown(self):
        text = self.textedit_edit.toPlainText()
        self.textedit_preview.setMarkdown(text)
        
    def remove_resource(self):
        count = self.grid_resources.count()
        if count > 2:
            label = self.grid_resources.itemAt(count - 2)
            field = self.grid_resources.itemAt(count - 1)

            self.grid_resources.removeWidget(label.widget())
            self.grid_resources.removeWidget(field.widget())

            self.resources.pop()
            self.update_resourcescount()

    def update_resourcescount(self):
        if self.grid_resources.count() > 1:
            update = f"Number of Resources: {len(self.resources)}"
            self.label_numofresources.setText(update)

    def export(self):
        tags = self.lineedit_tags.text().split(",")

        resources = [i.text() for i in self.resources]

        data = {"source": self.lineedit_source.text(),
                "note": self.combobox_note.currentText(),
                "tags": tags,
                "grok": self.slider_grokscore.value() + 1,
                "resources": resources,
                "title": self.lineedit_description.text(),
                "contents": self.textedit_edit.toPlainText()}

        ExportMD(data).export()

    def reset_ui(self):
        self.textedit_edit.clear()
        self.textedit_preview.clear()
        self.lineedit_description.clear()
        self.lineedit_tags.clear()
        
        # Deal with the resources
        num = self.grid_resources.count()
        while (num > 1):
            self.remove_resource()
            num -= 1
            
        self.resources[0].clear()

