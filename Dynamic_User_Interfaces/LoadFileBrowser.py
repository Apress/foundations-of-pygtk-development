#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SignalHandlers():

    def on_back_clicked(self, button ):
        pass

    def on_forward_clicked(self, button ):
        pass

    def on_up_clicked(self, button ):
        pass

    def on_refresh_clicked(self, button ):
        pass

    def on_home_clicked(self, button ):
        pass

    def on_delete_clicked(self, button ):
        pass

    def on_info_clicked(self, button ):
        pass

    def on_go_clicked(self, button ):
        pass

    def on_location_activate(self, button ):
        pass

    def on_row_activated(self, button ):
        pass

    def on_window_destroy(self, button ):
        pass

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            builder = Gtk.Builder()
            builder.add_from_file("./FileBrowser.glade")
            self.window = builder.get_object("main_window")
            self.add_window(self.window)
            builder.connect_signals(SignalHandlers())
            self.add_window(self.window)
        self.window.show_all()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
