#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
from pathlib import Path

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)

        rnm = Gtk.Button.new_with_label("Apply")
        name = Gtk.Entry.new()
        rnm.set_sensitive(False)
        name.set_sensitive(False)

        file = Gtk.FileChooserButton("Choose File", Gtk.FileChooserAction.OPEN)
        file.set_current_folder(str(Path.home()))

        file.connect("selection-changed", self.on_file_changed, file, rnm,
                     name)
        rnm.connect("clicked", self.on_rename_clicked, file, rnm, name)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.pack_start(name, True, True, 0)
        hbox.pack_start(rnm, False, True, 0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(file, False, True, 0)
        vbox.pack_start(hbox, False, True, 0)

        self.add(vbox)


    def on_file_changed(self, chooser, file, rnm, name):
        fn = file.get_filename()
        mode = os.access(fn, os.W_OK)

        rnm.set_sensitive(mode)
        name.set_sensitive(mode)

    def on_rename_clicked(self, chooser, file, rnm, name):
        old = file.get_filename()
        location = file.get_current_folder()
        new = location + "/" + name.get_text()

        os.rename(old, new)
        rnm.set_sensitive(False)
        name.set_sensitive(False)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="File Chooser Button Exercise")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
