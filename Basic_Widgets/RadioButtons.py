#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        radio1 = Gtk.RadioButton.new_with_label(None, "I want to be clicked!")
        radio2 = Gtk.RadioButton.new_with_label_from_widget(radio1, "Click me instead!")
        radio3 = Gtk.RadioButton.new_with_label_from_widget(radio1, "No! Click me!")
        radio4 = Gtk.RadioButton.new_with_label_from_widget(radio3, "No! Click me instead!")
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(radio1, False, False, 0)
        vbox.pack_start(radio2, False, False, 0)
        vbox.pack_start(radio3, False, False, 0)
        vbox.pack_start(radio4, False, False, 0)
        self.add(vbox)
        self.show_all()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Radio Buttons")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
