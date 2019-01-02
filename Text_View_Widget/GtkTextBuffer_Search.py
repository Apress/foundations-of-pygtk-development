#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        textview = Gtk.TextView.new()
        entry = Gtk.Entry.new()
        entry.set_text("Search for ...")
        find = Gtk.Button.new_with_label("Find")
        find.connect("clicked", self.on_find_clicked, (textview, entry))
        scrolled_win = Gtk.ScrolledWindow.new (None, None)
        scrolled_win.set_size_request(250, 200)
        scrolled_win.add(textview)
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        hbox.pack_start(entry, True, True, 0)
        hbox.pack_start(find, True, True, 0)
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        vbox.pack_start(scrolled_win, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)
        self.add(vbox)

    def on_find_clicked(self, button, w):
        find = w[1].get_text()
        find_len = len(find)
        buffer = w[0].get_buffer()
        start = buffer.get_start_iter()
        end_itr = buffer.get_end_iter()
        i = 0
        while True:
            end = start.copy()
            end.forward_chars(find_len)
            text = buffer.get_text(start, end, False)
            if text == find:
                i += 1
                start.forward_chars(find_len)
            else:
                start.forward_char()
            if end.compare(end_itr) == 0:
                break
        output = "The string '"+find+"' was found " + str(i) + " times!"
        dialog = Gtk.MessageDialog(parent=self, flags=Gtk.DialogFlags.MODAL,
                                   message_type=Gtk.MessageType.INFO,
                                   text=output, title="Information",
                                   buttons=("OK", Gtk.ResponseType.OK))
        dialog.run()
        dialog.destroy()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Searching Buffers")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
