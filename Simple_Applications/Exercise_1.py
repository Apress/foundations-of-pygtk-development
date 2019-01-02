#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = Gtk.Label.new("Bunny")
        label.set_selectable(True)
        self.add(label)
        self.set_size_request(300, 100)
        self.set_resizable(False)
        self.connect("key-press-event", self.on_window_keypress, label)

    def on_window_keypress(self, window, event, label):
        tmp = label.get_text()
        label.set_text(self.get_title())
        self.set_title(tmp)
        return False

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, 
                                    title="Bugs")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
