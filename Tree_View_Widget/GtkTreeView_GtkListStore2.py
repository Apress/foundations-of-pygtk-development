#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

BUY_IT = 0
QUANTITY = 1
PRODUCT = 2

GroceryItem = (( True, 1, "Paper Towels" ),
               ( True, 2, "Bread" ),
               ( False, 1, "Butter" ),
               ( True, 1, "Milk" ),
               ( False, 3, "Chips" ),
               ( True, 4, "Soda" ))

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(250, 175)
        treeview = Gtk.TreeView.new()
        self.setup_tree_view(treeview)
        store = Gtk.ListStore.new((GObject.TYPE_BOOLEAN, 
                               GObject.TYPE_INT, 
                               GObject.TYPE_STRING))
        for row in GroceryItem:
            iter = store.append(None)
            store.set(iter, BUY_IT, row[BUY_IT], QUANTITY, row[QUANTITY], PRODUCT, 
                      row[PRODUCT])
        treeview.set_model(store)
        scrolled_win = Gtk.ScrolledWindow.new(None, None)
        scrolled_win.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_win.add(treeview)
        self.add(scrolled_win)

    def setup_tree_view(self, treeview):
        renderer = Gtk.CellRendererToggle.new()
        renderer.set_property("activatable", True)
        column = Gtk.TreeViewColumn("Buy", renderer, active=BUY_IT)
        renderer.connect("toggled", self.do_toggled, treeview)
        treeview.append_column(column)
        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn("Count", renderer, text=QUANTITY)
        treeview.append_column(column)
        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn("Product", renderer, text=PRODUCT)
        treeview.append_column(column)

    def do_toggled(self, renderer, path, treeview):
        model = treeview.get_model()
        iter = model.get_iter(path)
        if iter:
            (value,) = model.get(iter, BUY_IT)
            model.set_row(iter, (not value, None, None))



class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Grocery List")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
