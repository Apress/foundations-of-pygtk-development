#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(200, 100)
        button = Gtk.Button.new_with_label("Open file(s) ...")
        button.connect("clicked", self.on_button_clicked, self)
        self.add(button)

    def on_button_clicked(self, button, parentwin):
        dialog = Gtk.FileChooserDialog(title="Open file(s) ...",
                                       parent=parentwin,
                                       action=Gtk.FileChooserAction.OPEN,
                                       buttons=("_Cancel", 
                                                Gtk.ResponseType.CANCEL,
                                        "_Open", Gtk.ResponseType.ACCEPT))
        dialog.set_select_multiple(True)
        response = dialog.run()
        if response == Gtk.ResponseType.ACCEPT:
            filenames = dialog.get_filenames()
            i = 0
            while i < len(filenames):
                file = filenames[i]
                print(file + " was selected.")
                i += 1
        dialog.destroy()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, 
                                    title="Open Nultiple Files")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
