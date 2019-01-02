#!/usr/bin/python3

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GdkPixbuf

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ICON = 0
        self.FILENAME = 1
        self.current_path = []
        self.set_border_width(10)
        self.set_size_request(250, 500)

        treeview = Gtk.TreeView.new()
        treeview.connect("row-activated", self.on_row_activated)

        self.setup_tree_view(treeview)
        self.setup_tree_model(treeview)

        scrolled_win = Gtk.ScrolledWindow.new()
        scrolled_win.set_policy(Gtk.PolicyType.AUTOMATIC, 
                                Gtk.PolicyType.AUTOMATIC)

        scrolled_win.add(treeview)
        self.add(scrolled_win)

    def setup_tree_view(self, treeview):
        column = Gtk.TreeViewColumn.new()
        column.set_title("File Browser")
  
        renderer = Gtk.CellRendererPixbuf.new()
        column.pack_start(renderer, False)
        column.add_attribute(renderer, "pixbuf", self.ICON)
  
        renderer = Gtk.CellRendererText.new()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, "text", self.FILENAME)
  
        treeview.append_column(column)

    def setup_tree_model(self, treeview):
        store = Gtk.ListStore(GdkPixbuf.Pixbuf, GObject.TYPE_STRING)
        treeview.set_model(store)
        
        self.populate_tree_model(treeview)

    def populate_tree_model(self, treeview):
        store = treeview.get_model()
        store.clear()
        
        # Build the tree path out of current_path.
        if self.current_path == []:
            location ="/"
        else:
            for temp in current_path:
                location = location + "/" + temp

            iter = store.append()
            store.set(iter, self.ICON, directory, self.FILENAME, "..")

        # Parse through the directory, adding all of its contents to the model.
        for file in os.listdir(location):
            temp = location + "/" + file

            if os.path.isdir(file):
                pixbuf = GdkPixbuf.Pixbuf.new_from_file ("directory.png")
            else:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file ("file.png")

        iter = store.append()
        store.set(iter, self.ICON, pixbuf, self.FILENAME, file)

    def on_row_activated(self, treeview, fpath, column):
        model = treeview.get_model()
        iter = model.get_iter(fpath)
        if iter:
            file = model.get(iter, self.FILENAME)
            
            if file == "..":
                node = pop(current_path)
                self.populate_tree_model(treeview)
            else:
                if len(self.current_path) == 0:
                  location = "/"
                else:
                    if self.current_path == []:
                        location ="/"
                    else:
                        for file in current_path:
                            location = location + "/" + file

                        iter = store.append()
                        store.set(iter, self.ICON, directory, self.FILENAME, "..")

                if os.path.isdir(location):
                    current_path = location
                    self.populate_tree_model(treeview)


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Exercise 1")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
