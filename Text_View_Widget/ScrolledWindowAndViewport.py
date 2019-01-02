#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        grid1 = Gtk.Grid.new()
        grid2 = Gtk.Grid.new()
        grid1.set_column_homogeneous = True
        grid2.set_column_homogeneous = True
        grid1.set_row_homogeneous = True
        grid2.set_row_homogeneous = True
        grid1.set_column_spacing = 5
        grid2.set_column_spacing = 5
        grid1.set_row_spacing = 5
        grid2.set_row_spacing = 5
        i = 0
        while i < 10:
            j = 0
            while j < 10:
                button = Gtk.Button.new_with_label("Close")
                button.set_relief(Gtk.ReliefStyle.NONE)
                button.connect("clicked", self.on_button_clicked)
                grid1.attach(button, i, j, 1, 1)
                button = Gtk.Button.new_with_label("Close")
                button.set_relief(Gtk.ReliefStyle.NONE)
                button.connect("clicked", self.on_button_clicked)
                grid2.attach(button, i, j, 1, 1)
                j += 1
            i += 1
        swin = Gtk.ScrolledWindow.new(None, None)
        horizontal = swin.get_hadjustment()
        vertical = swin.get_vadjustment()
        viewport = Gtk.Viewport.new(horizontal, vertical)
        swin.set_border_width(5)
        swin.set_propagate_natural_width(True)
        swin.set_propagate_natural_height(True)
        viewport.set_border_width(5)
        swin.set_policy (Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        swin.add_with_viewport(grid1)
        viewport.add(grid2)
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        vbox.set_homogeneous = True
        vbox.pack_start(viewport, True, True, 5)
        vbox.pack_start(swin, True, True, 5)
        self.add (vbox)
        self.show_all()

    def on_button_clicked(self, button):
        self.destroy()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Scrolled Windows & Viewports")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
