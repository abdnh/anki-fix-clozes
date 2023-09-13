import functools

from aqt import gui_hooks, mw
from aqt.browser import Browser
from aqt.qt import *

from .gui.field_selector import FieldSelectionDialog


def on_fix_clozes(browser: Browser) -> None:
    if not browser.selected_notes():
        return
    dialog = FieldSelectionDialog(mw, browser, browser.selected_notes())
    dialog.open()


def add_browser_menu(browser: Browser) -> None:
    action = QAction("Fix Clozes", browser)
    qconnect(action.triggered, functools.partial(on_fix_clozes, browser=browser))
    browser.form.menu_Notes.addAction(action)


gui_hooks.browser_menus_did_init.append(add_browser_menu)
