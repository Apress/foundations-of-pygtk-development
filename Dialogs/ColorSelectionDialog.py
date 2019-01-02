#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

global_color = Gdk.RGBA(red=.50, green=.50, blue=.50, alpha=1.0).to_color()
global_alpha = 65535

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(200, 100)
        modal = Gtk.Button.new_with_label("Modal")
        nonmodal = Gtk.Button.new_with_label("Non-Modal")
        modal.connect("clicked", self.on_run_color_selection_dialog, 
                      self, True)
        nonmodal.connect("clicked", self.on_run_color_selection_dialog, 
                         self, False)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.pack_start(modal, False, False, 5)
        hbox.pack_start(nonmodal, False, False, 5)
        self.add(hbox)

    def on_dialog_response(self, dialog, result):
        if result == Gtk.ResponseType.OK:
            colorsel = dialog.get_color_selection()
            alpha = colorsel.get_current_alpha()
            color = colorsel.get_current_color()
            print(color.to_string())
            global_color = color
            global_alpha = alpha
        dialog.destroy()

    def on_run_color_selection_dialog(self, button, window, domodal):
        if domodal:
            title = ("Choose Color -- Modal")
        else:
            title = ("Choose Color -- Non-Modal")
        dialog = Gtk.ColorSelectionDialog(title=title, parent=window, modal=domodal)
        colorsel = dialog.get_color_selection()
        colorsel.set_has_opacity_control(True)
        colorsel.set_current_color(global_color)
        dialog.connect("response", self.on_dialog_response)
        dialog.show_all()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Color Selection Dialog")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
