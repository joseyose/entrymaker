from ui.widget import Ui_Form
from PyQt5 import QtWidgets, QtGui  # , QtCore, QtGui
from pathlib import Path
from exportmd import ExportMD

WORDWRAP = 80


class Window(QtWidgets.QDialog, Ui_Form):
    def __init__(self):
        super(Window, self).__init__()

        self._setupUI()
        self.setWindowTitle("Entry Maker :D v0.1.0")
        self.configure_ui()

    def _setupUI(self):
        self.setupUi(self)
        self.resources = [self.lineedit_resource1]
        # self.resources.append(self.lineedit_resource1)
        # self.label_numofresources.setText(
        #     f"Number of Resources: {len(self.resources)}")
        self.update_resourcescount()

    def configure_ui(self):
        # BUTTONS CLICKED
        self.button_filedialog.clicked.connect(self.load_filedialog)
        self.button_add.clicked.connect(self.add_resource)
        self.button_remove.clicked.connect(self.remove_resource)
        self.button_export.clicked.connect(self.export)

        self.combobox_note.setEnabled(False)
        self.lineedit_description.textChanged.connect(
            self.changecolorpastlimit)
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
        # Good god this is a much shorter version of this, but it's basically
        # doing the same thing :)
        # md = Path(self.lineedit_source.text()).rglob("*.md")
        notes = [""]

        for path in Path(self.lineedit_source.text()).rglob("*.md"):
            path = str(path).split("\\")[-1].split(".")[0]
            notes.append(path)

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
            # count += 1

            self.resources.append(edit)
            # print(self.resources)

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
        # I don't have this working yet
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
        # for i in self.resources:
        #     print(i.text())

        # a = self.slider_grokscore.value()
        # print(a)
        tags = self.lineedit_tags.text().split(",")
        # print(tags)

        resources = [i.text() for i in self.resources]

        data = {"source": self.lineedit_source.text(),
                "note": self.combobox_note.currentText(),
                "tags": tags,
                "grok": self.slider_grokscore.value() + 1,
                "resources": resources,
                "title": self.lineedit_description.text(),
                "contents": self.textedit_edit.toPlainText()}

        ExportMD(data).export()

        # print(self.textedit_edit.toPlainText())

        # print(self.combobox_note.currentText())