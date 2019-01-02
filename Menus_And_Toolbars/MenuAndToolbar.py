#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def change_label(self):
        pass

    def maximize(self):
        pass

    def about(self):
        pass

    def quit(self):
        self.destroy()

    def newstandard(self):
        pass

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, 
                                    title="Hello World!")
            builder = Gtk.Builder()
            builder.add_from_file("./Menu_XML_File.ui")
            builder.add_from_file("./Toolbar_UI_File.xml")
            builder.connect_signals(self.window)
            self.set_menubar(builder.get_object("menubar"))
            self.window.add(builder.get_object("toolbar"))
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
