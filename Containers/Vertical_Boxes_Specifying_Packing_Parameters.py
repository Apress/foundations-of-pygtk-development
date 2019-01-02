#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

names = ["Andrew", "Joe", "Samantha", "Jonathan"]

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        for name in names:
            button = Gtk.Button.new_with_label(name)
            vbox.pack_end(button, False, False, 5)
            button.connect("clicked", self.on_button_clicked)
            button.set_relief(Gtk.ReliefStyle.NORMAL)
        self.set_border_width(10)
        self.set_size_request(200, -1)
        self.add(vbox)
        self.show_all()

    def on_button_clicked(self, widget):
        self.destroy()


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Boxes")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
