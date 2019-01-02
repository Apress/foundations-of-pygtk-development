#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        toggle1 = Gtk.ToggleButton.new_with_mnemonic("_Deactivate the other one!")
        toggle2 = Gtk.ToggleButton.new_with_mnemonic("_No! Deactivate that one!")
        toggle1.connect("toggled", self.on_button_toggled, toggle2)
        toggle2.connect("toggled", self.on_button_toggled, toggle1)
        vbox.pack_start(toggle1, True, True, 1)
        vbox.pack_start(toggle2, True, True, 1)
        self.add(vbox)

    def on_button_toggled(self, toggle, other_toggle):
        if (Gtk.ToggleButton.get_active(toggle)):
            other_toggle.set_sensitive(False)
        else:
            other_toggle.set_sensitive(True)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Toggle Buttons")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
