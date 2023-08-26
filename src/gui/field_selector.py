from typing import Iterable, Optional, Sequence

from anki.collection import Collection, OpChanges, OpChangesWithCount
from anki.notes import NoteId
from anki.utils import ids2str
from aqt import *
from aqt.main import AnkiQt
from aqt.operations import CollectionOp
from aqt.utils import tooltip

from ..fixes import apply_all_fixes


class FieldSelectionDialog(QDialog):
    def __init__(
        self, mw: AnkiQt, parent: Optional[QWidget], nids: Sequence[NoteId]
    ) -> None:
        super().__init__(parent)
        self.mw = mw
        self.nids = nids
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setWindowTitle("Fix Clozes - Select Field")
        self.setMinimumSize(400, 100)
        layout = QFormLayout(self)
        label = QLabel("Field to process", self)
        self.field_combobox = field_combobox = QComboBox(self)
        field_combobox.addItems(self.get_fields())
        process_button = QPushButton("Process", self)
        qconnect(process_button.clicked, self.on_process)
        layout.addRow(label, field_combobox)
        layout.addWidget(process_button)
        self.setLayout(layout)

    def get_fields(self) -> Iterable[str]:
        fields = self.mw.col.db.list(
            "select distinct name from fields where ntid in (select mid from notes where id in %s)"
            % ids2str(self.nids)
        )
        return fields

    def on_process(self) -> None:
        field = self.field_combobox.currentText()
        self.accept()

        def op(col: Collection) -> OpChanges:
            updated_notes = []
            for nid in self.nids:
                note = col.get_note(nid)
                if field not in note:
                    continue
                fixed = apply_all_fixes(note[field])
                if note[field] != fixed:
                    note[field] = fixed
                    updated_notes.append(note)
            return OpChangesWithCount(
                changes=col.update_notes(updated_notes), count=len(updated_notes)
            )

        def on_success(changes: OpChangesWithCount) -> None:
            tooltip(
                tr.browsing_cards_updated(count=changes.count),
                parent=self.parentWidget(),
            )

        CollectionOp(self.parentWidget(), op).success(on_success).run_in_background()
