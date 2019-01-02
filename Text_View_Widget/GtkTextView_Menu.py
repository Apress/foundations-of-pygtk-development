#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        textview = Gtk.TextView.new()
        cut = Gtk.Button.new_with_label("Cut")
        copy = Gtk.Button.new_with_label("Copy")
        paste = Gtk.Button.new_with_label("Paste")
        cut.connect("clicked", self.on_cut_clicked, textview)
        copy.connect("clicked", self.on_copy_clicked, textview)
        paste.connect("clicked", self.on_paste_clicked, textview)
        scrolled_win = Gtk.ScrolledWindow.new(None, None)
        scrolled_win.set_size_request(300, 200)
        scrolled_win.add(textview)
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        hbox.pack_start(cut, True, True, 0)
        hbox.pack_start(copy, True, True, 0)
        hbox.pack_start(paste, True, True, 0)
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        vbox.pack_start(scrolled_win, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)
        self.add(vbox)

    def on_cut_clicked(self, button, textview):
        clipboard = Gtk.Clipboard.get(Gdk.Atom.intern("CLIPBOARD", False))
        buffer = textview.get_buffer()
        buffer.cut_clipboard(clipboard, True)

    def on_copy_clicked(self, button, textview):
        clipboard = Gtk.Clipboard.get(Gdk.Atom.intern("CLIPBOARD", False))
        buffer = textview.get_buffer()
        buffer.copy_clipboard(clipboard)

    def on_paste_clicked(self, button, textview):
        clipboard = Gtk.Clipboard.get(Gdk.Atom.intern("CLIPBOARD", False))
        buffer = textview.get_buffer()
        buffer.paste_clipboard (clipboard, None, True)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Cut, Copy & Paste")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
