#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        label = Gtk.Label("Look at the font!")
        initial_font = Pango.font_description_from_string("Sans Bold 12")
        label.modify_font(initial_font)
        button = Gtk.FontButton.new_with_font("Sans Bold 12")
        button.set_title("Choose a Font")
        button.connect("font_set", self.on_font_changed, label)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(button, False, False, 0)
        vbox.pack_start(label, False, False, 0)
        self.add(vbox)

    def on_font_changed(self, button, label):
        font = button.get_font()
        desc = Pango.font_description_from_string(font)
        buffer = "Font: " + font
        label.set_text(buffer)
        label.modify_font(desc)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Font Button")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
