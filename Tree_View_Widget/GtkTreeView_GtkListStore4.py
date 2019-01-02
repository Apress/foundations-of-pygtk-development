#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

QUANTITY = 0
PRODUCT = 1

GroceryItem = (( 1, "Paper Towels" ),
               ( 2, "Bread" ),
               ( 1, "Butter" ),
               ( 1, "Milk" ),
               ( 3, "Chips" ),
               ( 4, "Soda" ))

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(250, 175)
        treeview = Gtk.TreeView.new()
        self.setup_tree_view(treeview)
        store = Gtk.ListStore.new((GObject.TYPE_STRING, 
                                  GObject.TYPE_STRING))
        for row in GroceryItem:
            iter = store.append(None)
            store.set(iter, QUANTITY, "%.0f" % row[QUANTITY], PRODUCT, row[PRODUCT])
        treeview.set_model(store)
        scrolled_win = Gtk.ScrolledWindow.new(None, None)
        scrolled_win.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_win.add(treeview)
        self.add(scrolled_win)

    def setup_tree_view(self, treeview):
        # Create a GtkListStore that will be used for the combo box renderer.
        model = Gtk.ListStore.new((GObject.TYPE_STRING, 
                                  GObject.TYPE_STRING))
        iter = model.append()
        model.set(iter, 0, "None")
        iter = model.append()
        model.set(iter, 0, "One")
        iter = model.append()
        model.set(iter, 0, "Half a Dozen")
        iter = model.append()
        model.set(iter, 0, "Dozen")
        iter = model.append()
        model.set(iter, 0, "Two Dozen")
        # Create the GtkCellRendererCombo and add the tree model. Then, add the
        # renderer to a new column and add the column to the GtkTreeView.
        renderer = Gtk.CellRendererCombo(text_column=0, editable=True, 
                                         has_entry=True, model=model)
        column = Gtk.TreeViewColumn("Count", renderer, text=QUANTITY)
        treeview.append_column(column)
        renderer.connect("edited", self.cell_edited, treeview)
        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn("Product", renderer, text=PRODUCT)
        treeview.append_column(column)

    def cell_edited(self, renderer, path, new_text, treeview):
        # Make sure the text is not empty. If not, apply it to the tree view cell.
        if new_text != "":
            model = treeview.get_model()
            iter = model.get_iter_from_string(path)
            if iter:
                model.set(iter, QUANTITY, new_text)

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
