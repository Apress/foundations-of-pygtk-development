#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(-1, -1)
        textview = Gtk.TextView.new()
        entry = Gtk.Entry.new()
        insert_button = Gtk.Button.new_with_label("Insert Text")
        retrieve = Gtk.Button.new_with_label("Get Text")
        insert_button.connect("clicked", self.on_insert_text, (entry, textview))
        retrieve.connect("clicked", self.on_retrieve_text, (entry, textview))
        scrolled_win = Gtk.ScrolledWindow.new(None, None)
        scrolled_win.add(textview)
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        hbox.pack_start(entry, True, True, 0)
        hbox.pack_start(insert_button, True, True, 0)
        hbox.pack_start(retrieve, True, True, 0)
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        vbox.pack_start(scrolled_win, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)
        self.add(vbox)
        self.show_all()

    def on_insert_text(self, button, w):
        buffer = w[1].get_buffer()
        text = w[0].get_text()
        mark = buffer.get_insert()
        iter = buffer.get_iter_at_mark(mark)
        buffer.insert(iter, text, len(text))

    def on_retrieve_text(self, button, w):
        buffer = w[1].get_buffer()
        (start, end) = buffer.get_selection_bounds()
        text = buffer.get_text(start, end, False)
        print(text)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Text Iterators")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
