#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        hpaned = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        button1 = Gtk.Button.new_with_label("Resize")
        button2 = Gtk.Button.new_with_label("Me!")
        button1.connect("clicked", self.on_button_clicked)
        button2.connect("clicked", self.on_button_clicked)
        hpaned.add1(button1)
        hpaned.add2(button2)
        self.add(hpaned)
        self.set_size_request(225, 150)
        self.show_all()

    def on_button_clicked(self, button):
        self.destroy()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Panes")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
