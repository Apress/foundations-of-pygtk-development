#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
from pathlib import Path

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)

        adj1 = Gtk.Adjustment.new(0.5, 0.0, 1.0, 0.01, 0.02, 0.02)
        adj2 = Gtk.Adjustment.new(0.5, 0.0, 1.02, 0.01, 0.02, 0.02)

        spin = Gtk.SpinButton.new(adj1, 0.01, 2)
        scale = Gtk.Scale.new(Gtk.Orientation.HORIZONTAL, adj2)
        check = Gtk.CheckButton.new_with_label("Synchronize Spin and Scale")

        check.set_active(True)
        scale.set_digits(2)
        scale.set_value_pos(Gtk.PositionType.RIGHT)

        spin.connect("value_changed", self.on_spin_value_changed, spin, scale, check)
        scale.connect("value_changed", self.on_scale_value_changed, spin, scale, check)

        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5);
        vbox.pack_start(spin, False, True, 0)
        vbox.pack_start(scale, False, True, 0);
        vbox.pack_start(check, False, True, 0);

        self.add(vbox)


    def on_spin_value_changed(self, widget, spin, scale, check):
        val1 = spin.get_value()
        val2 = scale.get_value()

        if (check.get_active() and val1 != val2):
            if isinstance(widget, Gtk.SpinButton):
                scale.set_value(val1)
            else:
                spin.set_value(val2)



class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Exercise 2")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
