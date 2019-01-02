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
        button = Gtk.Button.new_with_label("Run Font Selection Dialog")
        button.connect("clicked", self.on_run_font_selection_dialog)
        self.add(button)

    def on_run_font_selection_dialog(self, button):
        dialog = Gtk.FontSelectionDialog(title="Choose a Font",
                                         buttons=("Apply", Gtk.ResponseType.APPLY),
                                         parent=self)
        dialog.set_preview_text("GTK+ 3 Development With Python")
        dialog.connect("response", self.on_dialog_response)
#        dialog.show_all()
        dialog.run()

    def on_dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.OK or response == Gtk.ResponseType.APPLY:
            font = dialog.get_font_name()
            message = Gtk.MessageDialog(title="Selected Font",
                                        flags=Gtk.DialogFlags.MODAL,
                                        type=Gtk.MessageType.INFO,
                                        text=font,
                                        buttons=("Ok", Gtk.ResponseType.OK),
                                        parent=dialog);
            message.run()
            message.destroy()
            if response == Gtk.ResponseType.OK:
                dialog.destroy()
        else:
            dialog.destroy()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Font Selection Dialog")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
