#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        integer = Gtk.Adjustment(5.0, 0.0, 10.0, 1.0, 2.0, 2.0)
        float_pt = Gtk.Adjustment(5.0, 0.0, 1.0, 0.1, 0.5, 0.5)
        spin_int = Gtk.SpinButton()
        spin_int.set_adjustment(integer)
        spin_int.set_increments(1.0, 0)
        spin_int.set_digits(0)
        spin_float = Gtk.SpinButton()
        spin_float.set_adjustment(float_pt)
        spin_float.set_increments(0.1, 0)
        spin_float.set_digits(1)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(spin_int, False, False, 5)
        vbox.pack_start(spin_float, False, False, 5)
        self.add(vbox)
        self.set_size_request(180, 100)
        self.show_all()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Spin Buttons")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
