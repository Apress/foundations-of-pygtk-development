#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(250, -1)
        scale_int = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 
                                             0.0, 10.0, 1.0)
        scale_float = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 
                                               0.0, 1.0, 0.1)
        scale_int.set_digits(0)
        scale_float.set_digits(1)
        scale_int.set_value_pos(Gtk.PositionType.RIGHT)
        scale_float.set_value_pos(Gtk.PositionType.LEFT)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(scale_int, False, False, 5)
        vbox.pack_start(scale_float, False, False, 5)
        self.add(vbox)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Scales")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
