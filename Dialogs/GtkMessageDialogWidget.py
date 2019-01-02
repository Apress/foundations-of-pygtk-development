#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        button = Gtk.Button.new_with_mnemonic("_Click Me")
        button.connect("clicked", self.on_button_clicked, self)
        self.add(button)
        self.set_size_request(150, 50)

    def on_button_clicked(self, button, parent):
        dialog = Gtk.MessageDialog(type=Gtk.MessageType.INFO, parent=parent,
                                   flags=Gtk.DialogFlags.MODAL,
                                   buttons=("Ok", Gtk.ResponseType.OK),
                                   text="The button was clicked.",
                                   title="Information")
        dialog.run()
        dialog.destroy()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Dialogs")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
