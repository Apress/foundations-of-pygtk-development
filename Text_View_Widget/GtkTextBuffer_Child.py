#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(25)
        self.set_border_width(10)
        self.set_size_request(250, 100)
        textview = Gtk.TextView.new()
        buffer = textview.get_buffer()
        text = "\n Click  to exit!"
        buffer.set_text(text, len(text))
        iter = buffer.get_iter_at_offset(8)
        anchor = buffer.create_child_anchor(iter)
        button = Gtk.Button.new_with_label("the button")
        button.connect("clicked", self.on_button_clicked)
        button.set_relief(Gtk.ReliefStyle.NORMAL)
        textview.add_child_at_anchor(button, anchor)
        scrolled_win = Gtk.ScrolledWindow.new(None, None)
        scrolled_win.add(textview)
        scrolled_win.set_policy(Gtk.PolicyType.AUTOMATIC, 
                                Gtk.PolicyType.ALWAYS)
        self.add(scrolled_win)

    def on_button_clicked(self, button):
        self.destroy()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Child Widgets")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
