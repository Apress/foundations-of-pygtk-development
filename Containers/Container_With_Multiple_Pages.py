#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(250, 100)
        notebook = Gtk.Notebook.new()
        label1 = Gtk.Label.new("Page 1")
        label2 = Gtk.Label.new("Page 2")
        child1 = Gtk.Label.new("Go to page 2 to find the answer.")
        child2 = Gtk.Label.new("Go to page 1 to find the answer.")
        notebook.append_page(child1, label1)
        notebook.append_page(child2, label2)

        notebook.set_tab_pos(Gtk.PositionType.BOTTOM)
        self.add(notebook)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Notebook")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
