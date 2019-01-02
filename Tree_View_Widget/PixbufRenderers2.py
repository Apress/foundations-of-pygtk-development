#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GdkPixbuf

ICON = 0
ICON_NAME = 1

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(200, 175)
        treeview = Gtk.TreeView.new()
        self.setup_tree_view(treeview)
        store = Gtk.ListStore.new((GdkPixbuf.Pixbuf, 
                                  GObject.TYPE_STRING))
        icon_theme = Gtk.IconTheme.get_default()
        iter = store.append(None)
        icon = icon_theme.load_icon("edit-cut", -1, 
                                    Gtk.IconLookupFlags.FORCE_SIZE)
        store.set(iter, [ICON, ICON_NAME], [icon, "Cut"])
        iter = store.append(None)
        icon = icon_theme.load_icon("edit-copy", -1, 
                                    Gtk.IconLookupFlags.FORCE_SIZE)
        store.set(iter, [ICON, ICON_NAME], [icon, "Copy"])
        iter = store.append(None)
        icon = icon_theme.load_icon("edit-paste", -1, 
                                    Gtk.IconLookupFlags.FORCE_SIZE)
        store.set(iter, [ICON, ICON_NAME], [icon, "Paste"])
        iter = store.append(None)
        icon = icon_theme.load_icon("document-new", -1, 
                                    Gtk.IconLookupFlags.FORCE_SIZE)
        store.set(iter, [ICON, ICON_NAME], [icon, "New"])
        iter = store.append(None)
        icon = icon_theme.load_icon("document-open", -1, 
                                    Gtk.IconLookupFlags.FORCE_SIZE)
        store.set(iter, [ICON, ICON_NAME], [icon, "Open"])
        iter = store.append(None)
        icon = icon_theme.load_icon("document-print", -1, 
                                    Gtk.IconLookupFlags.FORCE_SIZE)
        store.set(iter, [ICON, ICON_NAME], [icon, "Print"])
        treeview.set_model(store)
        scrolled_win = Gtk.ScrolledWindow.new(None, None)
        scrolled_win.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_win.add(treeview)
        self.add(scrolled_win)

    def setup_tree_view(self, treeview):
        column = Gtk.TreeViewColumn.new()
        column.set_resizable(True)
        column.set_title("Some Items")
        renderer = Gtk.CellRendererPixbuf.new()
        # it is important to pack the renderer BEFORE adding attributes!!
        column.pack_start(renderer, False)
        column.add_attribute(renderer, "pixbuf", ICON)
        renderer = Gtk.CellRendererText.new()
        # it is important to pack the renderer BEFORE adding attributes!!
        column.pack_start(renderer, True)
        column.add_attribute(renderer, "text", ICON_NAME)
        treeview.append_column(column)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Some Items")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
