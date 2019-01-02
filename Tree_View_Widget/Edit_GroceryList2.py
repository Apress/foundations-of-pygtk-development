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

class AddDialog(Gtk.Dialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parent = kwargs['parent']
        # set up buttons
        self.add_button("Add", Gtk.ResponseType.OK)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        # set up dialog widgets
        combobox = Gtk.ComboBoxText.new()
        entry = Gtk.Entry.new()
        spin = Gtk.SpinButton.new_with_range(0, 100, 1)
        check = Gtk.CheckButton.new_with_mnemonic("_Buy the Product")
        spin.set_digits(0)
        # Add all of the categories to the combo box.
        for row in  GroceryItem:
            (ptype, buy, quant, prod) = row
            if ptype == PRODUCT_CATEGORY:
                combobox.append_text(prod)
        # create a grid
        grid = Gtk.Grid.new()
        grid.set_row_spacing (5)
        grid.set_column_spacing(5)
        # fill out the grid
        grid.attach(Gtk.Label.new("Category:"), 0, 0, 1, 1)
        grid.attach(Gtk.Label.new("Product:"), 0, 1, 1, 1)
        grid.attach(Gtk.Label.new("Quantity:"), 0, 2, 1, 1)
        grid.attach(combobox, 1, 0, 1, 1)
        grid.attach(entry, 1, 1, 1, 1)
        grid.attach(spin, 1, 2, 1, 1)
        grid.attach(check, 1, 3, 1, 1)
        self.get_content_area().pack_start(grid, True, True, 5)
        self.show_all()
        # run the dialog and check the results
        if self.run() != Gtk.ResponseType.OK:
            self.destroy()
            return
        quantity = spin.get_value()
        product = entry.get_text()
        category = combobox.get_active_text()
        buy = check.get_active()
        if product == "" or category == None:
            print("All of the fields were not correctly filled out!")
            return
        model = parent.get_treeview().get_model();
        iter = model.get_iter_from_string("0")
        # Retrieve an iterator pointing to the selected category.
        while iter:
            (name,) = model.get(iter, PRODUCT)
            if name.lower() == category.lower():
                break
            iter = model.iter_next(iter)
        # Convert the category iterator to a path so that it will not become invalid
        # and add the new product as a child of the category.
        path = model.get_path(iter)
        child = model.append(iter)
        model.set(child, BUY_IT, buy, QUANTITY, quantity, PRODUCT, product)
        # Add the quantity to the running total if it is to be purchased.
        if buy:
            iter = model.get_iter(path)
            (i,) = model.get(iter, QUANTITY)
            i += quantity
            model.set(iter, QUANTITY, i)
        self.destroy()

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(275, 270)
        self.treeview = Gtk.TreeView.new()
        self.setup_tree_view(self.treeview)
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
        self.treeview.set_model(store)
        self.treeview.expand_all()
        scrolled_win = Gtk.ScrolledWindow.new(None, None)
        scrolled_win.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_win.add(self.treeview)
        button_add = Gtk.Button.new_with_label("Add") 
        button_add.connect("clicked", self.on_add_button_clicked, self)
        button_remove = Gtk.Button.new_with_label("Remove") 
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.pack_end(button_remove, False, True, 5)
        hbox.pack_end(button_add, False, True, 5)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_end(hbox, False, True, 5)
        vbox.pack_end(scrolled_win, True, True, 5)
        self.add(vbox)

    def setup_tree_view(self, treeview):
        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn("Buy", renderer, text=BUY_IT)
        self.treeview.append_column(column)
        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn("Count", renderer, text=QUANTITY)
        treeview.append_column(column)
        renderer = Gtk.CellRendererText.new()
        renderer.set_property("editable", True)
        renderer.connect("edited", self.cell_edited, treeview)
        column = Gtk.TreeViewColumn("Product", renderer, text=PRODUCT)
        treeview.append_column(column)


    def on_add_button_clicked(self, button, parent):
        dialog = AddDialog(title="Add a Product", parent=parent,
                            flags=Gtk.DialogFlags.MODAL)

    def get_treeview(self):
        return self.treeview

    def cell_edited(self, renderer, path, new_text, treeview):
        if len(new_text) > 0:
            model = treeview.get_model()
            iter = model.get_iter_from_string(path)
            if iter:
                model.set(iter, PRODUCT, new_text)

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
