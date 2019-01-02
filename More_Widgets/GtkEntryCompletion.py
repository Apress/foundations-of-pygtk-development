#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widgets = ["GtkDialog", "GtkWindow", "GtkContainer", "GtkWidget"]
        self.set_border_width(10)
        label = Gtk.Label.new("Enter a widget in the following GtkEntry:")
        entry = Gtk.Entry.new()
        # Create a GtkListStore that will hold autocompletion possibilities.
        types = (GObject.TYPE_STRING,)
        store = Gtk.ListStore.new(types)
        for widget in widgets:
            iter = store.append()
            store.set(iter, 0, widget)
        completion = Gtk.EntryCompletion.new()
        entry.set_completion(completion)
        completion.set_model(store)
        completion.set_text_column(0)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(label, False, False, 0)
        vbox.pack_start(entry, False, False, 0)
        self.add(vbox)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, 
                                    title="Automatic Completion")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
