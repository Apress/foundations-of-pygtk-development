#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject

clr = ( "00", "33", "66", "99", "CC", "FF" )
COLOR = 0

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(250, 175)
        treeview = Gtk.TreeView.new()
        self.setup_tree_view(treeview)
        store = Gtk.ListStore.new((GObject.TYPE_STRING, 
                                  GObject.TYPE_STRING, GObject.TYPE_STRING))
        for var1 in clr:
            for var2 in clr:
                for var3 in clr:
                    color = "#" + var1 + var2 + var3
                    iter = store.append()
                    store.set(iter, (COLOR,), (color,))
        treeview.set_model(store)
        scrolled_win = Gtk.ScrolledWindow.new(None, None)
        scrolled_win.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_win.add(treeview)
        self.add(scrolled_win)

    def setup_tree_view(self, treeview):
        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn.new()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, "text", COLOR)
        column.set_title("Standard Colors")
        treeview.append_column(column)
        column.set_cell_data_func(renderer, self.cell_data_func, None)

    def cell_data_func(self, column, renderer, model, iter, data):
        # Get the color string stored by the column and make it the foreground color.
        (text,) = model.get(iter, COLOR)
        renderer.props.foreground_rgba = Gdk.RGBA(red=1.0, green=1.0, blue=1.0, alpha=1.0)
        red = int(text[1:3], 16) / 255
        green = int(text[3:5], 16) / 255
        blue = int(text[5:7], 16) / 255
        renderer.props.background_rgba = Gdk.RGBA(red=red, green=green, blue=blue, alpha=1.0)
        renderer.props.text = text

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, 
                                    title="Color List")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
