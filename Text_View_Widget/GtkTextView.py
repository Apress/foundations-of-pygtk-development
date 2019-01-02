#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(250, 150)
        textview = Gtk.TextView.new()
        buffer = textview.get_buffer()
        text = "Your 1st GtkTextView widget!"
        buffer.set_text(text, len(text))
        scrolled_win = Gtk.ScrolledWindow.new (None, None)
        scrolled_win.add(textview)
        self.add(scrolled_win)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Text Views")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
