#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject

ACTION = 0
MASK = 1
VALUE = 2

list = [( "Cut", Gdk.ModifierType.CONTROL_MASK, Gdk.KEY_X ),
        ( "Copy", Gdk.ModifierType.CONTROL_MASK, Gdk.KEY_C ),
        ( "Paste", Gdk.ModifierType.CONTROL_MASK, Gdk.KEY_V ),
        ( "New", Gdk.ModifierType.CONTROL_MASK, Gdk.KEY_N ),
        ( "Open", Gdk.ModifierType.CONTROL_MASK, Gdk.KEY_O ),
        ( "Print", Gdk.ModifierType.CONTROL_MASK, Gdk.KEY_P )]

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_request(250, 250)
        treeview = Gtk.TreeView.new()
        self.setup_tree_view(treeview)
        store = Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_INT, 
                               GObject.TYPE_UINT)
        for row in list:
            (action, mask, value) = row
            iter = store.append(None)
            store.set(iter, ACTION, action, MASK, mask, VALUE, value)
        treeview.set_model(store)
        scrolled_win = Gtk.ScrolledWindow.new(None, None)
        scrolled_win.set_policy(Gtk.PolicyType.AUTOMATIC, 
                                Gtk.PolicyType.AUTOMATIC)
        scrolled_win.add(treeview)
        self.add(scrolled_win)

    def setup_tree_view(self, treeview):
        renderer = Gtk.CellRendererAccel()
        column = Gtk.TreeViewColumn("Action", renderer, text=ACTION)
        treeview.append_column(column)
        renderer = Gtk.CellRendererAccel(accel_mode=Gtk.CellRendererAccelMode.GTK,
                                         editable=True)
        column = Gtk.TreeViewColumn("Key", renderer, accel_mods=MASK, 
                                    accel_key=VALUE)
        treeview.append_column(column)
        renderer.connect("accel_edited", self.accel_edited, treeview)

    def accel_edited(self, renderer, path, accel_key, mask, 
                     hardware_keycode, treeview):
        model = treeview.get_model()
        iter = model.get_iter_from_string(path)
        if iter:
            model.set(iter, MASK, mask, VALUE, accel_key)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, 
                                    title="Accelerator Keys")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
