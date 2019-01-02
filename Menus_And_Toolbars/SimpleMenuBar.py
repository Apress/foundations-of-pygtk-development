#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_request(250, -1)
        menubar = Gtk.MenuBar.new()
        file = Gtk.MenuItem.new_with_label("File")
        edit = Gtk.MenuItem.new_with_label("Edit")
        help = Gtk.MenuItem.new_with_label("Help")
        filemenu = Gtk.Menu.new()
        editmenu = Gtk.Menu.new()
        helpmenu = Gtk.Menu.new()
        file.set_submenu(filemenu)
        edit.set_submenu(editmenu)
        help.set_submenu(helpmenu)
        menubar.append(file)
        menubar.append(edit)
        menubar.append(help)
        # Create the File menu content.
        new = Gtk.MenuItem.new_with_label("New")
        open = Gtk.MenuItem.new_with_label("Open")
        filemenu.append(new)
        filemenu.append(open)
        # Create the Edit menu content.
        cut = Gtk.MenuItem.new_with_label("Cut")
        copy = Gtk.MenuItem.new_with_label("Copy")
        paste = Gtk.MenuItem.new_with_label("Paste")
        editmenu.append(cut)
        editmenu.append(copy) 
        editmenu.append(paste)
        # Create the Help menu content.
        contents = Gtk.MenuItem.new_with_label("Help")
        about = Gtk.MenuItem.new_with_label("About")
        helpmenu.append(contents)
        helpmenu.append(about)
        self.add(menubar)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, 
                                    title="Menu Bars")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
