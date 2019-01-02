#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pathlib import Path

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        label = Gtk.Label("")
        chooser1 = Gtk.FileChooserButton("Choose a Folder.", 
                                         Gtk.FileChooserAction.SELECT_FOLDER)
        chooser2 = Gtk.FileChooserButton("Choose a Folder.", 
                                         Gtk.FileChooserAction.OPEN)
        chooser1.connect("selection_changed", self.on_folder_changed, 
                         chooser2)
        chooser2.connect("selection_changed", self.on_file_changed, label)
        chooser1.set_current_folder(str(Path.home()))
        chooser2.set_current_folder(str(Path.home()))
        filter1 = Gtk.FileFilter()
        filter2 = Gtk.FileFilter()
        filter1.set_name("Image Files")
        filter2.set_name("All Files")
        filter1.add_pattern("*.png")
        filter1.add_pattern("*.jpg")
        filter1.add_pattern("*.gif")
        filter2.add_pattern("*")
        chooser2.add_filter(filter1)
        chooser2.add_filter(filter2)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(chooser1, False, False, 0)
        vbox.pack_start(chooser2, False, False, 0)
        vbox.pack_start(label, False, False, 0)
        self.add(vbox)
        self.set_size_request(240, -1)

    def on_folder_changed(self, chooser1, chooser2):
        folder = chooser1.get_filename()
        chooser2.set_current_folder(folder)

    def on_file_changed(self, chooser2, label):
        file = chooser2.get_filename()
        label.set_text(file)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="File Chooser Button")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
