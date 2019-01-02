#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        check1 = Gtk.CheckButton.new_with_label("I am the main option.")
        check2 = Gtk.CheckButton.new_with_label("I rely on the other guy.")
        check2.set_sensitive(False)
        check1.connect("toggled", self.on_button_checked, check2)
        closebutton = Gtk.Button.new_with_mnemonic("_Close")
        closebutton.connect("clicked", self.on_button_close_clicked)
        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(check1, False, True, 0)
        vbox.pack_start(check2, False, True, 0)
        vbox.pack_start(closebutton, False, True, 0)
        self.add(vbox)

    def on_button_checked(self, check1, check2):
        if check1.get_active():
            check2.set_sensitive(True);
        else:
            check2.set_sensitive(False)

    def on_button_close_clicked(self, button):
        self.destroy()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Check Buttons")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
