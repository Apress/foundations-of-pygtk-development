#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

BUY_IT = 0
QUANTITY = 1
PRODUCT = 2

PRODUCT_CATEGORY = 0
PRODUCT_CHILD = 1

GroceryItem = (( PRODUCT_CATEGORY, True, 0, "Cleaning Supplies"),
               ( PRODUCT_CHILD, True, 1, "Paper Towels" ),
               ( PRODUCT_CHILD, True, 3, "Toilet Paper" ),
               ( PRODUCT_CATEGORY, True, 0, "Food"),
               ( PRODUCT_CHILD, True, 2, "Bread" ),
               ( PRODUCT_CHILD, False, 1, "Butter" ),
               ( PRODUCT_CHILD, True, 1, "Milk" ),
               ( PRODUCT_CHILD, False, 3, "Chips" ),
               ( PRODUCT_CHILD, True, 4, "Soda" ))

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(275, 270)
        treeview = Gtk.TreeView.new()
        self.setup_tree_view(treeview)
        store = Gtk.TreeStore.new((GObject.TYPE_BOOLEAN, 
                               GObject.TYPE_INT, 
                               GObject.TYPE_STRING))
        iter = None
        i = 0
        for row in GroceryItem:
            (ptype, buy, quant, prod) = row
            if ptype == PRODUCT_CATEGORY:
                j = i + 1
                (ptype1, buy1, quant1, prod1) = GroceryItem[j]
                while j < len(GroceryItem) and ptype1 == PRODUCT_CHILD:
                    if buy1:
                        quant += quant1
                    j += 1;
                    if j < len(GroceryItem):
                        (ptype1, buy1, quant1, prod1) = GroceryItem[j]
                iter = store.append(None)
                store.set(iter, BUY_IT, buy, QUANTITY, quant, PRODUCT, prod)
            else:
                child = store.append(iter)
                store.set(child, BUY_IT, buy, QUANTITY, quant, PRODUCT, prod)
            i += 1
        treeview.set_model(store)
        treeview.expand_all()
        scrolled_win = Gtk.ScrolledWindow.new(None, None)
        scrolled_win.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_win.add(treeview)
        self.add(scrolled_win)

    def setup_tree_view(self, treeview):
        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn("Buy", renderer, text=BUY_IT)
        treeview.append_column(column)
        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn("Count", renderer, text=QUANTITY)
        treeview.append_column(column)
        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn("Product", renderer, text=PRODUCT)
        treeview.append_column(column)

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
