#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        toolbar = Gtk.Toolbar.new()
        entry = Gtk.Entry.new()
        vbox.pack_start(toolbar, True, False, 0)
        vbox.pack_start(entry, True, False, 0)
        self.create_toolbar(toolbar, entry)
        self.add(vbox)
        self.set_size_request(310, 75)

    def create_toolbar(self, toolbar, entry):
        icon_theme = Gtk.IconTheme.get_default()
        icon = icon_theme.load_icon("edit-cut", -1, 
                                    Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        cut = Gtk.ToolButton.new(image, "Cut")
        icon = icon_theme.load_icon("edit-copy", -1, 
                                    Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        copy = Gtk.ToolButton.new(image, "Copy")
        icon = icon_theme.load_icon("edit-paste", -1, 
                                    Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        paste = Gtk.ToolButton.new(image, "Paste")
        icon = icon_theme.load_icon("edit-select-all", -1, 
                                    Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        selectall = Gtk.ToolButton.new(image, "Select All")
        separator = Gtk.SeparatorToolItem.new()
        toolbar.set_show_arrow(True)
        toolbar.set_style(Gtk.ToolbarStyle.BOTH)
        toolbar.insert(cut, 0)
        toolbar.insert(copy, 1)
        toolbar.insert(paste, 2)
        toolbar.insert(separator, 3)
        toolbar.insert(selectall, 4)
        cut.connect("clicked", self.cut_clipboard, entry)
        copy.connect("clicked", self.copy_clipboard, entry)
        paste.connect("clicked", self.paste_clipboard, entry)
        selectall.connect("clicked", self.select_all, entry)
    
    def cut_clipboard(self, button, entry):
        entry.cut_clipboard()

    def copy_clipboard(self, button, entry):
        entry.copy_clipboard()

    def paste_clipboard(self, button, entry):
        entry.paste_clipboard()

    def select_all(self, button, entry):
        entry.select_region(0, -1)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, 
                                    title="Toolbar")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
