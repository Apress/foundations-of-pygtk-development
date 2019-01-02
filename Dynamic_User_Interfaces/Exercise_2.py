#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SignalHandlers():

    def on_new_clicked(self, button ):
        pass

    def on_open_clicked(self, button ):
        pass

    def on_save_clicked(self, button ):
        pass

    def on_cut_clicked(self, button ):
        pass

    def on_copy_clicked(self, button ):
        pass

    def on_paste_clicked(self, button ):
        pass

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            builder = Gtk.Builder()
            builder.add_from_file("./Exercise_2.glade")
            self.window = builder.get_object("window")
            self.add_window(self.window)
            builder.connect_signals(SignalHandlers())
            self.add_window(self.window)
        self.window.show_all()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
