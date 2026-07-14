"""
Hospital Records — a KivyMD app for searching patients/stays,
viewing full clinical details, adding new records, and exporting
results to Excel. Runs on Android (via Buildozer) or desktop.
"""

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel

import db


class PatternPad(MDBoxLayout):
    """A 3x3 tap-in-sequence pattern lock pad (tap dots in order, no drag needed)."""

    def __init__(self, on_change=None, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(10), **kwargs)
        self.size_hint = (None, None)
        self.size = (dp(220), dp(260))
        self.pos_hint = {"center_x": 0.5}
        self.on_change = on_change
        self.sequence = []
        self.dots = []

        grid = MDGridLayout(
            cols=3, spacing=dp(14), size_hint=(None, None),
            size=(dp(220), dp(220)), pos_hint={"center_x": 0.5},
        )
        for i in range(9):
            btn = MDIconButton(
                icon="circle-outline", icon_size="36sp",
                on_release=lambda x, idx=i: self.tap(idx),
            )
            self.dots.append(btn)
            grid.add_widget(btn)
        self.add_widget(grid)

        self.add_widget(MDFlatButton(text="CLEAR", pos_hint={"center_x": 0.5}, on_release=lambda x: self.clear()))

    def tap(self, idx):
        if idx not in self.sequence:
            self.sequence.append(idx)
            self.dots[idx].icon = "circle"
            if self.on_change:
                self.on_change(self.sequence)

    def clear(self):
        self.sequence = []
        for d in self.dots:
            d.icon = "circle-outline"
        if self.on_change:
            self.on_change(self.sequence)

    def get_pattern_str(self):
        return "-".join(str(i) for i in self.sequence)

KV = """
#:import dp kivy.metrics.dp

ScreenManager:
    LockScreen:
    SearchScreen:
    DetailScreen:
    AddScreen:

<LockScreen@MDScreen>:
    name: "lock"
    md_bg_color: app.theme_cls.primary_color

    MDBoxLayout:
        orientation: "vertical"
        padding: dp(32)
        spacing: dp(16)
        pos_hint: {"center_y": 0.5}

        MDIcon:
            icon: "lock"
            halign: "center"
            font_size: "48sp"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDLabel:
            id: lock_title
            text: "Enter PIN"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: "H6"

        MDBoxLayout:
            id: lock_container
            orientation: "vertical"
            spacing: dp(12)
            adaptive_height: True
            pos_hint: {"center_x": 0.5}

        MDRaisedButton:
            id: unlock_btn
            text: "UNLOCK"
            pos_hint: {"center_x": 0.5}
            on_release: app.attempt_unlock()

<SearchScreen@MDScreen>:
    name: "search"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Hospital Records"
            elevation: 4
            md_bg_color: app.theme_cls.primary_color
            right_action_items: [["lock-reset", lambda x: app.open_change_lock()], ["file-excel", lambda x: app.export_all()], ["plus", lambda x: app.goto_add()]]

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(16), dp(12), dp(16), dp(8)
            spacing: dp(8)
            adaptive_height: True

            MDTextField:
                id: search_field
                hint_text: "Search by name or diagnosis"
                icon_right: "magnify"
                on_text_validate: app.do_search(self.text)

            MDRaisedButton:
                text: "SEARCH"
                pos_hint: {"center_x": 0.5}
                on_release: app.do_search(search_field.text)

        ScrollView:
            MDList:
                id: results_list
                padding: dp(4)

<DetailScreen@MDScreen>:
    name: "detail"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Stay Details"
            elevation: 4
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [["arrow-left", lambda x: app.goto_search()]]
            right_action_items: [["file-excel-box", lambda x: app.export_current()]]

        ScrollView:
            MDBoxLayout:
                id: detail_box
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(12)
                adaptive_height: True

<AddScreen@MDScreen>:
    name: "add"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Add Patient Record"
            elevation: 4
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [["arrow-left", lambda x: app.goto_search()]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(10)
                adaptive_height: True

                MDTextField:
                    id: f_first
                    hint_text: "First name"
                MDTextField:
                    id: f_last
                    hint_text: "Last name"
                MDTextField:
                    id: f_dob
                    hint_text: "DOB (YYYY-MM-DD)"
                MDTextField:
                    id: f_mrn
                    hint_text: "MRN (unique)"
                MDTextField:
                    id: f_diag
                    hint_text: "Primary diagnosis"
                MDTextField:
                    id: f_notes
                    hint_text: "Daily progress notes"
                    multiline: True
                MDTextField:
                    id: f_course
                    hint_text: "Hospital course"
                    multiline: True
                MDTextField:
                    id: f_treatment
                    hint_text: "Treatment given"
                    multiline: True
                MDTextField:
                    id: f_condition
                    hint_text: "Discharge condition"
                    multiline: True
                MDTextField:
                    id: f_advice
                    hint_text: "Discharge advice"
                    multiline: True

                MDRaisedButton:
                    text: "SAVE RECORD"
                    pos_hint: {"center_x": 0.5}
                    on_release: app.save_new_record()
"""


class LockScreen(MDScreen):
    pass


class SearchScreen(MDScreen):
    pass


class DetailScreen(MDScreen):
    pass


class AddScreen(MDScreen):
    pass


class HospitalApp(MDApp):
    current_stay_id = None
    current_results = []

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        self.title = "Hospital Records"
        return Builder.load_string(KV)

    def on_start(self):
        db.init_db()
        self.render_lock_screen()
        self.root.current = "lock"

    # ---------- Lock screen (PIN or pattern) ----------
    def render_lock_screen(self):
        lock = db.get_lock()
        ids = self.root.get_screen("lock").ids
        ids.lock_container.clear_widgets()

        if lock["type"] == "pin":
            ids.lock_title.text = "Enter PIN"
            self._unlock_widget = MDTextField(
                hint_text="PIN", password=True, input_filter="int", halign="center",
                text_color_normal=(1, 1, 1, 1), hint_text_color_normal=(1, 1, 1, 1),
                line_color_normal=(1, 1, 1, 1), size_hint_x=None, width=dp(220),
                pos_hint={"center_x": 0.5},
                on_text_validate=lambda inst: self.attempt_unlock(),
            )
        else:
            ids.lock_title.text = "Draw your pattern"
            self._unlock_widget = PatternPad()
        ids.lock_container.add_widget(self._unlock_widget)

    def attempt_unlock(self):
        lock = db.get_lock()
        entered = self._unlock_widget.text if lock["type"] == "pin" else self._unlock_widget.get_pattern_str()
        if entered and entered == lock["value"]:
            self.root.current = "search"
            self.render_lock_screen()  # reset for next time
        else:
            Snackbar(text="Incorrect " + ("PIN" if lock["type"] == "pin" else "pattern")).open()
            self.render_lock_screen()

    # ---------- Change lock (from search screen) ----------
    def open_change_lock(self):
        self._change_stage = "verify"
        self._change_box = MDBoxLayout(orientation="vertical", spacing=dp(12), size_hint_y=None, height=dp(260))
        self._render_verify_stage()
        self._change_dialog = MDDialog(
            title="Change Lock",
            type="custom",
            content_cls=self._change_box,
            buttons=[MDFlatButton(text="CANCEL", on_release=lambda x: self._change_dialog.dismiss())],
        )
        self._change_dialog.open()

    def _render_verify_stage(self):
        self._change_box.clear_widgets()
        lock = db.get_lock()
        label = "PIN" if lock["type"] == "pin" else "pattern"
        self._change_box.add_widget(MDLabel(text=f"Verify your current {label}", adaptive_height=True))
        if lock["type"] == "pin":
            self._verify_widget = MDTextField(hint_text="Current PIN", password=True, input_filter="int")
        else:
            self._verify_widget = PatternPad()
        self._change_box.add_widget(self._verify_widget)
        self._change_box.add_widget(
            MDRaisedButton(text="VERIFY", pos_hint={"center_x": 0.5}, on_release=lambda x: self._verify_current())
        )

    def _verify_current(self):
        lock = db.get_lock()
        entered = self._verify_widget.text if lock["type"] == "pin" else self._verify_widget.get_pattern_str()
        if entered != lock["value"]:
            Snackbar(text="Verification failed").open()
            return
        self._render_choose_type_stage()

    def _render_choose_type_stage(self):
        self._change_box.clear_widgets()
        self._change_box.add_widget(MDLabel(text="Choose new lock type", adaptive_height=True))
        row = MDBoxLayout(spacing=dp(12), adaptive_height=True, pos_hint={"center_x": 0.5})
        row.add_widget(MDRaisedButton(text="USE PIN", on_release=lambda x: self._render_set_stage("pin")))
        row.add_widget(MDRaisedButton(text="USE PATTERN", on_release=lambda x: self._render_set_stage("pattern")))
        self._change_box.add_widget(row)

    def _render_set_stage(self, kind):
        self._change_box.clear_widgets()
        if kind == "pin":
            self._change_box.add_widget(MDLabel(text="Enter new PIN (min 4 digits)", adaptive_height=True))
            self._new_widget = MDTextField(hint_text="New PIN", password=True, input_filter="int")
        else:
            self._change_box.add_widget(MDLabel(text="Draw new pattern (connect 4+ dots)", adaptive_height=True))
            self._new_widget = PatternPad()
        self._change_box.add_widget(self._new_widget)
        self._change_box.add_widget(
            MDRaisedButton(text="SAVE", pos_hint={"center_x": 0.5}, on_release=lambda x: self._save_new_lock(kind))
        )

    def _save_new_lock(self, kind):
        if kind == "pin":
            val = self._new_widget.text
            if len(val) < 4:
                Snackbar(text="PIN must be at least 4 digits").open()
                return
        else:
            if len(self._new_widget.sequence) < 4:
                Snackbar(text="Pattern must connect at least 4 dots").open()
                return
            val = self._new_widget.get_pattern_str()

        db.set_lock(kind, val)
        self._change_dialog.dismiss()
        Snackbar(text=f"Lock updated to {kind.upper()}").open()

    # ---------- Search screen ----------
    def do_search(self, query):
        query = (query or "").strip()
        results_list = self.root.get_screen("search").ids.results_list
        results_list.clear_widgets()

        if not query:
            Snackbar(text="Type a name or diagnosis to search").open()
            return

        rows = db.search_patients(query)
        self.current_results = rows

        if not rows:
            Snackbar(text="No matching records found").open()
            return

        for r in rows:
            subtitle = f"{r['primary_diagnosis']}  •  MRN {r['mrn']}"
            item = OneLineAvatarIconListItem(
                text=f"{r['first_name']} {r['last_name']}",
                on_release=lambda x, sid=r["stay_id"]: self.goto_detail(sid),
            )
            results_list.add_widget(item)

    def goto_add(self):
        self.root.current = "add"

    def goto_search(self):
        self.root.current = "search"

    def export_all(self):
        if not self.current_results:
            Snackbar(text="Run a search first, then export").open()
            return
        path = db.export_rows_to_excel(self.current_results)
        Snackbar(text=f"Exported to {path}").open()

    # ---------- Detail screen ----------
    def goto_detail(self, stay_id):
        self.current_stay_id = stay_id
        detail = db.get_stay_detail(stay_id)
        box = self.root.get_screen("detail").ids.detail_box
        box.clear_widgets()

        if not detail:
            return

        def add_field(label, value):
            from kivymd.uix.label import MDLabel
            box.add_widget(MDLabel(
                text=f"[b]{label}[/b]", markup=True, adaptive_height=True,
                theme_text_color="Primary", font_style="Subtitle1",
            ))
            box.add_widget(MDLabel(
                text=value or "—", adaptive_height=True,
                theme_text_color="Secondary",
            ))

        add_field("Patient", f"{detail['first_name']} {detail['last_name']}  (MRN {detail['mrn']})")
        add_field("DOB", detail["dob"])
        add_field("Admission", detail["admission_date"])
        add_field("Discharge", detail["discharge_date"])
        add_field("Primary Diagnosis", detail["primary_diagnosis"])
        add_field("Daily Progress Notes", detail["daily_progress_notes"])
        add_field("Hospital Course", detail["hospital_course"])
        add_field("Treatment Given", detail["treatment_given"])
        add_field("Discharge Condition", detail["discharge_condition"])
        add_field("Discharge Advice", detail["discharge_advice"])

        self.root.current = "detail"

    def export_current(self):
        if not self.current_stay_id:
            return
        detail = db.get_stay_detail(self.current_stay_id)
        row = {
            "patient_id": None, "first_name": detail["first_name"],
            "last_name": detail["last_name"], "mrn": detail["mrn"], "dob": detail["dob"],
            "stay_id": detail["stay_id"], "primary_diagnosis": detail["primary_diagnosis"],
            "admission_date": detail["admission_date"], "discharge_date": detail["discharge_date"],
        }
        path = db.export_rows_to_excel([row], filename=f"stay_{self.current_stay_id}.xlsx")
        Snackbar(text=f"Exported to {path}").open()

    # ---------- Add screen ----------
    def save_new_record(self):
        ids = self.root.get_screen("add").ids
        data = {
            "first_name": ids.f_first.text.strip(),
            "last_name": ids.f_last.text.strip(),
            "dob": ids.f_dob.text.strip(),
            "mrn": ids.f_mrn.text.strip(),
            "primary_diagnosis": ids.f_diag.text.strip(),
            "daily_progress_notes": ids.f_notes.text.strip(),
            "hospital_course": ids.f_course.text.strip(),
            "treatment_given": ids.f_treatment.text.strip(),
            "discharge_condition": ids.f_condition.text.strip(),
            "discharge_advice": ids.f_advice.text.strip(),
        }
        if not (data["first_name"] and data["last_name"] and data["mrn"] and data["primary_diagnosis"]):
            Snackbar(text="First name, last name, MRN and diagnosis are required").open()
            return
        try:
            db.add_patient_and_stay(data)
        except Exception as e:
            Snackbar(text=f"Error: {e}").open()
            return

        for field in ids.values():
            if hasattr(field, "text"):
                field.text = ""
        Snackbar(text="Record saved").open()
        self.goto_search()


if __name__ == "__main__":
    HospitalApp().run()
